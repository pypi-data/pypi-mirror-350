import unittest
from src.DLMSCommunicationProfile.communication_profile import Parameters


class TestType(unittest.TestCase):

    def test_init(self) -> None:
        par = Parameters
        print(par)
