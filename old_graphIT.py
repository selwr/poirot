# Archysis v1.0
# created by Sam Wallis-Riches, 2019

import os
import warnings
warnings.filterwarnings("ignore", "(?s).*MATPLOTLIBDATA.*", category=UserWarning)
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import matplotlib.colors as c
import datetime as dt
import math as m



''' INITIAL SET-UP '''

# Setting fonts and fontsizes for plots
from matplotlib import rc
rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
rc('text', usetex=True)
plt.rcParams.update({'font.size': 15,
                     'font.weight' : 'bold'})


# Getting & formatting today's date and time
date_today = dt.date.today()

date_today = str(date_today)

date_today = date_today.split("-")

day = date_today[2]
month = date_today[1]
year = date_today[0][:-2]

now = dt.datetime.now()

current_time = now.strftime("%H:%M:%S")


# Getting the directory of the file
directory = os.path.dirname(os.path.realpath(__file__))



''' GETTING CONFIG INFO '''

with open("#config.txt", "r") as f:
    lines = f.readlines()


# Removing newline characters
for x in range(len(lines)):
    lines[x] = lines[x][:-1]


# Initialising customisable Booleans for contents file
deltasON = True
topPanelON = True
leaderboardON = True
headersON = True


# Extracting contents file toggles from config file
deltasBOOL = lines[-1]
topPanelBOOL = lines[-2]
leaderboardBOOL = lines[-3]
headersBOOL = lines[-4]


# Setting up contents file Booleans if different from defaults
if "False" in deltasBOOL:
    deltasON = False

if "False" in topPanelBOOL:
    topPanelON = False
    leaderboardON = False

if "False" in leaderboardBOOL:
    leaderboardON = False

if "False" in headersBOOL:
    headersON = False

if (leaderboardON == False) and (topPanelON == False) and (headersON == False):
    deltasON = False


# Initialising customisable Booleans for graph
metricsON = True
ratiosON = True
pieChartON = True
numbersON = True
percentagesON = True


# Extracting graph toggles from config file
metricsBOOL = lines[-6]
ratiosBOOL = lines[-7]
pieChartBOOL = lines[-8]
numbersBOOL = lines[-9]
percentagesBOOL = lines[-10]


# Setting up graph Booleans if different from defaults
if "False" in metricsBOOL:
    metricsON = False

if "False" in ratiosBOOL:
    ratiosON = False

if "False" in pieChartBOOL:
    pieChartON = False

if "False" in numbersBOOL:
    numbersON = False

if "False" in percentagesBOOL:
    percentagesON = False


# Extracting other config info for numerals, and width & height of graph
num_text = lines[-15]
width_text = lines[-13]
height_text = lines[-12]


# Removing non-subject config info from extracted list
lines = lines[:-16]


# Preparing numerals lists so they can be used
num_text = num_text.split(" ")
num_text = num_text[2:]

nums = []

for num in num_text:
    if "," not in num:
        nums.append(" " + num)
    else:
        nums.append(" " + num[:-1])


# Getting width of graph
width_text = width_text.split(": ")
width = int(width_text[1])


# Getting height of graph
height_text = height_text.split(": ")
height = int(height_text[1])



''' GETTING CATEGORY CODES AND AMOUNTS '''

# Getting all codes into a list
code = ""
cats = []

for file in os.listdir(directory):
    if "[" in file:
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                code+=e
        tmp = [code, 0]
        if (tmp not in cats) and (tmp[0] != ""):
            cats.append(tmp)
        code = ""


# Getting amounts per category
for file in os.listdir(directory):
    for x in range(len(cats)):
        if (f"[{cats[x][0]}]") in file:
            cats[x][1] += 1


# Getting number of categories
n = 0
for elem in cats:
    n += elem[1]


# Sorting categories by amount of articles
cats = sorted(cats, key = lambda x: x[1], reverse = True)


# Separating categories and amounts into respective lists
categories = []
amounts = []

