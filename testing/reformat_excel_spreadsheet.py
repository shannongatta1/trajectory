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



def ReadPhase():

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

        #if the file has two paragraphs
        if len(second_para) > 0:
            #modify each of the values to display according output on the .csv
            headings = heading
            file_name = filePath.replace(inputdir, "").split("\\")[1]

            #for each key in the second_para dictionary(which contains 12 keys[phases])
            for i in range(1, len(second_para)/2+1):
                #Kraken_FinStudy3_Config5_Run001 [first line of numbers]
                #key is set as a string to be able to append with "-2"
                explicit_start.append(file_name + " " + second_para[str(i)])
                explicit_end.append(file_name + " " + second_para[str(i) + "-2"])

            #if at some point the explicit files are needed
            # for i in range(1, len(first_para)/2+1):
            #     implicit_start.append(file_name + " " + first_para[str(i)])
            #     implicit_end.append(file_name + " " + first_para[str(i) + "-2"])

        #if the file has one paragraph
        elif len(first_para) > 0:
            headings = heading
            file_name = filePath.replace(inputdir, "").split("\\")[1]

            for i in range(1, len(first_para)/2+1):
                explicit_start.append(file_name + " " + first_para[str(i)])
                explicit_end.append(file_name + " " + first_para[str(i) + "-2"])
        #adding spaces between different files        
        explicit_start.append("")
        explicit_end.append("")
    #call function and pass through the lists needing to be written to .csv
    printCsv(implicit_start, implicit_end,
             explicit_start, explicit_end, headings)


def printCsv(implicit_start, implicit_end, explicit_start, explicit_end, headings):
    #assign time to distinguish between .csv files 
    timestr = time.strftime("%Y%m%d-")
    if len(implicit_start) > 0:
    #write out each file 
        with open(str(timestr)+ "OTIS_OP1_Phases_ByFile" + '.csv', 'w') as f:
            writeLines(f, implicit_start, "implicit_start", headings)
            writeLines(f, implicit_end, "implicit_end", headings)
            writeLines(f, explicit_start, "explicit_start", headings)
            writeLines(f, explicit_end, "explicit_end", headings)
        with open(str(timestr)+ "OTIS_OP1_Phases_ByPhase" + '.csv', 'w') as f:
            writePhase(f, explicit_start, "explicit_start", headings)
            writePhase(f, explicit_end, "explicit_end", headings)
    elif len(explicit_start) > 0:
        with open(str(timestr)+ "OTIS_OP1_Phases_ByFile" + '.csv', 'w') as f:
            writeLines(f, explicit_start, "explicit_start", headings)
            writeLines(f, explicit_end, "explicit_end", headings)
        with open(str(timestr)+ "OTIS_OP1_Phases_ByPhase" + '.csv', 'w') as f:
            writePhase(f, explicit_start, "explicit_start", headings)
            writePhase(f, explicit_end, "explicit_end", headings)

def writeLines(f, data_type, name, headings):
    #creates the structure of the .csv file
    #calls function to comma delim data
    f.write("\n")
    f.write(name + "\n")
    f.write(joinByComma("filepath " + headings) + "\n")
    for line in data_type:
        f.write(joinByComma(line) + "\n")

def writePhase(f, data_type, name, headings):
    #creates the structure of the .csv file
    #calls function to comma delim data
    count = 0
    f.write("\n")
    f.write(name + "\n")
    for line in range(len(data_type)):
        f.write(joinByComma("Phase_{}".format(line) + headings) + "\n")
        for data_number in data_type:
            data_test = data_number.split()
            print data_test
            phase_number = str(int(float(data_test[1])))
            print phase_number
            count += 1
            if phase_number == count:
                f.write(joinByComma(line) + "\n")
            else:
                print("working")



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
            data_points = line.split()
            if len(data_points) > 1:
                #using the ANPHASE number as the key
                #this does not take the number away from the line itself
                phase = str(int(float(data_points[0])))

            #if the current line is a blank line and we didn't start reading the first paragraph
            if line.strip() == "" and not start_first_paragraph:
                start_first_paragraph = True
                #contine allows you to return to the start of the loop instead of moving down to the following if statements
                continue
            #once it hits another blank line, we stop assigning start_first_paragraph and move the value to second_paragraph 
            #because if start paragraph already has lines in it switching start_first_paragraph to true, a NOT TRUE = FALSE
            # the elif statement for start_second_paragraph has start_first_paragraph as False, locating its second paragraph  
            elif line.strip() == "" and not start_second_paragraph:
                start_first_paragraph = False
                start_second_paragraph = True
                continue

            #modify dictionary
            #if a blank line appears(lack of character length), then first line is established
            if start_first_paragraph and len(first_para) < 1:

                first_para[phase] = line
            #else its the last line
            elif start_first_paragraph:
                #every time the loop runs phase-2 is updated with the new line that matches the phase number
                #once there are no more matching keys, the next key is created, leaving the last line of the phase to be logged in -2
                if phase in first_para:
                    first_para[phase + "-2"] = line
                else :
                    first_para[phase] = line


            #if a blank line appears(lack of character length), then first line is established
            if start_second_paragraph and len(second_para) < 1:
                #assigns the line (value) to a dictionary key as the loop runs
                second_para[phase] = line
            #else its the last line
            elif start_second_paragraph:
                if phase in second_para:
                    second_para[phase + "-2"] = line
                else :
                    second_para[phase] = line

    return (heading, first_para, second_para)

#make the data comma delimited
def joinByComma(text):
    return ",".join(text.split())

ReadPhase()