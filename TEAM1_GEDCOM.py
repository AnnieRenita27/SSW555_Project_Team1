#from socket import SOL_NETROM
import unittest
'''
SSW 555 Project:
Team 1
Team members :Annie Renita, Donjie Zou, and Jonathan Morrone
Public repository name on GitHub: SSW555_Project_Team1

Program:
This program calls the custom parse function to open to open the file via the 
path provided, to make a list of individuals with unique Id and name of each 
individual and a list of families with their indivial unique identifier, each 
family member's name and individual's unique identifier. Assuming the range for 
individuals will be less than 5000 and for families will be less than 1000.

'''

#Function for seeing if an indavidual has less than 15 siblings
def siblings(fam_list, ind):
    fam = fam_list[0]
    i = 1
    while(fam[0]!= ind[6]):
        fam = fam_list[i]
        i=i+1
    if(len(fam[5])<15):
        return True
    else:
        return False
#Function for seeing if all males in family have same last name
def male_lastName(ind_list, fam):
    last_name = getNameByID(list_indi,fam[1]).split()[1]
    for i in fam[5]:
        son = ind_list[0]
        x = 1
        while(son[0]!=i):
            son=ind_list[x]
            x=x+1
        if(son[2] == "M" and son[1].split()[1]!=last_name):
            return False

    return True
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
    return list_indi, list_fam

#Main 
list_indi, list_fam = parse('C://Users//Jonathan Morrone//Desktop//Stevens//SSW555_Project_Team1//GEDCOM_data.ged')
list_indi.sort()
list_fam.sort()
list_death = death_list(list_indi)
married = married_list(list_indi)


#Printing individual's unique identifer and name of that individual
for i in list_indi:
    print("Individual unique ID is: " + i[0] + "\nName: " + i[1] + "\n")
    
#Printing family's unique identifier, family member's names with their individual unique IDs
for i in list_fam:
    print("Family's unique ID: "+i[0]+
          "\nHusband's Name: "+getNameByID(list_indi,i[1])+", Individual unique ID:",i[1]+
          "\nWife's Name: "+getNameByID(list_indi,i[2])+", Individual unique ID:",i[2]+"\n")
for i in list_fam:
    print("Do all males in family " +i[0]+" have the same last name "+(str)(male_lastName(list_indi,i)))
    
#End