for x in range(len(cats)):
    categories.append(cats[x][0])
    amounts.append(cats[x][1])

codes_list2 = categories


# Determining overall satisfaction
total = 0
non = 0

for file in os.listdir(directory):
    if "[" in  file:
        total += 1
        if "+" not in file:
            non += 1

sat_overall = round((non/total) * 100, 2)



''' USING CONFIG INFO '''

# Extracting codes' subjects and subsquent colours from config list
codes = []

for elem in lines:
    codes.append(elem.split(": "))

codes_subjects = []
codes_colours = []

for elem in codes:
    problem = elem[1]
    problem = problem.split(" (")
    problem[1] = problem[1][:-1]
    tmp4 = []
    tmp4.append(elem[0])
    tmp4.append(problem[0])
    codes_subjects.append(tmp4)
    tmp4 = []
    tmp4.append(elem[0])
    tmp4.append(problem[1])
    codes_colours.append(tmp4)
    tmp4 = []


# Making the lists dictionaries to use filename codes as keys
subject_codes_tops = codes_subjects
codes_subjects = dict(codes_subjects)
codes_colours = dict(codes_colours)


# Using dictionaries to extract full subject names and colours
colours = []
for x in range(len(cats)):
    tmp = categories[x]
    categories[x] = codes_subjects[tmp]
    colours.append(codes_colours[tmp])



''' GETTING TOPICS '''

# Getting all filename codes
codes_list = []
for elem in subject_codes_tops:
    codes_list.append(elem[0])


# Setting up filenames list
filenames = []
for x in range(len(codes_list)):
    filenames.append([])


# Getting all filenames
for file in os.listdir(directory):
    if "[" in file:
        t = ""
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                t+=e
        filename = str(file)
        index = codes_list.index(t)
        filenames[index].append(file)


# Setting up topics list
topics = []
for x in range(len(codes_list)):
    topics.append([])


# Extracting topics from filenames
for part in filenames:
    for elem in part:
        tmp = ""
        topic = ""
        for x in elem:
            if x == "{":
                tmp = x
                continue
            elif x == "}":
                break
            elif tmp == "{":
                topic += x
        topics[filenames.index(part)].append(topic)


# Removing special symbols from topics
for part in topics:
    for elem in part:
        if "+" in  elem:
            part[part.index(elem)] = part[part.index(elem)][:-2]
    for elem in part:
        if "@" in  elem:
            part[part.index(elem)] = part[part.index(elem)][:-2]


# Removing numerals from topics
for part in topics:
    for elem in part:
        for num in nums:
            ending = elem[len(elem) - len(num):]
            if num in ending:
                part[part.index(elem)] = ""
                break
    while "" in part:
        part.remove("")


# Removing final numeral
for part in topics:
    for elem in part:
        ending = elem[len(elem) - len(" I"):]
        if " I" in ending:
            part[part.index(elem)] = part[part.index(elem)][:-2]


# Putting topics in the correct order, correlated with the order of number
# of articles per topic, as opposed to number of topics
# From lines 345 - 417, I cannot make head nor tails of. DO NOT TOUCH.
topics_actual = []
for x in range(len(topics)):
    topics_actual.append([])

used_codes = []
for file in os.listdir(directory):
    code=""
    sub=""
    topic=""
    if "[" in file:
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                code+=e
        if codes not in used_codes:
            for e in file:
                if e == "{":
                    continue
                elif e == "}":
                    break
                else:
                    topic+=e

            topic = topic[len(code)+3:]

            sub = codes_subjects[code]
            index_sub = codes_list2.index(sub)
            for subject in topics:
                for y in subject:
                    if y in topic:
                        index2 = topics.index(subject)
                        topics_actual[index_sub] = topics[index2]
            used_codes.append(code)

topics_numbers = []

