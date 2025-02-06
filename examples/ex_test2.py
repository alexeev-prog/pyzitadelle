from pyzitadelle.test_case import TestCase, expect

firstcase = TestCase()


def add(a: int, b: int) -> int:
	return a + b


@firstcase.test(comment="async test example", count_of_launchs=2)
async def example_test1(a: int = 2):
	expect(add(1, a), a + 1, "1 + 2 should be equal to 3")
	return 3


@firstcase.test()
def example_test2():
	assert add(1, 2) == 3
	return 3


@firstcase.test(skip_test=True)
def example_test3():
	expect(add(1, 2), 4, "1 + 2 should be equal to 3")
	return 4


@firstcase.test()
def example_test4():
	expect(add(10, 2), 12, "10 + 2 should be equal to 12")
	return 12


@firstcase.test()
def example_test5():
	assert add(1, 2) == 4
	return 4


@firstcase.test()
def example_test6():
	assert add(20, 40) == 60
	return 60


firstcase.run()
