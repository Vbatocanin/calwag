import yaml
import yamlordereddictloader
import start

# yaml file opening and loading
yamlName = start.yamlName()
yamlData = yaml.safe_load(open(yamlName))


def getDefault():
    defaultDay = None

    for (attribute, value) in yamlData.items():
        # fetching employees list
        if (attribute == "default_date_day"):
                defaultDay = int(value)
    return defaultDay


def getEmployeesList():
    employeesList = []
    for (attribute, value) in yamlData.items():
        # fetching employees list
        if (attribute == "employees"):
            for employee in value:
                for (attribute, value) in employee.items():
                    if (attribute == "employee"):
                        employeesList.append(value)
    return employeesList


def getRulesList():
    rulesList = []

    for (attribute, value) in yamlData.items():
        # fetching rules list
        if (attribute == "wage_rules"):
            for rule in value:
                for (attribute, value) in rule.items():
                    if (attribute == "rule"):
                            rulesList.append(value)
    return rulesList


def getYaml():
    return yamlName


def getHolidays():
    # getting string representations in string form
    holidayList = []
    for (attribute, value) in yamlData.items():
        if attribute == "bank-holidays":
            for day in value:
                holidayList.append(day)
            break
    return holidayList


def getSender():

    emailSender = None
    for (attribute, value) in yamlData.items():
        # fetching email server username
        if (attribute == "email_sender"):
                emailSender = value
    return emailSender


def getCalendarID():

    calendarID = None
    for (attribute, value) in yamlData.items():
        # fetching calendar ID
        if (attribute == "calendar_id"):
                calendarID = value
    return calendarID


def getEmailRecipients():

    emailRecipientsList=None
    for (attribute, value) in yamlData.items():
        # fetching email recipients list
        if (attribute == "email_recipients"):
            emailRecipientsList = []
            for recipient in value:
                    emailRecipientsList.append(recipient)
    return emailRecipientsList
