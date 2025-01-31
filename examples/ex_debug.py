from pyzitadelle.debug import debug_measurement


def fac(n):
	if n == 1:
		return 1
	return fac(n - 1) * n


@debug_measurement("ex_debug")
def test(num: int):
	for i in range(num**5):
		num = num**i

	return num


print(test(6))
