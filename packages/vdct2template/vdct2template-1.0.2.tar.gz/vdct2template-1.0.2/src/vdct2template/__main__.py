from pathlib import Path

import typer

from . import __version__
from .convert import convert

__all__ = ["main"]


cli = typer.Typer(rich_markup_mode="markdown")


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.command()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print the version and exit",
    ),
    folder: Path = typer.Argument(
        ...,
        help="folder of vdb files to convert to template files.",
        exists=True,
        file_okay=False,
        resolve_path=True,
    ),
    use_builder: bool = typer.Option(
        True,
        help="Use the builder.py file to look for direct references to template files.",
    ),
    builder: Path | None = typer.Option(
        None,
        help="Path to the builder file.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """
    ### VDCT to template conversion function.

    - This function assumes that all referenced VDCT files in the expand() blocks
    will be in the same folder.

    - We can use the builder.py file to check for direct references to template files
    Use --no-use-builder to disable this feature. Direct references to a template
    file is an error because we need to modify all macro names to add a _ prefix
    in templated files.

    - Files referenced in expand() blocks will have their macro names updated to
    all have a _ prefix, because MSI does not support substituting a macro with
    it's own name and passing a default. This is a workaround to that limitation.

    - The original expands() block is replaced with a series of substitute
    MSI directives and an include MSI directive.

    - The resulting set of templates can be expanded natively by MSI without the
    need for VDCT.

    - The DB files created by such an expansion should be equivalent to the
    original VDCT generated ones.
    """

    if use_builder:
        builder = builder or Path(folder.parent.parent / "etc" / "builder.py")
        builder_txt = builder.read_text()
    else:
        builder_txt = ""

    convert(folder, builder_txt)


# test with:
#  python -m vdct2template --version
if __name__ == "__main__":
    typer.run(main)
