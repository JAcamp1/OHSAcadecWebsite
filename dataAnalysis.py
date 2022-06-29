import pandas as pd
import numpy as np
from datetime import date, timedelta, datetime

def addtotals(db, compname):
    names = db.columns.tolist()
    names.remove("Date")
    names.remove("Category")
    print(names)
    for name in names:
        total = 0
        for test in db.index.tolist():
            if compname in test and test != "Score Total " + compname:
                print(db.at[test, name])
                total = total + db.at[test, name]
        db.at["Score Total " + compname, name] = total

    return db

def refreshRecs(database, export, startDate, endDate, multiply = 1000):
    #Defines D0 and D1 as the start and end date respectively in date-time format as well as getting the distance between them as delta
    temp = startDate.split("/")
    d0 = date(int(temp[2]), int(temp[0]), int(temp[1]))
    print(str(d0))
    temp = endDate.split("/")
    d1 = date(int(temp[2]), int(temp[0]), int(temp[1]))
    print(str(d1))
    delta = d1 - d0

    #Loads database as db
    db = pd.read_json(database)
    temp = db["Date"]
    testDates = []
    for each in temp:
        eachDate = str(each.to_pydatetime().date())
        testDates.append(eachDate)
        print(eachDate)
    print(testDates)

    testIndex = []
    for i in range(delta.days + 1):
        day = str(d0 + timedelta(days=i))
        print(day)
        testIndex = testIndex + np.where(testDates == day)[0]

    print(testIndex)
