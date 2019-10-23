import hoursAndWageCalculator
import gmail
import argparse
import autocred
import os
# FILE_NAME must be the same as filename on Google Drive
FILE_NAME = "calculator_data.yml"


def yamlName():
    return FILE_NAME


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="Start date as dd.mm.yyyy", nargs='?', default=None)
    parser.add_argument("end", help="End date as dd.mm.yyyy", nargs='?', default=None)
    parser.add_argument("-e", "-email", help="Option to send email", action='store_true')
    parser.add_argument("-n", "-new", help="Option to make new credentials", action='store_true')
    args = parser.parse_args()

    if args.n or not(os.path.exists("credentials.json")):
        if os.path.exists("credentials.json"):
            os.remove("credentials.json")
        if os.path.exists("credentials.pickle"):
            os.remove("credentials.pickle")
        autocred.autocred()

    msgEmail, msgPrint = hoursAndWageCalculator.getHoursAndWages(args.start, args.end)

    print(msgPrint)

    if args.e:
        gmail.generateAndSendEmail(msgEmail)


if __name__ == '__main__':
    start()
