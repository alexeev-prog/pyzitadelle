import inspect
import asyncio
from typing import Any
import traceback
from pyzitadelle.exceptions import TestError, SkippedTestException
from pyzitadelle.reporter import print_header, print_platform, print_test_result, print_comment
from pyzitadelle.standard import TestInfo


class Runner:
	"""
	This class describes a runner session.
	"""

	def __init__(self, tests: int, testcase: object):
		"""
		Constructs a new instance.

		:param      tests:     The tests
		:type       tests:     int
		:param      testcase:  The testcase
		:type       testcase:  TestCase
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

	def _run_test_cycle(self, test_name: str, test: TestInfo) -> Any:
		"""
		Run test launch cycle

		:param      test_name:  The test name
		:type       test_name:  str
		:param      test:       The test
		:type       test:       TestInfo

		:returns:   function result
		:rtype:     Any
		"""
		for n in range(test.count_of_launchs):
			if test.count_of_launchs > 1:
				print(f'Launch {test_name}: {n + 1}/{test.count_of_launchs}')

			if inspect.iscoroutinefunction(test.handler):
				result = asyncio.run(test.handler(*test.args, **test.kwargs))
			else:
				result = test.handler(*test.args, **test.kwargs)

		return result

	def _check_warnings(self, result: Any, results: list, percent: int, test_name: str):
		"""
		Check warnings in test

		:param      result:     The result
		:type       result:     Any
		:param      results:    The results
		:type       results:    list
		:param      percent:    The percent
		:type       percent:    int
		:param      test_name:  The test name
		:type       test_name:  str
		"""
		if len(results) > 0 and results[-1] == result and result is not None:
			print_test_result(
				percent,
				test_name,
				status="warning",
				output=f'Last result is equals current result ({results[-1]} == {result})',
			)
			self.testcase.warnings += 1
			self.testcase.passed += 1

	def _processing_tests_execution(self, test_num: int, test_name: str, test: TestInfo):
		percent = int((test_num / self.tests_count) * 100)
		results = []

		try:
			if test.skip:
				raise SkippedTestException()

			result = self._run_test_cycle(test_name, test)

			self._check_warnings(result, results, percent, test_name)

			results.append(result)
		except SkippedTestException:
			self.testcase.skipped += 1
			print_test_result(
				percent,
				test_name,
				status="skip"
			)
		except AssertionError:
			print_test_result(
				percent,
				test_name,
				status="error",
				output=f"AssertionError\n{traceback.format_exc()}",
			)
			self.testcase.errors += 1
		except TestError:
			print_test_result(
				percent,
				test_name,
				status="error",
				output=str(traceback.format_exc()),
			)
			self.testcase.errors += 1
		else:
			self.testcase.passed += 1

			print_test_result(percent, test_name)

	def launch_test_chain(self):
		"""
		Launch test chain

		:raises     SkippedTestException:  skip test
		"""
		for test_num, (test_name, test) in enumerate(self.tests.items(), start=1):
			self._processing_tests_execution(test_num, test_name, test)

			if test.comment is not None:
				print_comment(f'Comment {test_name}: [reset]{test.comment}[/reset]\n')
