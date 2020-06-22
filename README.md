# AWT (Automated Web Test)
The AWT (Automated Web Test) Interpreter is an interpreted, Turing complete language for writing automated web tests 
on multiple browsers. The very clear and concise syntax allows complex test scripts to be written 
in a very small amount of code. The purpose is to write scripts to test browsers in a browser independent, and language independent way.


## Getting Started
There are 2 options for getting AWT up and running. You can execute from Python source code, 
or download the latest standalone executable. 
The following are instructions on how to get started using both methods.

### Python Source
*Assumptions*: This section assumes you have Python installed (3.5 or higher), and pip properly installed.
Installing these items is outside the scope of this guide. 
This guide also assumes you have Python added to your computer's PATH/Environment variables.


Step 1 is obviously to clone or download this repository to your local machine with the following command:
```bash 
git clone https://github.com/CPSuperstore/AWT.git
```

Next, we can handle the dependencies. There are 2 Python packages which are required to run the interpreter `selenium`, and `argparse`, which can both be installed via pip with the following commands:
```bash
pip install selenium
pip install argparse
```

Once the libraries have finished installing, skip ahead to the *Web Drivers* section.

### Standalone Executable
First, you will need to download the latest build. The list of builds can be found [here](https://github.com/CPSuperstore/AWT/releases).

Optionally, you may add the executable to your computer's PATH/Environment variables so it can be accessed anywhere.

Once this is done, skip ahead to the *Web Drivers* section.

### Web Drivers
Once that is completed, you will need to download the web drivers of the browsers you plan on doing tests with.
The following table indicates where to get the driver for each browser

| Browser 	| Download URL 	| Save path 	|
|---------	|--------------	|-----------	|
| Chrome  	| https://chromedriver.chromium.org/downloads | `webDrivers/chromedriver.exe` |
| Edge    	| https://www.selenium.dev/downloads/ (Selenium Server Option) | `webDrivers/msedgedriver.exe`          	|

*Note*: Support for other browsers will be added in the future. 
Firefox is supported, but does not need a web driver on all machines.

*Note*: If you do not plan on using a particular browser, you do not need to download the driver for it!

## Hello World Example
To test that everything has been properly installed, we will execute a `Hello World` project.

To do this, simply create a new file, and call it `helloWorld.awt`. Inside that folder, paste the following code:
```
GOTO http://google.ca
LOG "Hello World!"
PAUSE
```

*Note*: For a complete command reference, please visit the repository's [wiki](https://github.com/CPSuperstore/AWT/wiki)..

If you are running AWT from Python source code, simply issue the following command in your terminal window:
```bash
python C:\path\to\interpreter\executor.py path\to\script\HelloWorld.awt -b firefox
```
*Note*: You can replace `firefox` with whatever browser you prefer which has its driver installed. 
Remember that Firefox does not always need a driver to execute.

If you are running AWT from a standalone executable, simply issue the following command in your terminal window:
```bash
C:\path\to\interpreter\awt.exe path\to\script\HelloWorld.awt -b firefox
```

Or if you have added AWT to your PATH/Environment variables:
```bash
awt path\to\script\HelloWorld.awt -b firefox
```
*Note*: You can replace `firefox` with whatever browser you prefer which has its driver installed. 
Remember that Firefox does not always need a driver to execute.

If everything has been properly installed, you should now see the browser of your choosing open a small window 
with the Google homepage, and your command window should look something like this:
```
Hello World!
Press any key to continue . . .
```

## Command Line Arguments
As you can see, the first argument is the path to the AWT file you would like to execute. This is followed by the -b (or --browser) flag, and the browser you would like to use. Browser names are case insensitive. Here is the list of currently supported browsers:
 - Firefox
 - Chrome
 - Edge
 
Those are the mandatory arguments. Here is a list of optional arguments with a brief description:

| Short Flag 	| Long Flag | Description |
|---------	|--------------	|-----------	|
| -e | --headless | Run the browser in headless mode (no GUI window opens). Not recommended for developing the script (easier to see the screen as the script executes). Headless is not supported by Edge, and is very temperamental on Chrome |
| -i | --highlight | Highlight any element which is selected by the script with a 2px, solid red border. Helpful for debugging. |
| -p | --pause-mode | Pause the script when it completes or when an error is raised. This is useful for getting a look at the final state of the browser when not in headless mode. Helpful for debugging. |
| -h | --help | Displays the help text, and terminates the application |
| -s | --screenshot [filename] | Creates a screenshot called `filename` when the script is terminated (by completing execution or by an exception) |
| -l | --log-file [filename] | Outputs log information to a file called `filename`. If the file exists, the log information will be appended. Use `[year]`, `[month]`, `[day]`, `[hour]`, `[minute]`, `[second]` in the filename to include the date and time of execution start in the log name  |

## AWT Naming Conventions
AWT has a very strict style guide (WIP), which ensures all code written can be easily understood by anyone, 
but most importantly, to avoid naming collisions as much as possible. 
The following table shows which casing to use, and when.

| Location 	| Case Type | Example |
|---------	|--------------	|-----------	|
| AWT file name  	| Camel case | securityUtils.awt |
| Imported AWT file name  	| Upper case snake case | SECURITY_UTILS |
| Block name  	| Pascal case | CreateUser |
| Variable name  	| Camel case | someVar |
| Exception name  	| Pascal case | ElementNotFoundException |

## Command Reference
Please visit the repository's [wiki](https://github.com/CPSuperstore/AWT/wiki) for a complete command reference.

## Top 10 Frequently Used Command List
- [GOTO](https://github.com/CPSuperstore/AWT/wiki/GOTO)
- [INPUT](https://github.com/CPSuperstore/AWT/wiki/INPUT)
- [CLICK](https://github.com/CPSuperstore/AWT/wiki/CLICK)
- [HIGHLIGHT](https://github.com/CPSuperstore/AWT/wiki/HIGHLIGHT)
- [TEST](https://github.com/CPSuperstore/AWT/wiki/TEST)
- [KILL](https://github.com/CPSuperstore/AWT/wiki/KILL)
- [LOG](https://github.com/CPSuperstore/AWT/wiki/LOG)
- [BLOCK](https://github.com/CPSuperstore/AWT/wiki/BLOCK)
- [CLEAR](https://github.com/CPSuperstore/AWT/wiki/CLEAR)
- [CONFIRM](https://github.com/CPSuperstore/AWT/wiki/CONFIRM)

## Exit Codes
The AWT interpreter may exit with any of the following exit codes:

- 0 = Successful execution
- 1 = Unhandled Exception (Python)
- 2 = Unhandled AWT Exception 