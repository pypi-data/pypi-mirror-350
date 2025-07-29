import sys
import os
import unittest
import json
#sys.path.append(os.environ['TF_VAR_testlib'])
from aviatrix_testlibs.test_utils.order_tests import load_ordered_tests
import aviatrix_testlibs.test_base.base as test_base
import aviatrix_testlibs.test_utils.test_utils as testut
from parameterized import parameterized, param,  parameterized_class

# Disable test sortingftu
load_tests = load_ordered_tests

def load_test_cases():
    """
    sample data:
    [
        {
            "gw_name": "spoke-gw",
            "gw_private_ip": "10.1.3.73",
            "gw_subnet_id": "subnet-0c9c8e12ffab484cb",
            "gw_subnet_cidr": "10.1.3.0/24",
            "private_subnet_id": "subnet-04be07cdc575a8bbf",
            "private_subnet_cidr": "10.1.4.0/24",
            "private_subnet_gw_ip": "10.1.4.1",
            "ec2_ip": "44.195.178.103",
            "ec2_2nd_private_ip": "10.1.4.240"
        },
        {
            "gw_name": "spoke-gw-hagw",
            "gw_private_ip": "10.1.1.34",
            "gw_subnet_id": "subnet-0156c3d66f079b434",
            "gw_subnet_cidr": "10.1.1.0/24",
            "private_subnet_id": "subnet-0ae4c804c32b25f16",
            "private_subnet_cidr": "10.1.2.0/24",
            "private_subnet_gw_ip": "10.1.2.1",
            "ec2_ip": "54.165.208.169",
            "ec2_2nd_private_ip": "10.1.2.51"
        }
    ]
    """
    f = open("config.json")
    data = json.load(f)
    return data

@parameterized_class(load_test_cases())
class Tests(test_base.TestBase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass(__name__)
        cls.logger.info("")
        cls.logger.info("---------------------------------------------")
        cls.logger.info(f"Test {cls.gw_name}")
        cls.logger.info("---------------------------------------------")
        cls.logger.info("")
        cls.logger.info(f'Run tests from {cls.private_subnet_id} ({cls.private_subnet_cidr}) to {cls.gw_name} ({cls.gw_private_ip})')
        cls.tu.setupRoute(cls.ec2_ip,'ec2-user',cls.private_subnet_gw_ip,cls.ec2_2nd_private_ip)

    def test_ping(self):
        allow="8.8.8.8"
        self.assertTrue(self.tu.ping(self.ec2_ip,self.ec2_2nd_private_ip,allow,None,'ec2-user'))

    def test_traceroute(self):
        expectPaths = str(self.gw_private_ip).split(',')
        self.assertTrue(self.tu.simple_trace(self.ec2_ip,self.ec2_2nd_private_ip,"8.8.8.8",expectPaths,'ec2-user'),f'Test Failed: trace route from {self.ec2_2nd_private_ip}')

if __name__ == '__main__':
    unittest.main()
