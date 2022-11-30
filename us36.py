from datetime import date, datetime,timedelta

def recent_deaths(input):
    notes_ = []

    for first, second in zip(input[0], input[2]):
        if first[5] != "True": #if dead
            try:
                death_Date = datetime.strptime(first[6], '%Y-%m-%d')

            except ValueError:
                death_Date = datetime.strptime("2022-11-25", '%Y-%m-%d')
            
            to_day = date.today().strftime("%Y-%m-%d")
            today_date = datetime.strptime(to_day, "%Y-%m-%d")
            timediff = today_date - death_Date
            if timediff.days < 30:
                print("NOTE:  personal: US36: Line: " + str(second[0]) + " ID: " + first[0] + ": death has occurred within the past 30 days")
                notes_.append("NOTE: personal: US36: Line: " + str(second[0]) + " ID: " + first[0] + ": death has occurred within the past 30 days")
        
    return notes_

def main(lists):
    recent_deaths(lists)