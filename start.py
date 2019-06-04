import hoursAndWageCalculator
import drive
import sys
import gmail
# FILE_NAME must be the same as filename on Google Drive
FILE_NAME = "calculator_data.yml"


def yamlName():
    return FILE_NAME


def start():
    if len(sys.argv) > 5:
        print("Wrong number of arguments.\n")
    elif len(sys.argv) == 4:
        if (sys.argv[3] == '-email'):
            drive.updateConfiguration()
            gmail.generateAndSendEmail(sys.argv[1], sys.argv[2])
        else:
            print("Wrong third argument")
            drive.updateConfiguration()
            hoursAndWageCalculator.getHoursAndWages(sys.argv[1], sys.argv[2])
    # both dates imputed with no email
    elif len(sys.argv) == 3:
        if (sys.argv[2] == '-email'):
            drive.updateConfiguration()
            gmail.generateAndSendEmail(sys.argv[1], '0')
        else:
            drive.updateConfiguration()
            hoursAndWageCalculator.getHoursAndWages(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        if(sys.argv[1]=='-email'):
            drive.updateConfiguration()
            gmail.generateAndSendEmail('0', '0')
        else:
            drive.updateConfiguration()
            hoursAndWageCalculator.getHoursAndWages(sys.argv[1], '0')
    else:
        drive.updateConfiguration()
        hoursAndWageCalculator.getHoursAndWages('0', '0')


if __name__ == '__main__':
    start()
