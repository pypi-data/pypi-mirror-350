#!./runmodule.sh

import os
import sys
import re
import time
import argparse
from collections.abc import Iterator, Sequence

import confattr
from confattr import Config, DictConfig, ConfigFile, Message, NotificationLevel, ConfigFileArgparseCommand, ParseException, Primitive, Dict
from confattr.formatters import AbstractFormatter
from confattr.types import CaseInsensitiveRegex, SubprocessCommandWithAlternatives
from confattr.quickstart import ConfigManager

import prompt_toolkit
from prompt_toolkit import print_formatted_text, PromptSession
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.completion import Completer, Completion, CompleteEvent
from prompt_toolkit.document import Document
from prompt_toolkit.styles import ANSI_COLOR_NAMES, NAMED_COLORS
from prompt_toolkit.styles.named_colors import NAMED_COLORS

import can
import cantools

from .can_setup import Bitrate
from .can_handler import CanBusHandler, CantoolsEncodeException, TYPE_CANTOOLS_MESSAGE, TYPE_CANTOOLS_NAMED_SIGNAL_VALUE
from .parse_error_frame import ErrorFrame
from .utils import hex_int, LiteralAction, CallAction
from .meta import __doc__, __version__


class Color(Primitive[str]):

	type_name = 'color'

	DEFAULT = 'default'
	CHOICES = (DEFAULT,) + tuple(ANSI_COLOR_NAMES) + tuple(c.lower() for c in NAMED_COLORS.keys())

	def __init__(self) -> None:
		super().__init__(str, allowed_values=self.CHOICES, type_name=self.type_name)


def assert_str(obj: object) -> str:
	assert isinstance(obj, str)
	return obj


class Directory:

	help = "The path to a directory"

	def __init__(self, path: str) -> None:
		self.path = path
		if not os.path.isdir(self.expand()):
			raise ValueError("%r is not a directory" % path)

	def __str__(self) -> str:
		return self.path

	def expand(self) -> str:
		return os.path.expanduser(self.path)


try:
	__parent = dict[re.Pattern[str], str]
except:
	__parent = dict  # type: ignore [misc]
class RegexToColorDict(__parent):

	def get_color(self, msg_name: str, default: str = Color.DEFAULT) -> str:
		for pattern, color in reversed(tuple(self.items())):
			if pattern.search(msg_name):
				return color
		return default

RegexToColorDictType: 'type[AbstractFormatter[RegexToColorDict]]'
class RegexToColorDictType(Dict):  # type: ignore [no-redef,type-arg]

	def __init__(self) -> None:
		super().__init__(key_type=Primitive(CaseInsensitiveRegex), value_type=Color())

	def parse_value(self, config_file: 'ConfigFile', values: str) -> 'RegexToColorDict':
		return RegexToColorDict(self.parse_item(config_file, i) for i in self.split_values(config_file, values))


def get_id_width(msg: 'TYPE_CANTOOLS_MESSAGE|can.Message') -> int:
	if isinstance(msg, can.Message):
		is_extended_id = msg.is_extended_id
	else:
		is_extended_id = msg.is_extended_frame
	if is_extended_id:
		return 8
	else:
		return 3


