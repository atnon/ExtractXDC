# ExtractXDC
Tool to extract port specifications from a Xilinx Vivado XDC file using RegEx.

Ever had to traverse a large .xdc file to find and extract a large amount of port-related constraints and definitions? 
That's pretty much the purpose of this script. 

## Usage
Running the script from prompt with the help flag

    #> python extractxdc.py -h

yields:

    usage: extractxdc.py [-h] [-o OUTFILE] [-v] [-i] infile pattern [pattern ...]
  
    Extract ports from .xdc file given regular expression.
  
    positional arguments:
      infile                Input file to read.
      pattern               Search patterns for port searching.

    optional arguments:
      -h, --help            show this help message and exit
      -o OUTFILE, --outfile OUTFILE
                            Output file for writing.
      -v, --verbose         If set, output will be printed to file as well as
                            stdout.
      -i, --ignorecase      If set, regular expression matching will ignore case
                            when searching.

## Patterns
The script reads the file and applies the regex to it. In order to make entering the regex a bit easier, 
the user only enters part of the full regex.

The regex in full is:

    /(.*?\[get_ports (.*?<USER EXPRESSION>.*?)\].*?)/gm

Pretty fuzzy, but works most of the time. 

Several regexes can be entered in a sucession, like

    python extractxdc.py foo.xdc "PORT1\d+_[N,P]" "PORT2\d+"

and so on.

The user can enter any RegEx, but should avoid introducing extra capturing groups.

## License
The code is licensed under the MIT License, so do what you like with the code. Pull requests are welcome!

The license in full can be read in the [LICENSE.md](LICENSE.md) file.

