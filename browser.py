from selenium import webdriver
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import os

import globals
import logging
import sys
import commands
import time

driver = None  # type:webdriver.Firefox

# define the Selenium browser configuration options
# each browser needs to be instantiated differently, so this dictionary allows this to happen
BROWSERS = {
    "firefox": {
        "class": webdriver.Firefox,
        "options": webdriver.firefox.options.Options,
    },
    "chrome": {
        "class": webdriver.Chrome,
        "options": webdriver.chrome.options.Options,
    },
    "edge": {
        "class": webdriver.Edge,
    },
    "ie": {
        "class": webdriver.Ie
    },
    "opera": {
        "class": webdriver.Opera
    }
}


def initialize_browser(browser: str, headless: bool = False):
    """
    Initializes the specified web browser with options
    :param browser: the name of the browser to use (case insensitive) (ie. Firefox, Chrome...)
    :param headless: if the browser should be run in headless mode. WARNING: Experamental
    """
    global driver
    browser_data = BROWSERS[browser.lower()]

    # create the specific browser options (if necessary)
    options = None
    if "options" in browser_data:
        options = browser_data["options"]()
        options.headless = headless

    # access the driver's path if specified
    driver_path = None
    if "driver" in browser_data:
        driver_path = browser_data["driver"]
        driver_path = os.path.join(os.path.dirname(__file__), driver_path)

    # instantiate the browser with necessary configurations
    os.environ['PATH'] += ";" + os.path.join(os.path.dirname(__file__), "webDrivers")
    if driver_path is None:
        driver = browser_data["class"]()
    elif options is None:
        driver = browser_data["class"](driver_path)
    else:
        driver = browser_data["class"](driver_path, options=options)

    # set the implicit wait time (maximum time to wait before giving up on finding elements)
    # and create the global action chain
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(10)
    globals.action_chain = ActionChains(driver)


def get_element_selector(selector: str, index=0, raise_exception_on_failure=False, get_mode=False):
    """
    Returns the element described by the parameters with the dynamic timeout
    :param selector: The CSS selector
    (use <selector>%<text> to search all elements that match "selector" with the inner text of "text")
    :param index: if multiple selectors exist, which selector to return (default=0)
    :param raise_exception_on_failure: the Python exception to raise if the element could not be found
    (default=False - raise AWT SelectorNotFoundException)
    :param get_mode: if all matching elements should be returned (ignore index param) (Default=False)
    :return: matching Selenium element(s)
    """
    start = time.time()
    while True:
        try:
            return locate_element(selector, index, RecursionError, get_mode)
        except RecursionError:
            if time.time() - start > globals.maximum_delay:
                if raise_exception_on_failure is False:
                    raise_error(
                        "SelectorNotFoundException",
                        "Could not find {}th occurrence of selector {}".format(index, selector)
                    )
                else:
                    raise raise_exception_on_failure
            time.sleep(globals.current_delay)
            globals.current_delay *= 2


def locate_element(selector: str, index=0, raise_exception_on_failure=False, get_mode=False):
    """
    Returns the element described by the parameters
    NOTE: call 'get_element_selector', not this funciton!
    :param selector: The CSS selector
    (use <selector>%<text> to search all elements that match "selector" with the inner text of "text")
    :param index: if multiple selectors exist, which selector to return (default=0)
    :param raise_exception_on_failure: the Python exception to raise if the element could not be found
    (default=False - raise AWT SelectorNotFoundException)
    :param get_mode: if all matching elements should be returned (ignore index param) (Default=False)
    :return: matching Selenium element(s)
    """
    index = int(index)

    inner_text_search = False
    text = None
    elements = []

    # check if the search involves a inner text search
    if "%" in selector:

        # if a text search is being executed, split into the CSS selector, and inner text
        s = selector.split("%")
        element, text = s[0], "%".join(s[1:])
        inner_text_search = True

        # raise an error if no selector has been specified
        if element == "":
            raise_error(
                "InvalidSelectorException", "A selector must precede the % (Search by tag text) selector ({})".format(
                    selector
                )
            )

    else:
        # if not in text search mode, copy the selector string by value
        element = selector[:]

    try:
        # get all elements with the specified CSS selector
        elements = driver.find_elements_by_css_selector(element)

    except selenium_exceptions.InvalidSelectorException:
        # wrapper Invalid Selector exception
        raise_error(
            "InvalidSelectorException", "The provided selector ({}) is invalid.".format(
                selector
            )
        )

    inner_text_index = 0
    if inner_text_search:
        # if an inner text search is done, filter out all of the tags which do not match the specified inner text
        # a second array is used as you can not modify the size of an array as you are iterating through it
        matches = []
        for e in elements:
            if e.text == text:
                if not get_mode:
                    if inner_text_index == index:
                        if globals.highlight_mode:
                            highlight_element(e)
                        return e
                    
                inner_text_index += 1
                matches.append(e)
        elements = matches

    if get_mode:
        # if get mode is enabled, highlight all matches (if running in highlight mode)
        if globals.highlight_mode:
            for e in elements:
                highlight_element(e)

        # and return all elements
        return elements

    else:
        try:
            # if we return a single item (get mode disabled), highlight the match (if running in highlight mode)
            if globals.highlight_mode:
                highlight_element(elements[index])

            # and return the match
            return elements[index]

        except IndexError:
            # if no matches exist, raise the proper error
            if raise_exception_on_failure is False:
                raise_error(
                    "SelectorNotFoundException", "Could not find {}th occurrence of selector {}".format(index, selector)
                )
            else:
                raise raise_exception_on_failure


""" 
SOME of the functions which are bound to commands are below this comment. See commands.py for the rest
"""


def highlight_element(selector, index=0, color="red", border=2):
    """
    Sets the element's border to a 2px solid red border
    :param selector: the item to highlight (either Selenium element, or string CSS selector)
    :param index: the index of the item to highlight
    :param color: the color of the border (Default=red)
    :param border: the line thickness of the border in px (Default=2)
    """

    # get the element if the selector is a CSS selector
    if type(selector) is str:
        selector = get_element_selector(selector, int(index))

    # apply the style to the element
    driver.execute_script(
        "arguments[0].setAttribute('style', arguments[1]);",
        selector,
        "border: {0}px solid {1};".format(border, color)
    )


def kill(status=0):
    """
    Kills execution of the script
    """
    if globals.final_screenshot is not False:
        commands.screenshot(globals.final_screenshot)

    # if pause mode is enabled, pause execution
    if globals.terminate_pause:
        commands.pause()

    # close the driver and quit the application
    driver.quit()

    commands.log("--------[ Finished in {}s with exit code {} ]--------".format(round(time.time() - globals.start_time, 2), status))

    sys.exit(status)


def raise_error(error_type, message):
    """
    Raises an error and terminates the application
    :param error_type: the error type. Must end with the text "Exception" (Not enforced, just best practice)
    :param message: the message to attach to the error
    """

    # log the error message as fatal (CRITICAL)
    logging.fatal("{} - {} @ File: '{}' - Block: '{}' - Line: {}".format(
        error_type, message, globals.current_code_block.filename, globals.current_code_block.block_name,
        globals.current_code_block.current_line
    ))

    # terminate and quit
    kill(2)
    quit()
