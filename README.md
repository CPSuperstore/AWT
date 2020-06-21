# AWT
The AWT (Automated Web Test) Interpreter

## Getting Started
There are 2 Python packages which are required to run the interpreter `selenium`, and `argparse`.
 
 They can both be installed via pip with the following commands:
```bash
pip install selenium
pip install argparse
```

Once that is completed, you will need to download the web drivers of the browsers you plan on doing tests with.
The following table indicates where to get the driver for each browser

| Browser 	| Download URL 	| Save path 	|
|---------	|--------------	|-----------	|
| Chrome  	| https://chromedriver.chromium.org/downloads | `webDrivers/chromedriver.exe` |
| Edge    	| https://www.selenium.dev/downloads/ (Selenium Server Option) | `webDrivers/msedgedriver.exe`          	|

*Note*: Support for other browsers will be added in the future. 
Firefox is supported, but does not need a web driver on all machines.

## What is AWT?
AWT (Automated Web Test) is a Turing complete programming language which was written in Python.
The purpose is to write scripts to test browsers in a browser independent, and language independent way.
