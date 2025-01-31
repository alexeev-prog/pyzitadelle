from pyzitadelle.test_case import TestCase, expect

firstcase = TestCase()


def add(a: int, b: int) -> int:
	return a + b


@firstcase.test()
def example_test():
	expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test2():
	expect(add(1, 2), 3, "1 + 2 should be equal to 3")


@firstcase.test()
def example_test3():
	expect(add(10, 2), 12, "10 + 2 should be equal to 12")


firstcase.run()
