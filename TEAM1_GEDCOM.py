
'''
SSW 555 Project:
Team 1
Team members :Annie Renita, Donjie Zou, Johnathan Morrone and Tirth Patel
Public repository name on GitHub: SSW555_Project_Team1

'''
from tabulate import tabulate
from datetime import date,datetime
import time
import us01,us02
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
            
    
#Function for storing data in list_indi, list_fam
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
                        indi[7] = age(indi[3],indi[4])
    return list_indi, list_fam

list_indi, list_fam = parse('C://Users//62717//Desktop//ssw 533//ssw555//clone//proj4//proj5//PythonApplication2//GEDCOM_data-1.ged')
list_indi.sort()
list_fam.sort()

list_death = death_list(list_indi)

married = married_list(list_indi)

duplicate_marriage_record = find_duplicate_marriages(list_fam)

myData = [] 
#Table header
head = ["Individual Unique ID", "Name","Gender","Birthday","Death Date","Age"]
#Printing individual's details in a tabular format
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
   
   
#End
