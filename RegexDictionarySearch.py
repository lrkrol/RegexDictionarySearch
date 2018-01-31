#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Python Regex Dictionary Search 1.0.0
Copyright 2015 Laurens R Krol

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This scripts extracts word entries from dictionary files and then
allows regex searches to be performed on those entries. The results of
the searches are both shown in the console and written to lastmatches.txt.

Empty input either exits the script (when in dictionary selection mode)
or goes back to dictionary selection.

Dictionaries can be added by simply adding the corresponding names and
expressions to the dictionaries array, below.
Encode the files in UTF-8 without BOM.

The dictionaries labelled with (Unknown Origin) have been found around
the Web without attribution; others are either public domain, or have 
their copyright statements either retained in the file itself or in a 
separate file in the dictionaries directory.
"""

import io
import sys
import re
import os.path

# directory that contains the dictionary files
dictionariesDirectory = "./dictionaries/"

dictionaries = [

        # ["name as it appears in the menu",
        #  "dictionary file",
        #  "expression to extract entries from file",
        #  "additional code (string operation) to exectute for each entry)
        
        ["Free On-line Dictionary of Computing (2007)",
                "foldoc2007.txt",
                "\S+$",
                ""],
        ["French WinEdt dictionary (2010-05-07)",
                "fr.dic",
                ".+$",
                ""],
        ["German WinEdt dictionary (New spelling) (2005-01-06)",
                "de_neu.dic",
                "(?!%).+$",
                ""],
        ["Latin WinEdt dictionary (2005-11-15)",
                "latin.dic",
                ".+$",
                ""],
        ["List of names (Unknown Origin)",
                "names.txt",
                ".+$",
                ""],
        ["OpenTaal Dutch Word List (2.10G)",
                "opentaal-210g.txt",
                "\S.*",
                ""],
        ["Oxford English Dictionary (Unknown Origin)",
                "oxford.txt",
                "\S+.*  ",
                "entry = ''.join([i for i in entry if not i.isdigit()])"],
        ["SCOWL: Spell Checker Oriented Word Lists (2014-08-11)",
                "scowl20170824.txt",
                ".+$",
                ""],
        ["Webster's Unabridged Dictionary (1913)",
                "websters1913.txt",
                "[A-Z]+$",
                "entry = entry.lower()"],
        ["WordNet Database 3.1 (2011)",
                "wordnet31.txt",
                "\S+ ",
                "entry = entry.replace('_', ' ')"]
        ]


print "\nCase-insensitive regex search throughout dictionary entries"

while True:
    """ SELECTING DICTIONARY """
    print "\n   Dictionary to use:\n"
    for option in range(len(dictionaries)):
        print "    ", option + 1, dictionaries[option][0]

    while True:
        selection = raw_input("\n   > ").decode(sys.stdin.encoding)

        if selection == "": exit()

        try:
            selection = int(selection) - 1
            dictionary = dictionaries[selection][1]
            entriesExpression = dictionaries[selection][2]
            entriesCode = dictionaries[selection][3]
        except:
            print "\n     Invalid key"
            continue

        if not os.path.isfile(dictionariesDirectory + dictionary):
            print "\n     Dictionary file " + dictionariesDirectory + dictionary + " not found"
        else:
            print "\n   Using file", dictionary
            break


    """ EXTRACTING ENTRIES"""
    print "   Extracting entries matching %s" % entriesExpression

    dictset = set()     # starting with set to ignore duplicates
    expression = re.compile(entriesExpression)

    with io.open(dictionariesDirectory + dictionary, encoding="utf8") as file:
        lines = 0
        for line in file:
            lines += 1
            match = expression.match(line)
            if match:
                entry = match.group().rstrip()
                if entriesCode: exec entriesCode
                dictset.update({entry})

                # updating feedback every 3000 entries
                if len(dictset) % 3000 == 0:
                    sys.stdout.write("   Found %d unique entries in %d lines\r" % (len(dictset), lines))

    print "   Found %d unique entries in %d lines" % (len(dictset), lines)

    # converting to list to have it sorted
    sys.stdout.write("   Sorting alphabetically... ")
    dictlist = list(dictset)
    dictlist = sorted(dictlist, key = unicode.lower)
    del(dictset)
    sys.stdout.write("Done\n")


    """ PROCESSING SEARCHES """
    while True:
        searchExpression = raw_input("\nPattern: ").decode(sys.stdin.encoding)

        if searchExpression == "":
            # empty input goes back to dictionary selection
            break
        else:
            # compiling case-insensitive regex
            try:
                expression = re.compile(searchExpression, re.IGNORECASE|re.UNICODE)
            except Exception, e:
                print "\n   Compilation error:", e
                continue

            print ""

            matchlist = []
            for entry in dictlist:
                if expression.search(entry):
                    matchlist.append(entry)
                    print "  ", entry.encode(sys.stdout.encoding, errors="replace")

            # saving expression and results to lastmatches.txt, overwriting if already exists
            outputFile = io.open("lastmatches.txt", "w", encoding="utf8")
            outputFile.write("%d match%s for %s in %s\n" % (len(matchlist), ("" if len(matchlist) == 1 else "es"), searchExpression, dictionary))
            for match in matchlist:
                outputFile.write(match + "\n")
            outputFile.close()

            print "\nFound %d match%s for %s" % (len(matchlist), ("" if len(matchlist) == 1 else "es"), searchExpression)