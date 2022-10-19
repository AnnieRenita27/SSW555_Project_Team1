'''
User Story 04
Marriage before divorce
'''
from datetime import datetime

                
def marriageBeforeDivorce(input):
    errors = []
    for j in input: 
        if j[1] != "NA":
            if j[2] != "NA":
                try:
                    marriageDate = datetime.strptime(j[1], '%Y-%m-%d')
                except ValueError:
                    marriageDate = datetime.strptime("2018-01-01", '%Y-%m-%d')
                try:
                    divorceDate = datetime.strptime(j[2], '%Y-%m-%d')
                except ValueError:
                    divorceDate = datetime.strptime("2018-01-01", '%Y-%m-%d')
                
                if marriageDate > divorceDate:
                    errors.append("ERROR: FAMILY: US04: " + j[0] + ": Divorce date occurs before their marriage.")
                    print("ERROR: FAMILY: US04: " + j[0] + ": Divorce date occurs before their marriage.")
    
    return errors

def main(lists):
    marriageBeforeDivorce(lists)