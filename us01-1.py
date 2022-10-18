'''
User Story 01
Dates before current date

'''

from datetime import date, datetime
from collections import OrderedDict


individual = OrderedDict()
family = OrderedDict()
months = {
    "JAN": "01",
    "FEB": "02",
    "MAR": "03",
    "APR": "04",
    "MAY": "05",
    "JUN": "06",
    "JUL": "07",
    "AUG": "08",
    "SEP": "09",
    "OCT": "10",
    "NOV": "11",
    "DEC": "12",
}


def parseGed(inputGed):
    lineNum = 0
    for line in inputGed:
        lineNum += 1
        values = line.split()
        level = values[0]
        tag = values[1]
        args = ' '.join(values[2:])
        if(tag[0] == '@'):
            tag = values[2]
            args = values[1]

        if(level == '0'):
            args = args.strip('@')
            index = args
            if(tag == 'INDI'):
                individual[index] = Individual(args)
                individual[index].setLineNum(lineNum)
            elif (tag == 'FAM'):
                family[index] = Family(args)
                family[index].setLineNum(lineNum)
        elif (level == '1'):
            if(tag == 'BIRT'):
                date = 'birthDate'
            elif (tag == 'DEAT'):
                date = 'deathDate'
            elif (tag == 'DIV'):
                date = 'divorceDate'
            elif (tag == 'HUSB'):
                args = args.strip('@')
                family[index].setHusband(args)
            elif (tag == 'WIFE'):
                args = args.strip('@')
                family[index].setWife(args)
            elif (tag == 'MARR'):
                date = 'marriageDate'
            elif (tag == 'SEX'):
                individual[index].setSex(args)
            elif (tag == 'FAMC'):
                args = args.strip('@')
                individual[index].setChildIdentity(args)
            elif (tag == 'CHIL'):
                args = args.strip('@')
                family[index].setFamilyChildren(args)
        elif (level == '2') and (tag == 'DATE'):
            if(date == 'birthDate'):
                individual[index].setBirthDate(args)
            elif(date == 'marriageDate'):
                husband = family[index].getHusband()
                wife = family[index].getWife()
                individual[husband].setMarriageDate(args)
                individual[wife].setMarriageDate(args)
                family[index].setMarriageDate(args)
            elif(date == 'deathDate'):
                individual[index].setDeathDate(args)
            elif(date == 'divorceDate'):
                husband = family[index].getHusband()
                wife = family[index].getWife()
                individual[husband].setDivorceDate(args)
                individual[wife].setDivorceDate(args)
                family[index].setDivorceDate(args)
    return (individual, family)


def formatDate(dates):
    date = dates.split()
    if len(date) == 1:  # if it only contains the year
        date.insert(0, '1')
        date.insert(1, 'JAN')
    if len(date) == 2:  # if it only contains month and year
        date.insert(0, '1')

    if (int(date[0]) in range(1, 10)):
        date[0] = "0" + date[0]
    month = months[date[1]]
    year = date[2]
    return (year + '-' + month + '-' + date[0])


class Individual(object):
    def __init__(self, ID='NA', birthDate='NA', marriageDate='NA', deathDate='NA', divorceDate='NA', sex='NA', childIdentity='NA'):
        self.ID = ID
        self.birthDate = birthDate
        self.marriageDate = marriageDate
        self.deathDate = deathDate
        self.divorceDate = divorceDate
        self.sex = sex
        self.childIdentity = childIdentity
        self.lineNum = 0

    def setBirthDate(self, birthDate):
        birthDate = formatDate(birthDate)
        self.birthDate = birthDate

    def setMarriageDate(self, marriageDate):
        marriageDate = formatDate(marriageDate)
        self.marriageDate = marriageDate

    def setDeathDate(self, deathDate):
        deathDate = formatDate(deathDate)
        self.deathDate = deathDate

    def setDivorceDate(self, divorceDate):
        divorceDate = formatDate(divorceDate)
        self.divorceDate = divorceDate

    def setSex(self, sex):
        self.sex = sex

    def getSex(self):
        return self.sex

    def setChildIdentity(self, childIdentity):
        self.childIdentity = childIdentity

    def setLineNum(self, lineNum):
        self.lineNum = lineNum


class Family(object):
    def __init__(self, ID='NA', husband='NA', wife='NA', marriageDate='NA', divorceDate='NA'):
        self.ID = ID
        self.husband = husband
        self.wife = wife
        self.marriageDate = marriageDate
        self.divorceDate = divorceDate
        self.children = []
        self.lineNum = 0

    def setHusband(self, husband):
        self.husband = husband

    def setWife(self, wife):
        self.wife = wife

    def getHusband(self):
        return self.husband

    def getWife(self):
        return self.wife

    def setMarriageDate(self, marriageDate):
        marriageDate = formatDate(marriageDate)
        self.marriageDate = marriageDate

    def setDivorceDate(self, divorceDate):
        divorceDate = formatDate(divorceDate)
        self.divorceDate = divorceDate

    def setFamilyChildren(self, children):
        self.children.append(children)

    def setLineNum(self, lineNum):
        self.lineNum = lineNum
 
 

def checkDate(date1, date2):
    try:
        dateTime1 = datetime.strptime(str(date1), "%Y-%m-%d")
    except ValueError:
        dateTime1 = datetime.strptime("2018-01-01", "%Y-%m-%d")
    try:
        dateTime2 = datetime.strptime(str(date2), "%Y-%m-%d")
    except ValueError:
        dateTime2 = datetime.strptime("2018-01-01", "%Y-%m-%d")

    return dateTime1 < dateTime2


def BirthBeforeCurrent(indi):
    currentDate = date.today().strftime("%Y-%m-%d")
    if individual[indi].birthDate != 'NA':
        return checkDate(individual[indi].birthDate, currentDate)
    else:
        return True


def DeathBeforeCurrent(indi):
    currentDate = date.today().strftime("%Y-%m-%d")
    if individual[indi].deathDate != 'NA':
        return checkDate(individual[indi].deathDate, currentDate)
    else:
        return True


def MarriageBeforeCurrent(indi):
    currentDate = date.today().strftime("%Y-%m-%d")
    if individual[indi].marriageDate != 'NA':
        return checkDate(individual[indi].marriageDate, currentDate)
    else:
        return True


def DivorceBeforeCurrent(indi):
    currentDate = date.today().strftime("%Y-%m-%d")
    if individual[indi].divorceDate != 'NA':
        return checkDate(individual[indi].divorceDate, currentDate)
    else:
        return True


def main():
    inputGed = open("C://Users//62717//Desktop//ssw 533//ssw555//clone//proj4//proj5//PythonApplication2//GEDCOM_data-1.ged", "r")
    result = parseGed(inputGed)
    return result
