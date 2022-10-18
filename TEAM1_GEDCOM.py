'''
SSW 555 Project:
Team 1
Team members :Annie Renita and Donjie Zou
Public repository name on GitHub: SSW555_Project_Team1

'''
from tabulate import tabulate
from datetime import date, datetime
import time
import us01,us02

families = []
individuals = []
FILE_NAME = "GEDCOM_data.ged"


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
    tbl_headers = ["User Story", "Description", "Notes", "Pass", "Result"]
    list_table = []
    marriage_after_fourteen()  # US10
    sibling_age_space(list_table)  # US13
    birth_before_parents_death(list_table)  # US09
    list_deceased(list_table)  # US29

    return tabulate(list_table, tbl_headers, tablefmt="fancy_grid")


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
    with open("GEDCOM_data.ged") as file:
        lines = file.readlines()
    file.close()
    return lines


def get_individual(ind_id):
    if ind_id is not None:
        return individuals[int(ind_id[2:-1]) - 1]


def get_husband_id(ind):
    return families[int(ind.child_id[2:-1]) - 1].husband


def get_wife_id(ind):
    return families[int(ind.child_id[2:-1]) - 1].wife


def print_individuals():
    headers = ["Id", "Name", "Sex", "Birthday", "Alive", "Death", "Child Id", "Spouse Id"]
    table = []
    for ind in individuals:
        table.append([ind.i_id, ind.name, ind.sex, format_date(ind.birth), True if ind.death is None else False,
                      format_date(ind.death) if ind.death is not None else "NA", ind.child_id, ind.spouse_id])
    return tabulate(table, headers, tablefmt="fancy_grid")


def print_families():
    tbl_headers = ["Id", "Married", "Divorced", "Husband Id", "Husband Name", "Wife Id", "Wife Name", "Children Ids"]
    list_table = []
    for fam in families:

        if fam.husband is not None:
            husband_name = get_individual(fam.husband).name
        else:
            husband_name = "NA"
        if fam.wife is not None:
            wife_name = get_individual(fam.wife).name
        else:
            wife_name = "NA"
        list_table.append([fam.f_id, format_date(fam.marriage) if fam.marriage is not None else "NA",
                           format_date(fam.divorce) if fam.divorce is not None else "NA", fam.husband,
                           husband_name, fam.wife, wife_name,
                      ", ".join(fam.children)])
    return tabulate(list_table, tbl_headers, tablefmt="fancy_grid")


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


# Calculate Age
def age(birthdate, death_date):
    birth_date_obj = datetime.strptime(birthdate, '%Y %b %d')
    if death_date == 0:
        today = date.today()
        age_calc = today.year - birth_date_obj.year - ((today.month, today.day) < (birth_date_obj.month, birth_date_obj.day))
    if death_date != 0:
        death_date_obj = datetime.strptime(death_date, '%Y %b %d')
        age_calc = death_date_obj.year - birth_date_obj.year - (
                    (death_date_obj.month, death_date_obj.day) < (birth_date_obj.month, birth_date_obj.day))
    return age_calc

# Function for file length
def file_len(f):
    for count, l in enumerate(f):
        pass
    return count + 1


# Function to create a list for individuals
def indi_list():
    return [0 for i in range(4999)]


# Function to create a list for families
def fam_list():
    plist = [0 for i in range(999)]
    plist[5] = []
    return plist


# Function to get the last name
def getLastName(str_name):
    temp = ''
    for i in str_name:
        if i != '/':
            temp += i
    return temp


# Function to get name by ID in list of individual
def getNameByID(individual_list, person_id):
    for i in individual_list:
        if i[0] == person_id:
            return i[1]

#Function for Listing Deascesed
def death_list(ind_list):
    dead_people = []
    for i in ind_list:
        if(len(i)>3):
            if (i[4] != 0):
                dead_people = dead_people+ [i[1]]
    return dead_people

#Funciton for Listing Living Married people
def married_list(ind_list):
    married = []
    for i in ind_list:
        if (i[4]==0 and i[6] != 0):
            married = married + [i[1]]
    return married

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

def find_duplicate_marriages(list_fam):
    unique_marriages = []
    duplicate_marriages = []
    temp  = [list_fam]
    for i in list_fam:
        for j in temp[0:]:
            if ((i[1] == j[1]) and (i[2] == j[2])) :
                print(getNameByID(indi_list, i[1]),getNameByID(indi_list, i[1]), "their marriage record is more than 1.")
                duplicate_marriages.append(i)
            elif(i[3] == j[3]):
                print(getNameByID(indi_list, i[1]),getNameByID(indi_list, i[1]), "their marriage record is more than 1.")
                duplicate_marriages.append(i)
            else:
                unique_marriages.append(i)       
    return duplicate_marriages
            
