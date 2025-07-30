[![CI](https://github.com/epics-containers/vdct2template/actions/workflows/ci.yml/badge.svg)](https://github.com/epics-containers/vdct2template/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/epics-containers/vdct2template/branch/main/graph/badge.svg)](https://codecov.io/gh/epics-containers/vdct2template)
[![PyPI](https://img.shields.io/pypi/v/vdct2template.svg)](https://pypi.org/project/vdct2template)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)

# vdct2template

Converts EPICS vdct templates to pure msi compatible EPICS db templates

This tool is designed to modify an EPICS support module in order to remove
its dependency on the vdct tool. This is useful for support modules that we
want to build with the upstream vanilla EPICS base that does not include vdct.

Source          | <https://github.com/epics-containers/vdct2template>
:---:           | :---:
PyPI            | `pip install vdct2template`
Releases        | <https://github.com/epics-containers/vdct2template/releases>


## Installation

To install the latest release from PyPI, create a virtual environment and
pip install like this:

```bash
python -m venv venv
source venv/bin/activate

pip install vdct2template
```

## Usage

<pre>$ vdct2template --help
<b>                                                                                          </b>
<b> </b><font color="#A2734C"><b>Usage: </b></font><b>vdct2template [OPTIONS] FOLDER                                                    </b>
<b>                                                                                          </b>
                          <b>VDCT to template conversion function.</b>

 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">This function assumes that all referenced VDCT files in the expand() blocks will be   </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">in the same folder.                                                                   </font>
 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">We can use the builder.py file to check for direct references to template files Use   </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">--no-use-builder to disable this feature. Direct references to a template file is an  </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">error because we need to modify all macro names to add a _ prefix in templated files. </font>
 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">Files referenced in expand() blocks will have their macro names updated to all have a </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">_ prefix, because MSI does not support substituting a macro with it&apos;s own name and    </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">passing a default. This is a workaround to that limitation.                           </font>
 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">The original expands() block is replaced with a series of substitute MSI directives   </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">and an include MSI directive.                                                         </font>
 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">The resulting set of templates can be expanded natively by MSI without the need for   </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">VDCT.                                                                                 </font>
 <font color="#A2734C"><b> • </b></font><font color="#AAAAAA">The DB files created by such an expansion should be equivalent to the original VDCT   </font>
 <font color="#A2734C"><b>   </b></font><font color="#AAAAAA">generated ones.                                                                       </font>

<font color="#AAAAAA">╭─ Arguments ────────────────────────────────────────────────────────────────────────────╮</font>
<font color="#AAAAAA">│ </font><font color="#C01C28">*</font>    folder      <font color="#A2734C"><b>DIRECTORY</b></font>  folder of vdb files to convert to template files.          │
<font color="#AAAAAA">│                             [default: None]                                            │</font>
<font color="#AAAAAA">│                             </font><font color="#80121A">[required]                                                </font> │
<font color="#AAAAAA">╰────────────────────────────────────────────────────────────────────────────────────────╯</font>
<font color="#AAAAAA">╭─ Options ──────────────────────────────────────────────────────────────────────────────╮</font>
<font color="#AAAAAA">│ </font><font color="#2AA1B3"><b>--version</b></font>                                   <font color="#A2734C"><b>    </b></font>  Print the version and exit           │
<font color="#AAAAAA">│ </font><font color="#2AA1B3"><b>--use-builder</b></font>           <font color="#A347BA"><b>--no-use-builder</b></font>    <font color="#A2734C"><b>    </b></font>  Use the builder.py file to look for  │
<font color="#AAAAAA">│                                                   direct references to template files. │</font>
<font color="#AAAAAA">│                                                   [default: use-builder]               │</font>
<font color="#AAAAAA">│ </font><font color="#2AA1B3"><b>--builder</b></font>                                   <font color="#A2734C"><b>FILE</b></font>  Path to the builder file.            │
<font color="#AAAAAA">│                                                   [default: None]                      │</font>
<font color="#AAAAAA">│ </font><font color="#2AA1B3"><b>--help</b></font>                                      <font color="#A2734C"><b>    </b></font>  Show this message and exit.          │
<font color="#AAAAAA">╰────────────────────────────────────────────────────────────────────────────────────────╯</font>

</pre>
