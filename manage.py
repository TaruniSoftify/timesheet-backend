#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

def check_db_connection():
    """Check database connection and print details"""
    from django.conf import settings
    from django.db import connections
    from django.db.utils import OperationalError

    db_settings = settings.DATABASES['default']

    print("\n========== DATABASE DETAILS ==========")

    print("Database Engine :", db_settings.get("ENGINE"))
    print("Database Name   :", db_settings.get("NAME"))
    print("Database User   :", db_settings.get("USER"))
    print("Database Host   :", db_settings.get("HOST"))
    print("Database Port   :", db_settings.get("PORT"))

    try:
        db_conn = connections['default']
        db_conn.cursor()
        print("Connection Status : [OK] CONNECTED")
    except OperationalError:
        print("Connection Status : [ERROR] NOT CONNECTED")

    print("======================================\n")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'timesheet_backend.settings')

    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()  # initialize Django
        check_db_connection()  # call DB check function

    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()