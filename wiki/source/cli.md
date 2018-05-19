# CLI usage

## Directives

### Info

* **tree** -- show commands tree.
* **describe [command_name]** -- show all info for command. Current command by default.
* **list** -- show all loaded commands.

### Tree manipulation

* **push [command_name]** -- add new command as child for current.
* **pop** -- delete command from tree.
* **goto [command_name]** -- move cursor to command.
* **reset** -- clear all tree.

## Command manipulation

* **rename** -- change name for current command.
* **args [list of args]** -- set arguments for current command.
* **sources** -- change data sources for current command.
* **flush** -- clear all command params to default: name, arguments, sources.

## Execution

* **run** -- run all commands.
* **pause** -- pause execution.
* **stop** -- stop execution.

