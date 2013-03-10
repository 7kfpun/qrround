import argparse
import os


def resetdb(reset=True):
    class customAction(argparse.Action):
        def __call__(self, parser, args, values, option_string=None):
           print("Reset DB", reset)
           os.system("rm database.sqlite")
           os.system("python manage.py syncdb --noinput")
           os.system("python manage.py schemamigration qrround --initial")
    return customAction


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--resetDB',
        action=resetdb(),
        help='Reset DB',
    )

    #./manage.py migrate qrround
    
    #os.system("./manage.py dumpdata --indent=2 auth > qrround/fixtures/initial_data.json")
    os.system("python manage.py syncdb --noinput")
    os.system("python manage.py schemamigration qrround --auto")
    os.system("python manage.py migrate qrround")
    
     