# Archive Analysis Tool v2.1
# created by Sam Wallis-Riches, 2021

'''
IMPORTS
'''

import os
import warnings
import PyPDF2
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.colors as c
import time as t
import numpy as np
import logging

from PyPDF2 import PdfFileReader
from matplotlib import rc
from matplotlib.lines import Line2D



'''
DATA INDICES
    Subjects:

    index:           0   1  2  3   4    5    6    7    8    9    10     11
    order will be: code, a, t, p, a-%, t-%, p-%, a:t, p:a, p:t, sat, hex colour


    Overall:

    index            0    1    2  3  4  5   6    7    8    9   10   11   12     13       14       15
    order will be: date, time, A, T, P, S, A:T, A:S, T:S, P:A, P:T, P:S, SAT, aColour, tColour, pColour
'''



'''
INITIAL SET-UP
'''

warnings.filterwarnings("ignore")

logging.getLogger('matplotlib.font_manager').disabled = True

rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)

global splitter
splitter = "======================================================================="



'''
FILE CHECK
'''

def checkFiles(folderPath):

    # Lists for files that need to be fixed
    corruptFiles = []
    wrongNameFiles = []


    # Grabs any filenames that either can't be opened, or don't have valid filenames
    for filename in os.listdir(folderPath):
        if "[" in filename:

            # Corrupted file net
            try:
                if ".pdf" in filename:
                    pdf = PdfFileReader(open(folderPath + "/" + filename, "rb"))
            except PyPDF2.utils.PdfReadError:
                corruptFiles.append(filename)

            # Bad filename net
            if ("]" not in filename) or ("{" not in filename) or ("}" not in filename):
                wrongNameFiles.append(filename)


    # Returns respective filenames
    if len(corruptFiles) == 0 and len(wrongNameFiles) == 0:

        return True, corruptFiles, wrongNameFiles

    else:

        return False, corruptFiles, wrongNameFiles



'''
GETTING CONFIG DATA
'''

def getConfigInfo(folderPath):

    # Get all of the file's lines imported
    for filename in os.listdir(folderPath):
        if "config" in filename:
            with open(filename) as f:
                lines = f.readlines()


    # Remove pointless parts
    lines = lines[3:]


    # Getting toggles for deltas and figure height & width
    global deltasON
    if "True" in lines[-1]:
        deltasON = True
        lines = lines[:-1]
    else:
        deltasON = False
        lines = lines[:-1]

    height_line = lines[-1]
    width_line = lines[-2]

    height_line = height_line.split(": ")
    width_line = width_line.split(": ")

    height = int(height_line[1][:-1])
    width = int(width_line[1][:-1])


    # Removing any unneeded lines
    lines = lines[:-5]


    # Getting rid of newline characters and closing brackets
    for line in lines:
        lines[lines.index(line)] = line[:-2]


    # Splitting up the subject lines to get colours/names & codes separate
    for line in lines:
        lines[lines.index(line)] = line.split(": ")


    # Splitting to get the colours and names separate
    for line in lines:
        lines[lines.index(line)][1] = line[1].split(" (")


    # Moving everything into a nice array
    for line in lines:
        index = lines.index(line)
        lines[index] = [line[0], line[1][0], line[1][1]]


    coloursList = []
    subjectCodes = []
    codesList = []

    # Getting each of the codes, names and colours separate
    for elem in lines:

        coloursList.append([elem[0], elem[2]])
        subjectCodes.append(elem[0])
        codesList.append([elem[0], elem[1]])


    # Making colours & name code dictionaries
    coloursDict = dict(coloursList)
    codesDictionary = dict(codesList)

    return subjectCodes, codesDictionary, coloursDict, width, height



'''
GETTING OLD DATA
'''