class App:

	APPNAME = 'cancli'

	bitrate = Config('can.bitrate', Bitrate('none'), help="default bitrate for new buses")

	colors = DictConfig('color.config', {NotificationLevel.ERROR: 'ansired', NotificationLevel.INFO: Color.DEFAULT}, type=Color())
	color_error = Config('color.signal.error', 'ansired', type=Color())
	color_unknown_message = Config('color.unknown-message', 'ansimagenta', type=Color())
	color_msg = Config('color.message', RegexToColorDict({CaseInsensitiveRegex(''): Color.DEFAULT}), type=RegexToColorDictType(), help="The last regex matching the name of a message defines the color of that message and all it's signals. The color of the signals can be overridden with %color.signal%.")
	color_sig = Config('color.signal', RegexToColorDict({CaseInsensitiveRegex('error|protect'): color_error.value, CaseInsensitiveRegex('warn|alarm'): 'ansiyellow'}), type=RegexToColorDictType(), help="The last regex matching the name of a signal defines the color of that signal if it's value is true. You can change the color for all signals of a certain message with %color.message%.")
	color_prompt = Config('color.prompt', 'ansiblue', type=Color())

	print_raw = Config('print.raw', True, help="Print received raw data")
	print_pretty = Config('print.pretty', True, help="Print decoded data")
	print_error = Config('print.error', True, help="Print CAN bus errors")
	prompt = Config('prompt', ">>> ")
	pattern_message = Config('pattern.message', "{canmsg.arbitration_id:>0{id_width}x} {msg.name}", help="How to format a message. Wildcards: canmsg (a can.Message object), msg (a cantools.db.Message object) and id_width (the number of hex characters required to represent the biggest possible arbitration_id depending on is_extended_id)")
	pattern_signal = Config('pattern.signal', "\t{key}: {val}{unit}", help="How to format a signal. Wildcards: key (a str), val (a str, int or float) and unit (a possibly empty str).")
	pattern_remote = Config('pattern.remote', "\tremote frame", help="How to format a remote message. This is printed instead of the signals. No wildcards.")
	min_time_span_between_can_errors_in_s = Config('print.min-time-span-between-errors', 1.0, unit="s", help="Do not print equal CAN bus errors more frequently than this")

	def __init__(self, argv: 'list[str]|None') -> None:
		CancliCommand.app = self
		self.cfg = ConfigManager(self.APPNAME, __version__, __doc__,
			show_python_version_in_version = True,
			show_additional_modules_in_version = [can, cantools, prompt_toolkit, confattr],
			changelog_url = "https://gitlab.com/erzo/cancli/-/tags",
		)

		self.show_by_default = True
		self._show: 'dict[str|int, float]' = {}
		self._hide: 'dict[str|int, float]' = {}
		self._last: 'dict[str|int, can.Message]' = {}
		self._next: 'set[str|int]' = set()
		self._last_error: 'can.Message|None' = None
		self.bus_handler = CanBusHandler(self.on_receive)
		self.init_config()
		self.create_parser().parse_args(argv)

	def init_config(self) -> None:
		self.cfg.load()

		# show errors in config
		def on_config_message(msg: Message) -> None:
			color = self.colors.get(msg.notification_level)
			self.colored_print(color, str(msg))
		self.cfg.set_ui_callback(on_config_message)

	def get_help_bash_completion(self) -> str:
		completion_script = os.path.join(os.path.dirname(__file__), "complete.sh")
		return f"""\
For bash completion add the following line to your ~/.bash_completion:
source {completion_script!r}
"""

	def create_parser(self) -> argparse.ArgumentParser:
		p = self.cfg.create_argument_parser()
		p.epilog = self.get_help_bash_completion()
		return p

	def run(self) -> None:
		p: 'PromptSession[str]' = PromptSession(FormattedText([(self.color_prompt, self.prompt)]), completer=ConfigFileCompleter(self.cfg.user_interface))
		while True:
			Message.reset()
			try:
				self.cfg.parse_line(p.prompt())
			except (EOFError, KeyboardInterrupt):
				break

	def on_receive(self, canmsg: can.Message) -> None:
		msg = self.print_message(canmsg, ignore_filters=False, prefix="rx")
		self._last[canmsg.arbitration_id] = canmsg
		if msg:
			self._last[msg.name] = canmsg

	def print_message(self, canmsg: can.Message, *, ignore_filters: bool, prefix: str) -> 'TYPE_CANTOOLS_MESSAGE|None':
		prefix = "[%s] " % prefix
		if canmsg.is_error_frame:
			if ignore_filters or self._last_error is None or canmsg.timestamp >= self._last_error.timestamp + self.min_time_span_between_can_errors_in_s:
				self._last_error = canmsg
				if self.print_error:
					if self.print_raw:
						self.colored_print(self.color_error, prefix + self.format_raw(canmsg))
					self.colored_print(self.color_error, prefix + str(ErrorFrame(canmsg)))
			return None

		if not ignore_filters and canmsg.arbitration_id in self._next or '*' in self._next:
			ignore_filters = True
			self._next.clear()

		msg = self.bus_handler.get_cantools_message(canmsg)
		if msg:
			if not ignore_filters and msg.name in self._next:
				ignore_filters = True
				self._next.clear()
			d = self.show_by_default
			if not ignore_filters and (
				max(self._hide.get(msg.name, 0), self._hide.get(canmsg.arbitration_id, 0)) >=
				max(self._show.get(msg.name, d), self._show.get(canmsg.arbitration_id, d))
			):
				return msg
			msgcolor = self.color_msg.get_color(msg.name)
			if self.print_raw:
				self.colored_print(msgcolor, prefix + self.format_raw(canmsg))
			if self.print_pretty:
				self.colored_print(msgcolor, prefix + self.pattern_message.format(canmsg=canmsg, msg=msg, id_width=get_id_width(canmsg)))
				if canmsg.is_remote_frame:
					self.colored_print(msgcolor, self.pattern_remote)
					return msg
				key: str
				val: cantools.typechecking.SignalValueType
				if self.bus_handler.is_node_id_set():
					key = self.bus_handler.PARAM_NODE_ID
					val = self.bus_handler.get_node_id(canmsg)
					self.colored_print(self.color_sig.get_color(key, msgcolor) if val else msgcolor, prefix + self.pattern_signal.format(key=key, val=val, unit=""))
				raw_data = canmsg.data.copy()
				while len(raw_data) < msg.length:
					raw_data.append(0)
				try:
					data = msg.decode_simple(raw_data)
				except cantools.database.errors.DecodeError as e:
					self.colored_print(self.color_error, "Failed to decode message: %s" % e)
					return msg
				for key, val in data.items():
					if isinstance(val, TYPE_CANTOOLS_NAMED_SIGNAL_VALUE):
						nonzero = bool(val.value)
					else:
						nonzero = bool(val)
					sig = msg.get_signal_by_name(key)
					unit = sig.unit if sig.unit else ""
					self.colored_print(self.color_sig.get_color(key, msgcolor) if nonzero else msgcolor, prefix + self.pattern_signal.format(key=key, val=val, unit=unit))
			return msg

		else:
			if not ignore_filters and self._hide.get(canmsg.arbitration_id, 0) >= self._show.get(canmsg.arbitration_id, self.show_by_default):
				return msg
			self.colored_print(self.color_unknown_message, prefix + self.format_raw(canmsg))
			return msg


	def format_raw(self, canmsg: can.Message) -> str:
		return str(canmsg)

	def colored_print(self, color: 'str|None', msg: str) -> None:
		if color and color != Color.DEFAULT:
			print_formatted_text(FormattedText([(color, str(msg))]))
		else:
			print_formatted_text(str(msg))


	def show(self, msg: 'str|int') -> None:
		if msg == '*':
			self.show_by_default = True
			self._hide.clear()
			self._show.clear()
			return
		self._hide.pop(msg, None)
		self._show[msg] = time.time()

	def hide(self, msg: 'str|int') -> None:
		if msg == '*':
			self.show_by_default = False
			self._hide.clear()
			self._show.clear()
			return
		self._show.pop(msg, None)
		self._hide[msg] = time.time()

	def prev(self, messages: 'Sequence[str|int]') -> None:
		l: 'list[can.Message]'
		if '*' in messages:
			# only int to avoid duplicates
			l = list(canmsg for key, canmsg in self._last.items() if isinstance(key, int))
		else:
			l = [self._last[msg] for msg in messages if msg in self._last]
		l.sort(key=lambda canmsg: canmsg.timestamp)
		for canmsg in l:
			self.print_message(canmsg, ignore_filters=True, prefix="prev")

	def next(self, messages: 'set[str|int]') -> None:
		self._next = messages


