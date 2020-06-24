import code_block
import time

start_time = time.time()

current_code_block = None       # type: code_block.CodeBlock
final_screenshot = False

current_delay = 0.125
maximum_delay = 10

stale_element_retries = 3

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
