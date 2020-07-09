import globals
import interpreter
import os

# initialize the memory heap with a binding to interpret a function
# add each command in the interpreter to the heap as well (with lowercase names)
# these items are added to allow Python blocks to access these functions as if they were built in
globals.memory_heap = {
    "interpret": interpreter.interpret_command,
    **{k.lower(): v for k, v in interpreter.INTERPRETER.items()},
    "filename": os.path.basename(globals.filename),
    "args": globals.args.args.split(",")
}


def execute_block(block_type, code):
    """
    Executes a language block -> enclosed in [start (language)] and [end (language)]
    :param block_type: the language to execute the code as
    :param code: the code to execute
    """
    BLOCKS[block_type.lower()](code)


def python_interpreter(code):
    """
    Interprets Python code with the global memory heap
    :param code: the code to execute
    """
    exec(code, globals.memory_heap)


# the bindings between the language execution function, and the name of the language
BLOCKS = {
    "python": python_interpreter
}
