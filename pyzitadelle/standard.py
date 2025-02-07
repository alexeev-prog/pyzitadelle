from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
	Any,
	AsyncGenerator,
	Awaitable,
	Callable,
	Generator,
	Optional,
	Tuple,
	Union,
)


class TestOutcome(Enum):
	"""
	Enumeration representing all possible outcomes of an attempt at running a test.

	Attributes:
					PASS: Represents a passing test outcome - no errors raised, no assertions failed, the test ran to completion.
					FAIL: The test failed in some way - e.g. an assertion failed or an exception was raised.
					SKIP: The test was skipped.
					XFAIL: The test was expected to fail, and it did fail.
					XPASS: The test was expected to fail, however it unexpectedly passed.
					DRYRUN: The test was not executed because the test session was a dry-run.
	"""

	PASS = auto()
	FAIL = auto()
	SKIP = auto()
	XFAIL = auto()	# expected fail
	XPASS = auto()	# unexpected pass
	DRYRUN = auto()	 # tests arent executed during dryruns

	@property
	def display_char(self):
		display_chars = {
			TestOutcome.PASS: ".",
			TestOutcome.FAIL: "F",
			TestOutcome.SKIP: "-",
			TestOutcome.XPASS: "U",
			TestOutcome.XFAIL: "x",
			TestOutcome.DRYRUN: ".",
		}
		assert len(display_chars) == len(TestOutcome)
		return display_chars[self]

	@property
	def display_name(self):
		display_names = {
			TestOutcome.PASS: "Passes",
			TestOutcome.FAIL: "Failures",
			TestOutcome.SKIP: "Skips",
			TestOutcome.XPASS: "Unexpected Passes",
			TestOutcome.XFAIL: "Expected Failures",
			TestOutcome.DRYRUN: "Dry-runs",
		}
		assert len(display_names) == len(TestOutcome)
		return display_names[self]

	@property
	def will_fail_session(self) -> bool:
		return self in {TestOutcome.FAIL, TestOutcome.XPASS}

	@property
	def wont_fail_session(self) -> bool:
		return not self.will_fail_session


@dataclass
class Argument:
	args: list = field(default_factory=list)
	kwargs: dict = field(default_factory=dict)


@dataclass
class Each:
	args: Tuple[Any]

	def __getitem__(self, args):
		return self.args[args]

	def __len__(self):
		return len(self.args)


@dataclass
class Marker:
	name: str
	reason: Optional[str] = None
	when: Union[bool, Callable] = True

	@property
	def active(self):
		try:
			return self.when()
		except TypeError:
			return self.when


@dataclass
class SkipMarker(Marker):
	"""
	Marker that gets attached to a test (via CollectionMetadata) to indicate it should be skipped.
	"""

	name: str = "SKIP"


@dataclass
class ExpectFailMarkup(Marker):
	"""
	Marker that gets attached to a test (via CollectionMetadata) to indicate that we expect it to fail.
	"""

	name: str = "XFAIL"


@dataclass
class CollectionMetadata:
	"""
	Attached to tests and fixtures during the collection phase for later use.
	"""

	marker: Optional[Marker] = None
	comment: Optional[str] = None
	tags: list = field(default_factory=list)
	arguments: list = field(default_factory=list)
	count_of_launchs: int = 1
	is_fixture: bool = False


@dataclass
class Fixture:
	handler: Union[Awaitable, Callable]
	gen: Union[Generator, AsyncGenerator, None] = None
	resolved_val: Any = None

	@property
	def metadata(self):
		return self.handler.pztdmeta
