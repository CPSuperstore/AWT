import code_block

current_code_block = None       # type: code_block.CodeBlock
final_screenshot = False

filename = None
line_number = 0
full_command = None
command_name = None
command_args = []
highlight_mode = False
step_mode = False
cwd = None
terminate_pause = False
action_chain = None

memory_heap = {}
point_line_names = {}
code_blocks = {}
