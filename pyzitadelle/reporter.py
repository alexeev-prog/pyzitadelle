import platform
import shutil
from datetime import datetime
from typing import Any, Optional

from rich import box, print
from rich.console import Console
from rich.table import Table


def print_results_table(
	total: int, passed: int, warnings: int, errors: int, skipped: int
):
	table = Table(title="Tests Result", expand=True, box=box.ROUNDED)

	table.add_column("N", style="cyan")
	table.add_column("Tests encountered", style="cyan")
	table.add_column("Percent", style="cyan")

	passed_percent = int((passed / total) * 100)
	warnings_percent = int((warnings / total) * 100)
	errors_percent = int((errors / total) * 100)
	skipped_percent = int((skipped / total) * 100)

	table.add_row(str(total), "Total", "100%")
	table.add_row(
		str(passed), "Passed", f"{passed_percent}%", style="black bold on green"
	)
	table.add_row(
		str(warnings), "Warnings", f"{warnings_percent}%", style="black bold on yellow"
	)
	table.add_row(
		str(errors), "Errors", f"{errors_percent}%", style="black bold on red"
	)
	table.add_row(
		str(skipped), "Skipped", f"{skipped_percent}%", style="black bold on blue"
	)

	console = Console()
	console.print(table)


def print_header(label: str, plus_len: int = 0, style: str = "bold"):
	"""
	Prints a header.

	:param		label:	   The label
	:type		label:	   str
	:param		plus_len:  The plus length
	:type		plus_len:  int
	:param		style:	   The style
	:type		style:	   str
	"""
	width = shutil.get_terminal_size().columns - 2 + plus_len

	line = f" {label} ".center(width, "=")

	print(f"[{style}]{line}[/{style}]")


def print_platform(items: int):
	"""
	Prints a platform.

	:param		items:	The items
	:type		items:	int
	"""
	print(f"[white]platform: [reset]{platform.platform()}[/white]")
	print(f"[white]version: [reset]{platform.version()}[/white]")
	print(f"[white]release: [reset]{platform.release()}[/white]")
	print(f"[white]system: [reset]{platform.system()}[/white]")
	print(f"[white]python: [reset]{platform.python_version()}[/white]")
	print(f"[white bold]Collected {items} items[/white bold]\n")


def print_comment(comment: str):
	print(f"[dim]{comment}[/dim]")


def print_test_result(
	percent: str,
	label: str,
	status: Optional[str] = "success",
	output: Optional[Any] = None,
):
	"""
	Prints a test result.

	:param		percent:  The percent
	:type		percent:  str
	:param		label:	  The label
	:type		label:	  str
	:param		status:	  The status
	:type		status:	  str
	:param		output:	  The output
	:type		output:	  Any
	"""
	date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
	width = shutil.get_terminal_size().columns - 13 - len(date)

	if status == "success":
		print(
			f"[black bold on green]PASS[/black bold on green] {date} [green]{label.ljust(width)}[/green][dim white][{str(percent).rjust(3)}%][/dim white]"
		)
	elif status == "error":
		print(
			f"\n[black bold on red]ERR [/black bold on red] {date} [red]{label.ljust(width)}[/red][dim white][{str(percent).rjust(3)}%][/dim white]"
		)
		print_header(f"ERROR: {label}", style="bold red")
		print(f"[red]{output}[/red]")
	elif status == "warning":
		print(
			f"[black bold on yellow]WARN[/black bold on yellow] {date} [yellow]{label.ljust(width)}[/yellow][dim white][{str(percent).rjust(3)}%][/dim white]"
		)
		print(f"[yellow] > {output}[/yellow]\n")
	elif status == "skip":
		print(
			f"[black bold on blue]SKIP[/black bold on blue] {date} [blue]{label.ljust(width)}[/blue][dim white][{str(percent).rjust(3)}%][/dim white]"
		)