class ConfigFileCompleter(Completer):

	def __init__(self, config_file: ConfigFile) -> None:
		super().__init__()
		self.config_file = config_file

	def get_completions(self, document: Document, complete_event: CompleteEvent) -> 'Iterator[Completion]':
		start_of_line, completions, end_of_line = self.config_file.get_completions(document.text, document.cursor_position)
		for word in completions:
			yield Completion(start_of_line + word.rstrip(os.path.sep), display=word, start_position=-document.cursor_position)



class CancliCommand(ConfigFileArgparseCommand, abstract=True):

	app: App


# ---------- setup ----------

class SetBitrate(CancliCommand):

	'''
	Set the default bitrate and change the bitrate of all active buses.
	'''

	COMPLETIONS = ('250k', '500k', '1M')

	name = "bitrate"

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("bitrate", type=Bitrate)

	def run_parsed(self, args: argparse.Namespace) -> None:
		self.app.bitrate = args.bitrate
		self.app.bus_handler.change_bitrate(self.app.bitrate)

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is not None and action.dest == 'bitrate':
			completions = [bus for bus in self.COMPLETIONS if bus.startswith(start)]
			return start_of_line, completions, end_of_line
		return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)

class Bus(CancliCommand):

	'''
	Activate a bus.
	'''

	BITRATE_COMPLETIONS = SetBitrate.COMPLETIONS

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("-a", "--add", help="Add a new bus instead of replacing the current bus")
		parser.add_argument("--bustype", default=None, help="https://python-can.readthedocs.io/en/stable/configuration.html#interface-names")
		parser.add_argument("channel")
		parser.add_argument("bitrate", type=Bitrate, default=None, nargs='?')

	def run_parsed(self, args: argparse.Namespace) -> None:
		if args.bitrate is None:
			bitrate = self.app.bitrate
		else:
			bitrate = args.bitrate

		try:
			if not args.add:
				self.app.bus_handler.disconnect_from_all_buses()
			self.app.bus_handler.connect_to_bus(bitrate=bitrate, channel=args.channel, bustype=args.bustype)
		except Exception as e:
			raise ParseException(e)

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is not None and action.dest == 'channel':
			completions = [bus for bus in self.find_available_interfaces() if bus.startswith(start)]
			return start_of_line, completions, end_of_line
		if action is not None and action.dest == 'bitrate':
			completions = [bus for bus in self.BITRATE_COMPLETIONS if bus.startswith(start)]
			return start_of_line, completions, end_of_line
		return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)

	@staticmethod
	def find_available_interfaces() -> 'list[str]':
		"""Returns the names of all can/vcan interfaces regardless of whether they are up or down.

		The function calls the ``ip link list`` command.

		:return: The list of all available CAN interfaces or an empty list if the command failed
		"""
		# based on https://github.com/hardbyte/python-can/blob/develop/can/interfaces/socketcan/utils.py
		# but in contrast to original this returns all CAN buses not only the activated CAN buses
		import subprocess
		import json
		try:
			command = ["ip", "-json", "link", "list"]
			output_str = subprocess.check_output(command, text=True)
		except Exception:  # pylint: disable=broad-except
			return []

		try:
			output_json = json.loads(output_str)
		except json.JSONDecodeError:
			return []

		interfaces = [i.get("ifname", "") for i in output_json if i.get("link_type") == "can"]
		return interfaces

