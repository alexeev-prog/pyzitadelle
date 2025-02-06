import traceback
import inspect
import asyncio
from dataclasses import dataclass, field
from time import time
from typing import Any, Callable, Awaitable, Union

from pyzitadelle.exceptions import TestError
from pyzitadelle.reporter import print_header, print_platform, print_test_result


@dataclass
class TestInfo:
	"""
	This class describes a test information.
	"""

	handler: Union[Callable, Awaitable]
	args: list = field(default_factory=list)
	kwargs: list = field(default_factory=dict)
	count_of_launchs: int = 1


class BaseTestCase:
	"""
	This class describes a base test case.
	"""

	def __init__(self, label: str = "AIOTestCase"):
		"""
		Constructs a new instance.

		:param      label:  The label
		:type       label:  str
		"""
		self.label = label

		self.warnings = 0
		self.errors = 0
		self.passed = 0

		self.tests = {}


class TestCase(BaseTestCase):
	"""
	This class describes a test case.
	"""

	def __init__(self, label: str = "TestCase"):
		"""
		Constructs a new instance.

		:param		label:	The label
		:type		label:	str
		"""
		super().__init__(label)

	def test(self, count_of_launchs: int = 1) -> Callable:
		"""
		Add test to environment
		
		:param      count_of_launchs:  The count of launchs
		:type       count_of_launchs:  int
		
		:returns:   wrapper
		:rtype:     Callable
		"""
		def wrapper(func, *args, **kwargs):
			self.tests[func.__name__] = TestInfo(
				handler=func,
				args=args,
				kwargs=kwargs,
				count_of_launchs=count_of_launchs,
			)
			return func

		return wrapper

	def _launch_test_chain(self, length: int):
		"""
		Launch testing chain

		:param      length:  The length of tests list
		:type       length:  int
		"""
		results = []

		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			percent = int((test_num / length) * 100)

			try:
				for _ in range(test.count_of_launchs):
					if inspect.iscoroutinefunction(test.handler):
						result = asyncio.run(test.handler(*test.args, **test.kwargs))
					else:
						result = test.handler(*test.args, **test.kwargs)

				results.append(result)
			except AssertionError:
				print_test_result(
					percent,
					test_name,
					status="error",
					output=f"AssertionError (use pyzitadelle.test_case.expect, not assert)\n{traceback.format_exc()}",
				)
				self.errors += 1
			except TestError:
				print_test_result(
					percent,
					test_name,
					status="error",
					output=str(traceback.format_exc()),
				)
				self.errors += 1
			else:
				self.passed += 1

				print_test_result(percent, test_name)

	def run(self):
		"""
		Run testing
		"""
		print_header("test session starts")

		length = len(self.tests)
		print_platform(length)

		start = time()

		self._launch_test_chain(length)

		end = time()
		total = end - start

		print_header(
			f"[cyan]{length} tests runned {round(total, 2)}s[/cyan]", plus_len=15
		)

		print_header(
			f"[green]{self.passed} passed[/green], [yellow]{self.warnings} warnings[/yellow], [red]{self.errors} errors[/red]",
			plus_len=45,
		)


def expect(lhs: Any, rhs: Any, message: str) -> bool:
	"""
	Expect lhs and rhs with message
	
	:param      lhs:        The left hand side
	:type       lhs:        Any
	:param      rhs:        The right hand side
	:type       rhs:        Any
	:param      message:    The message
	:type       message:    str
	
	:returns:   true is equals, raise error otherwise
	:rtype:     bool
	
	:raises     TestError:  lhs and rhs is not equals
	"""
	if lhs == rhs:
		return True
	else:
		raise TestError(message)
