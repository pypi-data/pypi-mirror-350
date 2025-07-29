import sys
import os
import unittest
#sys.path.append(os.environ['TF_VAR_testlib'])
from aviatrix_testlibs.test_utils.order_tests import load_ordered_tests
import aviatrix_testlibs.test_base.base as test_base
import aviatrix_testlibs.test_utils.test_utils as testut
import pdb

# Disable test sortingftu
load_tests = load_ordered_tests

class Tests(test_base.TestBase):
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass(__name__)
        cls.tu = testut.TestUtils(__name__)
 
    def test_ping(self):
        self.logger.info('basetest_ping')
        pdb.set_trace()
        allow=self.data['ping']
        self.assertTrue(self.tu.local_ping(allow,None))

    def test_trace_route(self):
        expectPaths = str(self.data["spoke_gw"]).split(',')
        self.assertTrue(self.tu.local_simple_trace(self.data['traceroute'],expectPaths),'Test Failed: trace route from 10.11.0.10')

if __name__ == '__main__':
    unittest.main()