class Read(CancliCommand):

	'''
	Read messages from a log file.
	'''

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("log")

	def run_parsed(self, args: argparse.Namespace) -> None:
		with open(args.log, 'rt') as f:
			try:
				parser = cantools.logreader.Parser(f)  # type: ignore [no-untyped-call]
				line: str
				frame: 'cantools.logreader.DataFrame|None'
				for line, frame in parser.iterlines(keep_unknowns=True):  # type: ignore [no-untyped-call]
					if frame is None:
						self.app.colored_print(self.app.color_error, "failed to parse line %r" % line)
					else:
						msg = can.Message(
							arbitration_id = frame.frame_id,
							data = frame.data,
							timestamp = frame.timestamp.timestamp(),
						)
						self.app.on_receive(msg)
			except KeyboardInterrupt:
				pass

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is not None and action.dest == 'log':
			return self.config_file.get_completions_for_file_name(start, relative_to=os.getcwd(), match=lambda path, name, start: start in name, start_of_line=start_of_line, end_of_line=end_of_line)
		return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)


class Db(CancliCommand):

	'''
	Load a database file (dbc/sym/...).

	Supported are all file formats that are supported by cantools.
	https://github.com/cantools/cantools#about
	'''

	default_path = Config('db.home', Directory("~"), help="If the db command gets a relative path then it is relative to this directory")

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("-a", "--add", help="Add a new bus db file instead of replacing the current db file")
		parser.add_argument("filename")

	def run_parsed(self, args: argparse.Namespace) -> None:
		if not args.add:
			self.app.bus_handler.remove_all_db_files()
		fn = os.path.expanduser(args.filename)
		if not os.path.isabs(fn):
			fn = os.path.join(self.default_path.expand(), args.filename)

		try:
			self.app.bus_handler.add_db_file(fn)
		except Exception as e:
			raise ParseException(e)

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is not None and action.dest == 'filename':
			return self.config_file.get_completions_for_file_name(start, relative_to=self.default_path.expand(), match=lambda path, name, start: start in name, start_of_line=start_of_line, end_of_line=end_of_line)
		return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)

