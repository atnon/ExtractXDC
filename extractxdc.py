import sys
import os
import re
import argparse

class SearchXDC:
    def __init__(self, InFile = None, OutFile = None):

        self.InFile = InFile

        if OutFile == None:
            self.OutFile = sys.stdout
        else:
            self.OutFile = OutFile

        self.HeaderString = (
            "# Generated with ExtractXDC, http://github.com/atnon/ExtractXDC\n"
            "# Source file: %s\n" % self.InFile.name
            )

    def readFile(self):
        with self.InFile as InFile:
            Data = InFile.read()
        return Data

    def searchFile(self, PatternList = None, CaseInsensitive = False, SortResults = True):
        if PatternList:
            CombinedPattern = "|".join(args.pattern)
            Expression = "(?:"+CombinedPattern+")"

            SearchPattern = r"(.*?\[get_ports (.*?"+Expression+".*?)\].*?)"
            SearchFlags = re.MULTILINE

            if CaseInsensitive:
                SearchFlags = SearchFlags | re.IGNORECASE

            Data = self.readFile()
            Matches = re.findall(SearchPattern, Data, flags=SearchFlags)

            if SortResults:
                self.Matches = sorted(Matches, key=lambda x: x[1])
            else:
                self.Matches = Matches

    def printMatches(self):
        print self.HeaderString
        for match in self.Matches:
            print match[0]

    def writeMatches(self, Verbose = False):
        if Verbose and (self.OutFile != sys.stdout):
            self.printMatches()
        if self.OutFile:
            with self.OutFile as OutFile:
                OutFile.write(self.HeaderString)
                for match in self.Matches:
                    OutFile.write(match[0]+"\n")
        else:
            print "No output written, no output file specified."

def parseArgs():
    parser = argparse.ArgumentParser(
        description="Extract ports from .xdc file given regular expression."
        )

    parser.add_argument(
        "infile", 
        type=argparse.FileType("r"), 
        help="Input file to read."
        )

    parser.add_argument(
        "pattern", 
        nargs="+", 
        help="Search patterns for port searching."
        )

    parser.add_argument(
        "-o", "--outfile", 
        type=argparse.FileType("w"), 
        help="Output file for writing."
        )

    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="If set, output will be printed to file as well as stdout."
        )

    parser.add_argument(
        "-i", "--ignorecase",
        action="store_true",
        help="If set, regular expression matching will ignore case when searching."
        )

    return parser.parse_args()


if __name__ == "__main__":
    args = parseArgs()
    XdcParser = SearchXDC(args.infile, args.outfile)
    XdcParser.searchFile(args.pattern)
    XdcParser.writeMatches(args.verbose)
    exit(0)

