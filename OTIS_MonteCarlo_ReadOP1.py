"""
OTIS_MonteCarlo_ReadOP1 reads OP1 data files and returns the first and final line of the first data chunk (generally, this is the implicit integration resutls) 
and the last data chunk (generally, this is the explicit integration resutls)
Version 1.0 - Shannon Gatta - 4/5/2018
"""
import sys
import datetime
import time
import os
import glob

from OTIS_MonteCarlo_ReadPhases import ReadPhase

ReadPhase()

def ReadOP1File():

    #if you want to go through folders in a particular filepath
    #Example: PS S:\4-ENGINEERING\18-Software\OTIS_RunSummary> python '.\OTIS_MonteCarlo_ReadOP1.py' 'S:/4-ENGINEERING/18-Software/OTIS_RunSummary/Smaller sample'
    #inputdir = sys.argv[1] 
    #if you want to run the file in the current working directory
    #Example: PS S:\4-ENGINEERING\18-Software\OTIS_RunSummary\Test01> python 'S:\4-ENGINEERING\18-Software\OTIS_RunSummary\OTIS_MonteCarlo_ReadOP1.py'
    inputdir = os.getcwd() 
    implicit_start = []
    implicit_end = []
    explicit_start = []
    explicit_end = []
    headings = ""
    full_path = []

    #grab the .op1 file out of the files withing the run folder and create the paths to that folder in a list
    dirList = glob.glob(inputdir + "/*/*.op1")
    for filePath in dirList:
        full_path.append(filePath)

    #extract and assign values from the dictionary
    for filePath in full_path:
        heading, first_para, second_para = get_first_and_last_line(
            filePath)
        if len(second_para) > 0:
            #modify each of the values to display according output on the .csv
            headings = heading
            file_name = filePath.replace(inputdir, "").split("\\")[1]
            implicit_start.append(file_name + " " + first_para["first-line"])
            implicit_end.append(file_name + " " + first_para["last-line"])
            explicit_start.append(file_name + " " + second_para["first-line"])
            explicit_end.append(file_name + " " + second_para["last-line"])
        elif len(first_para) > 0:
            headings = heading
            file_name = filePath.replace(inputdir, "").split("\\")[1]
            explicit_start.append(file_name + " " + first_para["first-line"])
            explicit_end.append(file_name + " " + first_para["last-line"])
    #call function and pass through the lists needing to be written to .csv
    printCsv(implicit_start, implicit_end,
             explicit_start, explicit_end, headings)


def printCsv(implicit_start, implicit_end, explicit_start, explicit_end, headings):
    #assign time to distinguish between .csv files 
    timestr = time.strftime("%Y%m%d-")
    if len(implicit_start) > 0:
    #write out each file 
        with open(str(timestr)+ "OTIS_OP1_Readings" + '.csv', 'w') as f:
            writeLines(f, implicit_start, "implicit_start", headings)
            writeLines(f, implicit_end, "implicit_end", headings)
            writeLines(f, explicit_start, "explicit_start", headings)
            writeLines(f, explicit_end, "explicit_end", headings)
    elif len(explicit_start) > 0:
        with open(str(timestr)+ "OTIS_OP1_Readings" + '.csv', 'w') as f:
            writeLines(f, explicit_start, "explicit_start", headings)
            writeLines(f, explicit_end, "explicit_end", headings)


def writeLines(f, data_type, name, headings):
    #creates the structure of the .csv file
    #calls function to comma delim data
    f.write("\n")
    f.write(name + "\n")
    f.write(joinByComma("filepath " + headings) + "\n")
    for line in data_type:
        f.write(joinByComma(line) + "\n")


def get_first_and_last_line(file_path):
    start_first_paragraph = False
    start_second_paragraph = False
    first_para = {}
    second_para = {}
    #open each .op1 file by filepath
    with open(file_path, "rb") as f:
        #first line is the headers
        heading = f.readline()

        #identify the first paragraph  through lack of string content
        #if the line is blank above the string, then this initiates the first_paragraph
        for line in f:
            if line.strip() == "" and not start_first_paragraph:
                start_first_paragraph = True
                continue
            #once it hits another blank line, we stop assigning start_first_paragraph and move the value to second_paragraph    
            elif line.strip() == "" and not start_second_paragraph:
                start_first_paragraph = False
                start_second_paragraph = True
                continue

            #modify dictionary
            #if a blank line appears(lack of character length), then first line is established
            #len(first_para) < 1 etablishes that the dictionary contains no keys. Because of this, this means this is the first line
            #of the paragraph

            if start_first_paragraph and len(first_para) < 1:
                first_para["first-line"] = line
            #else its the last line
            #this line updates every time it loops through until the loop ends
            #when the loop ends, the last line of the loop is the last one recorded, making it the last line
            elif start_first_paragraph:
                first_para["last-line"] = line

            #if a blank line appears(lack of character length), then first line is established
            if start_second_paragraph and len(second_para) < 1:
                #assigns the line (value) to a dictionary key as the loop runs
                second_para["first-line"] = line
            #else its the last line
            elif start_second_paragraph:
                second_para["last-line"] = line
    return (heading, first_para, second_para)

#make the data comma delimited
def joinByComma(text):
    return ",".join(text.split())

ReadOP1File()
