from dataclasses import dataclass, field
from typing import Callable, Awaitable, Union


@dataclass
class TestInfo:
	"""
	This class describes a test information.
	"""

	handler: Union[Callable, Awaitable]
	skip: bool = False
	comment: Union[str, None] = None
	args: list = field(default_factory=list)
	kwargs: list = field(default_factory=dict)
	count_of_launchs: int = 1