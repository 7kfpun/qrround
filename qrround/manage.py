#!/usr/bin/env python
import os


if __name__ == "__main__":

    if os.environ.get('PYTHONPATH', None) == '/home/dotcloud':
        from django.core.management import execute_manager
        from qrround.settings import dotcloud

        execute_manager(dotcloud)

    else:
        from django.core.management import execute_from_command_line
        import sys

        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "qrround.settings.settings")
        execute_from_command_line(sys.argv)
