import pandas as pd
import numpy as np
from datetime import date
import re

#.CSV file import support
def csvimport(inputFile, database, dateOverride = "", ignore = [], addSuffix = ""):
    #loads up datafram from input file
    df = pd.read_csv(inputFile)
    print(df)

    #collects all of the first column's names
    names = list(df.iloc[:,0])

    #Deletes empty names
    while np.nan in names:
        print("removing nan")
        names.remove(np.nan)

    #Deletes the class averages
    while "Class Average" in names:
        print("Removing Average")
        names.remove("Class Average")
    while "Average" in names:
        print("Removing Average")
        names.remove("Average")

    #Removes all category averages
    while "Honors" in names:
        print("Removing Honors")
        names.remove("Honors")
    while "Scholastic" in names:
        print("Removing Scholastic")
        names.remove("Scholastic")
    while "Varsity" in names:
        print("Removing Varsity")
        names.remove("Varsity")

    print(names)

    #Finds the column filled with names and renames it accurately
    df.rename(columns={'Unnamed: 0': "Names"}, inplace=True)

    #Gets rid of the extra garbage columns
    df.drop(df.columns[df.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)
    df.drop(df.columns[df.columns.str.contains('Running Average', case=False)], axis=1, inplace=True)

    #Makes a list of all the tests
    test = df.columns.to_list()
    if "Names" in test:
        test.remove("Names")
    if "Name" in test:
        test.remove("Name")

    for each in test:
        for void in ignore:
            if each.lower().find(void.lower()) != -1:
                print(each)
                print(void)
                test.remove(each)

    print(test)


    if dateOverride == "":
        #pulls out date info and compiles it into list "dates"
        for full in test:
            splits = re.split(" ", full)
            print(splits)
            day = splits[0]
            day = re.sub(r'[^\d/]', '', day)
            if day.count("/") == 1:
                day = day + "/" + str(date.today().year)
            try:
                dates.append(day)
            except NameError:
                dates = [day]
    else:
        for full in test:
            day = dateOverride
            try:
                dates.append(day)
            except NameError:
                dates = [day]

    #Finds the subject area in the title and outputs as list "subjects"
    for title in test:
        print(title)
        if "math" in title.lower():
            subject = "Mathematics"
        if "econ" in title.lower():
            subject = "Economics"
        if "art" in title.lower():
            subject = "Art"
        if "lit" in title.lower():
            subject = "Literature"
        if "music" in title.lower():
            subject = "Music"
        if "science" in title.lower():
            if "social" in title.lower():
                subject = "Social Science"
            else:
                subject = "Science"
        if "essay" in title.lower():
            subject = "Essay"
        if "interview" in title.lower():
            subject = "Interview"
        if "speech" in title.lower():
            subject = "Speech"
        try:
            subjects.append(subject)
        except NameError:
            subjects = [subject]

    print(dates)
    print(subjects)

    db = pd.read_json(database)

    #Finds all scorers not currently in db (outputs list toAddNames)
    currentNames = db.columns.to_list()
    toAddNames = [x for x in names if x not in currentNames]
    print(toAddNames)

    #Finds all tests not currently in db (outputs list toAddTests)
    currentTests = db.index.tolist()
    toAddTests = [x for x in test if x not in currentTests]
    print(toAddTests)

    #Adds all names to the db
    for toAddName in toAddNames:
        db.insert(len(db.columns) - 2, toAddName, 0)


    #Adds all tests as labels with Date and Category
    for toAddTest in toAddTests:
        if addSuffix != "":
            toAddTestName = toAddTest + " " + addSuffix
        else:
            toAddTestName = toAddTest
        print(toAddTestName)
        db.at[toAddTestName, "Date"] = dates[test.index(toAddTest)]
        db.at[toAddTestName, "Category"] = subjects[test.index(toAddTest)]



    #Adds all values into the db
    for item in test:
        for name in names:
            value = df.iat[names.index(name), test.index(item) + 1]
            try:
                if not pd.isna(value):
                    if addSuffix == "":
                        db.at[item, name] = value
                    else:
                        db.at[item + " " + addSuffix, name] = value
            except TypeError:
                print("It failed idk, " + value)
            #else:
                #print("No Value Given")
                #This just floods shit

    input("Review Changes")

    db.to_json(database)
    return db

#Combines two columns because Peter is incompitent
def cleandb(db, column1, column2):
    print(db.columns)
    values1 = db[column1].to_numpy()
    values2 = db[column2].to_numpy()
    proper1 = []
    proper2 = []
    for each in values1:
        proper1.append(each == each)
    for each in values2:
        proper2.append(each != each)
    print(proper1)
    print(proper2)
    bothTrue = [i==j and i for i, j in zip(proper1, proper2)]
    print(bothTrue)
    i = 0
    while i <= len(bothTrue):
        if bothTrue[i]:
            db.at[column2, i] = db.at[column1, i]
            print(db.at[column2, i])

    return db
