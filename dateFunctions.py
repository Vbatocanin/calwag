from datetime import datetime
from datetime import timedelta
import yamlReader


# Function for determining the year and number of days in a month
# judging from current date, for calculating interval of currentMonth-1,minDays to currentMonth-1,maxDays

# returns the date of the next hour

def getNextHourDate(date):
    newDate = date + timedelta(seconds=3600)
    return newDate


def getNextHalfHourDate(date):
    newDate = date + timedelta(seconds=1800)
    return newDate


# returns next day at midnight
def getNextDayDate(date):
    tmpDate = date + timedelta(days=1)
    newDate = datetime(tmpDate.year, tmpDate.month, tmpDate.day, 0, 0)

    return newDate


def getLastDayDate(date):
    tmpDate = date - timedelta(days=1)
    newDate = datetime(tmpDate.year, tmpDate.month, tmpDate.day, 0, 0)

    return newDate


def isHolliday(curDate):
    # gets hollidays
    [hDays, hDates, hSpecificDates] = getHollidays()

    weekDay = curDate.weekday()
    day = curDate.day
    month = curDate.month
    year = curDate.year

    # checks if it's a sunday
    if weekDay in hDays:
        return True

    # checks if it's a holliday by date
    for tmpDate in hDates:
        if day == tmpDate.day and month == tmpDate.month:
            return True

    for tmpDate in hSpecificDates:
        if day == tmpDate.day and month == tmpDate.month and year == tmpDate.year:

            return True

    return False


def getHollidays():
    hollidaysList = yamlReader.getHollidays()
    dayNames = {"Mon": 0,
                "Tue": 1,
                "Wed": 2,
                "Thu": 3,
                "Fri": 4,
                "Sat": 5,
                "Sun": 6}
    sundays = []
    dateslist = []
    specificDateslist = []
    for tmpDay in hollidaysList:
        # it's a day of the week
        if len(tmpDay) == 3:
            sundays.append(dayNames[tmpDay])
        # add normal dates
        # determining format, if it includes the year or not
        elif len(tmpDay) <= 6:
            tmpDate = datetime.strptime(tmpDay, "%b %d")
            dateslist.append(tmpDate)
        else:
            tmpDate = datetime.strptime(tmpDay, "%b %d, %Y")
            specificDateslist.append(tmpDate)

    return [sundays, dateslist, specificDateslist]


def monthToDaysYears(month, year):
    if (month == 1):
        month2 = 12
        year2 = year - 1
    else:
        month2 = month - 1
        year2 = year

    tmp1 = [1, 3, 5, 7, 9, 11]
    tmp2 = [4, 6, 8, 10, 12]
    if month2 in tmp1:
        return 31, year2
    if month2 in tmp2:
        return 30, year2
    else:
        if ((year2 % 4 == 0 and year2 % 100 != 0) or year2 % 400 == 0):
            return 29, year2
        else:
            return 28, year2


# returns month2,year2 that are 1 month prior to month,year
def dateLastMonth(month, year):
    if (month == 1):
        month2 = 12
        year2 = year - 1
    else:
        month2 = month - 1
        year2 = year

    return [month2, year2]


def dateNextMonth(month, year):
    if (month == 12):
        month2 = 1
        year2 = year + 1
    else:
        month2 = month + 1
        year2 = year

    return [month2, year2]


# function that compares two dates, not counting minutes
def closeEnough(startDate, endDate):
    if startDate.year == endDate.year:
        if startDate.month == endDate.month:
            if startDate.day == endDate.day:
                if startDate.hour == endDate.hour:
                    if startDate.minute == endDate.minute:
                        return True
    return False


# Function that takes inputted date strings and converts them to dates
# Uses last month if nothing is inputted
def getDates(start, end):
    try:
        if end is not None:
            startDate = start
            startDate = startDate.split(".")
            startDateInts = [int(x) for x in startDate]

            endDate = end
            endDate = endDate.split(".")
            endDateInts = [int(x) for x in endDate]

            startDate = datetime(startDateInts[2], startDateInts[1], startDateInts[0])
            endDate = datetime(endDateInts[2], endDateInts[1], endDateInts[0], 23, 59, 59)

            # if (endDate-startDate>0):
            #     return startDate, endDate
            # else:
            #     raise ValueError

            return [startDate, endDate]
        else:
            startDate = start
            startDate = startDate.split(".")
            startDateInts = [int(x) for x in startDate]
            startDate = datetime(startDateInts[2], startDateInts[1], startDateInts[0])

            # calculates date of last month
            [endDatemonth, endDateYear] = dateNextMonth(startDateInts[1], startDateInts[2])
            tmpEndDate = datetime(endDateYear, endDatemonth, startDateInts[0])

            # subtracts 1 day
            endDate = getLastDayDate(tmpEndDate)

            return [startDate, endDate]


    except ValueError:
        return

def main():
    return None



if __name__ == '__main__':
   main()