for file in os.listdir(directory):
    topic = ""
    code = ""
    if "[" in file:
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                code+=e
        for e in file:
            if e == "{":
                continue
            elif e == "}":
                break
            else:
                topic+=e

        topic = topic[len(code)+3:]

        if "+" in topic or "@" in topic:
            topic = topic[:-2]

        for num in nums:
            ending = topic[len(topic) - len(num):]
            if (ending == num):
                topic = topic[:len(topic) - len(num)]
                break
            if ending == " I":
                topic = topic[:len(topic) - 2]
                break

        topics_numbers.append(topic)


# Adding in counts for topics with more than one article
for sub in topics_actual:
    for top in sub:
        count = topics_numbers.count(top)
        if count > 1:
            index_top = sub.index(top)
            index_sub = topics_actual.index(sub)
            topics_actual[index_sub][index_top] += f" ({count})"



''' CHECKING OLD CONTENTS FILE '''

# Determining if an old contents file exists
found_contents = False
for file in os.listdir(directory):
    if "contents" in file:
        filename = file
        found_contents = True


# Extracting necessary parts (old t value) in order to open file
split_n = filename.split("(")
split_n = split_n[1]
split_n = split_n.split(")")
split_n = split_n[0]
split_n = split_n.split(" = ")
split_n = int(split_n[1])


# Opening and extracting old contents file data
lines = None
for file in os.listdir(directory):
    if "contents" in file:
        with open(f"contents (t = {split_n}).txt") as f:
            lines = f.readlines()


# Determining some Booleans
if found_contents == True:

    # Determining if there were subject headers in old contents file
    old_headersBOOL = False

    for elem in lines:
        if "|" in elem:
            old_headersBOOL = True
            break


    # Determining if there was a top panel in old contents file
    old_topPanelBOOL = False

    if ":" not in lines[0]:
        old_topPanelBOOL = True


    # Determining if there was a leaderboard in old contents file
    old_leaderboardBOOL = False

    for elem in lines:
        if "1. " in elem:
            old_leaderboardBOOL = True



''' EXTRACTING OLD DATA '''

# Extracting old satisfaction level
if old_topPanelBOOL == True:
    old_sat = lines[6]
    old_sat = old_sat[15:20]


# Extracting subject header lines
if old_headersBOOL == True:
    headers = []
    for line in lines:
        if ":" in line:
            headers.append(line)


    # Removing ratio and time line if there was a top panel
    if old_topPanelBOOL == True:
        headers = headers[2:]


    # Removing endings of subject header lines
    for elem in headers:
        tmp = elem[3:-4]
        headers[headers.index(elem)] = tmp


    # Splitting subject header lines in twain, the subject and the data
    for elem in headers:
        tmp = elem.split(" #")
        headers[headers.index(elem)] = tmp


    # Formatting data into just subject and data, no HEX value
    for elem in headers:
        tmp = [elem[0], elem[1][7:]]
        headers[headers.index(elem)] = tmp


    # Removing end brackets of data
    for elem in headers:
        tmp = [elem[0], elem[1][2:-2]]
        headers[headers.index(elem)] = tmp


    # Splitting up the data by property
    for elem in headers:
        tmp = [elem[0], elem[1].split(" | ")]
        headers[headers.index(elem)] = tmp


    # Getting the data out of the 'split' list
    for elem in headers:
        for prop in elem[1]:
            headers[headers.index(elem)].append(prop)
        elem.remove(elem[1])


    # Splitting up each property into its parts
    for elem in headers:
        for prop in elem:
            if " " in prop:
                tmp = prop.split(" ")
                headers[headers.index(elem)][elem.index(prop)] = tmp


    # Getting out just the data into the list
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    for elem in headers:
        for prop in elem:
            if type(prop) == list:
                for x in prop:
                    for num in numbers:
                        if num in x and "[" not in x:
                            headers[headers.index(elem)][elem.index(prop)] = x
                            break


    # Joining up any subject names that got split up
    for elem in headers:
        for prop in elem:
            if type(prop) == list:
                headers[headers.index(elem)][elem.index(prop)] = " ".join(prop)


    # Removing any % symbols
    for elem in headers:
        for prop in elem:
            if "%" in prop:
                headers[headers.index(elem)][elem.index(prop)] = prop[:-1]


    # Converting all numerical data values to ints and floats
    for elem in headers:
        for prop in elem:
            if " " in prop:
                tmp = prop.replace(" ", "")
                if not tmp.isalpha():
                    if "." in prop:
                        headers[headers.index(elem)][elem.index(prop)] = float(prop)
                    elif "." not in prop:
                        headers[headers.index(elem)][elem.index(prop)] = int(prop)
            else:
                if not prop.isalpha():
                    if "." in prop:
                        headers[headers.index(elem)][elem.index(prop)] = float(prop)
                    elif "." not in prop:
                        headers[headers.index(elem)][elem.index(prop)] = int(prop)


    # Renaming variable for later
    old_stats = headers



