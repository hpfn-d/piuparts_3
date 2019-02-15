from unittest import TestCase

from mox3 import mox

# that way for mox
from piupartslib import dwke
from piupartslib.dwke import (
    build_kprs, get_where, get_pkg, kprs_string, make_kprs
)


class DwkeTests(TestCase):
    """ Tests for module dwke. """

    def setUp(self):
        self.mox = mox.Mox()

    def tearDown(self):
        self.mox.UnsetStubs()

    def test_get_where_pass(self):
        """
        get_where must return a str. The name
        of the subdiretory where the file is in
        """
        self.assertEqual('anywhere', get_where('/etc/anywhere/logfile.log'))
        # return logpath.split('/')[-2]

    def test_get_pkg_pass(self):
        """
        get_pkg must return the name of the pkg
        whitout the _x.x-1 part
        """
        self.assertEqual('btcheck', get_pkg('btcheck_2.1-4_amd64.deb'))

    def test_prblname_kprs_string(self):
        """
        Problem.has_problem returns True
        a list exists and join() is called
        """
        problem = self.mox.CreateMockAnything()
        problem.name = 'test_name'
        problem.has_problem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(True)
        self.mox.ReplayAll()
        problem_list = [problem]
        kprs = kprs_string('/etc/anywhere/logfile.log', 'pkg_spec', problem_list, 'Ignore')
        self.assertEqual('anywhere/pkg_spec.log test_name\n', kprs)
        self.mox.VerifyAll()

    def test_unclassified_kprs_string(self):
        """
        Problem.has_problem returns False
        kprs is empty, where is not 'pass'
        """
        problem = self.mox.CreateMockAnything()
        problem.name = 'test_name'
        problem.has_problem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        self.mox.ReplayAll()
        problem_list = [problem]
        kprs = kprs_string('/etc/anywhere/logfile.log', 'pkg_spec', problem_list, '')
        self.assertEqual('anywhere/pkg_spec.log unclassified_failures.conf\n', kprs)
        self.mox.VerifyAll()

    def test_empty_kprs_string(self):
        """
        Problem.has_problem returns False
        kprs is empty, where is 'pass'
        """
        problem = self.mox.CreateMockAnything()
        problem.has_problem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        self.mox.ReplayAll()
        problem_list = [problem]
        kprs = kprs_string('/etc/pass/logfile.log', 'pkg_spec', problem_list, '')
        self.assertEqual('', kprs)
        self.mox.VerifyAll()

    # def test_build_kprs_without_logbody(self):
    #     """
    #     read_path return None - logbody is None
    #     kprs stuff are not called
    #     """
    #     self.mox.StubOutWithMock(dwke, 'read_logpath')
    #     dwke.read_logpath(mox.IgnoreArg())
    #     self.mox.ReplayAll()
    #     needs_kpr = ['btcheck']
    #     logdict = dict(btcheck='/var/log/btcheck.log')
    #     self.assertIsNone(build_kprs(needs_kpr, logdict, 'Raises'))
    #     self.mox.VerifyAll()

    def test_build_kprs_with_logbody(self):
        """
        logbody exists
        kprs stuff are called
        Problem.has_problem False simplify test
        """
        self.mox.StubOutWithMock(dwke, 'read_logpath')
        dwke.read_logpath(mox.IgnoreArg()).AndReturn('Exists')
        self.mox.StubOutWithMock(dwke, 'write_kprs')
        dwke.write_kprs(mox.IgnoreArg(), mox.IgnoreArg())
        self.mox.StubOutWithMock(dwke, 'Problem')
        dwke.Problem.has_problem(mox.IgnoreArg(), mox.IgnoreArg()).AndReturn(False)
        self.mox.ReplayAll()
        needs_kpr = ['btcheck']
        logdict = dict(btcheck='/var/log/btcheck.log')
        build_kprs(needs_kpr, logdict, [dwke.Problem])
        self.mox.VerifyAll()

    def test_make_kprs_return_1(self):
        self.mox.StubOutWithMock(dwke, 'build_kprs')
        dwke.build_kprs(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg())
        self.mox.ReplayAll()
        logdict = dict(btcheck='/var/log/btcheck.log')
        kprdict = dict()
        self.assertEqual(1, make_kprs(logdict, kprdict, 'no_matter'))
        self.mox.VerifyAll()
