#!./runmodule.sh

'''
parse Socket CAN error frames
https://github.com/torvalds/linux/blob/master/include/uapi/linux/can/error.h

usage:
	err = ErrorFrame(canmsg)
	logging.warning('CAN bus error: %s', err)
'''

import enum
import collections.abc
import can


def format_enum_item(val: 'enum.Enum|enum.IntFlag') -> str:
	if isinstance(val, enum.IntFlag):
		return format_int_flag(val)
	else:
		return format_single_enum_item(val)

def format_single_enum_item(val: 'enum.Enum|enum.IntFlag') -> str:
	if val.name is None:
		raise TypeError(f'{val} has no name')
	return val.name.lower().replace('_', ' ')

def format_int_flag(val: enum.IntFlag) -> str:
	out: 'list[enum.IntFlag]' = []
	for i in tuple(type(val)):
		assert isinstance(i, enum.IntFlag)
		if i in val:
			out.append(i)
	return format_enums(out)

def format_enums(l: 'collections.abc.Iterable[enum.Enum|enum.IntFlag]') -> str:
	return ', '.join(format_single_enum_item(i) for i in l)



@enum.unique
class ErrorClass(enum.IntFlag):
	TX_TIMEOUT           = 0x00000001,  # TX timeout (by netdevice driver)
	LOST_ARBITRATION     = 0x00000002,  # lost arbitration    / data[0]
	CONTROLLER_PROBLEM   = 0x00000004,  # controller problems / data[1]
	PROTOCOL_VIOLATION   = 0x00000008,  # protocol violations / data[2..3]
	TRANSCEIVER_PROBLEM  = 0x00000010,  # transceiver status  / data[4]
	MISSING_ACK          = 0x00000020,  # received no ACK on transmission
	BUS_OFF              = 0x00000040,  # bus off
	BUS_ERROR            = 0x00000080,  # bus error (may flood!)
	CONTROLLER_RESTARTED = 0x00000100,  # controller restarted
	COUNTER              = 0x00000200,  # TX error counter / data[6]
	                                    # RX error counter / data[7]

@enum.unique
class ControllerStatus(enum.IntFlag):
	UNSPECIFIED = 0x00  # unspecified
	RX_OVERFLOW = 0x01  # RX buffer overflow
	TX_OVERFLOW = 0x02  # TX buffer overflow
	RX_WARNING  = 0x04  # reached warning level for RX errors
	TX_WARNING  = 0x08  # reached warning level for TX errors
	RX_PASSIVE  = 0x10  # reached error passive status RX
	TX_PASSIVE  = 0x20  # reached error passive status TX
	                    # (at least one error counter exceeds
	                    # the protocol-defined level of 127)
	ACTIVE      = 0x40  # recovered to error active state

@enum.unique
class ProtocolViolationType(enum.IntFlag):
	UNSPECIFIED    = 0x00  # unspecified
	SINGLE_BIT     = 0x01  # single bit error
	FRAME_FORMAT   = 0x02  # frame format error
	BIT_STUFFING   = 0x04  # bit stuffing error
	BIT0           = 0x08  # unable to send dominant bit
	BIT1           = 0x10  # unable to send recessive bit
	OVERLOAD       = 0x20  # bus overload
	ACTIVE         = 0x40  # active error announcement
	TX             = 0x80  # error occurred on transmission