''' CALCULATING SUBJECT SATISFACTIONS '''

# Setting up subject satisfactions list
sub_sats = []
for x in range(len(categories)):
    sub_sats.append([])


# Obtaining codes and their indices
used_codes = []
codes_and_indices = []
index = 0
for file in os.listdir(directory):
    code = ""
    if "[" in file:
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                code+=e
        if code not in used_codes:
            sub_sats[index].append(file)
            codes_and_indices.append([code, index])
            used_codes.append(code)
            index += 1


# Getting all the filenames into a list for satisfaction calculation
for file in os.listdir(directory):
    code = ""
    actual_index = 0
    if "[" in file:
        for e in file:
            if e == "[":
                continue
            elif e == "]":
                break
            else:
                code+=e
        for elem in codes_and_indices:
            if code in elem:
                actual_index = elem[1]
        if file not in sub_sats[actual_index]:
            sub_sats[actual_index].append(file)


# Sorting the list so they're in order of number of articles per subject
sub_sats = sorted(sub_sats, key=len, reverse=True)


# Calculating subject satisfactions
sats_subjects = []
for sub in sub_sats:
    total = 0
    non = 0
    for art in sub:
        total += 1
        if "+" not in art:
            non += 1
    sat = round((non/total) * 100, 2)
    sats_subjects.append(sat)



''' NEW SUBJECT DATA '''

# Order of header metrics is: rank, % share of articles, a, t, a:t, sat

# Setting up new stats list with all subject names
new_stats = []
for x in range(len(topics_actual)):
    new_stats.append([categories[x]])


# Adding all the new ranks to the new stats list for each suject
for x in range(len(topics_actual)):
    new_stats[x].append(categories.index(new_stats[x][0]) + 1)


# Obtaining all new values for percentage share, a and t per subject, and appending to a list
percentages = []
article_numbers = []
topics_numbers_delta = []
for e in topics_actual:
    cat = codes_list2[topics_actual.index(e)]
    articles_n = amounts[categories.index(cat)]
    percent = round(articles_n/n *100, 2)
    percentages.append(percent)
    article_numbers.append(articles_n)
    topics_numbers_delta.append(len(e))


# Adding new stats to respective sub-lists in new stats list
for x in range(len(topics_actual)):
    new_stats[x].append(percentages[x])
    new_stats[x].append(article_numbers[x])
    new_stats[x].append(topics_numbers_delta[x])
    new_stats[x].append(round(article_numbers[x]/topics_numbers_delta[x], 2))
    new_stats[x].append(sats_subjects[x])



''' PREPARING FOR DELTA CALCULATIONS '''

# Setting up the deltas list
deltas = []
for x in range(len(topics_actual)):
    deltas.append([])


# Calulating new a and t values
new_a = 0
new_t = 0
for sub in new_stats:
    new_a += sub[3]
    new_t += sub[4]


# Calculating new s value
new_s = len(new_stats)


# Calulating new t:s value
new_ts = new_t//new_s


# Calculating new a:s value
new_as = new_a//new_s


# Calulating new a:t value
new_at = round(new_a/new_t, 2)


# Renaming overall satisfaction value variable
new_sat_overall = sat_overall


# Finding, and then deleting, old contents file
found_contents = False

