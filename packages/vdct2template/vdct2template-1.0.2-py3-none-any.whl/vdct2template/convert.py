from pathlib import Path

from .expansion import Expansion
from .regex import DROP, TEMPLATE


def convert(folder: Path, builder_txt: str):
    """
    function to oversee conversion of a set of VDB files to template files.
    """
    warning = False
    targets = sorted(folder.glob("*.vdb"))

    print(f"converting vdb files in {folder}\n ...")

    for target in targets:
        expansion = Expansion(target, folder)
        if expansion.parse_expands() > 0:
            print(f"writing expansion {expansion.template_path.name}")
            expansion.template_path.write_text(expansion.text.strip() + "\n")

            for file, text in expansion.process_includes():
                print(f"writing template {file.name}")
                file.write_text(text.strip() + "\n")
                if file.name in builder_txt:
                    warning = True
                    print(f"  WARNING: direct reference from builder.py to {file.name}")

    # process the remaining (flat) vdbs
    all_vdb_files = {target.name for target in targets}
    unprocessed = all_vdb_files - set(Expansion.processed)

    for file in unprocessed:
        path = folder / file
        template_path = path.with_suffix(".template")

        text = path.read_text()
        # remove VDCT comments
        text = DROP.sub("", text)
        # remove any remaining empty template entries
        text = TEMPLATE.sub("", text)

        print(f"writing flat {file}")
        template_path.write_text(text.strip() + "\n")

    # give warnings if there are inconsistent macro substitutions
    # NOTE: process_includes() should have already fixed this!
    warning |= Expansion.validate_includes()

    if warning:
        print("\n  WARNINGS DETECTED: check above for details.")
        exit(1)
