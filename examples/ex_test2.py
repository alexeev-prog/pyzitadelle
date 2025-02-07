from pyzitadelle.test_case import TestCase, expect, skip, expectfail
from pyzitadelle.standard import Argument

firstcase = TestCase()
debug = False


def add(a: int, b: int) -> int:
	return a + b


@firstcase.test(comment="async test example", count_of_launchs=2)
async def example_test1(a: int = 2):
	expect(add(1, a), a + 1, "1 + 2 should be equal to 3")
	return a + 1


@firstcase.test(comment="example with Argument", tags=["assert"], arguments=(Argument(args=[2]), Argument(args=[3])))
def example_test2(a: int):
	assert add(a, 2) == a + 2
	return a + 2


@skip
@firstcase.test()
def example_test3():
	expect(add(1, 2), 4, "1 + 2 should be equal to 3")
	return 4


@firstcase.test()
@skip(reason="not completed", when=debug)
def example_test4():
	expect(add(10, 2), 12, "10 + 2 should be equal to 12")
	return 12


@firstcase.test(comment="use each", tags=["assert"])
@expectfail("each dont work")
def example_test5(a: int = 2):
	assert add(1, a) == a + 2
	return a + 1


@firstcase.test(tags=["assert"])
def example_test6():
	assert add(20, 40) == 60
	return 60


firstcase.run()
