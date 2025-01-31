class TestError(Exception):
	def __init__(self, *args):
		"""
		Constructs a new instance.

		:param		args:  The arguments
		:type		args:  list
		"""
		if args:
			self.message = args[0]
		else:
			self.message = None

	def get_explanation(self) -> str:
		"""
		Gets the explanation.

		:returns:	The explanation.
		:rtype:		str
		"""
		return f"Message: {self.message if self.message else 'missing'}"

	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"TestError has been raised. {self.get_explanation()}"


class TestValidationError(TestError):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"TestValidationError has been raised. {self.get_explanation()}"


class FixtureError(TestError):
	def __str__(self):
		"""
		Returns a string representation of the object.

		:returns:	String representation of the object.
		:rtype:		str
		"""
		return f"FixtureError has been raised. {self.get_explanation()}"
