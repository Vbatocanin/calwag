from __future__ import print_function
from datetime import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import dateFunctions
import yamlReader


# If modifying these scopes, delete the file calendar.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main(start, end):
    creds = None
    # The file calendar.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('calendar.pickle'):
        with open('calendar.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'calendar.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('calendar.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    # message to be sent by mail
    msg = ""
    # message to be printed to terminal
    msgPrint = ""

    # DATE GETTING SECTION

    # If a date is not inputted, calculate wage from curMonth-2,defaultDay to curMonth-1,defaultDay
    # defaultDay is fetched from shatterhand2.yml as default_date_day
    if (start == '0'):
        todayDate = datetime.now()

        # reads default day and calculates wage from currentMonth-2,defaultDay to currentMonth-1,defaultDay
        defaultDay = yamlReader.getDefault()

        [monthGoogleEnd, yearGoogleEnd] = dateFunctions.dateLastMonth(todayDate.month, todayDate.year)
        [monthGoogleBegin, yearGoogleBegin] = dateFunctions.dateLastMonth(monthGoogleEnd, yearGoogleEnd)

        # making begin and end time both for googleApi and datetime formatting
        googleBeginTime = datetime(yearGoogleBegin, monthGoogleBegin, defaultDay).isoformat() + 'Z'
        googleEndTime = datetime(yearGoogleEnd, monthGoogleEnd, defaultDay, 23, 59).isoformat() + 'Z'

        beginTime = datetime(yearGoogleBegin, monthGoogleBegin, defaultDay)
        endTime = datetime(yearGoogleEnd, monthGoogleEnd, defaultDay)

        # MSG FORMATTING
        msgPrint = msgPrint + "\n"
        msgPrint = msgPrint + ("Wages from {}.{}.{} to {}.{}.{}\n".format(beginTime.year, beginTime.month,
                                                                          beginTime.day, endTime.year, endTime.month,
                                                                          endTime.day, ))
        msg = msg + "<tr><td colspan=" + str(6) + \
              ">Wages from: <b>{}.{}.{}</b> to: <b>{}.{}.{}</b></td>".format(beginTime.year, beginTime.month,
                                                                             beginTime.day, endTime.year,
                                                                             endTime.month, endTime.day, )
        msg = msg + "<tr><th>Name</th><th>Regular hours</th><th>After 5pm</th><th>After 8pm</th><th>Sunday</th><th>" \
                    "Total for employee:</th></tr>"
        msgPrint = msgPrint + ("-------------------------------------------------------------------------------\n")

    # in case of only d1 inputed, calculates from d1.month,d1.day to d1.month+1,d1.day-1
    elif (end == '0'):
        # Fetching initial date values
        inputedDates = dateFunctions.getDates(start, None)
        googleBeginTime = inputedDates[0].isoformat() + 'Z'
        # msgPrint = msgPrint + ("Begin time: {}\n".format(googleBeginTime))

        googleEndTime = inputedDates[1].isoformat() + 'Z'
        # msgPrint = msgPrint + ("End time: {} \n".format(googleEndTime))

        # MSG FORMATTING
        msgPrint = msgPrint + ("\n")
        msgPrint = msgPrint + (
            "Wages from {}.{}.{} to {}.{}.{}\n".format(inputedDates[0].year, inputedDates[0].month, inputedDates[0].day,
                                                       inputedDates[1].year, inputedDates[1].month,
                                                       inputedDates[1].day))
        msg = msg + "<tr><td colspan=" + str(6) + \
              ">Wages from: <b>{}.{}.{}</b> to: <b>{}.{}.{}</b></td>".format(inputedDates[0].year,
                                                                             inputedDates[0].month, inputedDates[0].day,
                                                                             inputedDates[1].year,
                                                                             inputedDates[1].month,
                                                                             inputedDates[1].day)
        msg = msg + "  <tr><th>Name</th><th>Regular hours</th><th>After 5pm</th><th>After 8pm</th><th>Sunday</th>" \
                    "<th>Total for employee:</th></tr>"
        msgPrint = msgPrint + ("-------------------------------------------------------------------------------\n")
        msg = msg + "<br>" + "-------------------------------------------------------------------------------"

    # Else, calculates dates accordingly
    else:
        # Fetching initial date values
        inputedDates = dateFunctions.getDates(start, end)
        googleBeginTime = inputedDates[0].isoformat() + 'Z'
        # msgPrint = msgPrint + ("Begin time: {}\n".format(googleBeginTime))

        googleEndTime = inputedDates[1].isoformat() + 'Z'
        # msgPrint = msgPrint + ("End time: {} \n".format(googleEndTime))

        # MSG FORMATTING
        msgPrint = msgPrint + ("\n")
        msgPrint = msgPrint + (
            "Wages from {}.{}.{} to {}.{}.{}\n".format(inputedDates[0].year, inputedDates[0].month, inputedDates[0].day,
                                                       inputedDates[1].year, inputedDates[1].month,
                                                       inputedDates[1].day))
        msg = msg + "<tr><td colspan=" + str(6) + \
              ">Wages from: <b>{}.{}.{}</b> to: <b>{}.{}.{}</b></td>".format(inputedDates[0].year,
                                                                             inputedDates[0].month, inputedDates[0].day,
                                                                             inputedDates[1].year,
                                                                             inputedDates[1].month,
                                                                             inputedDates[1].day)
        msg = msg + "  <tr><th>Name</th><th>Regular hours</th><th>After 5pm</th><th>After 8pm</th><th>Sunday</th>" \
                    "<th>Total for employee:</th></tr>"
        msgPrint = msgPrint + ("-------------------------------------------------------------------------------\n")

    # Call the Calendar API
    calendar = yamlReader.getCalendarID()
    # Getting the events from the appropriate time period
    events_result = service.events().list(calendarId=calendar,
                                          timeMin=googleBeginTime,
                                          timeMax=googleEndTime,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    ########################

    employees = yamlReader.getEmployeesList()
    rules = yamlReader.getRulesList()

    ########################

    # HOURS COUNTER SECTION
    grandTotal = 0
    if not events:
        msgPrint = msgPrint + ("No registered work time.\n")
        msg = msg + "<br> No registered work time."
    for employee in employees:
        empWage = 0
        name = employee['name']
        hr = employee['hourly_wage']
        rates = []
        for rule in rules:
            tmp = eval(rule['formula'])
            rates.append(tmp)
        normalCoef = rates[1]
        lateCoef = rates[2]
        lateLateCoef = rates[3]
        sundayCoef = rates[0]

        # number of special and normal work hours
        normalNum = 0
        lateNum = 0
        lateLateNum = 0
        sundayNum = 0
        # counter is for determining if at least one event exists for a given worker
        counter = 0
        for tmpEvent in events:
            if (-1 != tmpEvent['summary'].find(name) and -1 == tmpEvent['summary'].find(name + "s")):
                if counter == 0:
                    counter = 1
                # only the first 19 chars are used because of timezone formatting
                startDatetime = datetime.strptime(tmpEvent['start']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')
                endDatetime = datetime.strptime(tmpEvent['end']['dateTime'][:19], '%Y-%m-%dT%H:%M:%S')
                # determining type of work hours
                # judging by weekday and time
                tmpNormalNum = 0
                tmpLateNum = 0
                tmpLateLateNum = 0
                tmpSundayNum = 0

                tmpDateTime = startDatetime

                while True:

                    if (dateFunctions.closeEnough(tmpDateTime, endDatetime) == True):
                        break
                    holidayInd = dateFunctions.isHolliday(tmpDateTime)
                    tmpHour = tmpDateTime.hour
                    if tmpDateTime.minute > 0:
                        tmpHour+=0.5
                    if holidayInd is True:
                        tmpSundayNum += 0.5
                    elif tmpHour < 8:
                        tmpLateLateNum += 0.5
                    elif (tmpHour >= 8 and tmpHour < 17):
                        tmpNormalNum += 0.5
                    elif (tmpHour >= 17 and tmpHour < 20):
                        tmpLateNum += 0.5
                    elif (tmpHour >= 20):
                        tmpLateLateNum += 0.5
                    tmpDateTime = dateFunctions.getNextHalfHourDate(tmpDateTime)

                # WAGE CALCULATOR SUBSECTION
                wage = normalCoef * tmpNormalNum + lateCoef * tmpLateNum + lateLateCoef * tmpLateLateNum + sundayCoef * tmpSundayNum
                grandTotal += wage
                empWage += wage
                normalNum += tmpNormalNum
                lateNum += tmpLateNum
                lateLateNum += tmpLateLateNum
                sundayNum += tmpSundayNum
        if counter != 0:
            msgPrint = msgPrint + (
                "{:>10}: {:>5}x{} + {:>5}x{} + {:>5}x{} + {:>5}x{} = {:8.2f}\n".format(name, normalNum, normalCoef,
                                                                                       lateNum, lateCoef,
                                                                                       lateLateNum, lateLateCoef,
                                                                                       sundayNum, sundayCoef,
                                                                                       empWage))
            msg = msg + "<tr><td>{}</td><td>{}x{}</td><td>{}x{}</td><td>{}x{}</td><td>{}x{}</td><td>{}</td></tr>".format(
                name, normalNum, normalCoef, lateNum,
                lateCoef, lateLateNum, lateLateCoef,
                sundayNum, sundayCoef, empWage)

    msgPrint = msgPrint + ("-------------------------------------------------------------------------------\n")
    msgPrint = msgPrint + ("                                                       Total: {:8.2f}\n".format(grandTotal))
    msg = msg + "<tr><td></td><td></td><td></td><td></td><td><b>Total:</b></td><td><b>{}</b></td></tr>".format(
        grandTotal)

    print(msgPrint)
    return msg


if __name__ == '__main__':
    main('0', '0')