def getOldData(folderPath, codesDictionary):

    if oldMetricsFile:

        # Getting in all the data
        with open(folderPath + "/metrics.txt") as f:
            data = f.readlines()


        # Getting rid of unnecessary lines
        data = data[5:-2]


        # Getting rid of newline characters
        for line in data:
            data[data.index(line)] = line[:-1]


        # Getting rid of blank lines
        while "" in data:
            data.remove("")


        oldOverallData = []

        # Getting & formatting each of the overall data points
        for line in data[:11]:

            datum = ""

            for elem in line:

                if elem == " " and datum != "":
                    break

                if elem.isdigit() or elem == ".":
                    datum += elem

            if "." in datum:
                datum = float(datum)

            else:
                datum = int(datum)

            oldOverallData.append(datum)


        # Removing overall data
        data = data[14:]


        # Getting and formatting old date & time data
        date_line = data[0]
        date_line = date_line.split(" ")

        oldDate = date_line[7].split("/")
        oldTime = date_line[9]

        oldOverallData = [oldDate] + [oldTime] + oldOverallData


        # Getting rid of date line
        data = data[2:]

        oldSubjectData = []

        subjectLines = []
        eachLine = []


        # Splitting up old data by subject
        for line in data:

            if line != splitter:
                eachLine.append(line)

            elif line == splitter:
                subjectLines.append(eachLine)
                eachLine = []

        subjectLinesData = []


        # Adding the relevant parts of the data to lists
        for subject in subjectLines:

            dataPieces = [subject[0]] + subject[3:6] + subject[7:-1]
            subjectLinesData.append(dataPieces)


        # Getting and formatting all subject old data
        for subject in subjectLinesData:

            subjectName = subject[0].split(":: ")[1][:-3]

            if subjectName in codesDictionary.values():

                subjectData = []
                key_list = list(codesDictionary.keys())
                val_list = list(codesDictionary.values())
                subjectCode = key_list[val_list.index(subjectName)]
                subjectData.append(subjectCode)

                for metric in subject[1:]:

                    if "[" in metric:
                        metric = metric.split(" [")[0]

                    metric = metric.split("= ")

                    datum = metric[1]

                    if "%" in datum:
                        datum = datum[:-2]

                    if "." in datum:
                        datum = float(datum)

                    else:
                        datum = int(datum)

                    subjectData.append(datum)

                oldSubjectData.append(subjectData)

    else:

        # Giving back blank lists if there was no old metrics file to read from
        oldSubjectData = []
        oldOverallData = []

    return oldSubjectData, oldOverallData



'''
ROMAN NUMERAL CONVERSION
'''

