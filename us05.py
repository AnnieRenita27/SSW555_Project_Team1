from datetime import datetime

                
def indivDeaths(input):
    fams = []
    indivs = []
    
    for i in input: 
        if i[2] != "NA":
            fams = []
            fams.append(i[0])
            fams.append(i[2])
            fams.append(i[3])
            fams.append(i[5])
            indivs.append(fams)
                  
    return indivs

def checkFams(input, indivs, famNums):
    errors = []
    
    for i in input:
        for j, k in zip(indivs, famNums):
            if j[2] == i[0] or j[3] == i[0]: #checks 
                if i[6] != "NA": #if dead
                    try:
                        deathDate = datetime.strptime(i[6], '%Y-%m-%d')
                    except ValueError:
                        deathDate = datetime.strptime("2020-04-01", '%Y-%m-%d')

                    try:
                        marriageDate = datetime.strptime(j[1], '%Y-%m-%d')
                    except ValueError:
                        marriageDate = datetime.strptime("2020-04-01", '%Y-%m-%d')
                    
                    if marriageDate > deathDate:
                        print(f"ERROR: INDIVIDUAL: US05: {i[0]}: Marriage date occurs after their date of death on line {k[0]}.")
                        errors.append(f"ERROR: INDIVIDUAL: US05: {i[0]}: Marriage date occurs after their date of death on line {k[0]}.")
                        
    return errors


def main(inputindi, inputfam, famNums):
    return checkFams(inputindi, indivDeaths(inputfam), famNums)