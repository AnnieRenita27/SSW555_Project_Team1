'''
User Story 02
Birth before marriage

'''
import us01


def BirthBeforeMarriage(individual):
    if individual.birthDate != 'NA' and individual.marriageDate != 'NA':
        return us01.checkDate(individual.birthDate, individual.marriageDate)
    elif individual.birthDate == 'NA':
        return True
    elif individual.marriageDate == 'NA':
        return True


def main():
    result = us01.main()
    individual = result[0]
    return individual