def int_to_Roman(num):

    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]

    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]

    roman_num = ''

    i = 0

    while  num > 0:

        for _ in range(num // val[i]):

            roman_num += syb[i]
            num -= val[i]

        i += 1

    return roman_num



'''
GETTING TOPICS
'''

def getTopics(folderPath, subjectCodes, A):

    # Setting up the filenames array
    filenames = [[] for x in range(len(subjectCodes))]


    # Getting in all filenames and splitting them up by subject
    for filename in os.listdir(folderPath):

        if "[" in filename:

            code = ""

            for e in filename:

                if e == "[":
                    continue

                elif e == "]":
                    break

                else:
                    code+=e

            filename = str(filename)
            index = subjectCodes.index(code)
            filenames[index].append(filename)


    # Setting up the topics array
    topics = [[subjectCodes[x], []] for x in range(len(subjectCodes))]


    # Getting each of the topics from the filenames
    for subject in filenames:

        for filename in subject:

            code = ""

            for e in filename:

                if e == "[":
                    continue

                elif e == "]":
                    break

                else:
                    code+=e

            index = subjectCodes.index(code)

            start = filename.index("{")
            end = filename.index("}")
            topic = filename[start + 1 : end]
            topics[index][1].append(topic)


    # Removing '+' signs
    for subject in topics:

        for topic in subject[1]:

            if "+" in topic:
                subject[1][subject[1].index(topic)] = subject[1][subject[1].index(topic)][:-2]


    nums = []

    # Generating the Roman numerals that may be in use
    for x in range(2, A):
        nums.append(" " + int_to_Roman(x))


    # Removing any numerals > 1
    for subject in topics:

        for topic in subject[1]:

            for num in nums:
                ending = topic[len(topic) - len(num):]

                if num in ending:
                    subject[1][subject[1].index(topic)] = ""

                    break

        while "" in subject[1]:
            subject[1].remove("")


    # Removing any 'I' numerals
    for subject in topics:

        for topic in subject[1]:
            ending = topic[len(topic) - len(" I"):]

            if " I" in ending:
                subject[1][subject[1].index(topic)] = subject[1][subject[1].index(topic)][:-2]


    # Adding in the number of articles per topic if > 1
    for subject in topics:

        for topic in subject[1]:
            count = 0

            for filename in os.listdir(folderPath):
                file_test = filename.split(topic)

                if len(file_test) != 1:
                    tmp = file_test[1].split(" ")

                    if (tmp[0] == "" or tmp[0] == "}") and (("{" + topic) in filename):
                        count += 1

            if count > 1:

                index_top = subject[1].index(topic)
                index_sub = topics.index(subject)
                topics[index_sub][1][index_top] += f" ({count})"


    # Sorting topics by amount in subject
    topics = sorted(topics, key=lambda x: len(x[1]), reverse=True)

    return topics, filenames



'''
GETTING NEW DATA
'''

def getNewData(subjectCodes, folderPath, coloursDict):

    # Setting up new data arrays
    newSubjectData = []
    newOverallData = []


    # Getting new date and time info
    newDate = str(dt.date.today())
    newDate = newDate.split("-")[::-1]
    now = dt.datetime.now()
    timeNow = now.strftime("%H:%M:%S")

    newOverallData.append(newDate)
    newOverallData.append(timeNow)


    # Setting up article amounts array
    artAmounts = [[subjectCodes[x], 0] for x in range(len(subjectCodes))]


    # Getting article amounts
    for filename in os.listdir(folderPath):

        if "[" in filename:
            code = ""

            for e in filename:

                if e == "[":
                    continue

                elif e == "]":
                    break

                else:
                    code+=e

            for elem in artAmounts:

                if code in elem:
                    artAmounts[artAmounts.index(elem)][1] += 1


    # Adding the article amounts to the new subject data array
    for subject in artAmounts:
        newSubjectData.append(subject)


    # Calculating total number of articles and appending to new overall data list
    newA = 0
    for subject in newSubjectData:
        newA += subject[1]

    newOverallData.append(newA)


    # Gets topics
    topics, filenames = getTopics(folderPath, subjectCodes, newA)


    # Setting up topic amounts array
    topAmounts = [[subjectCodes[x], 0] for x in range(len(subjectCodes))]


    # Getting topic amounts
    for subject in topics:
        count = 0

        for topic in subject[1]:
            count += 1

        for sub in topAmounts:

            if subject[0] in sub:
                index = topAmounts.index(sub)

        topAmounts[index][1] += count


    # Putting topic amounts in new subject data array
    for subject in topAmounts:

        for sub in newSubjectData:

            if subject[0] in sub:
                index = newSubjectData.index(sub)

        newSubjectData[index].append(subject[1])


    # Calculating total number of topics & adding to overall data array
    newT = 0
    for subject in newSubjectData:
        newT += subject[2]

    newOverallData.append(newT)


    # Setting up array for pages data
    for subject in newSubjectData:
        subject.append(0)


    # Getting page data
    for filename in os.listdir(folderPath):
        pages = 0
        code = ""

        if "[" not in filename:
            continue

        with open(folderPath + "/" + filename, "rb") as f:
            pdf = PdfFileReader(f)
            pages += pdf.getNumPages()

        for e in filename:

            if e == "[":
                continue

            elif e == "]":
                break

            else:
                code+=e

        for subject in newSubjectData:

            if code == subject[0]:
                index = newSubjectData.index(subject)

        newSubjectData[index][3] += pages


    # Calcuating overall number of pages & adding to overall data list
    newP = 0
    for subject in newSubjectData:
        newP += subject[3]

    newOverallData.append(newP)


    # Adding total number of subjects to overall data list
    newOverallData.append(len(newSubjectData))


    # Data indices
    '''
    DATA INDICES
        Subjects:

        index:           0   1  2  3   4    5    6    7    8    9    10     11
        order will be: code, a, t, p, a-%, t-%, p-%, a:t, p:a, p:t, sat, hex colour


        Overall:

        index            0    1    2  3  4  5   6    7    8    9   10   11   12     13       14       15
        order will be: date, time, A, T, P, S, A:T, A:S, T:S, P:A, P:T, P:S, SAT, aColour, tColour, pColour
    '''


    # Calculating percentage shares
    for subject in newSubjectData:

        a_share = round( ( subject[1] / newOverallData[2]) * 100 , 2 )
        t_share = round( ( subject[2]/ newOverallData[3]) * 100 , 2 )
        p_share = round( ( subject[3]/ newOverallData[4]) * 100 , 2 )
        newSubjectData[newSubjectData.index(subject)].extend([a_share, t_share, p_share])


    # Calculating subject ratios
    for subject in newSubjectData:

        subject.append( round( subject[1] / subject[2] , 2) ) # a:t
        subject.append( round( subject[3] / subject[1] , 2) ) # p:a
        subject.append( round( subject[3] / subject[2] , 2) ) # p:t


    # Calculating overall ratios
    newOverallData.append( round( newOverallData[2] / newOverallData[3] , 2) ) # A:T
    newOverallData.append( round( newOverallData[2] / newOverallData[5] , 2) ) # A:S
    newOverallData.append( round( newOverallData[3] / newOverallData[5] , 2) ) # T:S
    newOverallData.append( round( newOverallData[4] / newOverallData[2] , 2) ) # P:A
    newOverallData.append( round( newOverallData[4] / newOverallData[3] , 2) ) # P:T
    newOverallData.append( round( newOverallData[4] / newOverallData[5] , 2) ) # P:S


    # Calculating subject satisfaction
    overall_count = 0
    for subject in filenames:

        subject_count = 0
        file = subject[0]
        code = ""

        for e in file:

            if e == "[":
                continue

            elif e == "]":
                break

            else:
                code+=e

        for sub in newSubjectData:

            if code == sub[0]:
                index = newSubjectData.index(sub)

        for filename in subject:

            if "+" not in filename:
                subject_count += 1
                overall_count += 1

        sat = round( (subject_count / newSubjectData[index][1]) * 100, 1)
        newSubjectData[index].append(sat)


    # Calculating overall satisfaction
    sat = round( (overall_count / newOverallData[2]) * 100 , 1)

    newOverallData.append(sat)


    # Adding colour of each subject to new subject data array
    for subject in newSubjectData:

        colour = coloursDict[subject[0]]

        if "xkcd" in colour:
            colour = f"{c.to_hex(colour)}, {colour[5:].title()} (XKCD Colour Palette)"

        else:
            colour = f"{c.to_hex(colour)}, {colour.title()} (Matplotlib Colour Palette)"

        subject.append(colour)


    # Sorting new subject data array by subject code alphabetically
    newSubjectData = sorted(newSubjectData, key=lambda x: x[0])


    # Adding all integer values of the colours to a list
    colours = []
    for subject in newSubjectData:
        colours.append(int(c.to_hex(coloursDict[subject[0]])[1:], 16))


    # Calculating & formatting weighted average colour for articles
    count = 0
    for subject, colour in zip(newSubjectData, colours):
        count += ( round( subject[1]/newOverallData[2] * 100, 2 )) * colour

    averageArtColour = hex(round(count/100))[2:]

    while len(averageArtColour) < 6:
        averageArtColour = "0" + averageArtColour

    newOverallData.append("#" + averageArtColour)


    # Calculating & formatting weighted average colour for topics
    count = 0
    for subject, colour in zip(newSubjectData, colours):
        count += ( round( subject[2]/newOverallData[3] * 100, 2 )) * colour

    averageTopColour = hex(round(count/100))[2:]

    while len(averageTopColour) < 6:
        averageTopColour = "0" + averageTopColour

    newOverallData.append("#" + averageTopColour)


    # Calculating & formatting weighted average colour for pages
    count = 0
    for subject, colour in zip(newSubjectData, colours):
        count += ( round( subject[3]/newOverallData[4] * 100, 2 )) * colour

    averagePageColour = hex(round(count/100))[2:]

    while len(averagePageColour) < 6:
        averagePageColour = "0" + averagePageColour

    newOverallData.append("#" + averagePageColour)


    return newSubjectData, newOverallData, topics



'''
CALCULATING DELTAS
'''

def calculateDeltas(oldSubjectData, newSubjectData, oldOverallData, newOverallData, subjectCodes):

    if deltasON:

        # Setting up subject deltas list
        subjectDeltas = []

        for code in subjectCodes:

            old_index = None
            new_index = None


            # Finding indices of subjects in old data and new data
            for subject in oldSubjectData:

                if code in subject:
                    old_index = oldSubjectData.index(subject)

            for subject in newSubjectData:

                if code in subject:
                    new_index = newSubjectData.index(subject)


            # Conditionally calculating & appending deltas to list
            if old_index != None and new_index != None:

                currentDeltas = [code]

                for x in range(1, 11):

                    delta = round( newSubjectData[new_index][x] - oldSubjectData[old_index][x], 2)
                    currentDeltas.append(delta)

                subjectDeltas.append(currentDeltas)


            # Just adding 0s for formatting later if subject is new
            elif old_index == None:
                currentDeltas = [code]

                for x in range(1, 11):
                    currentDeltas.append(0)

                subjectDeltas.append(currentDeltas)


        # Setting up overall deltas list
        overallDeltas = []


        # Just adding 0s for formatting later if subject is new
        if oldMetricsFile == False:

            for x in range(2, 13):
                overallDeltas.append(0)


        # Calculating overall data deltas
        else:

            for x in range(2, 13):
                delta = round(newOverallData[x] - oldOverallData[x], 2)
                overallDeltas.append(delta)


    # Getting the deltas lists formatted emptily if deltas aren't wanted
    else:

        subjectDeltas = []

        for code in subjectCodes:
            currentDeltas = [code]

            for x in range(1, 11):
                currentDeltas.append("")

            subjectDeltas.append(currentDeltas)

        subjectDeltas = sorted(subjectDeltas, key=lambda x: x[0])

        overallDeltas = []

        for x in range(2, 13):
            overallDeltas.append("")

    return subjectDeltas, overallDeltas



'''
FORMATTING DELTAS
'''

def formatDeltas(subjectDeltas, overallDeltas):


    # Adding in square brackets, '+' signs, or making blank depending on value
    for delta in overallDeltas:

        if delta == 0 or delta == 0.0:
            overallDeltas[overallDeltas.index(delta)] = ""

        elif delta < 0:
            overallDeltas[overallDeltas.index(delta)] = f" [{delta}]"

        elif delta > 0:
            overallDeltas[overallDeltas.index(delta)] = f" [+{delta}]"


    # Adding in square brackets, '+' signs, or making blank depending on value
    for subject in subjectDeltas:

        for delta in subject:

            try:

                if delta == 0 or delta == 0.0:
                    subject[subject.index(delta)] = ""

                elif delta < 0:
                    subject[subject.index(delta)] = f" [{delta}]"

                elif delta > 0:
                    subject[subject.index(delta)] = f" [+{delta}]"

            except TypeError:
                continue


    # Sorting deltas so in same order as everything else
    subjectDeltas = sorted(subjectDeltas, key= lambda x: x[0])

    return subjectDeltas, overallDeltas



'''
DELETION OF OLD FILES
'''

def deleteOldFiles(folderPath):


    # If the old file exists, it is deleted
    for file in os.listdir(folderPath):

        if "contents" in file:
            os.remove(file)

        elif "visuals" in file:
            os.remove(file)

        elif "metrics" in file:
            os.remove(file)



'''
WRITING TO CONTENTS FILE
'''

def writeContentsFile(Topics, subjectColours, codesDictionary, folderPath):


    # Writing to the contents file
    with open(folderPath + "/contents.txt", "w+", encoding='utf-8') as f:


        # Opening remarks
        f.write("~ CONTENTS ~\n\n")

        f.write("==========================================================================================================================\n\n")


        # Writing each of the topics in turn, by subject
        for subject in Topics:

            subjectName = codesDictionary[subject[0]]
            colour = c.to_hex(subjectColours[subject[0]])
            f.write(f":: {subjectName} {colour} ::\n")

            for topic in subject[1]:

                f.write(f"- {topic}\n")

            f.write("\n")

            f.write("==========================================================================================================================\n\n")


        # Closing remarks
        f.write("\n")

        f.write("~ END ~")



'''
WRITING TO METRICS FILES
'''

def writeMetricsFile(newSubjectData, newOverallData, codesDictionary, subjectDeltas, overallDeltas, folderPath):

    # Data indices
    '''
    DATA INDICES
        Subjects:

        index:           0   1  2  3   4    5    6    7    8    9    10     11
        order will be: code, a, t, p, a-%, t-%, p-%, a:t, p:a, p:t, sat, hex colour


        Overall:

        index            0    1    2  3  4  5   6    7    8    9   10   11   12     13       14       15
        order will be: date, time, A, T, P, S, A:T, A:S, T:S, P:A, P:T, P:S, SAT, aColour, tColour, pColour
    '''


    # Writing to metrics file
    with open(folderPath + "/metrics.txt", "w+", encoding='utf-8') as f:


        # Opening remarks
        f.write("~ METRICS ~\n\n")

        f.write(splitter + "\n")


        # Extracting all of the overall data from the lists
        day = newOverallData[0][0]
        month = newOverallData[0][1]
        year = newOverallData[0][2]

        time = newOverallData[1]

        A = newOverallData[2]
        T = newOverallData[3]
        P = newOverallData[4]
        S = newOverallData[5]
        AT = newOverallData[6]
        AS = newOverallData[7]
        TS = newOverallData[8]
        PA = newOverallData[9]
        PT = newOverallData[10]
        PS = newOverallData[11]
        SAT = newOverallData[12]
        averageArtColour = newOverallData[13]
        averageTopColour = newOverallData[14]
        averagePageColour = newOverallData[15]


        # Writing overall data top panel
        f.write(f"""
    No. of:
        - articles                              = {A}{overallDeltas[0]}
        - topics                                = {T}{overallDeltas[1]}
        - pages                                 = {P}{overallDeltas[2]}
        - subjects                              = {S}{overallDeltas[3]}

    Articles per topic                          = {AT}{overallDeltas[4]}
    Articles per subject                        = {AS}{overallDeltas[5]}

    Topics per subject                          = {TS}{overallDeltas[6]}

    Pages per article                           = {PA}{overallDeltas[7]}
    Pages per topic                             = {PT}{overallDeltas[8]}
    Pages per subject                           = {PS}{overallDeltas[9]}

    Overall satisfaction of non-preprints       = {SAT} %{overallDeltas[10]}

    Average article colour                      = {averageArtColour}
    Average topic colour                        = {averageTopColour}
    Average page colour                         = {averagePageColour}


    Last updated on {day}/{month}/{year} at {time}


""")


        # Writing the splitter
        f.write(f"{splitter}\n\n")


        # Writing subject data
        for subject in newSubjectData:


            # Getting all of the data per subject
            subjectName = codesDictionary[subject[0]]
            a = subject[1]
            t = subject[2]
            p = subject[3]
            a_share = subject[4]
            t_share = subject[5]
            p_share = subject[6]
            at = subject[7]
            pa = subject[8]
            pt = subject[9]
            sat = subject[10]
            colour = subject[11]
            underline = "=" * (len(subjectName) + 6)

            index = newSubjectData.index(subject)


            # Writing each subject's details
            f.write(f"""
    :: {subjectName} ::
    {underline}

    No. of:
        - articles                              = {a}{subjectDeltas[index][1]}
        - topics                                = {t}{subjectDeltas[index][2]}
        - pages                                 = {p}{subjectDeltas[index][3]}

    Percentage share of:
        - articles                              = {a_share} %{subjectDeltas[index][4]}
        - topics                                = {t_share} %{subjectDeltas[index][5]}
        - pages                                 = {p_share} %{subjectDeltas[index][6]}

    Articles per topic                          = {at}{subjectDeltas[index][7]}
    Pages per article                           = {pa}{subjectDeltas[index][8]}
    Pages per topic                             = {pt}{subjectDeltas[index][9]}

    Satisfaction of non-preprints               = {sat} %{subjectDeltas[index][10]}

    Colour = {colour}


""")

            f.write(f"{splitter}\n\n")


        # CLosing remarks
        f.write("\n~ END ~")



'''
GETTING COLOURS
'''

def getColours(newSubjectData, subjectColours):

    aColours = []
    tColours = []
    pColours = []

    # Sorting subject data by article amount
    newSubjectData = sorted(newSubjectData, key = lambda x: x[1], reverse = True)


    # Getting colours in correct order
    for subject in newSubjectData:

        aColours.append(subjectColours[subject[0]])


    # Sorting subject data by topic amount
    newSubjectData = sorted(newSubjectData, key = lambda x: x[2], reverse = True)


    # Getting colours in correct order
    for subject in newSubjectData:

        tColours.append(subjectColours[subject[0]])


    # Sorting subject data by page amount
    newSubjectData = sorted(newSubjectData, key = lambda x: x[3], reverse = True)


    # Getting colours in correct order
    for subject in newSubjectData:

        pColours.append(subjectColours[subject[0]])

    return aColours, tColours, pColours



'''
PLOTTING GRAPHS
'''

def plotGraphs(newSubjectData, newOverallData, subjectColours, codesDictionary, width, height, folderPath):

    # Setting up data lists
    colours = []
    subjectNames = []
    aValues = []
    tValues = []
    pValues = []
    atValues = []
    paValues = []
    ptValues = []
    satValues = []

    '''
    DATA INDICES
        Subjects:

        index:           0   1  2  3   4    5    6    7    8    9    10     11
        order will be: code, a, t, p, a-%, t-%, p-%, a:t, p:a, p:t, sat, hex colour


        Overall:

        index            0    1    2  3  4  5   6    7    8    9   10   11   12     13       14       15
        order will be: date, time, A, T, P, S, A:T, A:S, T:S, P:A, P:T, P:S, SAT, aColour, tColour, pColour
    '''


    # Getting all of the subject data
    for subject in newSubjectData:

        colours.append(subjectColours[subject[0]])
        subjectNames.append(codesDictionary[subject[0]])
        aValues.append(subject[1]*10)
        tValues.append(subject[2]*10)
        pValues.append(subject[3])
        atValues.append(subject[7])
        paValues.append(subject[8])
        ptValues.append(subject[9])
        satValues.append(subject[10])


    # Formatting subject names
    for x in range(len(subjectNames)):

        if " " in subjectNames[x]:
            subjectNames[x] = subjectNames[x].replace(" ", "\n")


    # Getting vars for plotting graphs
    S = len(newSubjectData)

    x_vals = np.arange(S)


    # Configuring figure properties
    fig_size = plt.rcParams["figure.figsize"]
    fig_size[0] = width
    fig_size[1] = height
    plt.rcParams["figure.figsize"] = fig_size

    fig = plt.figure()

    fig.suptitle("Visual Representation of Metrics", fontsize = 32, weight="extra bold")


    # Plotting bar charts
    bars = fig.add_subplot(1,1,1)
    # bars.set_title("Visual Representation of Metrics", fontsize = 32, weight="extra bold")

    bars.bar(5*x_vals - 1.5, aValues, color=colours, width=1)
    bars.bar(5*x_vals, tValues, color=colours, width=1)
    bars.bar(5*x_vals + 1.5, pValues, color=colours, width=1)
    

    # Configuring bar charts
    bars.margins(x=0.01)

    bars.set_xticks(5*x_vals)
    bars.set_xticklabels(subjectNames, fontsize=12)

    bars.set_yticks([])
    bars.set_yticklabels([])

    bars.set_frame_on(False)
    
    xmin, xmax = bars.get_xaxis().get_view_interval()
    ymin, ymax = bars.get_yaxis().get_view_interval()
    bars.add_artist(Line2D((xmin, xmax), (ymin, ymin), color='black', linewidth=1))

    # Getting colours
    aColours, tColours, pColours = getColours(newSubjectData, subjectColours)


    # Sorting values for pie charts
    aValues = sorted(aValues, reverse=True)
    tValues = sorted(tValues, reverse=True)
    pValues = sorted(pValues, reverse=True)


    # Setting up values for explosions
    explosions = [0.1 for x in range(len(newSubjectData))]


    # Setting up parameters for pie charts
    averageList = [1]
    artColour = [newOverallData[13]]
    topColour = [newOverallData[14]]
    pageColour = [newOverallData[15]]


    # Plotting articles pie chart
    aPie = fig.add_subplot(4,9,1)

    aPie.pie(aValues, colors=aColours, counterclock=True, wedgeprops=dict(width=0.4), explode=explosions)
    aPie.set_xlabel("Articles", fontsize=15, weight="bold")
    aPie.pie(averageList, colors=artColour, radius=0.5)
    

    # Plotting topics pie chart
    tPie = fig.add_subplot(4,9,2)

    tPie.pie(tValues, colors=tColours, counterclock=True, wedgeprops=dict(width=0.4), explode=explosions)
    tPie.set_xlabel("Topics", fontsize=15, weight="bold")
    tPie.pie(averageList, colors=topColour, radius=0.5)


    # Plotting pages pie chart
    pPie = fig.add_subplot(4,9,3)

    pPie.pie(pValues, colors=pColours, counterclock=True, wedgeprops=dict(width=0.4), explode=explosions)
    pPie.set_xlabel("Pages", fontsize=15, weight="bold")
    pPie.pie(averageList, colors=pageColour, radius=0.5)

    
    # a:t ratio plot
    atPlot = fig.add_subplot(4,4,3)
    atPlot.plot(5*x_vals, atValues, color="b", marker="o", markersize=5, linewidth=2)

    atPlot.set_yticks([])
    atPlot.set_yticklabels([])

    atPlot.set_xlabel("Articles per Topic")
    atPlot.set_xticks([])
    atPlot.set_xticklabels([])

    y_vals = np.full(S, newOverallData[6])
    atPlot.plot(5*x_vals, y_vals, color="b", ls='--', linewidth=1)
    
    
    
    # p:a ratio plot
    paPlot = fig.add_subplot(4,4,4)
    paPlot.plot(5*x_vals, paValues, color="r", marker="o", markersize=5, linewidth=2)

    paPlot.set_yticks([])
    paPlot.set_yticklabels([])

    paPlot.set_xlabel("Pages per Article")
    paPlot.set_xticks([])
    paPlot.set_xticklabels([])

    y_vals = np.full(S, newOverallData[9])
    paPlot.plot(5*x_vals, y_vals, color="r", ls='--', linewidth=1)
    

    # p:t ratio plot
    ptPlot = fig.add_subplot(4,4,7)
    ptPlot.plot(5*x_vals, ptValues, color="y", marker="o", markersize=5, linewidth=2)

    ptPlot.set_yticks([])
    ptPlot.set_yticklabels([])

    ptPlot.set_xlabel("Pages per Topic")
    ptPlot.set_xticks([])
    ptPlot.set_xticklabels([])

    y_vals = np.full(S, newOverallData[10])
    ptPlot.plot(5*x_vals, y_vals, color="y", ls='--', linewidth=1)


    # sat plot
    satPlot = fig.add_subplot(4,4,8)
    satPlot.plot(5*x_vals, satValues, color="g", marker="o", markersize=5, linewidth=2)

    satPlot.set_yticks([])
    satPlot.set_yticklabels([])

    satPlot.set_xlabel("Satisfaction")
    satPlot.set_xticks([])
    satPlot.set_xticklabels([])

    y_vals = np.full(S, newOverallData[12])
    satPlot.plot(5*x_vals, y_vals, color="g", ls='--', linewidth=1)


    # Saving the figure
    plt.savefig(folderPath + "/visuals.pdf", bbox_inches="tight", dpi=3000)


# Getting the folder directories
in_dir = r"/Users/selwr/Documents/Almanac"
config_dir = os.path.dirname(os.path.realpath(__file__))
out_dir = os.path.dirname(os.path.realpath(__file__))



life = True



'''
MASTER RUNNING OF ArchiveAnalysisTool
'''

while life:

    # Starting up print
    print("Starting...\n")


    # File check
    life, filesToFixCorrupted, filesToFixName = checkFiles(in_dir)

    global oldMetricsFile
    oldMetricsFile = False

    for filename in os.listdir(config_dir):
        if "metrics" in filename:
            oldMetricsFile = True
        
    print("File check complete!\n")
            

    if life == True:

        # Getting config data
        codes, codesDict, colours, width, height = getConfigInfo(config_dir)

        print("Config data extracted!\n")


        # Getting old data
        old_subject_data, old_overall_data = getOldData(config_dir, codesDict)

        print("Old data extracted!\n")


        # Getting new data
        new_subject_data, new_overall_data, topics = getNewData(codes, in_dir, colours)

        print("New data obtained!\n")


        # Calculating deltas
        subject_deltas, overall_deltas = calculateDeltas(old_subject_data, new_subject_data, old_overall_data, new_overall_data, codes)


        # Formatting deltas, if needed
        if deltasON:
            
            print("Deltas calculated!\n")

            subject_deltas, overall_deltas = formatDeltas(subject_deltas, overall_deltas)

            print("Deltas formatted!\n")


        # Deleting old files
        deleteOldFiles(config_dir)

        print("Old files deleted!\n")


        # Writing to the contents file
        writeContentsFile(topics, colours, codesDict, out_dir)

        print("Contents file written!\n")


        # Writing to the metrics file
        writeMetricsFile(new_subject_data, new_overall_data, codesDict, subject_deltas, overall_deltas, out_dir)
    
        print("Metric file written!\n")


        # Plotting the graphs
        plotGraphs(new_subject_data, new_overall_data, colours, codesDict, width, height, out_dir)
        
        print("Graphs plotted!\n")


        # Ending print
        print("Done!")


        # Ending the program
        life = False

    else:

        # Printing any corrupted files' filenames
        if len(filesToFixCorrupted) != 0:
            print("The following files are corrupted and need to be fixed:\n")

            for name in filesToFixCorrupted:
                print(name + "\n")


        # Printing any filenames with invalid filenames
        if len(filesToFixName) != 0:
            print("The following filenames are invalid and need to be fixed:\n")

            for name in filesToFixName:
                print(name + "\n")


        # Wait a bit before code exits & closes
        t.sleep(30)


        # Exit from while loop
        break
