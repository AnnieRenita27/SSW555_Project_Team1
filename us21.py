import us01
def checkgender(family, indiv):
    wife = family.getWife()
    husband = family.getHusband()
   
    if(indiv[wife].getSex() != 'F'):
        return False
    if(indiv[husband].getSex() != 'M'):
        return False 
    else:
        return True


def main():
    result = us01.main()
    family = result[1]
    return family