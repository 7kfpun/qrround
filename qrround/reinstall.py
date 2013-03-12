import argparse
from subprocess import Popen


def parse_args():
    parser = argparse.ArgumentParser(description='Reinstall project')
    parser.add_argument('--resetdb', action='store_true',
                        help='Remove and create db again')
    parser.add_argument('--settings', help='Settings file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    if args.settings is not None:
        settings_arg = "--settings=%s" % args.settings
    else:
        settings_arg = ""

    run = lambda cmd: Popen(cmd, shell=True).communicate()
    django_run = lambda cmd: run("python manage.py %s %s" %
                                 (cmd, settings_arg))
    if args.resetdb:
        # remove database
        django_run("reset_db --router=default --noinput")
        django_run("sqlcreate --router=default")

    django_run("syncdb --noinput")
    django_run("migrate")


if __name__ == "__main__":
    main()


#def resetdb(reset=True):
#    class customAction(argparse.Action):
#        def __call__(self, parser, args, values, option_string=None):
#            print("Reset DB", reset)
#            os.system("rm database.sqlite")
#            # os.system("python manage.py schemamigration qrround --initial")
#            # os.system("python manage.py migrate qrround")
#            os.system("python manage.py syncdb --noinput")
#    return customAction
#
#
#if __name__ == '__main__':
#    parser = argparse.ArgumentParser()
#    parser.add_argument(
#        '--resetDB',
#        action=resetdb(),
#        help='Reset DB',
#    )
#
#    #./manage.py migrate qrround
#
#    #os.system("./manage.py dumpdata --indent=2 auth > qrround/fixtures/initial_data.json")  # noqa
#    os.system("python manage.py syncdb --noinput")
#    os.system("python manage.py schemamigration qrround --auto")
#    os.system("python manage.py migrate qrround")
