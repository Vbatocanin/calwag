import yaml
import yamlordereddictloader
import start


# yamlName = "shatterhand-drive.yml"
yamlName = start.yamlName()


# yamlID = start.yamlID()

def getDefault():
    defaultDay = -1
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching employees list
            if (attribute == "default_date_day"):
                defaultDay = int(value)
    return defaultDay


def getEmployeesList():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching employees list
            if (attribute == "employees"):
                employeesList = []
                for employee in value:
                    for (attribute, value) in employee.items():
                        if (attribute == "employee"):
                            employeesList.append(value)
    return employeesList


def getRulesList():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching rules list
            if (attribute == "wage_rules"):
                rulesList = []
                for rule in value:
                    for (attribute, value) in rule.items():
                        if (attribute == "rule"):
                            rulesList.append(value)
    return rulesList


def getYaml():
    return yamlName


def getHollidays():
    # getting string representations in string form
    hollidayList = []
    with open(yamlName, "r") as f:
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            if attribute == "bank-hollidays":
                for day in value:
                    hollidayList.append(day)
                break
    return hollidayList


def getEmployees():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching employees list
            if (attribute == "employees"):
                employeesList = []
                for employee in value:
                    employeesList.append(employee)
    return employeesList


def getHourlyWage():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching hourly wage
            if (attribute == "hourly_wage"):
                hourlyWage = value
    return hourlyWage


def getHourlyWageAfter5pm():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching hourly wage
            if (attribute == "hourly_wage_after_5pm"):
                hourlyWageAfter5pm = value
    return hourlyWageAfter5pm


def getHourlyWageAfter8pm():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching hourly wage
            if (attribute == "hourly_wage_after_8pm"):
                hourlyWageAfter8pm = value
    return hourlyWageAfter8pm


def getHourlyWageSunday():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching hourly wage
            if (attribute == "hourly_wage_sunday"):
                hourlyWageSunday = value
    return hourlyWageSunday


def getSender():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching email server username
            if (attribute == "email_sender"):
                emailSender = value
    return emailSender


def getPassword():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching email server password
            if (attribute == "email_server_password"):
                emailServerPassword = value
    return emailServerPassword


def getCalendarID():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching calendar ID
            if (attribute == "calendar_id"):
                calendarID = value
    return calendarID


def getEmailRecipients():
    with open(yamlName, "r") as f:
        # yaml file opening and loading
        y = yaml.load(f, Loader=yamlordereddictloader.Loader)
        for (attribute, value) in y.items():
            # fetching email recipients list
            if (attribute == "email_recipients"):
                emailRecipientsList = []
                for recipient in value:
                    emailRecipientsList.append(recipient)
    return emailRecipientsList
