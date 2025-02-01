from dataclasses import dataclass, field
from time import time
from typing import Callable

from pyzitadelle.exceptions import TestError
from pyzitadelle.reporter import print_header, print_platform, print_test_result


@dataclass
class TestInfo:
	handler: Callable
	args: list = field(default_factory=list)
	kwargs: list = field(default_factory=dict)


class BaseTestCase:
	def __init__(self, label: str = "AIOTestCase"):
		self.label = label

		self.warnings = 0
		self.errors = 0
		self.passed = 0

		self.tests = {}


class TestCase(BaseTestCase):
	def __init__(self, label: str = "TestCase"):
		super().__init__(label)

	def test(self):
		def wrapper(func, *args, **kwargs):
			self.tests[func.__name__] = TestInfo(handler=func, args=args, kwargs=kwargs)
			return func

		return wrapper

	def run(self):
		print_header("test session starts")

		length = len(self.tests)
		print_platform(length)

		results = []

		start = time()
		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			percent = int((test_num / length) * 100)

			try:
				result = test.handler(*test.args, **test.kwargs)
				results.append(result)
			except AssertionError:
				print_test_result(
					percent, test_name, status="error", output="AssertionError"
				)
				self.errors += 1
			except TestError as te:
				print_test_result(percent, test_name, status="error", output=str(te))
				self.errors += 1
			else:
				self.passed += 1

				print_test_result(percent, test_name)

		end = time()

		total = end - start

		print_header(f'[cyan]{length} tests runned {round(total, 2)}s[/cyan]', plus_len=15)

		print_header(
			f"[green]{self.passed} passed[/green], [yellow]{self.warnings} warnings[/yellow], [red]{self.errors} errors[/red]",
			plus_len=45,
		)


def expect(lhs, rhs, message: str):
	if lhs == rhs:
		return True
	else:
		raise TestError(message)
