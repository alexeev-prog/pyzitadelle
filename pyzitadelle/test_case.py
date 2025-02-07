from time import time
from functools import wraps, partial
from typing import Any, Callable, List, Dict, Optional, Awaitable, Union, Tuple
from pyzitadelle.exceptions import TestError
from pyzitadelle.reporter import print_header, print_results_table
from pyzitadelle.sessions import Runner
from pyzitadelle.standard import Argument, Each, Fixture, CollectionMetadata, SkipMarker, ExpectFailMarkup


def skip(
	func_or_reason: Union[str, Callable, None] = None,
	*,
	reason: Optional[str] = None,
	when: Union[bool, Callable] = True,
):
	"""
	Decorator which can be used to optionally skip tests.
	"""
	if func_or_reason is None:
		return partial(skip, reason=reason, when=when)

	if isinstance(func_or_reason, str):
		return partial(skip, reason=func_or_reason, when=when)

	func = func_or_reason

	marker = SkipMarker(reason=reason, when=when)

	if hasattr(func, "ward_meta"):
		func.pztdmeta.marker = marker  # type: ignore[attr-defined]
	else:
		func.pztdmeta = CollectionMetadata(marker=marker)  # type: ignore[attr-defined]

	@wraps(func)
	def wrapper(*args, **kwargs):
		return func(*args, **kwargs)

	return wrapper


def expectfail(
	func_or_reason: Union[str, Callable, None] = None,
	*,
	reason: Optional[str] = None,
	when: Union[bool, Callable] = True,
):
	if func_or_reason is None:
		return partial(expectfail, reason=reason, when=when)

	if isinstance(func_or_reason, str):
		return partial(expectfail, reason=func_or_reason, when=when)

	func = func_or_reason
	marker = ExpectFailMarkup(reason=reason, when=when)
	
	if hasattr(func, "pztdmeta"):
		func.pztdmeta.marker = marker  # type: ignore[attr-defined]
	else:
		func.pztdmeta = CollectionMetadata(marker=marker)  # type: ignore[attr-defined]

	@wraps(func)
	def wrapper(*args, **kwargs):
		return func(*args, **kwargs)

	return wrapper


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
		self.label: str = label

		self.warnings: int = 0
		self.tags: List[str] = []
		self.fixtures: Dict[str, Fixture] = []
		self.skipped: int = 0
		self.errors: int = 0
		self.passed: int = 0

		self.tests: Dict[str, Union[Callable, Awaitable]] = {}


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

	def fixture(self):
		def wrapper(func: Union[Awaitable, Callable], *args, **kwargs) -> Union[Awaitable, Callable]:
			if not hasattr(func, 'pztdmeta'):
				func.pztdmeta = CollectionMetadata(is_fixture=True)
			else:
				func.pztdmeta.is_fixture = True

			self.fixtures[func.__name__] = Fixture(handler=func)

			return func(*args, **kwargs)
		return wrapper

	def test(
		self, comment: str = None, 
		tags: List[str] = [], 
		count_of_launchs: int = 1,
		arguments: Tuple[Argument] = (),
	) -> Callable:
		"""
		Add test to environment
		
		:param      comment:           The comment
		:type       comment:           str
		:param      tags:              The tags
		:type       tags:              Array
		:param      count_of_launchs:  The count of launchs
		:type       count_of_launchs:  int
		:param      skip_test:         The skip test
		:type       skip_test:         bool
		:param      arguments:         The arguments
		:type       arguments:         Tuple[Argument]
		
		:returns:   wrapper
		:rtype:     Callable
		"""

		def wrapper(func: Union[Awaitable, Callable], *args, **kwargs) -> Union[Awaitable, Callable]:
			"""
			Wrapper for @test decorator

			:param      func:    The function
			:type       func:    Union[Awaitable, Callable]
			:param      args:    The arguments
			:type       args:    list
			:param      kwargs:  The keywords arguments
			:type       kwargs:  dictionary

			:returns:   function
			:rtype:     Union[Awaitable, Callable]
			"""
			if not hasattr(func, 'pztdmeta'):
				func.pztdmeta = CollectionMetadata(comment=comment.format(**kwargs) if comment is not None else None,
													tags=tags,
													arguments=arguments,
													count_of_launchs=count_of_launchs)
			else:
				func.pztdmeta.comment = comment.format(**kwargs) if comment is not None else None
				func.pztdmeta.tags = tags
				func.pztdmeta.arguments = arguments
				func.pztdmeta.count_of_launchs = count_of_launchs

			self.tags = list(set(self.tags + tags))

			self.tests[func.__name__] = func
			return func

		return wrapper

	def run(self, tags: Optional[List[str]] = []):
		"""
		Run testing
		"""
		runner = Runner(self.tests, self)

		start = time()

		runner.launch_test_chain(tags=tags)

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


def each(*args):
	return Each(args)
