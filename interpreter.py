import shlex
import commands
import browser
import globals


def interpret_command(cmd):
    """
    Executes a single command
    :param cmd: the command to execute
    """

    # break up the command into spaces
    broken_cmd = shlex.split(cmd)

    if not broken_cmd:
        return

    # if the command is declaring a point, skip execution
    if broken_cmd[0] == "POINT":
        return

    # update global attributes (full command, command, and args)
    globals.full_command = cmd
    globals.command_name = broken_cmd[0]
    globals.command_args = broken_cmd[1:]

    # if the command is a code block, execute the block
    if broken_cmd[0] in globals.code_blocks:
        globals.code_blocks[broken_cmd[0]].execute(*broken_cmd[1:])
        return

    for name, block in globals.code_blocks.items():
        if block.alias is not None:
            if name.replace(block.alias + ".", "") == broken_cmd[0]:
                block.execute(*broken_cmd[1:])
                return

    # if the command is an internal command, execute the command
    if broken_cmd[0] in INTERPRETER:
        INTERPRETER[broken_cmd[0]](*broken_cmd[1:])
        return

    # if the command is neither a block or a command, raise the unknown command error
    browser.raise_error(
        "UnknownCommandException",
        "Unknown Command '{}'. Please Refer To The Manual For A List Of Commands!".format(cmd)
    )


def conditional(condition, *actions):
    """
    The function which is bound to the SWITCH command
    :param condition: the condition to evaluate
    :param actions: the command and arguments to execute if the statement evaluates to True.
    Optionally add a colon (:) followed by a command to execute if the condition evaluates to False
    """
    def format_command(full_cmd: tuple):
        cmd = full_cmd[0]
        args = full_cmd[1:]
        return cmd + " " + " ".join(['"{}"'.format(i) for i in args])

    # break the actions down into the True and False action (delimited by a colon)
    if ":" in actions:
        true = actions[:actions.index(":")]
        false = actions[actions.index(":") + 1:]
    else:
        true = actions
        false = None

    # execute the appropriate action. Use the global memory heap when evaluating to allow access to variables
    if eval(condition, globals.memory_heap):
        interpret_command(format_command(true))
    elif false is not None:
        interpret_command(format_command(false))


def do_nothing():
    """
    This is used for commands which are to have no action
    """
    pass


# The bindings between the command and the function
INTERPRETER = {
    "GOTO": commands.goto,
    "INPUT": commands.text_input,
    "CLICK": commands.click,
    "WAITFOR": commands.wait_for,
    "BACK": commands.back,
    "FORWARD": commands.forward,
    "REFRESH": commands.refresh,
    "LOG": commands.log,
    "WAIT": commands.wait,
    "SCREENSHOT": commands.screenshot,
    "HIGHLIGHT": browser.highlight_element,
    "PAUSE": commands.pause,
    "KILL": browser.kill,
    "ERROR": browser.raise_error,
    "SET": commands.set_var,
    "SKIPTO": commands.skip_to,
    "COUNT": commands.count,
    "SETFILE": commands.set_file,
    "SETVAR": commands.set_variable,
    "GETATTR": commands.get_attr,
    "TEST": commands.test,
    "IMPORT": commands.import_module,
    "ENDBLOCK": do_nothing,
    "GETELEM": commands.get_raw_elements,
    "GETELEMPARENT": commands.get_element_parent,
    "FORCECLICK": commands.force_click,
    "SWITCH": conditional,
    "ALERT": commands.alert,
    "CONFIRM": commands.confirm,
    "PROMPT": commands.prompt,
    "PASS": do_nothing,
    "CLEAR": commands.clear,
    "ANTITEST": commands.anti_test,
    "CHANGE": commands.change,
    "SENDKEYS": commands.send_keys,
    "SETDATE": commands.date_input,
    "EXTRACT": commands.extract_html,
    "SWITCHNEWWINDOW": commands.switch_to_newly_opened_window,
    "SWITCHFIRSTWINDOW": commands.switch_to_original_window
}
