import logging
import os
import time

import selenium.webdriver

import globals
from code_block import CodeBlock

import browser as b

"""
All the functions which are bound to AWT commands 
"""


def goto(dst):
    b.driver.get(dst)


def text_input(selector, value, index=0):
    index = int(index)

    elem = b.get_element_selector(selector, index)
    elem.send_keys(value)


def click(selector, index=0):
    index = int(index)
    elem = b.get_element_selector(selector, index)
    elem.click()


def force_click(selector, index=0):
    elem = b.get_element_selector(selector, int(index))
    b.driver.execute_script("arguments[0].click();", elem)
    wait(1)


def wait_for(selector, timeout=10, check_interval=0.5):
    timeout = float(timeout)
    check_interval = float(check_interval)

    start = time.time()

    while True:
        try:
            b.get_element_selector(selector, raise_exception_on_failure=IndexError)
            break
        except IndexError:
            if time.time() - start >= timeout:
                b.raise_error(
                    "TimeoutException", "Maximum allowed time exceeded ({}s) while waiting for selector '{}'".format(
                        timeout, selector
                    )
                )
            time.sleep(check_interval)


def back():
    b.driver.back()


def forward():
    b.driver.forward()


def refresh():
    b.driver.refresh()


def log(text, level="info"):
    levels = {
        "debug": logging.debug,
        "info": logging.info,
        "warn": logging.warning,
        "error": logging.error,
        "fatal": logging.fatal
    }

    variables = {
        "line": globals.line_number,
        "file": globals.filename
    }

    for key, val in variables.items():
        text = text.replace("[{}]".format(key), str(val))

    levels[level.lower()](text)


def wait(delay):
    time.sleep(float(delay))


def screenshot(filename: str = "output.png"):
    if not filename.endswith(".png"):
        filename += ".png"

    b.driver.save_screenshot(filename)


def pause():
    os.system("pause")


def set_var(variable, selector, index=0, attribute="innerText"):
    elem = b.get_element_selector(selector, index)
    globals.memory_heap[variable] = elem.get_attribute(attribute)


def get_attr(selector, index=0, attribute="innerText"):
    elem = b.get_element_selector(selector, index)
    return elem.get_attribute(attribute)


def skip_to(point):
    globals.current_code_block.line_number = globals.current_code_block.points[point]


def set_file(selector, path, index=0):
    text_input(selector, os.path.abspath(path), index)


def set_variable(variable, value):
    if value.isdigit():
        value = int(value)
        
    elif value.replace('.','',1).isdigit():
        value = float(value)

    globals.memory_heap[variable] = value


def count(selector, variable=None):
    c = b.get_element_selector(selector, 0, get_mode=True)
    if variable is not None:
        globals.memory_heap[variable] = len(c)

    return len(c)


def test(selector, index=0):
    b.get_element_selector(selector, index)


def anti_test(selector, index=0):
    try:
        b.get_element_selector(selector, index, raise_exception_on_failure=IndexError)
        b.raise_error(
            "SelectorFoundException", "Found {}th occurrence of selector {}. Expected not to!".format(index, selector)
        )
    except IndexError:
        pass


def import_module(path, alias, literal_path=False):
    if alias is None:
        mod_prefix = ""
    else:
        mod_prefix = alias + "."

    if not literal_path:
        path = os.path.join(globals.cwd, path)

    with open(path) as f:
        code = []
        block_start = -1

        for i, line in enumerate(f.readlines()):
            if line.startswith("BLOCK"):
                block_start = i
                code = []
            code.append(line.rstrip("\n"))
            if line.startswith("ENDBLOCK"):
                args = code[0].split(" ")[1:]
                args[-1] = args[-1].rstrip("\n")
                globals.code_blocks[mod_prefix + args[0]] = CodeBlock(
                    os.path.abspath(path), mod_prefix + args[0], args[1:], code[1:], block_start + 1
                )


def get_raw_elements(selector, index=0):
    get_mode = False

    if index == "all":
        get_mode = True

    return b.get_element_selector(selector, index, get_mode=get_mode)


def get_element_parent(selector, index=0):
    return b.get_element_selector(selector, index).find_element_by_xpath('..')


def alert(action="accept"):
    a = b.driver.switch_to.alert
    if action.lower() == "accept":
        a.accept()
    else:
        a.dismiss()


def confirm(action="yes"):
    a = b.driver.switch_to.alert
    if action.lower() == "yes":
        a.accept()
    else:
        a.dismiss()


def prompt(text, action="yes"):
    a = b.driver.switch_to.alert
    a.send_keys(text)

    if action:
        a.accept()
    else:
        a.dismiss()


def clear(selector, index=0):
    b.get_element_selector(selector, index).clear()


def change(variable, delta):
    globals.memory_heap[variable] += float(delta)


def send_keys(selector, keys, index=0):
    b.get_element_selector(selector, index).send_keys(keys)


def date_input(selector, date, index=0):
    remove_chars = [" ", "-", "/", "\\"]
    for c in remove_chars:
        date = date.replace(c, "")

    selenium.webdriver.ActionChains(b.driver)\
        .move_to_element(b.get_element_selector(selector, index)).click()\
        .send_keys(date).perform()
    
    
def extract_html(filename, selector=None, index=0):
    filename = os.path.join(globals.cwd, filename)

    if selector is None:
        html = b.driver.page_source
    else:
        html = b.get_element_selector(selector, index).get_attribute("innerHTML")

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)