# Us10 marriage after fourteen
def marriage_after_fourteen():  # US10: Marriage After 14
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
        result = "Someone got married way too early."
    print(result)


# US13 siblings spacing
def sibling_age_space(table_list):  # US13: Sibling Age Spacing
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

    table_list.append(
        ["US13", "Sibling Age Spacing", "\n".join(notes), sibling_space, result])


def birth_before_parents_death(list_table):  # US09: Birth Before Death of Parents
    valid_birth = True
    notes = []
    for ind in individuals:
        if ind.child_id is None:
            continue

        husband = get_individual(get_husband_id(ind))  # get husband
        wife = get_individual(get_wife_id(ind))  # get wife
        if wife is not None:
            if husband.death is None and wife.death is None:  # if husband and wife are alive
                continue
            elif husband.death is not None and wife.death is not None:  # if husband and wife are both dead
                if ind.birth < husband.death and ind.birth < wife.death:
                    continue
                else:
                    valid_birth = False
                    notes.append("{} was born after death of parent(s).".format(ind.name))
            elif husband.death is not None and ind.birth < husband.death:  # if husband is dead
                continue
            elif wife.death is not None and ind.birth < wife.death:  # if wife is dead
                continue
            else:
                valid_birth = False
                notes.append("{} was born after death of parent(s).".format(ind.name))

    if valid_birth:
        result = "All birth dates were before parents' deaths."
    else:
        result = "One or more birth dates were incorrect."

    list_table.append(
        ["US09", "Birth Before Death of Parents", "\n".join(notes), valid_birth, result])


def list_deceased(list_table):  # US29: List Deceased
    results = "\n".join([ind.name for ind in individuals if ind.death is not None])

    list_table.append(
        ["US29", "List Deceased", "", True, results])

#Function for storing data in list_indi, list_fam
def parse(file_name):
    f = open(file_name, 'r')
    f_len = file_len(open(file_name))
    indi_on = 0
    fam_on = 0
    list_individual = []
    list_family = []
    indi = indi_list()
    fam = fam_list()
    for line in f:
        str_array = line.split()
        if str_array:
            if str_array[0] == '0':
                if indi_on == 1:
                    list_individual.append(indi)
                    indi = indi_list()
                    indi_on = 0
                if fam_on == 1:
                    list_family.append(fam)
                    fam = fam_list()
                    fam_on = 0
                if str_array[1] in ['NOTE', 'HEAD', 'TRLR']:
                    pass
                else:
                    if str_array[2] == 'INDI':
                        indi_on = 1
                        indi[0] = (str_array[1])
                    if str_array[2] == 'FAM':
                        fam_on = 1
                        fam[0] = (str_array[1])
            if str_array[0] == '1':
                if str_array[1] == 'NAME':
                    indi[1] = str_array[2] + " " + getLastName(str_array[3])
                if str_array[1] == 'SEX':
                    indi[2] = str_array[2]
                if str_array[1] == 'BIRT':
                    date_id = 'BIRT'
                if str_array[1] == 'DEAT':
                    date_id = 'DEAT'
                if str_array[1] == 'MARR':
                    date_id = 'MARR'
                if str_array[1] == 'DIV':
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
    return list_indi, list_fam

#Main 
list_indi, list_fam = parse('C://Users//15513//Documents//Stevens Institute of Technology//Sem 3//SSW 555 Web Campus//Project//Project Assignment 3//GEDCOM_data.ged')
list_indi.sort()
list_fam.sort()

list_death = death_list(list_indi)
married = married_list(list_indi)
duplicate_marriage_record = find_duplicate_marriages(list_fam)
myData = []
# Table header
head = ["individual Unique ID", "Name", "Gender", "Birthday", "Age"]
# Printing individual's unique identifier and name of that individual
for i in list_indi:
    myData.append([i[0],i[1],i[2],i[3],i[4],i[7]])
    #print("Individual unique ID is: " + i[0] + "\nName: " + i[1] + "\n")
    
#Printing family's unique identifier, family member's names with their individual unique IDs
for i in list_fam:
    print("Family's unique ID: ", i[0],
          "\nHusband's Name: " , getNameByID(list_indi,i[1])  , ", Individual unique ID:",i[1],
          "\nWife's Name: ",getNameByID(list_indi,i[2]),", Individual unique ID:",i[2],"\n")
    
 

# display table
 
print(tabulate(myData, headers=head, tablefmt="grid"))
headers = ["User Story", "Description", "Notes", "Pass", "Result"]
table = []
def main():
    process_file(read_file())
    print("--- Individuals ---\n{}\n".format(print_individuals()))
    print("--- Families ---\n{}\n".format(print_families()))
    print("--- User Stories ---\n{}".format(run_stories()))

if __name__ == '__main__':
    main()
   
#End
