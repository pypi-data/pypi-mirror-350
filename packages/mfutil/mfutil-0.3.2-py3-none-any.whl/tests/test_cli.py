import sys
from unittest import TestCase, skipIf
from mfutil.cli import echo_ok, echo_nok, echo_warning, echo_bold, \
    echo_running, echo_clean


class TestCaseCli(TestCase):

    @skipIf(sys.version_info < (3, 6, 0), "python version")
    def test_echo_ok(self):
        echo_ok("foo ok")

    @skipIf(sys.version_info < (3, 6, 0), "python version")
    def test_echo_nok(self):
        echo_nok("foo nok")

    @skipIf(sys.version_info < (3, 6, 0), "python version")
    def test_echo_warning(self):
        echo_warning("foo warning")

    @skipIf(sys.version_info < (3, 6, 0), "python version")
    def test_echo_bold(self):
        echo_bold("foo bold")

    @skipIf(sys.version_info < (3, 6, 0), "python version")
    def test_echo_running_clean(self):
        echo_running()
        echo_clean()
