#!/usr/bin/env python

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

    def searchFile(self, SearchPattern = None, CaseInsensitive = False, SortResults = True):
        if SearchPattern:
            SearchFlags = re.MULTILINE

            if CaseInsensitive:
                SearchFlags = SearchFlags | re.IGNORECASE

            Data = self.readFile()
            Matches = re.findall(SearchPattern, Data, flags=SearchFlags)

            if SortResults:
                self.Matches = sorted(Matches, key=lambda x: x[1])
            else:
                self.Matches = Matches

    def searchPort(self, PatternList = None, CaseInsensitive = False, SortResults = True):
        CombinedPattern = "|".join(args.pattern)
        Expression = "(?:"+CombinedPattern+")"
        SearchPattern = r"(.*?\[get_ports .*?"+Expression+r".*?\].*?)"

        self.searchFile(SearchPattern, CaseInsensitive)

    def searchPin(self, PatternList = None, CaseInsensitive = False, SortResults = True):
        CombinedPattern = "|".join(args.pattern)
        Expression = "(?:"+CombinedPattern+")"
        SearchPattern = r"(.*?PACKAGE_PIN\s*?"+Expression+r"\s*?.*?\])"

        self.searchFile(SearchPattern, CaseInsensitive)

    def printMatches(self):
        print self.HeaderString
        for match in self.Matches:
            print match

    def writeMatches(self, Verbose = False):
        if Verbose and (self.OutFile != sys.stdout):
            self.printMatches()
        if self.OutFile:
            with self.OutFile as OutFile:
                OutFile.write(self.HeaderString)
                for match in self.Matches:
                    OutFile.write(match+"\n")
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

    parser.add_argument(
        "-p", "--pin",
        action="store_true",
        help="Search for package pin."
        )

    return parser.parse_args()


if __name__ == "__main__":
    args = parseArgs()
    XdcParser = SearchXDC(args.infile, args.outfile)
    if args.pin:
        XdcParser.searchPin(args.pattern, args.ignorecase)
    else:
        XdcParser.searchPort(args.pattern, args.ignorecase)
    XdcParser.writeMatches(args.verbose)
    exit(0)

