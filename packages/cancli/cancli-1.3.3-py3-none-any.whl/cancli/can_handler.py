#!./runmodule.sh

from collections.abc import Callable, Iterator

import can
import cantools
from confattr import ParseException

from . import can_setup

TYPE_BUS = can_setup.TYPE_BUS
TYPE_CANTOOLS_MESSAGE = cantools.database.can.message.Message
TYPE_CANTOOLS_DATABASE = cantools.database.can.database.Database
TYPE_CANTOOLS_NAMED_SIGNAL_VALUE = cantools.database.namedsignalvalue.NamedSignalValue

class CantoolsEncodeException(Exception):
	pass

class CanBusHandler:

	PARAM_NODE_ID = 'node_id'

	def __init__(self, listener: 'Callable[[can.Message], None]') -> None:
		self.listener = listener
		self.notifier: 'can.Notifier|None' = None
		self.buses: 'dict[tuple[str|None, str|None], TYPE_BUS]' = {}
		self.db_files: 'dict[str, TYPE_CANTOOLS_DATABASE]' = {}
		self.node_id_mask = 0
		self.node_id_shift = 0
		self.and_mask = 0
		self.or_mask = 0

	# ------- buses -------

	def connect_to_bus(self, bitrate: can_setup.Bitrate, channel: 'str|None', bustype: 'str|None') -> None:
		bus = can_setup.init(bitrate=bitrate, channel=channel, bustype=bustype)
		self.buses[(channel, bustype)] = bus
		if self.notifier:
			self.notifier.add_bus(bus)
		else:
			self.notifier = can.Notifier(list(self.buses.values()), [self.on_receive])

	def disconnect_from_all_buses(self) -> None:
		if self.notifier:
			self.notifier.remove_listener(self.on_receive)
			self.notifier.stop()
			self.notifier = None

		for bus in self.buses.values():
			can_setup.shutdown(bus)
		self.buses = {}

	def change_bitrate(self, bitrate: can_setup.Bitrate) -> None:
		bus_params = tuple(self.buses.keys())
		self.disconnect_from_all_buses()
		for channel, bustype in bus_params:
			self.connect_to_bus(bitrate, channel, bustype)

	def get_active_bus(self) -> 'TYPE_BUS|None':
		if not self.buses:
			return None
		return tuple(self.buses.values())[-1]

	# ------- dbc/sym files -------

	def add_db_file(self, fn: str) -> None:
		self.db_files[fn] = cantools.db.load_file(fn)

	def remove_all_db_files(self) -> None:
		self.db_files = {}

	def set_node_id(self, mask: int, shift: int) -> None:
		self.node_id_mask = mask
		self.node_id_shift = shift

	def set_and_mask(self, mask: int) -> None:
		self.and_mask = mask

	def set_or_mask(self, mask: int) -> None:
		self.or_mask = mask

	# ------- getters -------

	def is_node_id_set(self) -> bool:
		return bool(self.node_id_mask)

	def get_node_id(self, canmsg: can.Message) -> int:
		return canmsg.arbitration_id >> self.node_id_shift & self.node_id_mask

	def get_cantools_message(self, canmsg: can.Message) -> 'TYPE_CANTOOLS_MESSAGE|None':
		for db in self.db_files.values():
			arbitration_id: int = canmsg.arbitration_id
			try:
				return db.get_message_by_frame_id(arbitration_id)
			except KeyError:
				pass
			if self.node_id_mask:
				arbitration_id &= ~(self.node_id_mask << self.node_id_shift)
				try:
					return db.get_message_by_frame_id(arbitration_id)
				except KeyError:
					pass
			if self.and_mask:
				arbitration_id &= self.and_mask
				try:
					return db.get_message_by_frame_id(arbitration_id)
				except KeyError:
					pass
			if self.or_mask:
				arbitration_id |= self.or_mask
				try:
					return db.get_message_by_frame_id(arbitration_id)
				except KeyError:
					pass
		return None

	def get_cantools_message_by_name(self, name: str) -> 'TYPE_CANTOOLS_MESSAGE|None':
		for db in self.db_files.values():
			try:
				return db.get_message_by_name(name)
			except KeyError:
				pass
		return None

	def iter_cantools_messages(self) -> 'Iterator[TYPE_CANTOOLS_MESSAGE]':
		for db in self.db_files.values():
			yield from db.messages

	# ------- send and receive -------

	def on_receive(self, canmsg: can.Message) -> None:
		self.listener(canmsg)

	def send(self, msg: 'TYPE_CANTOOLS_MESSAGE', signals: 'cantools.typechecking.SignalMappingType', *, is_remote_frame: bool) -> can.Message:
		assert isinstance(signals, dict)
		arbitration_id = msg.frame_id
		if self.node_id_mask and self.PARAM_NODE_ID in signals:
			arbitration_id &= ~(self.node_id_mask << self.node_id_shift)
			arbitration_id |= signals.pop(self.PARAM_NODE_ID) << self.node_id_shift
		if is_remote_frame:
			return self.send_raw(arbitration_id, is_extended_id=msg.is_extended_frame, data=None, is_remote_frame=True)

		for s in msg.signals:
			if s.name not in signals and not s.multiplexer_signal:
				signals[s.name] = 0

		try:
			data = msg.encode(signals)
		except Exception as e:
			raise CantoolsEncodeException(e)
		return self.send_raw(arbitration_id, is_extended_id=msg.is_extended_frame, data=data, is_remote_frame=False)

	def send_raw(self, arbitration_id: int, *, is_extended_id: bool, data: 'bytes|None', is_remote_frame: bool) -> can.Message:
		bus = self.get_active_bus()
		if bus is None:
			raise ParseException(f"please setup a bus with 'bus can0 [bitrate]' first")

		canmsg = can.Message(arbitration_id=arbitration_id, is_extended_id=is_extended_id, data=data, is_remote_frame=is_remote_frame)
		bus.send(canmsg)
		return canmsg

	# ------- auto completion -------

	def get_completions_for_message_name(self, msg_start: str) -> 'list[str]':
		msg_start = msg_start.casefold()
		out = []
		for db in self.db_files.values():
			for msg in db.messages:
				if msg_start in msg.name.casefold():
					out.append(msg.name)
		return out

	def get_completions_for_signal_name(self, msg_name: str, signal_start: str) -> 'list[str]':
		msg = self.get_cantools_message_by_name(msg_name)
		if not msg:
			return []

		out = []
		signal_start = signal_start.casefold()
		for sig in msg.signals:
			if signal_start in sig.name.casefold():
				out.append(sig.name)
		if self.node_id_mask and signal_start in self.PARAM_NODE_ID:
			out.append(self.PARAM_NODE_ID)
		return out

	def get_completions_for_signal_value(self, msg_name: str, signal_name: str, value_start: str) -> 'list[str]':
		msg = self.get_cantools_message_by_name(msg_name)
		if not msg:
			return []

		try:
			sig = msg.get_signal_by_name(signal_name)
		except KeyError:
			return []
		if not sig.choices:
			return []

		value_start = value_start.casefold()
		return [str(name) for name in sig.choices.values() if value_start in str(name).casefold()]
