def file_len(f):
    for i,l in enumerate(f):
        pass
    return i+1

def indi_list():
    return [0 for i in range(7)]

def fam_list():
    oplist = [0 for i in range(6)]
    oplist[5] = []
    return oplist

def getLastName(str):
    temp=''
    for i in str:
        if(i != '/'):
            temp += i
    return temp

def getNameByID(indi_list, id):
    for i in indi_list:
        if(i[0] == id):
            return i[1]

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

list_indi, list_fam = parse('C://Users//62717//Desktop//ssw 533//ssw555//clone//project1//dongjezou.ged')
list_indi.sort()
list_fam.sort()

for i in list_indi:
    print("ID: " + i[0] + "\nName: " + i[1] + "\n")
for i in list_fam:
    print("ID: "+i[0]+"\nHusband's Name: "+getNameByID(list_indi,i[1])+"\nWife's Name: "+getNameByID(list_indi,i[2])+"\n")