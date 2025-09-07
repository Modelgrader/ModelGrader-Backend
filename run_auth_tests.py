#!/usr/bin/env python
"""
Test runner script for Auth Service unit tests
Run this script to execute all auth service tests

Usage:
    python run_auth_tests.py
    
    Or with Django's test runner:
    python manage.py test api.services.auth.test_auth_service
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Backend.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Run only the auth service tests
    failures = test_runner.run_tests(["api.services.auth.test_auth_service"])
    
    if failures:
        sys.exit(bool(failures))
