import unittest
from DLMSCommunicationProfile.osi import OSI


class Test(unittest.TestCase):
    def test_OSI(self) -> None:

        level = OSI.PHYSICAL | OSI.DATA_LINK
        print(level)
        print(OSI.PHYSICAL not in level)
        level |= OSI.APPLICATION
        print(level)
        level -= OSI.APPLICATION
        print(level)
