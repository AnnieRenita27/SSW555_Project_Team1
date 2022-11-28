from datetime import datetime

def checkfarms(input, personals):
    errors = []
    for i in input:
        for j in personals:
            if  j[4] == i[0] or  j[3] == i[0]:  
                if i[6] != "NA": #if dead 
                    try:
                        div_date = datetime.strptime(j[2], '%Y-%m-%d')
                        death_date = datetime.strptime(i[6], '%Y-%m-%d')
                    except ValueError:
                        div_date = datetime.strptime("2018-01-01", '%Y-%m-%d') 
                        death_date = datetime.strptime("2018-01-01", '%Y-%m-%d') 
                    if div_date > death_date:
                        errors.append("err: personals: US06: " + i[0] + ": Divorce date occurs after their date of death on line " + str(j[0]))
                        print("err: personals: US06: " + i[0] + ": Divorce date occurs after their date of death on line " + str(j[0]))
                        
    return errors  

def indivDeaths(input, newfarms):
    farms = []
    individual = []
    
    for i, b in zip(input, newfarms): 
        if i[2] != "NA":
            farms = []
            farms.append(b[0])
            farms.append(i[0])
            farms.append(i[2])
            farms.append(i[3])
            farms.append(i[5])
            individual.append(farms)
                   
    return individual

 


def main(inputindi, inputfam, newFam):
    #indivDeaths(tables[1])
    return checkfarms(inputindi, indivDeaths(inputfam, newFam))