class NodeId(CancliCommand):

	'''
	Specify that part of an arbitration id is a node id.

	If several devices of the same type are connected to the same bus
	and they are distinguished by part of the arbitration id
	you can use this command to specify this "node id".

	- The node id is displayed like a signal
	  and can be passed to the send command like a signal.
	- If the arbitration id of a received message
	  is not found in the data base file
	  the lookup is tried again for node id = 0.
	'''

	name = "node-id"

	MAX_ID = (1 << 29) - 1

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("mask", type=hex_int)
		parser.add_argument("<<", action=LiteralAction, optional=True)
		parser.add_argument("shift", type=int, default=0, nargs='?')

	def run_parsed(self, args: argparse.Namespace) -> None:
		if args.mask << args.shift > self.MAX_ID:
			raise ParseException(f"{hex(args.mask)} << {args.shift} is too big, must not be bigger than {hex(self.MAX_ID)}")

		self.app.bus_handler.set_node_id(args.mask, args.shift)

	def get_completions_for_positional_argument(self, position: int, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if position == 0:
			completions = ['0xFF']
		elif position == 1:
			completions = ['<<']
		elif position == 2:
			completions = [str(i) for i in range(0,64,8)]
		else:
			completions = []
		return start_of_line, completions, end_of_line

class Mask(CancliCommand):

	'''
	If a CAN bus message is not found in the dbc file apply these masks to the arbitration ID and try again.

	`clear` is identical to setting the bitwise inverted mask for `and`.
	`set` is identical to `or`.

	`clear`/`and` is applied before `set`/`or`.
	`node-id` is applied before these masks.

	A mask of 0 disables this feature.
	'''

	MAX_ID = NodeId.MAX_ID

	TYPE_AND = 'and'
	TYPE_OR = 'or'
	TYPE_SET = 'set'
	TYPE_CLEAR = 'clear'
	TYPES = (TYPE_CLEAR, TYPE_SET, TYPE_AND, TYPE_OR)

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("type", choices=self.TYPES)
		parser.add_argument("mask", type=hex_int)

	def run_parsed(self, args: argparse.Namespace) -> None:
		if args.mask > self.MAX_ID:
			raise ParseException(f"{hex(args.mask)} is too big, must not be bigger than {hex(self.MAX_ID)}")

		if args.type == self.TYPE_AND:
			self.app.bus_handler.set_and_mask(args.mask)
		elif args.type == self.TYPE_OR:
			self.app.bus_handler.set_or_mask(args.mask)
		elif args.type == self.TYPE_SET:
			self.app.bus_handler.set_or_mask(args.mask)
		elif args.type == self.TYPE_CLEAR:
			self.app.bus_handler.set_and_mask(~args.mask)
		else:
			raise NotImplementedError("type %r is not implemented" % args.type)

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if action is not None and action.dest == 'type':
			completions = list(self.TYPES)
		elif action is not None and action.dest == 'mask':
			completions = ['1f000000', '00ff0000', '0000ff00', '000000ff']
		else:
			return super().get_completions_for_action(action, start, start_of_line=start_of_line, end_of_line=end_of_line)
		return start_of_line, completions, end_of_line


# ---------- meta ----------

class Save(CancliCommand):

	"""
	Save the settings.
	"""

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		pass

	def run_parsed(self, args: argparse.Namespace) -> None:
		self.config_file.save()

class Quit(CancliCommand):

	'''
	Quit the program.
	'''

	aliases = ["q"]

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		pass

	def run_parsed(self, args: argparse.Namespace) -> None:
		raise EOFError()


# ---------- normal operation ----------

class Send(CancliCommand):

	'''
	Send a message on the last activated CAN bus.

	data consists of signalname=value pairs which are encoded using cantools.
	This requires that you have loaded a database file with the command db.

	After `node-id` you can pass node_id=<number> in order to set the node id in the arbitration id.
	If you do not pass node_id=<number> the unmodified frame id as specified in the dbc file is used as arbitration id.
	'''

	KEY_VAL_SEP = "="

	aliases = ["s"]

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("-r", "--raw", action='store_true', help="Interpret the data as raw data bytes to be send instead of processing them with cantools")
		parser.add_argument("msg", help="The name or frame id of the message to be sent")
		parser.add_argument("data", nargs="*", help="The data to be send, if this is a single R, send a remote frame")

	def run_parsed(self, args: argparse.Namespace) -> None:
		try:
			canmsg = self.send(args)
			self.app.print_message(canmsg, ignore_filters=True, prefix="tx")
		except CantoolsEncodeException as e:
			self.app.colored_print(self.app.color_error, "Failed to encode data. Are you sure the dbc file is correct?")
			self.app.colored_print(self.app.color_error, str(e))

	def send(self, args: argparse.Namespace) -> can.Message:
		msg = self.app.bus_handler.get_cantools_message_by_name(args.msg)
		if not msg:
			if args.raw:
				arbitration_id, is_extended_id = self.parse_raw_id(args.msg)
				data, is_remote_frame = self.parse_raw_data(args.data)
				return self.app.bus_handler.send_raw(arbitration_id, is_extended_id=is_extended_id, data=data, is_remote_frame=is_remote_frame)
			raise ParseException("unknown message %r" % args.msg)

		if args.raw:
			data, is_remote_frame = self.parse_raw_data(args.data)
			return self.app.bus_handler.send_raw(msg.frame_id, is_extended_id=msg.is_extended_frame, data=data, is_remote_frame=is_remote_frame)

		if args.data == ["R"]:
			return self.app.bus_handler.send(msg, signals={}, is_remote_frame=True)

		signals: 'dict[str, int|float]' = {}
		i = 0
		for signal in args.data:
			if self.KEY_VAL_SEP in signal:
				name, value = signal.split(self.KEY_VAL_SEP, 1)
				if self.app.bus_handler.is_node_id_set() and name == self.app.bus_handler.PARAM_NODE_ID:
					try:
						signals[name] = int(value, base=0)
					except ValueError as e:
						raise ParseException(f"invalid value for {name!r}, should be an int")
					continue
				try:
					s = msg.get_signal_by_name(name)
					i = msg.signals.index(s)
				except KeyError:
					raise ParseException(f"unknown signal {name!r} in message {msg.name!r}")
			else:
				try:
					s = msg.signals[i]
				except IndexError:
					raise ParseException(f"invalid signal position {i}, message {msg.name!r} has only {len(msg.signals)} signals")
				value = signal
			try:
				signals[s.name] = s.choice_to_number(value)
			except (ValueError, KeyError):
				try:
					signals[s.name] = int(value, base=0)
				except ValueError:
					signals[s.name] = float(value)
			i += 1
		return self.app.bus_handler.send(msg, signals, is_remote_frame=False)

	def parse_raw_id(self, val: str) -> 'tuple[int, bool]':
		try:
			if val.startswith('0x'):
				is_extended_id = len(val) > 3+2
				return int(val, base=0), is_extended_id
			is_extended_id = len(val) > 3
			return int(val, base=16), is_extended_id
		except ValueError:
			raise ParseException(f"failed to parse arbitration id {val!r}")

	def parse_raw_data(self, val: 'Sequence[str]') -> 'tuple[bytes|None, bool]':
		if len(val) == 1:
			sval, = val
			if sval == 'R':
				return None, True
			n = len(sval)
			if n > 2 and n % 2 != 0:
				raise ParseException(f"incomplete data byte, expected an even number of hex digits")
			val = [sval[i:i+2] for i in range(0, len(sval), 2)]
		try:
			return bytes(int(b, base=16) for b in val), False
		except ValueError as e:
			raise ParseException(f"invalid data: {e}")


	def get_completions(self, cmd: 'Sequence[str]', argument_pos: int, cursor_pos: int, *, in_between: bool, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		self.__cmd = cmd
		return super().get_completions(cmd, argument_pos, cursor_pos, in_between=in_between, start_of_line=start_of_line, end_of_line=end_of_line)

	def get_completions_for_positional_argument(self, position: int, start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if position == 0:
			return start_of_line, self.app.bus_handler.get_completions_for_message_name(start), end_of_line

		msg = next(w for w in self.__cmd[1:] if not w.startswith("-"))
		if '=' in start:
			sig_name, start = start.split('=', 1)
			start_of_line += sig_name + '='
			return start_of_line, self.app.bus_handler.get_completions_for_signal_value(msg, sig_name, start), end_of_line

		return start_of_line, self.app.bus_handler.get_completions_for_signal_name(msg, start), end_of_line


class MessageTakingCommand(CancliCommand, abstract=True):

	'''
	Messages can be specified by name or by id.
	For messages specified by name the node id is ignored.
	Either way extended frame vs standard frame is ignored.
	'''

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument('messages', nargs='*', help="Message name or ID, * can be used to match an arbitrary sequence of characters in the name")
		parser.add_argument('-E', '--re', action='store_true', help="'messages' are regular expressions in python syntax")
		g = parser.add_mutually_exclusive_group()
		g.add_argument('--id', action='store_true', help="'messages' are arbitration ids, no names")
		g.add_argument('--name', action='store_true', help="'messages' names, no arbitration ids")

	def iter_messages(self, args: argparse.Namespace) -> 'Iterator[str|int]':
		if not args.messages or '*' in args.messages:
			yield '*'
			return

		int_allowed = args.id or not args.name
		str_allowed = args.name or not args.id
		assert str_allowed or int_allowed
		msg: str
		for msg in args.messages:
			if str_allowed and self.app.bus_handler.get_cantools_message_by_name(msg):
				yield msg
				continue
			if int_allowed and msg.startswith('0x'):
				try:
					yield int(msg, base=0)
					continue
				except:
					pass
			if str_allowed:
				if not args.re:
					# I am not escaping msg because no special characters are allowed in a message name
					# so if you want to use some regex features, why not? Just remember that * has a different meaning.
					msg = msg.replace('*', '.*')
				reo = re.compile(msg, flags=re.I)
				found_something = False
				for ct_msg in self.app.bus_handler.iter_cantools_messages():
					if reo.search(ct_msg.name):
						yield ct_msg.name
						found_something = True
				if found_something:
					continue
			if int_allowed:
				try:
					yield int(msg, base=16)
					continue
				except ValueError:
					pass
			self.app.colored_print(self.app.color_error, f"invalid value {msg!r}")

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if '--id' in start_of_line:
			completions = [f"{msg.frame_id:0{get_id_width(msg)}x}" for msg in self.app.bus_handler.iter_cantools_messages()]
			completions = [m for m in completions if m.startswith(start)]
		else:
			completions = self.app.bus_handler.get_completions_for_message_name(start)
		return start_of_line, completions, end_of_line


class Hide(MessageTakingCommand):

	__doc__ = '''
	Do not print received messages of the specified type.

	''' + assert_str(MessageTakingCommand.__doc__)

	aliases = ('-',)

	def run_parsed(self, args: argparse.Namespace) -> None:
		for msg in self.iter_messages(args):
			self.app.hide(msg)

class Show(MessageTakingCommand):

	__doc__ = '''
	Undo the effect of a previous hide command.

	''' + assert_str(MessageTakingCommand.__doc__)

	aliases = ('+',)

	def run_parsed(self, args: argparse.Namespace) -> None:
		for msg in self.iter_messages(args):
			self.app.show(msg)

class Next(MessageTakingCommand):

	__doc__ = '''
	Print the next received message of the specified type
	regardless of whether it has been disabled with the hide command.

	''' + assert_str(MessageTakingCommand.__doc__)

	aliases = ('/',)

	def run_parsed(self, args: argparse.Namespace) -> None:
		self.app.next(set(self.iter_messages(args)))

class Prev(MessageTakingCommand):

	__doc__ = '''
	Print the last received message of the specified type.

	''' + assert_str(MessageTakingCommand.__doc__)

	aliases = ('?',)

	def run_parsed(self, args: argparse.Namespace) -> None:
		self.app.prev(list(self.iter_messages(args)))

	def get_completions_for_action(self, action: 'argparse.Action|None', start: str, *, start_of_line: str, end_of_line: str) -> 'tuple[str, list[str], str]':
		if '--id' in start_of_line:
			completions = [f"{msg:x}" for msg in self.app._last.keys() if isinstance(msg, int)]
		else:
			completions = [msg for msg in self.app._last.keys() if isinstance(msg, str)]
		completions = [m for m in completions if m.startswith(start)]
		return start_of_line, completions, end_of_line

# ---------- query database ----------

class Grep(CancliCommand):

	'''
	Search for signal.
	'''

	PREFIXES = ('m', 'k', 'M')
	TIME_UNITS = ('s', 'min', 'h')

	def init_parser(self, parser: argparse.ArgumentParser) -> None:
		parser.add_argument("signal", default='', nargs='?')
		parser.add_argument("-u", "--unit", help="limit results to signals matching the given unit, units referring to the same physical quantity are tried to consider equal, e.g. searching for --unit=mAh will also yield signals in Ah")

		self.reo_has_prefix = re.compile('^(%s).' % '|'.join(self.PREFIXES))
		self.pattern_opt_prefix = '(%s)?' % '|'.join(self.PREFIXES)

	def run_parsed(self, args: argparse.Namespace) -> None:
		if args.unit:
			p = args.unit
			if p == "C":
				p = ".*C"
			elif p in self.TIME_UNITS:
				p = "|".join(self.TIME_UNITS)
			else:
				m = self.reo_has_prefix.match(p)
				if m:
					p = p[len(m.group(1)):]
				p = self.pattern_opt_prefix + p
			p += '$'
			reo_unit = re.compile(p)
			def match_unit(unit: 'str|None') -> bool:
				if not unit:
					return False
				return bool(reo_unit.match(unit))
		else:
			def match_unit(unit: 'str|None') -> bool:
				return True

		reo = re.compile(args.signal, re.I)
		for msg in self.app.bus_handler.iter_cantools_messages():
			for sig in msg.signals:
				if match_unit(sig.unit) and reo.search(sig.name):
					self.app.colored_print(None, f"{msg.name}.{sig.name}")


# ---------- main ----------

def main(args: 'list[str]|None' = None) -> None:
	app = App(args)
	app.run()

if __name__ == '__main__':
	main()
