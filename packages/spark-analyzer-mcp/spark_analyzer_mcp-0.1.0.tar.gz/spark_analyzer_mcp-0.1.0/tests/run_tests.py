#!/usr/bin/env python
import unittest
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import test modules
from test_spark_analyzer import TestSparkAnalyzer
from test_spark_log_parser import TestSparkLogParser


def run_tests():
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    loader = unittest.TestLoader()
    test_suite.addTests(loader.loadTestsFromTestCase(TestSparkLogParser))
    test_suite.addTests(loader.loadTestsFromTestCase(TestSparkAnalyzer))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
