
'''
SSW 555 Project:
Team 1
Team members :Annie Renita and Donjie Zou
Public repository name on GitHub: SSW555_Project_Team1

Program:
This program calls the custom parse function to open to open the file via the 
path provided, to make a list of individuals with unique Id and name of each 
individual and a list of families with their indivial unique identifier, each 
family member's name and individual's unique identifier. Assuming the range for 
individuals will be less than 5000 and for families will be less than 1000.

'''
from tabulate import tabulate
from datetime import date,datetime
import time

families = []
individuals = []
FILE_NAME = "Final_GEDCOM_data.ged"

class Individual:
    def __init__(self, i_id):
        self.i_id = i_id
        self.name = None
        self.sex = None
        self.spouse_id = None
        self.child_id = None
        self.birth = None
        self.death = None


class Family:
    def __init__(self, f_id):
        self.f_id = f_id
        self.marriage = None
        self.divorce = None
        self.husband = None
        self.wife = None
        self.children = []

def run_stories():
    headers = ["User Story", "Description", "Notes", "Pass", "Result"]
    table = []
    marriage_after_fourteen(table)  # US10
    sibling_age_space(table)  # US13
    
    return tabulate(table, headers, tablefmt="fancy_grid")

def process_date(obj, line, date_type):
    if line[0] == "2" and line[1] == "DATE":
        if isinstance(obj, Individual):
            if date_type == "BIRT":
                obj.birth = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
            elif date_type == "DEAT":
                obj.death = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
        elif isinstance(obj, Family):
            if date_type == "MARR":
                obj.marriage = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()
            elif date_type == "DIV":
                obj.divorce = datetime.strptime(line[2].rstrip(), '%d %b %Y').date()


def process_individual(lines, index, new_individual):
    details = lines[index].split(" ", 2)
    while details[0] != "0" and index < len(lines):
        if details[0] == "1":
            if details[1] == "NAME":
                new_individual.name = details[2].strip().replace("/", "")
            elif details[1] == "SEX":
                new_individual.sex = details[2].rstrip()
            elif details[1] == "FAMS":
                new_individual.spouse_id = details[2].rstrip()
            elif details[1] == "FAMC":
                new_individual.child_id = details[2].rstrip()
            elif details[1].rstrip() == "BIRT" or details[1].rstrip() == "DEAT":
                process_date(new_individual, lines[index + 1].split(" ", 2), details[1].rstrip())
        index += 1
        details = lines[index].split(" ", 2)
    individuals.append(new_individual)
def read_file():
    with open('C://Users//parag//Downloads//Team1 - Project Assignment 3//Assignment-3//SSW555_Project_Team1//Final_GEDCOM_data.ged') as file:
        lines = file.readlines()
    file.close()
    return lines

def get_individual(ind_id):
    if ind_id != None:
        return individuals[int(ind_id[2:-1]) - 1]

def print_individuals():
    headers = ["Id", "Name", "Sex", "Birthday", "Alive", "Death", "Child Id", "Spouse Id"]
    table = []
    for ind in individuals:
        table.append([ind.i_id, ind.name, ind.sex, format_date(ind.birth), True if ind.death is None else False,
                      format_date(ind.death) if ind.death is not None else "NA", ind.child_id, ind.spouse_id])
    return tabulate(table, headers, tablefmt="fancy_grid")

def print_families():
    headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children Ids"]
    table = []
    for fam in families:
        table.append([fam.f_id, format_date(fam.marriage) if fam.marriage is not None else "NA",
                      format_date(fam.divorce) if fam.divorce is not None else "NA", fam.husband,
                      get_individual(fam.husband), fam.wife, get_individual(fam.wife),
                      ", ".join(fam.children)])
    return tabulate(table, headers, tablefmt="fancy_grid")

def process_file(lines):
    index = 0
    while index < len(lines):
        line = lines[index].split(" ", 2)
        if len(line) == 3 and line[0] == "0":
            if line[2].rstrip() == "INDI":
                process_individual(lines, index + 1, Individual(line[1].rstrip()))
            elif line[2].rstrip() == "FAM":
                process_family(lines, index + 1, Family(line[1].rstrip()))
        index += 1
    individuals.sort(key=lambda x: int(x.i_id[2:-1]))
    families.sort(key=lambda x: int(x.f_id[2:-1]))

