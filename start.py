import hoursAndWageCalculator
import drive
import gmail
import argparse
# FILE_NAME must be the same as filename on Google Drive
FILE_NAME = "calculator_data.yml"


def yamlName():
    return FILE_NAME


def start():
    parser = argparse.ArgumentParser()
    parser.add_argument("start", help="Start date as dd.mm.yyyy", nargs='?', default=None)
    parser.add_argument("end", help="End date as dd.mm.yyyy", nargs='?', default=None)
    parser.add_argument("-e", "-email", help="Option to send email", action='store_true')
    args = parser.parse_args()

    if args.start is not None and args.end is not None and args.start > args.end:
        print("Start date must be before end date")
    elif args.e:
        drive.updateConfiguration()
        gmail.generateAndSendEmail(args.start, args.end)
    else:
        drive.updateConfiguration()
        hoursAndWageCalculator.getHoursAndWages(args.start, args.end)


if __name__ == '__main__':
    start()
