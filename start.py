import GoogleApi
import drive
import sys
import gmail


# ******************************************************
# *********** PUT CONFIGURATION FILE ID HERE ***********
fileID = "18Hzz__cX7K3fv_tpZmJsa620EXYwPj0d"
fileName = sys.argv[1]
# ******************************************************
# ******************************************************


def yamlID():
    return fileID


def yamlName():
    return fileName


def main():
    # print("Number of arguments: ", len(sys.argv))
    # print("The arguments are: ", str(sys.argv))
    # answer = input("Would you like to send the report by email? (Y/N): ")
    if (sys.argv[1].find(".yml") == -1):
        print("Wrong file type: the configuration file must be .yml")
    elif len(sys.argv) > 5:
        print("Wrong number of arguments.\n")
    elif len(sys.argv) == 5:

        if (sys.argv[4] == '-email'):
            drive.main()
            gmail.main(sys.argv[2], sys.argv[3])
        else:
            print("Wrong third argument")
            drive.main()
            GoogleApi.main(sys.argv[2], sys.argv[3])
    # both dates imputed with no email
    elif len(sys.argv) == 4:

        if (sys.argv[3] == '-email'):
            drive.main()
            gmail.main(sys.argv[2], '0')
        else:
            drive.main()
            GoogleApi.main(sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        if(sys.argv[2]=='-email'):
            drive.main()
            gmail.main('0', '0')
        else:
            drive.main()
            GoogleApi.main(sys.argv[2], '0')
    else:
        drive.main()
        GoogleApi.main('0', '0')


if __name__ == '__main__':
    main()
