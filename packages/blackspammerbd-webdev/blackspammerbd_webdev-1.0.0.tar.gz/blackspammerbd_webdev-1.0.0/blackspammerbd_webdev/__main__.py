import sys
import click
from colorama import Fore, Style
from .core import main as cli_main

"""
Module entrypoint so that users can run:
    python -m blackspammerbd_webdev [OPTIONS] COMMAND [ARGS]...

Prints the branded ASCII logo and delegates to the Click CLI in core.py.
"""

def print_logo() -> None:
    """
    Print the bold, magenta "BSB" ASCII logo for immediate branding.
    """
    logo = f"""
{Fore.MAGENTA}{Style.BRIGHT}
┳┓┏┓┳┓
┣┫┗┓┣┫
┻┛┗┛┻┛{Style.RESET_ALL}

{Fore.MAGENTA}      B   S   B   WebDev Pentester   (v1.0.0){Style.RESET_ALL}
"""
    click.echo(logo)

@click.command("entrypoint", context_settings={"ignore_unknown_options": True})
@click.pass_context
def main(ctx: click.Context) -> None:
    """
    Entry point for `python -m blackspammerbd_webdev ...`
    Delegates to the 'sp' CLI defined in core.py after printing the logo.
    """
    print_logo()
    # Replace argv[0] so Click displays "sp" in usage text
    sys.argv[0] = "sp"
    ctx.forward(cli_main)

if __name__ == "__main__":
    main(prog_name="sp")
