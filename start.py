import GoogleApi
import drive
import sys
import gmail

# ******************************************************
# *********** PUT CONFIGURATION FILE ID HERE ***********
# fileID = "18Hzz__cX7K3fv_tpZmJsa620EXYwPj0d"
fileName = "calculator_data.yml"
# ******************************************************
# ******************************************************


#def yamlID():
#    return fileID


def yamlName():
    return fileName


def main():
    if len(sys.argv) > 5:
        print("Wrong number of arguments.\n")
    elif len(sys.argv) == 4:
        if (sys.argv[3] == '-email'):
            drive.main()
            gmail.main(sys.argv[1], sys.argv[2])
        else:
            print("Wrong third argument")
            drive.main()
            GoogleApi.main(sys.argv[1], sys.argv[2])
    # both dates imputed with no email
    elif len(sys.argv) == 3:
        if (sys.argv[2] == '-email'):
            drive.main()
            gmail.main(sys.argv[1], '0')
        else:
            drive.main()
            GoogleApi.main(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        if(sys.argv[1]=='-email'):
            drive.main()
            gmail.main('0', '0')
        else:
            drive.main()
            GoogleApi.main(sys.argv[1], '0')
    else:
        drive.main()
        GoogleApi.main('0', '0')


if __name__ == '__main__':
    main()
