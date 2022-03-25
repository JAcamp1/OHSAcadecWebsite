import pandas as pd
import numpy as np
from datetime import date
import re

def csvimport(inputFile, database):
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
    test.remove("Names")
    print(test)

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

    #Finds the subject area in the title and outputs as list "subjects"
    for title in test:
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
                subject = "Math"
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
        basic = []
        db[toAddName] = basic

    #Adds all tests as labels with Date and Category
    for toAddTest in toAddTests:
        print(toAddTest)
        db.at[toAddTest, "Date"] = dates[test.index(toAddTest)]
        db.at[toAddTest, "Category"] = subjects[test.index(toAddTest)]

    #Adds all values into the db
    for item in test:
        for name in names:
            itemnum = test.index(item) + 1
            namenum = names.index(name)
            value = df.iloc[namenum, itemnum]
            if not np.isnan(value):
                db.at[item, name] = value
                print(value)
            #else:
                #print("No Value Given")
                #This just floods shit

    input("Review Changes")

    db.to_json(database)
    return db

#Idk man, deprecated
def cleandb(file):
    df = pd.read_json(file)
    print(df)
    df.rename(columns={'Unnamed: 0': "Names"}, inplace=True)
    df.drop(df.columns[df.columns.str.contains('Unnamed', case=False)], axis=1, inplace=True)
    df.drop(df.columns[df.columns.str.contains('Running Average', case=False)], axis=1, inplace=True)
    df.dropna(how="all")
    print(df)
    input("confirm solid change")
    df.to_json(file)