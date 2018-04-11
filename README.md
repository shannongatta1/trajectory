# **OTIS Trajectory Predictions** 
### These python scripts give a summary of OTIS projection data.

## OTIS_MonteCarlo_ReadOP1.py
This is the main file of the two to be run by command line. The script detects the individual paragraphs of data. If there are two paragraphs, the script identifies the first paragraph as Implicit and the second paragraph as Explicit. If there is only one paragraph  then the script will identify the data as Explicit. After that, each paragraph is parsed through to identify the first and last line, then output to a .csv file with it's filepath and Implicit/Explicit identifyer. This will run throught the course of multiple .op1 files.

## OTIS_MonteCarlo_ReadPhases.py
This is secondary file to be run with ReadOP1 script. The script detects the individual paragraphs of data. If there are two paragraphs, the script identifies the first paragraph as Implicit and the second paragraph as Explicit. If there is only one paragraph  then the script will identify the data as Explicit. The only data the script will output is the Explicit data. After that, each paragraph is parsed through to identify the different phases of the trajectory, depicted in the ANPHASE column. For each phase the script will find the first and last line, then output to a .csv file with it's filepath and Explicit identifyer. This will run throught the course of multiple .op1 files.

## Steps to execute:
In command line, navigate your current directory to the folder containing all the Run Folders that contain your .op1 files. Once there, type ` python [complete filepath to location of .py files] ` then press Enter. Your .csv files will pop up in the current working directory, showing up as [today's date]-OTIS_OP1_Phases.csv and [today's date]-OTIS_OP1_Readings.csv. Because the files will be overwritten with each script run, be sure to close the .csv files if you have them open, otherwise they cannot be overwritten and an IOError: [Errno 13] Permission denied: '20180410-OTIS_OP1_Phases.csv' will be thrown. Make sure you have both .py files in the same directory and all according libraries installed.
