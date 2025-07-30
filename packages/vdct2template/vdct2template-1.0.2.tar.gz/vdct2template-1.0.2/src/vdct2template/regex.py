import re

# all redundant VDB header/footer info lines start with #!
DROP = re.compile(r"#!.*\n")

# template blocks are also redundant
TEMPLATE = re.compile(r"^ *template *\( *\) * {[\S\s]*?}", re.M)

# this extracts the arguments from expand blocks
EXPAND = re.compile(r'^ *expand\("(.*)" *, *([^\)]*)\) *[\s\S]*?{([\s\S]*?)}', re.M)

# this extracts the macro entries from an expand block's 3rd argument
MACRO = re.compile(r'^ *macro *\(([^,]*), *"([^"]*) *', re.M)
