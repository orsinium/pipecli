# Command definition

## Attributes

### Definited

* **name** (str) -- default name for command.
* **implement** (str) -- that protocol this command implement.
* **required** (tuple) -- required protocols or names into command parents list. Command will get all messages from this commands.
* **optional** (tuple) -- like `required`, but optional.

### Generated

* **subcommands** (list) -- subcommands list for command into tree.
* **args** (dict) -- arguments for command.
* **sources** (tuple) -- names and protocols for getting messages. `required` + `optional` by default, can be redifined by user.

## Methods

* **entrypoint** -- entrypoint for command.
    * init subcommands entrypoints,
    * init current `proccess`,
    * propagate messages to subcommands,
    * send messages to `proccess`,
    * send messages from `proccess` to subcommands.
* **propagate** -- propagate message from some parent to some subcommand. By default propagate all messages to all subcommands. Can be redefined some commands for messages filtering.
* **proccess** -- main command logic.
* **finish** -- calls after proccess end and can return last message for subcommands. Do nothing by default. Can be redefined for reduce-type commands.
* **get_parser** -- return `argparse` parser for `update_args`.
* **update_args** -- update `args` dict from user input.
* **rename** -- change command name.
* **describe** -- return all info for command: description, allowed args, default values etc.
* **flush** -- return new clear command instance.

## Proccess structure

**IMPORTANT:** Output message MUST NOT BE `None`! This is indicate end of cicle.

Generate (no input -> many output):

```python
def process(self):
    yield  # get init params from root
    for i in range(n):
        new_message = do_something(i)
        yield new_message
```

Transform (one input -> one output):

```python
def process(self):
    while 1:
        source_command, message = yield
        new_message = do_something(message)
        yield new_message
```

Discover (one input -> many output):

```python
def process(self):
    while 1:
        source_command, message = yield
        for new_message in do_something(message):
            yield new_message
```

Reduce (many input -> one output):

```python
def process(self):
    self.result = 0
    while 1:
        source_command, message = yield
        self.result += message

def finish(self):
    return self.result
```

