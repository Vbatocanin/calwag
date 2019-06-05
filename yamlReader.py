import yaml
import start
import drive

# yaml file updating and loading
drive.updateConfiguration()
yamlName = start.yamlName()
yamlData = yaml.safe_load(open(yamlName))


def getDefault():
    return int(yamlData.get('default_date_day'))


def getEmployeesList():
    empList = []
    employees = yamlData.get('employees')
    for emp in employees:
        empList.append(emp['employee'])

    return empList


def getRulesList():
    rulesList=[]
    rules = yamlData.get('wage_rules')
    for rule in rules:
        rulesList.append(rule['rule'])
    return rulesList


def getYaml():
    return yamlName


def getHolidays():
    # getting string representations in string form
    return yamlData.get('bank-holidays')


def getSender():
    return yamlData.get('email_sender')


def getCalendarID():
    return yamlData.get('calendar_id')


def getEmailRecipients():
    return yamlData.get('email_recipients')
