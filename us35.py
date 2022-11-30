from datetime import date, datetime
import us01


def RecentBirth(indiv):
    recentbirthID = []
    for indi in indiv:
        if indiv[indi].birthDate != 'NA':
            bir_date = indiv[indi].birthDate
            to_day = date.today().strftime("%Y-%m-%d")
            today_date = datetime.strptime(to_day, "%Y-%m-%d")
            try:
                birthDate = datetime.strptime(bir_date, "%Y-%m-%d")
            except ValueError:
                birthDate = datetime.strptime("2022-11-25", "%Y-%m-%d")
            diffDate = (today_date - birthDate)

            if diffDate.days < 30 and diffDate.days > 0:
                recentbirthID.append(indi)
    return recentbirthID


def main():
    result = us01.main()
    individual = result[0]
    return individual