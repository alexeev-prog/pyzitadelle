from time import time
from typing import Any, Callable

from pyzitadelle.exceptions import TestError
from pyzitadelle.reporter import print_header, print_results_table
from pyzitadelle.sessions import Runner
from pyzitadelle.standard import TestInfo


class BaseTestCase:
	"""
	This class describes a base test case.
	"""

	def __init__(self, label: str = "TestCase"):
		"""
		Constructs a new instance.

		:param		label:	The label
		:type		label:	str
		"""
		self.label = label

		self.warnings = 0
		self.skipped = 0
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

	def test(
		self, comment: str = None, count_of_launchs: int = 1, skip_test: bool = False
	) -> Callable:
		"""
		Add test to environment

		:param		count_of_launchs:  The count of launchs
		:type		count_of_launchs:  int

		:returns:	wrapper
		:rtype:		Callable
		"""

		def wrapper(func, *args, **kwargs):
			self.tests[func.__name__] = TestInfo(
				skip=skip_test,
				comment=comment.format(**kwargs) if comment is not None else None,
				handler=func,
				args=args,
				kwargs=kwargs,
				count_of_launchs=count_of_launchs,
			)
			return func

		return wrapper

	def run(self):
		"""
		Run testing
		"""
		runner = Runner(self.tests, self)

		start = time()

		runner.launch_test_chain()

		end = time()
		total = end - start

		print_header(
			f"[cyan]{len(self.tests)} tests runned {round(total, 2)}s[/cyan]",
			plus_len=15,
		)

		print_results_table(
			len(self.tests), self.passed, self.warnings, self.errors, self.skipped
		)


def expect(lhs: Any, rhs: Any, message: str) -> bool:
	"""
	Expect lhs and rhs with message

	:param		lhs:		The left hand side
	:type		lhs:		Any
	:param		rhs:		The right hand side
	:type		rhs:		Any
	:param		message:	The message
	:type		message:	str

	:returns:	true is equals, raise error otherwise
	:rtype:		bool

	:raises		TestError:	lhs and rhs is not equals
	"""
	if lhs == rhs:
		return True
	else:
		raise TestError(message)