for file in os.listdir(directory):
    if "contents" in file:
        found_contents = True
        filename = file

        split_n = filename.split("(")
        split_n = split_n[1]
        split_n = split_n.split(")")
        split_n = split_n[0]
        split_n = split_n.split(" = ")
        split_n = int(split_n[1])

        os.remove(f"contents (t = {split_n}).txt")


# Turning off calculating deltas if no old contents file exists
if found_contents == False:
    deltasON = False



''' DELTAS '''

# Order of header metrics is: rank, % share of articles, a, t, a:t, sat

# Ensuring conditions are met for deltas to be calculated
if deltasON == True and old_headersBOOL == True:
    for elem in new_stats:
        subject = elem[0]
        found = False
        for parts in old_stats:

            # Checking to see if current subject is new or not
            if subject in parts:
                # Calculating deltas, and then adding them to deltas list
                found = True
                index = old_stats.index(parts)
                deltas[index].append((-1) * (elem[1] - parts[1]))
                deltas[index].append(round((elem[2] - parts[2]), 2))
                deltas[index].append((elem[3] - parts[3]))
                deltas[index].append((elem[4] - parts[4]))
                deltas[index].append(round((elem[5] - parts[5]), 2))
                deltas[index].append(round((elem[6] - parts[6]), 2))

        # If current subject is new, just add their new stat values as 'deltas'
        if found == False:
            deltas[new_stats.index(elem)] = elem[1:]


    # Formatting each of the deltas
    for elem in deltas:
        for delta in elem:

            # If zero, then [=]
            if delta == 0 or delta == 0.0:
                deltas[deltas.index(elem)][elem.index(delta)] = " [=]"

            # If positive, then adding in a + sign and square brackets
            elif delta > 0:
                deltas[deltas.index(elem)][elem.index(delta)] = " [+" + str(delta) + "]"

            # If negative, just adding in the square brackets
            elif delta < 0:
                deltas[deltas.index(elem)][elem.index(delta)] = " [" + str(delta) + "]"


    # Calculating old a and t values
    old_a = 0
    old_t = 0
    for sub in old_stats:
        old_a += sub[3]
        old_t += sub[4]


    # Calculating a and t deltas
    delta_a = new_a - old_a
    delta_t = new_t - old_t


    # Formatting a delta
    if delta_a == 0:
        delta_a = " [=]"
    elif delta_a > 0:
        delta_a = " [+" + str(delta_a) + "]"
    elif delta_a < 0:
        delta_a = " [" + str(delta_a) + "]"


    # Formatting t delta
    if delta_t == 0:
        delta_t = " [=]"
    elif delta_t > 0:
        delta_t = " [+" + str(delta_t) + "]"
    elif delta_t < 0:
        delta_t = " [" + str(delta_t) + "]"


    # Calulating old s value
    old_s = len(old_stats)


    # Calulating s delta
    delta_s = new_s - old_s


    # Formatting s delta
    if delta_s == 0:
        delta_s = " [=]"
    elif delta_s > 0:
        delta_s = " [+" + str(delta_s) + "]"
    elif delta_s < 0:
        delta_s = " [" + str(delta_s) + "]"


    # Calculating old a:t value
    old_at = round(old_a/old_t, 2)


    # Calculting a:t delta
    delta_at = new_at - old_at


    # Formatting a:t delta
    if delta_at == 0:
        delta_at = " [=]"
    elif delta_at > 0:
        delta_at = " [+" + str(delta_at) + "]"
    elif delta_at < 0:
        delta_at = " [" + str(delta_at) + "]"


    # Calulcating old t:s value
    old_ts = old_t//old_s


    # Calculating t:s delta
    delta_ts = new_ts - old_ts


    # Formatting t:s delta
    if delta_ts == 0:
        delta_ts = " [=]"
    elif delta_ts > 0:
        delta_ts = " [+" + str(delta_ts) + "]"
    elif delta_ts < 0:
        delta_ts = " [" + str(delta_ts) + "]"


    # Calculating old a:s value
    old_as = old_a//old_s


    # Calculting a:s delta
    delta_as = new_as - old_as


    # Formatting a:s delta
    if delta_as == 0:
        delta_as = " [=]"
    elif delta_as > 0:
        delta_as = " [+" + str(delta_as) + "]"
    elif delta_as < 0:
        delta_as = " [" + str(delta_as) + "]"


    # Calculating time delta if old leaderboard exists
    if old_leaderboardBOOL == True:

        #Calculating correct index
        date_line_index = 10 + m.ceil(len(categories)/2)


        # Obtaining the line with the date in
        date_line = lines[date_line_index]


        # Splitting up the date line
        date_line = date_line.split(" ")


        # Getting the old date from the split line
        old_date = date_line[6]


        # Getting each piece of the date
        old_day = int(old_date[:2])
        old_month = int(old_date[3:5])
        old_year = int(old_date[6:])


        # Converting old & current dates to datetime objects
        old_date = dt.date(old_year, old_month, old_day)
        new_date = dt.date(int(year), int(month), int(day))


        # Calculating the time delta
        delta_date = new_date - old_date


        # Extracting just the number of days
        delta_date = delta_date.days


        # Correctly formatting the time delta
        if delta_date == 1:
            delta_date = f" [ {delta_date} day ago ] ####################"
        else:
            delta_date = f" [ {delta_date} days ago ] ###################"


    # If time delta can't be calculated, ensuring the contents file will be correctly formatted
    elif old_leaderboardBOOL == False and old_topPanelBOOL == False:
        delta_date = " ##################################"


    # Calclation of time delta if no leaderboard is present in old file
    elif old_leaderboardBOOL == False and old_topPanelBOOL == True:

        # Setting correct date line index
        date_line_index = 8


        # Obtaining the date line
        date_line = lines[date_line_index]


        # Splitting up the date line
        date_line = date_line.split(" ")


        # Getting the old date from the split list
        old_date = date_line[6]


        # Getting each part of the date
        old_day = int(old_date[:2])
        old_month = int(old_date[3:5])
        old_year = int(old_date[6:])


        # Converting the old and current dates into datetime objects
        old_date = dt.date(old_year, old_month, old_day)
        new_date = dt.date(int(year), int(month), int(day))


        # Calculating the time delta
        delta_date = new_date - old_date


        # Getting just the number of days
        delta_date = delta_date.days


        # Formatting time delta correctly
        if delta_date == 1:
            delta_date = f" [ {delta_date} day ago ] ####################"
        else:
            delta_date = f" [ {delta_date} days ago ] ###################"


    # Calculating old satisfaction value, if possible
    if old_topPanelBOOL == True:
        old_sat_overall = float(old_sat)

        delta_sat_overall = round(new_sat_overall - old_sat_overall, 2)

        # Formatting satisfaction delta
        if delta_sat_overall == 0.0:
            delta_sat_overall = " [=]"
        elif delta_sat_overall < 0:
            delta_sat_overall = " [" + str(delta_sat_overall) + "]"
        elif delta_sat_overall > 0:
            delta_sat_overall = " [+" + str(delta_sat_overall) + "]"