def process_family(lines, index, new_family):
    details = lines[index].split(" ", 2)
    while details[0] != "0" and index < len(lines):
        if details[0] == "1":
            if details[1] == "HUSB":
                new_family.husband = details[2].rstrip()
            elif details[1] == "WIFE":
                new_family.wife = details[2].rstrip()
            elif details[1] == "CHIL":
                new_family.children.append(details[2].rstrip())
            elif details[1].rstrip() == "MARR" or details[1].rstrip() == "DIV":
                process_date(new_family, lines[index + 1].split(" ", 2), details[1].rstrip())
        index += 1
        details = lines[index].split(" ", 2)
    families.append(new_family)

def format_date(input_date):
    return datetime.strftime(input_date, '%d %b %Y')

#Calculate Age 
def age(birthdate,deathdate):
    birth_date_obj = datetime.strptime(birthdate, '%Y %b %d')
    if(deathdate==0):
        today = date.today()
        age = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
    if(deathdate != 0):
        death_date_obj = datetime.strptime(deathdate, '%Y %b %d')
        age = death_date_obj.year - birth_date_obj.year - ((death_date_obj.month, death_date_obj.day) < (birth_date_obj.month, birth_date_obj.day))
    #datetime.strptime(birthdate, format)

    return age

#Function for file length
def file_len(f):
    for i,l in enumerate(f):
        pass
    return i+1

# Function to create a list for indivials
def indi_list():
    return [0 for i in range(4999)]

#Function to create a list for families
def fam_list():
    oplist = [0 for i in range(999)]
    oplist[5] = []
    return oplist

#Function to get the last name
def getLastName(str):
    temp=''
    for i in str:
        if(i != '/'):
            temp += i
    return temp

#Function to get name by ID in list of individual
def getNameByID(indi_list, id):
    for i in indi_list:
        if(i[0] == id):
            return i[1]

#Us10 marriage after fourteen
def marriage_after_fourteen(table):  # US10: Marriage After 14
    proper_marriage = True
    notes = []
    for fam in families:
        if fam.marriage is None:
            continue

        wife = get_individual(fam.wife)
        hubby = get_individual(fam.husband)

        wife_marriage_age = (fam.marriage - wife.birth).days / 365.24
        husband_marriage_age = (fam.marriage - hubby.birth).days / 365.24

        if wife_marriage_age < 14 and husband_marriage_age < 14:
            notes.append("{} and {} both got married before the age of 14!".format(wife.name, hubby.name))
            notes.append("They got married on: {} and {}'s birth date is: {} and {}'s birth date is: {}".format(
                format_date(fam.marriage),
                wife.name, format_date(wife.birth), hubby.name, format_date(hubby.birth)))
            proper_marriage = False
        elif wife_marriage_age < 14:
            notes.append("{} got married before the age of 14!".format(wife.name))
            notes.append(
                "{} got married on: {} and their birth date is: {}".format(wife.name, format_date(fam.marriage),
                                                                           format_date(wife.birth)))
            proper_marriage = False
        elif husband_marriage_age < 14:
            notes.append("{} got married before the age of 14!".format(hubby.name))
            notes.append(
                "{} got married on: {} and their birth date is: {}".format(hubby.name, format_date(fam.marriage),
                                                                           format_date(hubby.birth)))
            proper_marriage = False

    if proper_marriage:
        result = "Every person here got married at the right age."
    else:
        result = "Someone got married waaay too early."
    print(result)

#US13 siblings spacing
def sibling_age_space(table):  # US13: Sibling Age Spacing
    sibling_space = True
    notes = []
    for fam in families:
        if fam.children and len(fam.children) > 1:
            for i in range(len(fam.children)):
                for j in range(i + 1, len(fam.children)):
                    if 2 < abs((get_individual(fam.children[i]).birth - get_individual(fam.children[j]).birth).days) < \
                            243.3:
                        notes.append("{} and {} are not spaced properly.".format(get_individual(fam.children[i]).name,
                                                                                    get_individual(fam.children[j]).name))
                        sibling_space = False

    if sibling_space:
        result = "All sibling ages are spaced properly."
    else:
        result = "Some sibling ages are not spaced properly."

    table.append(
        ["US13", "Sibling Age Spacing", "\n".join(notes), sibling_space, result])
 
