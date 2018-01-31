# Python Regex Dictionary Search

This scripts extracts word entries from dictionary files and then allows regex searches to be performed on those entries. The results of the searches are both shown in the console and written to `lastmatches.txt`.

Empty input either exits the script (when in dictionary selection mode) or goes back to dictionary selection.

Dictionaries can be added by simply adding the corresponding names and extraction expressions to the dictionaries array. Encode the files in UTF-8 without BOM.