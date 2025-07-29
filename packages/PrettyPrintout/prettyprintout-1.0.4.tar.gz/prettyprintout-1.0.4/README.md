# PrettyPrint - Yassify your console logs

This is the PrettyPrint package. It essentially wraps the ANSI escape sequences into an easy to use framework and provides some useful features for logging and status reporting in the console.<br>
This is my first ever package so be nice please

## Contents
- [Installation](#Installation)
- [Printing](#Printing)
  - [Tagged Prints](#Tagged-Prints)
- [Formatting](#Formatting)
  - [Options](#Options)
  - [PPFormat](#PPFormat)
  - [Presets](#Presets)
- [Logging](#Logging)
- [Reporting](#Reporting)
  - [ProgressBar](#ProgressBar)
  - [RunningIndicator](#RunningIndicator)
  - [Table](#Table)
- [Licence](#Licence)

## Installation
This project is available on pypi at: https://pypi.org/project/PrettyPrintout/

To install just run

    pip install prettyprintout

## Printing 
To use the ANSI printing features first import the package and create a Printer object.
Printer has two arguments:
- log_type: String, default None <br> Controls what type of log file will be created, see Logging
   
- timestamps: Bool, default False <br> False = no timestamps <br> True = Y-M-D-H:M:S timestamps each time printer gets called

To print something simply call the Printer object with your message as the argument
For employing different formats pass the fmt argument on call with your desired formatting configuration. See [Formatting](#Formatting) for more info.

    import PrettyPrint
    printer = PrettyPrint.Printer(log_type='txt', timestamps=True) # initialize printer object
    format = PrettyPrint.PPFormat() # initialize formatter object, more info on how to create a formatter in Formatting
    printer('hello world', fmt=format) # call printer to print

### Tagged Prints
Tagged prints allow you to print a statement(=Tag) in one format and then a message in a different format after, separated by a :.
To achieve this call the tagged_print function, which takes 4 arguments:
- tag: String, required = the tag to be printed
- msg: String, required = the message to follow the tag
- tag_fmt: PPFormat, required = the format for the tag
- msg_fmt: PPFormat, optional = the format for the message, if left empty will use the default setting


    import PrettyPrint
    printer = PrettyPrint.Printer(log_type='txt', timestamps=True) # initialize printer object
    format = PrettyPrint.Warning() # initialize formatter object, more info on how to create a formatter in Formatting
    printer.tagged_print('hello world', fmt=format) # call printer to print

There are tagged_print presets available:
- Warning: uses the Warning format preset for the tag (=WARNING)
- Success: uses the Success format preset for the tag (=SUCCESS)
- Fail: uses the Error format preset for the tag (=FAIL)
- Error: uses the Error format preset for the tag (=ERROR)

Each of these functions take one argument:
- msg: String, required = the message to be printed with the preset tag


    import PrettyPrint
    printer = PrettyPrint.Printer(log_type='txt', timestamps=True) # initialize printer object
    printer.success('PrettyPrint has been installed correctly') # call printer to print

## Formatting
Ansi escape sequences are basically tags that control the text that follows afterward.
A great ressource to learn more about them is this Stackoverflow post, which is the main piece of information this package is built on: https://stackoverflow.com/questions/4842424/list-of-ansi-color-escape-sequences

The main purpose of this package is to avoid having to build these sequences by hand. To do this you have three main options available:

- ColourText = The colour of the foreground text
- ColourBackground = The colour of the background
- Effect = Texteffects like bold, italic and underlined

### Options

- ColourText - controls the colour of the foreground text<br> Arguments:
  - colour: String or List
    - String: a valid colour from the list below
    - List: a list of RGB values as integers between 0 and 255
  - option: String
    - 'default': no change
    - 'bright': increases colour intensity


- ColourBackground - controls the colour of the background<br> Arguments:
  - colour: String or List
    - String: a valid colour from the list below
    - List: a list of RGB values as integers between 0 and 255
  - option: String
    - 'default': no change
    - 'bright': increases colour intensity
    

- Effect - controls the effects applied to the text <br> Arguments:
  - effect: String
    - a valid effect from the list below


- Colours: 
  - default
  - black
  - red
  - green
  - yellow
  - blue
  - magenta
  - cyan
  - white


- Effects:
  - reset: resets the format to default
  - bold: bold lettering
  - dim: decrease colour intensity
  - italic: italic lettering
  - underlined: underlines the text
  - inverted: switches background and text colour
  - strikethrough: letters appear as crossed out
  - double_underline: thick underlines
  - framed: encircles the text
  - encircled: same as above but with round corners
  
### PPFormat
Each of these options are objects that return an ANSI sequence on call, according to the specification on initialization.
You could technically use these objects by themselves and just get the sequence and append your message to it. In PrettyPrint however the PPFormat object is used to tie multiple options together and build a formatter to be passed to the Printer´s fmt argument.

PPFormat takes only one argument: options: list <br>
Options is a list of the formatting objects named above in no particular order.

    from PrettyPrint import *
    printer = Printer(log_type='txt', timestamps=True) # initialize printer object
    format = PPFormat([ColourText('black'), ColourBackground('white'), Effect('underlined')]) # initialize formatter object
    printer('hello world', fmt=format) # call printer to print

### Presets
PrettyPrint comes with a few format presets to speed up the usage.
- Error: Red, Bold and underlined text
- Success: Green, Bold and underlined text
- Warning: Yellow, Bold and underlined text

To use any of the presets simply instantiate a preset object, which will create a ready to use PPFormat object.

    import PrettyPrint
    preset = PrettyPrint.Warning()
    printer = PrettyPrint.Printer()
    printer('warning: something happened', preset)

## Logging
Logfiles will be created with the name YMD-H:M_PrettyPrint_Autolog in the script working directory.
Logfiles are created when Printer is initialized with a valid log_type argument.
Valid log_types are:
- None = No file created
- 'txt' = Textfile, no colour support
- 'html' = Html file, colour support is work in progress

## Reporting
This module features some useful status reporting tools for your loops.

### ProgressBar
The ProgressBar object is intended to run with for-loops. It wraps an interable object into a new iterable ProgressBar object, that will update a progress bar in the console print according to the specification.

In python each for loop is essentially a foreach loop, since range(n) is essentially just an array [0,1,...,n], hence the for i in range() syntax
ProgressBar works with any iterable like range, list or a numpy array.
Progress Bar takes 3 arguments:
- underlying_iterable: Iterable, required
  - the underlying object from the foreach loop like range(n) for example
- bins: Int, optional, default = 10
  - controls how many characters the full bar has and how big the update increment is. Has to be between 1 and 100.
  - 10 means that the bar consists of 10 characters at full length and will be updated in increments of 10% of work done
  - 20 means that the bar consists of 20 characters at full length and will be updated in increments of 5% of work done
  - ...
- symbol: String, optional, default = '='
  - controls what character is used to draw the progress bar

The ProgressBar printout also gives information about the average time a loop takes, how much time has passed and how much time is approximately left until completion. All the time is presented in seconds (time formatting to H:M:S is WIP, colour support is WIP)

    from PrettyPrint.figures import *
    import time
    for i in ProgressBar(range(1000), bins=10, symbol='='):
        time.sleep(0.1)

### RunningIndicator
The RunningIndicator object is designed to indicate whether your potentially infinite while loop is actually running or hung up somewhere, without spamming the console with a 'running' printout every loop (*cough cough*)

The printout features a little animation and information about avg time per loop and time elapsed. To use it simply instantiate a RunningIndicator object and call it on every iteration. The printout will be updated according to the arguments:
- mode: String, optional, default = 'dots'
  - controls the kind of animation to indicate the running loop: 'dots' or 'rotate'
- update_frq: Int, optional, default = 1
  - controls the update frequency of the output, in number of iterations. The output is updated every n

usage:

    from PrettyPrint.figures import *
    import time
    indicator = RunningIndicator(mode='dots', update_frq=100)
    while 1:
        indicator()
        time.sleep(0.1)

### Table
Table offers a simple way to print formatted pandas.DataFrame objects to the console or create a log of tabular data.
The object is designed to be instantiated before a loop and then add a row of data i.e. a series of data at the end of each iteration.
Logged data can be accessed at the end by simply accessing the underlying dataframe using Table.df

Arguments:
- data: pandas.DataFrame, optional, default = None
  - The underlying dataframe, used in case the loop is used to expand on existing data. The entire table will be printed upon instantiation
- columns: list, optional, default = None
  - In case no existing dataframe is used a new one will be instantiated in the table using this argument as columns. Ignored if something is passed for the data argument
- printer: pp.Printer, optional, default = None
  - The format printer to be used, if None a new one will be instantiated with default settings. It is recommended to use an existing printer if a log file is used and logging of the table is desired, otherwise the table cant be logged
- cell_num: String/None/list(String), optional, default = None
  - The string(s) used to parse numbers into the cells of the table, default will print with two decimal numbers. 
    - If String: a single formatter used for all cells
    - If None: default format for all cells
    - If list of Strings: must be same length as amount of cols, with the corresponding formatter for each column at the index location of the column
  - Note: Strings cant be parsed by this formatting, pass a '' empty string instead for cells containing strings
- col_width: Int/None/list(Int), optional, default = None
  - The width of each column in the printout
    - If Int: a single size used for all cells
    - If None: takes the length of the column name for the width
    - If list of Integers: must be same length as amount of cols, with the corresponding length for each column at the index location of the column
- cell_fmt: PPFormat/None/list(PPFormat), optional, default = None
  - The PPFormat used for the content of the cells in the printout
    - If PPFormat: a single format is used for all cells
    - If None: the default format is used for all cells
    - If List of PPFormat: must be same length as amount of cols, with the corresponding format for each column at the index location of the column
- frame_fmt: PPFormat/None, optional, default = None
  - The PPFormat used for the frame of the table
  - Note: It is recommended not to use Effects other than 'bold' here, Colour can be used in all ways

To add a new series i.e. row to the table call the add_row() function at the end of the loop and pass the new series of data as the argument
Functions
- add_row(series): adds a new row of data to the table and prints
  - series: list
    - the series of data to add

Usage:

    import pandas as pd
    import PrettyPrint as pp
    from PrettyPrint import figures
    
    df = pd.DataFrame({'Time': [1, 2], 'Place': [1, 2]})
    
    fmt = pp.PPFormat([pp.ColourText('green')])
    fmt1 = pp.PPFormat([pp.ColourText('red')])
    printer = pp.Printer()
    
    table = figures.Table(columns=df.columns, printer=printer, cell_num=[':.2f', ':.3f'], cell_fmt=fmt, frame_fmt=fmt1, col_width=10)
    
    table.add_row([3, 3])

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
