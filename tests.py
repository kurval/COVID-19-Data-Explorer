import unittest
import sys
from selenium import webdriver
from test_cases.test_compare_countries import CompareCountries
from test_cases.test_most_cases import WorstHitCountries
from test_cases.test_continent_cases import ContinentCases
from test_cases.test_world_cases import WorldCases
from test_cases.common import CommonMethods

if __name__ == "__main__":
    if len(sys.argv) > 1:
        CommonMethods.BROWSER = sys.argv.pop()
    unittest.main()