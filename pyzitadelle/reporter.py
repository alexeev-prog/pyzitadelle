import platform
import shutil
from datetime import datetime
from typing import Any, Optional

from rich import print


def print_header(label: str, plus_len: int = 0, style: str = 'bold'):
	width = shutil.get_terminal_size().columns - 2 + plus_len

	line = f" {label} ".center(width, "=")

	print(f"[{style}]{line}[/{style}]")


def print_platform(items: int):
	print(f"[white]platform: [reset]{platform.platform()}[/white]")
	print(f"[white]version: [reset]{platform.version()}[/white]")
	print(f"[white]release: [reset]{platform.release()}[/white]")
	print(f"[white]system: [reset]{platform.system()}[/white]")
	print(f"[white]python: [reset]{platform.python_version()}[/white]")
	print(f"[white bold]Collected {items} items[/white bold]\n")


def print_test_result(
	percent: str,
	label: str,
	status: Optional[str] = "success",
	output: Optional[Any] = None,
):
	date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
	width = shutil.get_terminal_size().columns - 8 - len(date)

	if status == "success":
		print(f"{date} [green]{label.ljust(width)} [{str(percent).rjust(3)}%][/green]")
	elif status == "error":
		print(f"\n{date} [red]{label.ljust(width)} [{str(percent).rjust(3)}%][/red]")
		print_header(f'ERROR: {label}', style='bold red')
		print(f"[red]{output}[/red]")
	elif status == "warning":
		print(f"{date} [yellow]{label.ljust(width)} [{str(percent).rjust(3)}%][/yellow]")
		print(f"[red] > {output}[/red]")