@enum.unique
class ProtocolViolationLocation(enum.Enum):
	UNSPECIFIED     = 0x00  # unspecified
	START_OF_FRAME  = 0x03  # start of frame
	ID_28_to_21     = 0x02  # ID bits 28 - 21 (SFF: 10 - 3)
	ID_20_to_18     = 0x06  # ID bits 20 - 18 (SFF: 2 - 0 )
	SUSTITUTE_RTR   = 0x04  # substitute RTR (SFF: RTR)
	ID_EXTENSION    = 0x05  # identifier extension
	ID_17_to_13     = 0x07  # ID bits 17-13
	ID_12_to_05     = 0x0F  # ID bits 12-5
	ID_04_to_00     = 0x0E  # ID bits 4-0
	RTR             = 0x0C  # RTR
	RESERVED_BIT_1  = 0x0D  # reserved bit 1
	RESERVED_BIT_0  = 0x09  # reserved bit 0
	DLC             = 0x0B  # data length code
	DATA            = 0x0A  # data section
	CRC_SEQ         = 0x08  # CRC sequence
	CRC_DEL         = 0x18  # CRC delimiter
	ACK             = 0x19  # ACK slot
	ACK_DEL         = 0x1B  # ACK delimiter
	END_OF_FRAME    = 0x1A  # end of frame
	INTERMISSION    = 0x12  # intermission

@enum.unique
class TransceiverStatus(enum.Enum):
	CAN_ERR_TRX_UNSPEC             = 0x00  #0000 0000
	CAN_ERR_TRX_CANH_NO_WIRE       = 0x04  #0000 0100
	CAN_ERR_TRX_CANH_SHORT_TO_BAT  = 0x05  #0000 0101
	CAN_ERR_TRX_CANH_SHORT_TO_VCC  = 0x06  #0000 0110
	CAN_ERR_TRX_CANH_SHORT_TO_GND  = 0x07  #0000 0111
	CAN_ERR_TRX_CANL_NO_WIRE       = 0x40  #0100 0000
	CAN_ERR_TRX_CANL_SHORT_TO_BAT  = 0x50  #0101 0000
	CAN_ERR_TRX_CANL_SHORT_TO_VCC  = 0x60  #0110 0000
	CAN_ERR_TRX_CANL_SHORT_TO_GND  = 0x70  #0111 0000
	CAN_ERR_TRX_CANL_SHORT_TO_CANH = 0x80  #1000 0000



class ErrorFrame:

	def __init__(self, canmsg: can.Message) -> None:
		if not canmsg.is_error_frame:
			raise TypeError('canmsg is not an error frame')
		self.canmsg = canmsg

	def get_error_class(self) -> ErrorClass:
		return ErrorClass(self.canmsg.arbitration_id)

	def get_bit_where_arbitration_was_lost(self) -> int:
		'''0: UNSPECIFIED'''
		return self.canmsg.data[0]

	def get_controller_status(self) -> ControllerStatus:
		return ControllerStatus(self.canmsg.data[1])

	def get_protocol_violation_type(self) -> ProtocolViolationType:
		return ProtocolViolationType(self.canmsg.data[2])

	def get_protocol_violation_location(self) -> ProtocolViolationLocation:
		return ProtocolViolationLocation(self.canmsg.data[3])

	def get_transceiver_status(self) -> TransceiverStatus:
		return TransceiverStatus(self.canmsg.data[4])

	def get_tx_error_counter(self) -> int:
		return self.canmsg.data[6]

	def get_rx_error_counter(self) -> int:
		return self.canmsg.data[7]

	def __str__(self) -> str:
		error = self.get_error_class()
		out = format_int_flag(error)
		p = ' (%s)'
		if ErrorClass.LOST_ARBITRATION in error:
			out += p % f'bit where arbitration was lost: {self.get_bit_where_arbitration_was_lost()}'
		if ErrorClass.CONTROLLER_PROBLEM in error:
			out += p % f'controller status: {format_enum_item(self.get_controller_status())}'
		if ErrorClass.PROTOCOL_VIOLATION in error:
			out += p % f'violation type: {format_enum_item(self.get_protocol_violation_type())}; ' \
			           f'violation location: {format_enum_item(self.get_protocol_violation_location())}'
		if ErrorClass.TRANSCEIVER_PROBLEM in error:
			out += p % f'transceiver status: {format_enum_item(self.get_transceiver_status())}'
		if ErrorClass.COUNTER in error:
			out += p % f'TX error counter: {self.get_tx_error_counter()}; RX error counter: {self.get_rx_error_counter()}'
		return out
