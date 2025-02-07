import asyncio
import inspect
import traceback
from typing import Any, Awaitable, Callable, List, Union

from pyzitadelle.exceptions import SkippedTestException, TestError
from pyzitadelle.reporter import print_header, print_platform, print_test_result
from pyzitadelle.standard import ExpectFailMarkup, SkipMarker


class Runner:
	"""
	This class describes a runner session.
	"""

	def __init__(self, tests: int, testcase: object):
		"""
		Constructs a new instance.

		:param		tests:	   The tests
		:type		tests:	   int
		:param		testcase:  The testcase
		:type		testcase:  TestCase
		"""
		self.tests = tests
		self.tests_count = len(self.tests)
		self.testcase = testcase

	def _print_prelude(self):
		"""
		Prints a prelude.
		"""
		print_header("runner session starts")

		print_platform(self.tests_count)

	def _run_testinfo(self, test: Union[Callable, Awaitable], *args, **kwargs) -> Any:
		"""
		Run test with args

		:param		test:	 The test
		:type		test:	 TestInfo
		:param		args:	 The arguments
		:type		args:	 list
		:param		kwargs:	 The keywords arguments
		:type		kwargs:	 dictionary

		:returns:	function result
		:rtype:		Any
		"""
		if inspect.iscoroutinefunction(test):
			result = asyncio.run(test(*args, **kwargs))
		else:
			result = test(*args, **kwargs)

		return result

	def _run_test_cycle(self, test_name: str, test: Union[Awaitable, Callable]) -> Any:
		"""
		Run test launch cycle

		:param		test_name:	The test name
		:type		test_name:	str
		:param		test:		The test
		:type		test:		TestInfo

		:returns:	function result
		:rtype:		Any
		"""
		for n in range(test.pztdmeta.count_of_launchs):
			if test.pztdmeta.arguments:
				for argument in test.pztdmeta.arguments:
					result = self._run_testinfo(test, *argument.args, **argument.kwargs)
			else:
				result = self._run_testinfo(test)

		return result

	def _check_warnings(self, result: Any, results: list, percent: int, test_name: str):
		"""
		Check warnings in test

		:param		result:		The result
		:type		result:		Any
		:param		results:	The results
		:type		results:	list
		:param		percent:	The percent
		:type		percent:	int
		:param		test_name:	The test name
		:type		test_name:	str
		"""
		if len(results) > 0 and results[-1] == result and result is not None:
			print_test_result(
				percent,
				test_name,
				status="warning",
				output=f"Last result is equals current result ({results[-1]} == {result})",
			)
			self.testcase.warnings += 1
			self.testcase.passed += 1

	def _processing_tests_execution(
		self,
		tags: List[str],
		test_num: int,
		test_name: str,
		test: Union[Awaitable, Callable],
	):
		"""
		Processing tests execution

		:param		tags:				   The tags
		:type		tags:				   List[str]
		:param		test_num:			   The test number
		:type		test_num:			   int
		:param		test_name:			   The test name
		:type		test_name:			   str
		:param		test:				   The test
		:type		test:				   TestInfo

		:raises		SkippedTestException:  skip test
		"""
		percent = int((test_num / self.tests_count) * 100)
		results = []

		lines = inspect.getsourcelines(test)[1]
		test_name = f"{test_name}:{lines}"

		try:
			if tags and list(set(tags) & set(test.tags)):
				raise SkippedTestException()
			elif isinstance(test.pztdmeta.marker, SkipMarker):
				marker = test.pztdmeta.marker

				if marker.when:
					raise SkippedTestException(
						marker.reason if marker.reason else "SkippedTest"
					)
			elif isinstance(test.pztdmeta.marker, ExpectFailMarkup):
				marker = test.pztdmeta.marker

			result = self._run_test_cycle(test_name, test)

			self._check_warnings(result, results, percent, test_name)

			results.append(result)
		except SkippedTestException as ex:
			self.testcase.skipped += 1
			print_test_result(
				percent,
				test_name,
				status="skip",
				postmessage=str(ex),
				comment=test.pztdmeta.comment,
			)
		except (AssertionError, TestError):
			self.testcase.errors += 1

			if isinstance(marker, ExpectFailMarkup):
				print_test_result(
					percent,
					test_name,
					status="error",
					output=f"{traceback.format_exc()}",
					postmessage=marker.reason if marker.reason else "XFAIL",
					comment=test.pztdmeta.comment,
				)
			else:
				print_test_result(
					percent,
					test_name,
					status="error",
					output=f"{traceback.format_exc()}",
					comment=test.pztdmeta.comment,
				)
		else:
			self.testcase.passed += 1

			print_test_result(percent, test_name, comment=test.pztdmeta.comment)

	def launch_test_chain(self, tags: List[str]):
		"""
		Launch test chain

		:raises		SkippedTestException:  skip test

		:param		tags:  The tags
		:type		tags:  List[str]
		"""
		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			self._processing_tests_execution(tags, test_num, test_name, test)
