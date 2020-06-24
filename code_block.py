import shlex
import re
import browser
import logging
import globals
import sys
import os
from selenium.common.exceptions import NoSuchWindowException, StaleElementReferenceException

# RegEx patterns to indicate the start and end of language blocks.
# For example, the Python language block looks like this:
#
# LANGBLOCK python
# some python code
# ENDLANGBLOCK python

BLOCK_START_PATTERN = re.compile(r"LANGBLOCK .*")
BLOCK_END_PATTERN = re.compile(r"ENDLANGBLOCK.*")

# RegEx patterns to indicate the start and end of code blocks.
# For example, a code block to click a button might look like this
#
# BLOCK ClickButton
# CLICK button
# ENDBLOCK

BLOCK_SECTION_START_PATTERN = re.compile(r"BLOCK .*")
BLOCK_SECTION_END_PATTERN = re.compile(r"ENDBLOCK.*")


def ignore_line(s) -> bool:
    """
    Determines if a line should be ignored by the interpreter
    :param s: the line to check
    :return: if the line should be ignored (True) or interpreted (False)
    """

    # ignore the line if it starts with the # character (a comment)
    if s.startswith("#"):
        return True

    # also ignore blank lines too
    if s in ["\n", "", " "]:
        return True
    return False


class CodeBlock:
    def __init__(self, filename, block_name, block_args, code, start_line):
        """
        This class represents and handles a runnable code block
        It has it's own variable scope which is copied from the global variable scope on each execution
        :param filename: the name of the file this block was read from
        :param block_name: the name of the block
        :param block_args: the argument structure for the block
        :param code: the code which is contained within the block
        :param start_line: The line where this block starts
        """
        self.filename = filename
        self.block_name = block_name
        self.start_line = start_line
        self.code = code
        self.points = {}            # the bindings between code points, and their line numbers
        self.line_number = 0        # current line number relative to the block.
                                    # Note that changing this during runtime will change the line of code
                                    # which will execute next

        if "." in self.block_name:
            self.alias, self.raw_block_name = self.block_name.split(".")
        else:
            self.alias = None
            self.raw_block_name = self.block_name

        # build mandatory (block_args) and optional (block_default_arg_values) argument structure
        self.block_args = []
        self.block_default_arg_values = {}
        for a in block_args:      # type: str
            if "=" in a:
                # if the argument contains an = sign, it is optional,
                # so add the arg name and default value to the block_default_arg_values
                # and add the argument name to the list of mandatory block_args to preserve order
                self.block_default_arg_values[a[:a.index("=")]] = a[a.index("=") + 1:]
                self.block_args.append(a[:a.index("=")])

            else:
                # if no default value is provided, add the argument name to the list of mandatory block_args
                self.block_args.append(a)

        # generate the point name to line number bindings
        self.generate_points()

    def __str__(self):
        return "ARGS:\n{}\n\nCODE:\n{}".format(self.block_args, self.code)

    def generate_points(self):
        """
        Generates the point name to line number bindings for use of the SKIPTO command
        """
        for line, s in enumerate(self.code):
            # if the line starts with the command "POINT", add the binding to the points dictionary
            if s.startswith("POINT"):
                b = shlex.split(s)
                self.points[b[1].rstrip("\n")] = line + 1

    @property
    def current_line(self):
        return self.line_number + self.start_line

    def execute(self, *block_args):
        """
        Executes this block
        :param block_args: the arguments supplied to the block's execution
        """

        # imported here to avoid a gigantic circular import
        # very annoying problem to solve, so to prevent you from pulling out your hair
        # PLEASE just keep these imports here
        import blocks
        import interpreter

        # reset local properties
        self.line_number = 0
        globals.current_code_block = self
        variables = globals.memory_heap

        # get the code block arguments for execution
        # iterate over the list of code block arguments
        for i, a in enumerate(self.block_args):
            try:
                # attempt to write the argument name and value binding to the memory heap
                variables[a] = block_args[i]

            except IndexError:
                # if the argument does not have a value, attempt to use the default value
                variables[a] = self.block_default_arg_values[a]

        # other variables to initialize
        block = False
        block_type = ""
        code = ""
        block_section = False

        while self.line_number < len(self.code):
            # get the current statement and increase the line number
            s = self.code[self.line_number]  # type: str
            s.lstrip(" ")
            s.lstrip("\t")
            self.line_number += 1

            # if the line should be ignored, skip it
            if ignore_line(s):
                continue

            # remove all training EOL characters
            s = s.rstrip("\n")

            # variables are in the format ${varname}
            # make necessary replacements to input the variable values
            for key, val in variables.items():
                s = s.replace("${" + str(key) + "}", str(val))

            # ----------{ Block Sections }----------

            # ignore all code in a block section
            if re.match(BLOCK_SECTION_START_PATTERN, s):
                block_section = True
                continue

            if re.match(BLOCK_SECTION_END_PATTERN, s):
                block_section = False
                continue

            if block_section:
                continue

            # ----------{ Language Blocks }----------

            # compile the code in a language block into a single string
            if re.match(BLOCK_START_PATTERN, s):
                block_type = s[10:]
                block = True
                continue

            # when the end of the block has been reached, execute it amd continue on to the next line
            if re.match(BLOCK_END_PATTERN, s) and block is True:
                block = False
                try:
                    blocks.execute_block(block_type, code)
                    globals.current_code_block = self
                    code = ""
                except SystemExit:
                    sys.exit()
                except:
                    logging.exception(
                        "The following error has occurred @ File: '{}' - Line: {}".format(
                            os.path.abspath(self.filename), self.current_line
                        )
                    )
                    browser.kill(2)
                    sys.exit(2)

                continue

            if block is True:
                code += s + "\n"
                continue

            # ----------{ Command Execution }----------

            # interpret the command and handle all errors which arise
            try:
                retry = 0
                while True:
                    try:
                        interpreter.interpret_command(s)
                        break
                    except StaleElementReferenceException as e:
                        retry += 0
                        if retry >= globals.stale_element_retries:
                            logging.fatal("Maximum retries exceeded {}".format(globals.stale_element_retries))
                            raise e
                globals.current_code_block = self

            except SystemExit:
                sys.exit()
            except NoSuchWindowException:
                logging.fatal("Execution terminated because browser window was externally closed")
                sys.exit(2)
            except:
                logging.exception(
                    "The following error has occurred @ File: '{}' - Line: {}".format(
                        os.path.abspath(self.filename), self.current_line
                    )
                )
                browser.kill(2)
                sys.exit(2)
