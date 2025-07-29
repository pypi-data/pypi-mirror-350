#!./runmodule.sh

import platform
import logging
import atexit
import typing

import can


TYPE_BUS: 'typing.TypeAlias' = 'can.BusABC'

logger = logging.getLogger(__name__)
buses: 'list[TYPE_BUS]' = []


class Bitrate:

	NONE = "none"

	help = "The bitrate of the CAN bus"

	def __init__(self, val: str) -> None:
		if val == self.NONE:
			self.value = None
		else:
			self.value = int(val.replace('k', '_000').replace('M', '_000_000'))

	def __str__(self) -> str:
		if self.value is None:
			return self.NONE

		out = "%s" % self.value
		if out.endswith("000000"):
			out = out[:-6] + "M"
		elif out.endswith("000"):
			out = out[:-3] + "k"
		return out

	def __eq__(self, other: object) -> bool:
		if isinstance(other, Bitrate):
			return self.value == other.value
		return self.value == other

	def is_none(self) -> bool:
		return self.value is None


class CanSetupException(Exception):

	pass


if platform.system() == "Linux":
	import subprocess

	def init(bitrate: Bitrate, *, channel: 'str|None' = None, bustype: 'str|None' = None) -> 'TYPE_BUS':
		if bustype is None:
			bustype = "socketcan"
		if channel is None:
			channel = "can0"

		check_configured_bitrate(channel, bitrate)

		bus: 'TYPE_BUS' = can.Bus(channel, bustype=bustype)
		buses.append(bus)
		return bus

	def check_configured_bitrate(channel: str, bitrate: Bitrate) -> None:
		if channel.startswith("v"):
			# virtual CAN bus has no bitrate
			return

		cmd_bus_down = ["sudo", "ip", "link", "set", channel, "down"]
		cmd_bus_up   = ["sudo", "ip", "link", "set", channel, "up", "type", "can", "bitrate", str(bitrate.value)]

		# ------- check if CAN bus is up or down --------
		cmd = "ip -d link show " + channel + " | grep 'state DOWN'"
		p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
		if p.returncode == 0:
			if bitrate.is_none():
				raise CanSetupException("CAN bus %s is down and no bitrate has been specified" % channel)
			try:
				_run(cmd_bus_up)
				return
			except Exception as e:
				raise CanSetupException("Failed to start CAN bus: %s" % e)

		# ------- check if CAN bus has correct bitrate ------
		if bitrate.is_none():
			return

		cmd = "ip -d link show " + channel + " | awk '/bitrate/ {print $2}'"
		# check is not that useful here because awk overrides the return code of ip
		p = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
		if p.stderr:
			raise CanSetupException(p.stderr.decode(encoding="utf8"))
		if not p.stdout:
			try:
				_run(cmd_bus_up)
				return
			except Exception as e:
				raise CanSetupException("Failed to determine the current bitrate. Failed to set the bitrate. %s" % e)

		configured_bitrate = Bitrate(p.stdout.decode())

		if configured_bitrate != bitrate:
			try:
				_run(cmd_bus_down)
				_run(cmd_bus_up)
				return
			except Exception as e:
				raise CanSetupException(f"Failed to restart the CAN bus in order to change the bitrate from {configured_bitrate} to {bitrate}")

	def _run(cmd: 'list[str]') -> None:
		print("[executing %s]" % " ".join(cmd))
		subprocess.run(cmd, check=True)

	def set_tx_queue_len(channel: str, length: int) -> None:
		cmd = ['sudo', 'ifconfig', channel, 'txqueuelen', str(length)]
		_run(cmd)

	# in python error frames are always enabled so we don't need a function to do that
	# https://github.com/hardbyte/python-can/pull/384

else:
	def init(bitrate: Bitrate, *, channel: 'str|None' = None, bustype: 'str|None' = None) -> 'TYPE_BUS':
		if bustype is None:
			bustype = "pcan"
		if channel is None:
			channel = "PCAN_USBBUS2"
		bus: 'TYPE_BUS' = can.Bus(channel, bustype=bustype, bitrate=bitrate.value)
		buses.append(bus)
		return bus

	def set_tx_queue_len(channel: str, length: int) -> None:
		raise NotImplementedError()


def shutdown(bus: 'TYPE_BUS') -> None:
	logger.info("shutting down CAN bus %s" % bus.channel_info)
	bus.shutdown()
	buses.remove(bus)

def shutdown_all() -> None:
	"""
	Close all buses which have been opened with :func:`init` and not yet been closed with :func:`shutdown`.
	This function is called automatically by atexit and does not need to be called manually.
	"""
	for bus in buses:
		shutdown(bus)

atexit.register(shutdown_all)