# Zeroing delta values if they can't/shouldn't be calculated
elif deltasON == False or old_headersBOOL == False:
    for elem in deltas:
        for x in range(6):
            elem.append("")
    delta_a = ""
    delta_s = ""
    delta_t = ""
    delta_as = ""
    delta_at = ""
    delta_ts = ""
    delta_sat_overall = ""
    delta_date = " ##################################"


# Setting delta values based on customisable and previous conditions
if found_contents:
    if old_topPanelBOOL == False and deltasON == True:
        delta_sat_overall = " [=]"
        delta_date = " ##################################"
    elif old_topPanelBOOL == False and deltasON == False:
        delta_sat_overall = ""
        delta_date = " ##################################"



''' CONTENTS FILE WRITING '''

# Opening the file
with open(f"contents (t = {new_t}).txt", "w+", encoding='utf-8') as f1:

    # Writing the top panel if wanted
    if topPanelON:
        f1.write("####################################### Contents #########################################\n\n")
        f1.write(f"			  a = {new_a}{delta_a}       t = {new_t}{delta_t}       s = {new_s}{delta_s}\n\n")
        f1.write(f"			  a:s = {new_as}{delta_as}      t:s = {new_ts}{delta_ts}      a:t = {new_at}{delta_at}\n\n")
        f1.write(f"				     sat = {new_sat_overall}% {delta_sat_overall}\n")


    # Writing leaderboard if wanted
    if leaderboardON:
        f1.write("\n\n")

        # If there is an odd number of subjects
        if len(categories) % 2 != 0:
            for x in range(len(topics_actual)//2 + 1):

                # If length of primary subject in leaderboard > 20, use 2 tabs
                if len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) > 20:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})		{x + 2 + len(topics_actual)//2}. {categories[x + 1 + len(topics_actual)//2]} ({len(sub_sats[x + 1 + len(topics_actual)//2])}{deltas[x + 1 + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break


                # If length of primary subject in leaderboard <= 20, and greater than 12, use 3 tabs
                elif len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) <= 20 and len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) > 12:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})			{x + 2 + len(topics_actual)//2}. {categories[x + 1 + len(topics_actual)//2]} ({len(sub_sats[x + 1 + len(topics_actual)//2])}{deltas[x + 1 + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break


                # If length of primary subject in leaderboard <= 12, use 4 tabs
                elif len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) <= 12:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})				{x + 2 + len(topics_actual)//2}. {categories[x + 1 + len(topics_actual)//2]} ({len(sub_sats[x + 1 + len(topics_actual)//2])}{deltas[x + 1 + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break


            # Add the final line on the leaderboard
            f1.write(f"	{len(categories)//2 + 1}. {categories[len(categories)//2]} ({len(sub_sats[len(categories)//2])}{deltas[len(categories)//2][4]})\n")


        # If there is an even number of subjects
        elif len(categories) % 2 == 0:
            for x in range(len(topics_actual)//2 + 1):

                # If length of primary subject in leaderboard > 20, use 2 tabs
                if len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) > 20:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})		{x + 1 + len(topics_actual)//2}. {categories[x + len(topics_actual)//2]} ({len(sub_sats[x + len(topics_actual)//2])}{deltas[x + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break


                # If length of primary subject in leaderboard <= 20, and greater than 12, use 3 tabs
                elif len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) <= 20 and len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) > 12:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})			{x + 1 + len(topics_actual)//2}. {categories[x + len(topics_actual)//2]} ({len(sub_sats[x + len(topics_actual)//2])}{deltas[x + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break


                # If length of primary subject in leaderboard <= 12, use 4 tabs
                elif len(categories[x]) + 3 + len(str(len(sub_sats[x]))) + len(deltas[x][3]) <= 12:
                    try:
                        f1.write(f"	{x+1}. {categories[x]} ({len(sub_sats[x])}{deltas[x][3]})				{x + 1 + len(topics_actual)//2}. {categories[x + len(topics_actual)//2]} ({len(sub_sats[x + len(topics_actual)//2])}{deltas[x + len(topics_actual)//2][3]})\n")
                    except IndexError:
                        break

        f1.write("\n")


    # Writing the last time updated, and the time delta if wanted
    if topPanelON:
        f1.write(f"################## Last updated at {current_time} on {day}/{month}/{year}{delta_date}\n\n")


    # Writing the actual topics to the contents file
    index = 0
    for e in topics_actual:

        if topics_actual.index(e) != 0:
            f1.write("\n")

        # Getting the subject, a, percentage share, colour and rank of each subject
        cat = codes_list2[topics_actual.index(e)]
        articles_n = amounts[categories.index(cat)]
        percent = round(articles_n/new_a *100, 2)
        colour = colours[topics_actual.index(e)]
        rank = topics_actual.index(e) + 1

        # Writing the subject header, with all of its metrics
        if headersON:
            f1.write(f":: {cat} {c.to_hex(colour)} ( {rank}{deltas[index][0]} | {percent}%{deltas[index][1]} | a = {articles_n}{deltas[index][2]} | t = {len(e)}{deltas[index][3]} | a:t = {round(articles_n/len(e), 2)}{deltas[index][4]} | sat = {sats_subjects[index]}%{deltas[index][5]} ) ::\n")


        # Writing a basic header if a metric-heavy one is not wanted
        elif headersON == False:
            f1.write(f":: {cat} ::\n")


        # Writing each topic in turn
        for topic in e:
            f1.write(f"- {topic}\n")
        f1.write("\n")

        # Writing a spacer to break up the contents file after each subject
        f1.write("##########################################################################################################################\n")
        index += 1

    # Indication to show writing has finished successfully
    f1.write("\n\n~ END ~")



''' SETTING UP PLOTS '''

# Finding, and removing, old distribution file
for file in os.listdir(directory):
    if "distribution" in file:
        filename2 = file


        # Extracting necessary parts (old a value) in order to open file
        split_n2 = filename2.split("(")
        split_n2 = split_n2[1]
        split_n2 = split_n2.split(")")
        split_n2 = split_n2[0]
        split_n2 = split_n2.split(" = ")
        split_n2 = int(split_n2[1])

        os.remove(f"distribution (a = {split_n2}).pdf")


# Replacing any subject names containing spaces with newline characters so that the graph looks better
for x in range(len(categories)):
    if " " in categories[x]:
        categories[x] = categories[x].replace(" ", "\n")



''' PLOTTING AND SAVING GRAPH '''

# Setting up the figure
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = width
fig_size[1] = height
plt.rcParams["figure.figsize"] = fig_size


# Configuring subplots
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
if pieChartON:
    ax2 = fig.add_subplot(2,4,4)


# Adding a title
ax1.set_title("Distribution of Articles", fontsize = 30, weight="bold", ha="center")


# Plotting the bars
ax1.bar(categories, amounts, color=colours, width = 1)


# Adding the numbers on the bars, and the percentages - if wanted
for a,b in zip(categories, amounts):
    if numbersON:
        ax1.text(a, b+0.5, str(b), ha="center", weight="bold")
    if percentagesON:
        ax1.text(a, b-4.8, f"({round(b/new_a *100, 2)}\%)", ha="center", weight="bold", fontsize=13, color="w")


# Setting x- and y-axis labels
ax1.set_ylabel("Article\nFrequency", fontsize=21, weight="bold", rotation=0, labelpad=35, va='center')
ax1.set_xlabel("Subjects", fontsize=21, weight="bold", labelpad=10, ha='center')


# Setting the margins to zero, making the graph look better
ax1.margins(x=0)


# Plotting the metrics, if wanted
if metricsON:
    ax1.text(x=len(categories)//2, y=amounts[0], s=f"a = {new_a} ~ t = {new_t} ~ s = {new_s}", ha='center', weight='bold', ma='center')


# Plotting ratios, either at a higher or lower height depending on the metrics' presence, if wanted
if ratiosON == True and metricsON == False:
    ax1.text(x=len(categories)//2, y=amounts[0], s=f"a:s = {new_as} ~ t:s = {new_ts} ~ a:t = {new_at}", ha='center', weight='bold', ma='center')
elif ratiosON == True and metricsON == True:
    ax1.text(x=len(categories)//2, y=amounts[0]-6, s=f"a:s = {new_as} ~ t:s = {new_ts} ~ a:t = {new_at}", ha='center', weight='bold', ma='center')


# Plotting the pie chart, if wanted
if pieChartON:
    ax2.pie(amounts, colors=colours, startangle=360, counterclock=True)


# Saving the figure
plt.savefig(f"distribution (a = {new_a}).pdf", bbox_inches="tight", dpi=3000)