#Function for parsing through the file and entering values in list_indi, list_fam
def parse(file_name):
    f = open(file_name,'r')
    f_len = file_len(open(file_name))
    indi_on = 0
    fam_on = 0
    list_indi = []
    list_fam = []
    indi = indi_list()
    fam = fam_list()
    for line in f:
        str = line.split()
        if(str != []):
            if(str[0] == '0'):
                if(indi_on == 1):
                    list_indi.append(indi)
                    indi = indi_list()
                    indi_on = 0
                if(fam_on == 1):
                    list_fam.append(fam)
                    fam = fam_list()
                    fam_on = 0
                if(str[1] in ['NOTE', 'HEAD', 'TRLR']):
                    pass
                else:
                    if(str[2] == 'INDI'):
                        indi_on = 1
                        indi[0] = (str[1])
                    if(str[2] == 'FAM'):
                        fam_on = 1
                        fam[0] = (str[1])
            if(str[0] == '1'):
                if(str[1] == 'NAME'):
                    indi[1] = str[2] + " " + getLastName(str[3])
                if(str[1] == 'SEX'):
                    indi[2] = str[2]
                if(str[1] == 'BIRT'):
                    date_id = 'BIRT'
                if(str[1] == 'DEAT'):
                    date_id = 'DEAT'
                if(str[1] == 'MARR'):
                    date_id = 'MARR'
                if(str[1] == 'DIV'):
                    date_id = 'DIV'
                if(str[1] == 'FAMS'):
                    indi[5] = str[2]
                if(str[1] == 'FAMC'):
                    indi[6] = str[2]
                if(str[1] == 'HUSB'):
                    fam[1] = str[2]
                if(str[1] == 'WIFE'):
                    fam[2] = str[2]
                if(str[1] == 'CHIL'):
                    fam[5].append(str[2])
            if(str[0] == '2'):
                if(str[1] == 'DATE'):
                    date = str[4] + " " + str[3] + " " + str[2]
                    if(date_id == 'BIRT'):
                        indi[3] = date
                    if(date_id == 'DEAT'):
                        indi[4] = date
                    if(date_id == 'MARR'):
                        fam[3] = date
                    if(date_id == 'DIV'):
                        fam[4] = date
                    if(indi[3] != 0):
                        indi[5] = age(indi[3],indi[4])
    return list_indi, list_fam

#Main 
list_indi, list_fam = parse('C://Users//parag//Downloads//Team1 - Project Assignment 3//Assignment-3//SSW555_Project_Team1//Final_GEDCOM_data.ged')
list_indi.sort()
list_fam.sort()

myData=[]
#Table header
head = ["individual Unique ID", "Name","Gender","Birthday","Age"]
#Printing individual's unique identifer and name of that individual
for i in list_indi:
    print("Individual unique ID is: " + i[0] + "\nName: " + i[1] + "\n")
    myData.append([i[0],i[1],i[2],i[3]])
    
#Printing family's unique identifier, family member's names with their individual unique IDs
# for i in list_fam:
#     print("Family's unique ID: "+str(i[0])+
#           "\nHusband's Name: "+getNameByID(list_indi,i[1])+", Individual unique ID:",i[1]+
#           "\nWife's Name: "+getNameByID(list_indi,i[2])+", Individual unique ID:",i[2]+"\n")
 # display table
print(tabulate(myData, headers=head, tablefmt="grid"))
headers = ["User Story", "Description", "Notes", "Pass", "Result"]
table = []
marriage_after_fourteen(table)
#End

def main():
    process_file(read_file())
    print("--- Individuals ---\n{}\n".format(print_individuals()))
    print("--- Families ---\n{}\n".format(print_families()))
    print("--- User Stories ---\n{}".format(run_stories()))


if __name__ == '__main__':
    main()
