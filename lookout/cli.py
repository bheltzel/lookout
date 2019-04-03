"""
lookout
 
Usage:
  lookout new <host> [--sa | --eu | --au]
  lookout usage <host>
  lookout conns <host>
  lookout users <host>

  lookout hello

  lookout --help
  lookout --version
 
Options:
  --help                         Show this screen.
  --version                      Show version.
  --sa                           Specify instance in South America (sa), Europe (eu), or Australia (au). North America (na) is default.
 
Examples:
  lookout hello
  lookout new host_name --loc au
  lookout new host_name --loc eu
  lookout new host_name --loc sa
 
Help:
  For help using this tool, please open an issue on the Github repository:
  https://github.com/bheltzel/lookout
"""
 
 
from inspect import getmembers, isclass
 
from docopt import docopt
 
from . import __version__ as VERSION
 

def main():
    """Main CLI entrypoint."""
    import lookout.commands
    options = docopt(__doc__, version=VERSION)

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items(): 
        if hasattr(lookout.commands, k) and v:
            module = getattr(lookout.commands, k)
            lookout.commands = getmembers(module, isclass)
            command = [command[1] for command in lookout.commands if command[0] != 'Base'][0]
            command = command(options)
            command.run()