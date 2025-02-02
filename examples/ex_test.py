import asyncio
from pyzitadelle.test_case import TestCase, expect, AIOTestCase

firstcase = TestCase()
aiocase = AIOTestCase()


def add(a: int, b: int) -> int:
	return a + b


@aiocase.test()
async def aioexample_test():
	expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test():
	expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test2():
	expect(add(1, 2), 4, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test3():
	expect(add(10, 2), 12, "10 + 2 should be equal to 12")


@firstcase.test()
def example_test4():
	assert add(1, 2) == 4


firstcase.run()
asyncio.run(aiocase.run())
