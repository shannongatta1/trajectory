"""
OTIS_MonteCarlo_ReadOP1 reads OP1 data files and returns the final line of the first data chunk (generally, this is the implicit integration resutls)

Version 1.0 - Bryan Munro - 7/25/2017

"""
import sys


def ReadOP1File():
    import sys
    import os
    import glob
    from pathlib import Path
    # Initialize variables
    # inputdir = sys.argv[1]
    # 'S:\\4-ENGINEERING\\18-Software\\OTIS_RunSummary\\Smaller sample'
    inputdir = "/Users/bummookoh/Projects/trajectory/example"
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

    print full_path

    for filePath in full_path:
        heading, first_para, second_para, isTwoPara = get_first_and_last_line(
            filePath)
        print heading
        print first_para[0]
        print first_para[1]

        print second_para[0]
        print second_para[1]


def get_first_and_last_line(file_path):
    start_first_paragraph = False
    start_second_paragraph = False
    first_para = {}
    second_para = {}
    with open(file_path, "rb") as f:
        first_line = f.readline()

        for line in f:
            if line.strip() == "" and not start_first_paragraph:
                start_first_paragraph = True
                continue
            elif line.strip() == "" and not start_second_paragraph:
                start_first_paragraph = False
                start_second_paragraph = True
                continue

            if len(first_para) < 1:
                first_para[0] = line
            elif start_first_paragraph:
                first_para[1] = line

            if len(second_para) < 1:
                second_para[0] = line
                
            elif start_second_paragraph:
                second_para[1] = line

    return (first_line,first_para,second_para,start_second_paragraph)


def convertToCsv(text):
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
