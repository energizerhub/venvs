from StringIO import StringIO
from functools import partial
from unittest import TestCase
import os

from mkenv import find
from mkenv.common import VIRTUALENVS_ROOT


class TestFind(TestCase):
    def run_cli(self, argv=(), exit_status=os.EX_OK):
        stdin, stdout, stderr = StringIO(), StringIO(), StringIO()
        find.run(
            argv=argv,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            exit=partial(self.assertEqual, 0),
        )
        return stdin.getvalue(), stdout.getvalue(), stderr.getvalue()

    def test_find_without_args_finds_the_virtualenv_root(self):
        stdin, stdout, stderr = self.run_cli()
        self.assertEqual(
            (stdin, stdout, stderr),
            ("", VIRTUALENVS_ROOT + "\n", ""),
        )

    def test_find_d_finds_envs_by_directory(self):
        this_dir = os.path.basename(__file__)
        stdin, stdout, stderr = self.run_cli(["-d", this_dir])
        self.assertEqual(
            (stdin, stdout, stderr),
            ("", find.env_for_directory(this_dir) + "\n", ""),
        )

    def test_find_d_defaults_to_cwd(self):
        this_dir = os.getcwd()
        stdin, stdout, stderr = self.run_cli(["-d"])
        self.assertEqual(
            (stdin, stdout, stderr),
            ("", find.env_for_directory(this_dir) + "\n", ""),
        )

    def test_find_n_finds_envs_by_name(self):
        stdin, stdout, stderr = self.run_cli(["-n", "bla"])
        self.assertEqual(
            (stdin, stdout, stderr),
            ("", find.env_for_name("bla") + "\n", ""),
        )
