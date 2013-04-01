#!/usr/bin/env python
import os


if __name__ == "__main__":

    if 'dotcloud' in os.environ.get('PYTHONPATH', ''):
        from django.core.management import execute_manager
        from qrround.settings import settings

        execute_manager(settings)

    else:  # local
        from django.core.management import execute_from_command_line
        import sys

        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "qrround.settings.settings")
        execute_from_command_line(sys.argv)
