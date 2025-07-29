#!/usr/bin/env python3

import argparse
from collections.abc import Sequence, Callable

def hex_int(val: str) -> int:
	if val.startswith('0x'):
		return int(val, base=0)
	return int(val, base=16)

class LiteralAction(argparse.Action):

	def __init__(self, option_strings: 'list[str]', dest: str, *, required: bool, optional: bool) -> None:
		if optional:
			required = False
		self.literal = dest
		super().__init__(option_strings=option_strings, dest=dest, metavar=self.literal, required=required)
		
	def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: object, option_string: 'str|None' = None) -> None:
		if values != self.literal:
			raise argparse.ArgumentError(self, f"expected {self.literal!r} instead of {values!r}")


class CallAction(argparse.Action):

	def __init__(self, option_strings: 'Sequence[str]', dest: str, callback: 'Callable[[], None]', help: str) -> None:
		argparse.Action.__init__(self, option_strings, dest, nargs=0, help=help)
		self.callback = callback

	def __call__(self, parser: argparse.ArgumentParser, namespace: argparse.Namespace, values: object, option_string: 'str|None' = None) -> None:
		self.callback()
