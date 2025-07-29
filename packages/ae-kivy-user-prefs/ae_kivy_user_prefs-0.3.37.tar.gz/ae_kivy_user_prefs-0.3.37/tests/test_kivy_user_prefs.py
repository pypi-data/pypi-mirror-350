""" ae.kivy_user_prefs unit tests.

This is a minimal unit test module with incomplete coverage because kivy is currently not testable via gitlab CI.
"""
from ae.kivy_user_prefs import __version__


def test_import_basics():  # to pass gitlab-CI
    assert __version__
