import sqlite3


def main():

    rawData = getRawData()
    cleanData = getCleanData(rawData)
    writeToDB(cleanData)


def writeToDB(data):

    con = sqlite3.connect("jeopardy.db")
    cur = con.cursor()

    cur.executemany("INSERT INTO jeopardy VALUES (?,?,?,?,?)", data)

    con.commit()
    con.close()

    return


def getCleanData(rawData):

    translateDict = {92: None}

    for item in rawData:

        for i in range(len(item)):

            if i >= 2:

                item[i] = item[i].translate(translateDict)
                item[i] = " ".join(item[i].split())

            if i == 4:

                item[i] = item[i][0].upper() + item[i][1:]

    return [tuple(x) for x in rawData]


def getRawData():

    con = sqlite3.connect("jeopardy.db")
    cur = con.cursor()

    cur.execute("SELECT * FROM jeopardy_raw")
    allData = cur.fetchall()

    con.commit()
    con.close()

    allData = [list(x) for x in allData]

    return allData


main()
