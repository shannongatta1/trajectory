"""
OTIS_MonteCarlo_ReadOP1 reads OP1 data files and returns the final line of the first data chunk (generally, this is the implicit integration resutls)

Version 1.0 - Bryan Munro - 7/25/2017

"""
import sys
import datetime
import os
import glob
from pathlib import Path


def ReadOP1File():

    # Initialize variables
    # inputdir = sys.argv[1]
    # 'S:\\4-ENGINEERING\\18-Software\\OTIS_RunSummary\\Smaller sample'
    inputdir = sys.argv[1] #"/Users/bummookoh/Projects/trajectory/example"
    # inputdir = 'S:\\4-ENGINEERING\\18-Software\\OTIS_RunSummary\\foldertest'
    EmptyLineCounter = 0
    HeaderLine = False
    ImplicitLine = False
    ExplicitLine = False
    PreviousLine = False
    index = 0

    full_path = []
    dirList = glob.glob(inputdir + "/*/*.op1")
    for filePath in dirList:
        full_path.append(filePath)

    implicit_start = []
    implicit_end = []
    explicit_start = []
    explicit_end = []

    headings = ""

    for filePath in full_path:
        heading, first_para, second_para, isTwoPara = get_first_and_last_line(
            filePath)
        headings = heading
        file_name = filePath.replace(inputdir, "").split("/")[1]
        implicit_start.append(file_name + " " + first_para["first-line"])
        implicit_end.append(file_name + " " + first_para["last-line"])
        explicit_start.append(file_name + " " + second_para["first-line"])
        explicit_end.append(file_name + " " + second_para["last-line"])
    printCsv(implicit_start, implicit_end,
             explicit_start, explicit_end, headings)


def printCsv(implicit_start, implicit_end, explicit_start, explicit_end, headings):
    time = datetime.datetime.utcnow()
    with open(str(time) + '.csv', 'w') as f:
        writeLines(f, implicit_start, "implicit_start", headings)
        writeLines(f, implicit_end, "implicit_end", headings)
        writeLines(f, explicit_start, "explicit_start", headings)
        writeLines(f, explicit_end, "explicit_end", headings)


def writeLines(f, data_type, name, headings):
    f.write("\n")
    f.write(name + "\n")
    f.write(joinByComma("folder " + headings) + "\n")
    for line in data_type:
        f.write(joinByComma(line) + "\n")


def get_first_and_last_line(file_path):
    start_first_paragraph = False
    start_second_paragraph = False
    first_para = {}
    second_para = {}
    with open(file_path, "rb") as f:
        heading = f.readline()

        for line in f:
            if line.strip() == "" and not start_first_paragraph:
                start_first_paragraph = True
                continue
            elif line.strip() == "" and not start_second_paragraph:
                start_first_paragraph = False
                start_second_paragraph = True
                continue

            if start_first_paragraph and len(first_para) < 1:
                first_para["first-line"] = line
            elif start_first_paragraph:
                first_para["last-line"] = line

            if start_second_paragraph and len(second_para) < 1:
                second_para["first-line"] = line
            elif start_second_paragraph:
                second_para["last-line"] = line

    return (heading, first_para, second_para, start_second_paragraph)


def joinByComma(text):
    return ",".join(text.split())

    # Read the file line by line
    # with input as OP1File:

    #         #Loop through file
    #         for LineIndex, CurrentLine in enumerate(OP1File):

    #             #Grab the first line and store as the header line
    #             if LineIndex == 0:
    #                 HeaderLine = CurrentLine
    #                 #print "Header Line: " + CurrentLine

    #             #Check for empty lines and increment counter
    #             if not CurrentLine.strip():
    #                 EmptyLineCounter += 1
    #                 #print "Hit Empty Line" + CurrentLine

    #             #If this is the second empty line, then we have encountered the end of the implicit data block
    #             if (EmptyLineCounter == 2 and not ImplicitLine):
    #                 ImplicitLine = PreviousLine
    #                 #print "Hit Implicit Line: " + ImplicitLine

    #             #If this is the third empty line, then we have encountered the end of the explicit data block
    #             if (EmptyLineCounter == 3 and not ExplicitLine):
    #                 ExplicitLine = PreviousLine
    #                 #print "Hit Explicit Line: " + ExplicitLine

    #             #Set the previous line
    #             PreviousLine = CurrentLine

    #         #Otherwise, the end of the file is reached
    #         else:
    #             #print "Hit the end of the file: " + PreviousLine
    #             ExplicitLine = PreviousLine

    #     #If an explicit line but not an implicit line was found, duplicate
    #     if (not ImplicitLine) and (ExplicitLine):
    #         #print "Over writing implicit with explicit: " + ExplicitLine
    #         ImplicitLine = ExplicitLine

    #     with ExplicitLine as el:
    #     first = next(el).decode()

    #     fh.seek(-1024, 2)
    #     last = el.readlines()[-1].decode()

    #     with ImplicitLine as il:
    #     first = next(il).decode()

    #     fh.seek(-1024, 2)
    #     last = il.readlines()[-1].decode()

    #     #Split the return lines using spaces (the default) and return the associated lists
    #     HeaderList = HeaderLine.split()
    #     ImplicitList = ImplicitLine.split()
    #     ExplicitList = ExplicitLine.split()


    #     #Return the data
    #     return HeaderList, ImplicitList, ExplicitList;
ReadOP1File()
