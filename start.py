import hoursAndWageCalculator
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

    msgEmail, msgPrint, startTime, endTime = hoursAndWageCalculator.getHoursAndWages(args.start, args.end)

    print(msgPrint)


if __name__ == '__main__':
    start()
