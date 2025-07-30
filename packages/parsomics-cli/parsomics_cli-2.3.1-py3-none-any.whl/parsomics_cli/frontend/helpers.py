from rich import print


def print_exception(e: Exception):
    """
    Pretty-prints an exception with nice colors and formatting
    """
    print(f"[bold red]{e.__class__.__name__}[/bold red]: {e}")


def print_success(s: str):
    """
    Pretty-prints a success message
    """
    print(f"[bold green]{s} ✔ [/bold green]")


def print_info(s: str):
    """
    Pretty-prints an information message
    """
    print(f"[bold blue]{s} ⓘ [/bold blue]")


def print_warning(s: str):
    """
    Pretty-prints a warning message
    """
    print(f"[bold yellow]{s} ⚠ [/bold yellow]")


def print_failure(s: str):
    """
    Pretty-prints a failure message
    """
    print(f"[bold red]{s} ✘ [/bold red]")


def bool_to_yn(b: bool):
    """
    Pretty-prints a bool as "Yes" or "No"
    """
    return "[bold green]Yes[/bold green]" if b else "[bold red]No[/bold red]"


def bool_to_checkbox(b: bool):
    """
    Pretty-prints a bool as "Yes" or "No"
    """
    return "[bold green]☑[/bold green]" if b else "[bold red]☐[/bold red]"
