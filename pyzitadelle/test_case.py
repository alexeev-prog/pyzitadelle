from dataclasses import dataclass, field
from time import time
from typing import Callable, Any
import traceback
from functools import wraps
from pyzitadelle.exceptions import TestError
from pyzitadelle.reporter import print_header, print_platform, print_test_result


@dataclass
class TestInfo:
	handler: Callable
	args: list = field(default_factory=list)
	kwargs: list = field(default_factory=dict)
	count_of_launchs: int = 1


class BaseTestCase:
	def __init__(self, label: str = "AIOTestCase"):
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

		:param      label:  The label
		:type       label:  str
		"""
		super().__init__(label)

	def test(self, count_of_launchs: int = 1):
		def wrapper(func, *args, **kwargs):
			self.tests[func.__name__] = TestInfo(handler=func, args=args, kwargs=kwargs, count_of_launchs=count_of_launchs)
			return func

		return wrapper

	def _launch_test_chain(self, length: int):
		results = []

		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			percent = int((test_num / length) * 100)

			try:
				result = test.handler(*test.args, **test.kwargs)
				results.append(result)
			except AssertionError:
				print_test_result(
					percent, test_name, status="warning", output=f"AssertionError (use pyzitadelle.test_case.expect, not assert)\n{traceback.format_exc()}"
				)
				self.errors += 1
				self.warnings += 1
			except TestError:
				print_test_result(percent, test_name, status="error", output=str(traceback.format_exc()))
				self.errors += 1
			else:
				self.passed += 1

				print_test_result(percent, test_name)

	def run(self):
		print_header("test session starts")

		length = len(self.tests)
		print_platform(length)

		start = time()

		self._launch_test_chain(length)

		end = time()
		total = end - start

		print_header(f'[cyan]{length} tests runned {round(total, 2)}s[/cyan]', plus_len=15)

		print_header(
			f"[green]{self.passed} passed[/green], [yellow]{self.warnings} warnings[/yellow], [red]{self.errors} errors[/red]",
			plus_len=45,
		)


class AIOTestCase(BaseTestCase):
	"""
	This class describes a test case.
	"""

	def __init__(self, label: str = "AIOTestCase"):
		"""
		Constructs a new instance.

		:param      label:  The label
		:type       label:  str
		"""
		super().__init__(label)

	def test(self, count_of_launchs: int = 1):
		def decorator(func):
			@wraps(func)
			async def wrapper(*args, **kwargs):
				self.tests[func.__name__] = TestInfo(handler=func, args=args, kwargs=kwargs, count_of_launchs=count_of_launchs)
				return func

			return wrapper

		return decorator

	async def _launch_test_chain(self, length: int):
		results = []

		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			percent = int((test_num / length) * 100)

			try:
				result = await test.handler(*test.args, **test.kwargs)
				results.append(result)
			except AssertionError:
				print_test_result(
					percent, test_name, status="warning", output=f"AssertionError (use pyzitadelle.test_case.expect, not assert)\n{traceback.format_exc()}"
				)
				self.errors += 1
				self.warnings += 1
			except TestError:
				print_test_result(percent, test_name, status="error", output=str(traceback.format_exc()))
				self.errors += 1
			else:
				self.passed += 1

				print_test_result(percent, test_name)

	async def run(self):
		print_header("test session starts")

		length = len(self.tests)
		print_platform(length)

		start = time()

		await self._launch_test_chain(length)

		end = time()
		total = end - start

		print_header(f'[cyan]{length} tests runned {round(total, 2)}s[/cyan]', plus_len=15)

		print_header(
			f"[green]{self.passed} passed[/green], [yellow]{self.warnings} warnings[/yellow], [red]{self.errors} errors[/red]",
			plus_len=45,
		)


def expect(lhs: Any, rhs: Any, message: str):
	if lhs == rhs:
		return True
	else:
		raise TestError(message)
