# The Lookout
A command line tool for managing Looker instances.

## Functions
### new
Add a new instance to your config file.

### conns
Check if connections exist in the instance and test them.

### users
Get list of users and last login date.

### usage
Get last 50 queries run.


## Usage
Usage:
  lookout new <host> [--sa | --eu | --au]
  lookout usage <host>
  lookout conns <host>
  lookout users <host>

  lookout --help
  lookout --version
 
Options:
  --help                         Show this screen.
  --version                      Show version.
  --sa                           Specify instance in South America (sa), Europe (eu), or Australia (au). North America (na) is default.
 
Examples:
  lookout new host_name --loc au
  lookout new host_name --loc eu
  lookout new host_name --loc sa
  lookout usage
  lookout conns
  lookout users


# Development

### Building CLI
pip install -e .[test]

### Credit
Forked from https://stormpath.com/blog/building-simple-cli-interfaces-in-python
