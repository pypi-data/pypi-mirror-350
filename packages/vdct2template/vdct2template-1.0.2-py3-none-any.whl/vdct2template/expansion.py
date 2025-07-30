from pathlib import Path

from vdct2template.macros import Macros

from .regex import DROP, EXPAND


class Expansion:
    """
    A class to represent a VDB file that contains expands() blocks.

    Provides the necessary conversion to MSI include/substitute statements.
    """

    # class level list of all Expansion instances created
    expansions: list["Expansion"] = []
    # class level list of all vdb files processed so far
    processed: list[str] = []

    def __init__(self, filename: Path, folder: Path) -> None:
        """
        Constructor: set up properties
        """
        self.vdb_path = filename.resolve()
        self.folder = folder
        self.template_path = filename.with_suffix(".template")
        self.includes: list[Macros] = []
        self.text = filename.read_text()

        Expansion.expansions.append(self)

    def parse_expands(self) -> int:
        """
        Parse an expands() blocks in a VDB file.

        Updates the class attribute 'substitutions' with the macro substitutions parsed.
        Updates the class attribute text with the VDB file text with the expands()
        blocks processed into MSI substitute/include statements.

        returns the number of expands() blocks found.
        """

        expands = EXPAND.findall(self.text)
        if not expands:
            return 0

        for match in expands:
            # match: 0=include path, 1=name, 2=macro text
            include_path = self.folder / match[0]
            macros = Macros(self.template_path, include_path, match[2])
            self.includes.append(macros)
            self._normalise_macros(macros)

            # replace the expands() block with the MSI directives
            self.text = EXPAND.sub(macros.render_include(), self.text, 1)

        # remove other extraneous VDB things
        self.text = DROP.sub("", self.text)

        self.processed.append(self.vdb_path.name)

        return len(expands)

    def _normalise_macros(self, macros: Macros):
        """
        Given a set of macros for a given expand block, search for all other
        instances of an expand against the same template file.

        Make sure that this set of macros is consistent with all other instances
        by adding in a self referencing macro for any missing ones out of the list
        of all macros passed by all instances of such an expansion. (OMLGG!)
        """
        vdb_list = sorted(self.folder.glob("*.vdb"))
        for vdb in vdb_list:
            vdb_text = vdb.read_text()
            expands = EXPAND.findall(vdb_text)
            for match in expands:
                # match: 0=include path, 1=name, 2=macro text
                if match[0] == macros.vdb_path.name:
                    other_macros = Macros(self.template_path, macros.vdb_path, match[2])
                    for macro in other_macros.macros:
                        if macro not in macros.macros:
                            print(f"adding missing {macro} to {macros.parent.name}")
                            macros.macros[macro] = f"$({macro})"

    def process_includes(self):
        """
        Process the included files for this VDB file. Returns a generator of
        tuples of the file and the text to write to the file.
        """
        for include in self.includes:
            if include.vdb_path.name not in Expansion.processed:
                yield include.process()
                Expansion.processed.append(include.vdb_path.name)
            # else:
            #     cur_macros = Expansion.processed[include.vdb_path.name]
            #     if cur_macros != include.macros:
            #         print(f"WARNING: inconsistent macros for {include.vdb_path.name}")

    @classmethod
    def validate_includes(cls) -> bool:
        """
        Check that all included files are always using the same substitutions
        every time they are included. If not then the the replacing of macro
        names with _ prefix will be inconsistent between uses of the included
        templates and this approach will fail.

        NOTE: with the introduction of _normalise_macros() this should not be
        necessary but it is left in for now as a backup check.
        """
        warning = False
        index: dict[str, Macros] = {}

        print()
        for expansion in cls.expansions:
            for include in expansion.includes:
                if include.template_path.name in index:
                    original = index[include.template_path.name]
                    if include.compare(original):
                        warning = True
                        print(
                            f"  WARNING: inconsistent macros for "
                            f"{include.template_path.name}"
                        )
                        print(
                            f"  {include.parent.name} missing:"
                            f"{original.missing_str(include)}"
                        )
                        print(
                            f"  {original.parent.name} missing: "
                            f"{include.missing_str(original)}"
                        )
                else:
                    index[include.template_path.name] = include

        return warning
