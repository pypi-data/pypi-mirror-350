#!/usr/bin/env python3
"""
Tests for the parsing mechanisms in the metrics module.

This specifically tests the parsing of output from the tools:
- radon (for complexity metrics)
- ruff (for linting)
- cloc (for code statistics)
"""

import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Import the module to test
from codeqa import metrics


class TestRadonParsing(unittest.TestCase):
    """Test case for Radon output parsing."""

    def setUp(self):
        """Set up test case with sample Radon outputs."""
        # Sample text output from radon cc
        self.radon_text_output = """test_file.py
    F 3:0 complex_function - C (16)
    C 19:0 TestClass - A (3)
    M 23:4 TestClass.complex_method - B (8)
    F 16:0 simple_function - A (1)
    M 20:4 TestClass.__init__ - A (1)"""

        # Sample JSON output from radon cc --json
        self.radon_json_output = {
            "test_file.py": [
                {
                    "type": "function",
                    "rank": "C",
                    "complexity": 16,
                    "endline": 14,
                    "col_offset": 0,
                    "lineno": 3,
                    "name": "complex_function",
                    "closures": []
                },
                {
                    "type": "class",
                    "rank": "A",
                    "complexity": 3,
                    "endline": 30,
                    "col_offset": 0,
                    "lineno": 19,
                    "name": "TestClass",
                    "methods": [
                        {
                            "type": "method",
                            "rank": "A",
                            "complexity": 1,
                            "endline": 21,
                            "col_offset": 4,
                            "lineno": 20,
                            "name": "__init__",
                            "classname": "TestClass",
                            "closures": []
                        },
                        {
                            "type": "method",
                            "rank": "B",
                            "complexity": 8,
                            "endline": 30,
                            "col_offset": 4,
                            "lineno": 23,
                            "name": "complex_method",
                            "classname": "TestClass",
                            "closures": []
                        }
                    ]
                },
                {
                    "type": "method",
                    "rank": "B",
                    "complexity": 8,
                    "endline": 30,
                    "col_offset": 4,
                    "lineno": 23,
                    "name": "complex_method",
                    "classname": "TestClass",
                    "closures": []
                },
                {
                    "type": "function",
                    "rank": "A",
                    "complexity": 1,
                    "endline": 17,
                    "col_offset": 0,
                    "lineno": 16,
                    "name": "simple_function",
                    "closures": []
                },
                {
                    "type": "method",
                    "rank": "A",
                    "complexity": 1,
                    "endline": 21,
                    "col_offset": 4,
                    "lineno": 20,
                    "name": "__init__",
                    "classname": "TestClass",
                    "closures": []
                }
            ]
        }
        
        # Sample JSON output with string entries (the issue we fixed in v0.1.5)
        self.radon_json_with_strings = {
            "test_file.py": [
                {
                    "type": "function",
                    "rank": "C",
                    "complexity": 16,
                    "name": "complex_function"
                },
                "this is a string entry that should be handled",  # This caused the AttributeError
                {
                    "type": "function",
                    "rank": "A",
                    "complexity": 1,
                    "name": "simple_function"
                }
            ]
        }

        # Config for testing
        self.test_config = {
            "include_paths": ["test"],
            "exclude_patterns": ["__pycache__"]
        }

    @patch('json.loads')
    @patch('codeqa.metrics.is_project_file', return_value=True)
    def test_radon_cc_json_parsing(self, mock_is_project_file, mock_json_loads):
        """Test that radon CC JSON output is correctly parsed."""
        # Set up the mock to return our sample data
        mock_json_loads.return_value = self.radon_json_output
        
        # Call the function under test
        from codeqa.metrics_parsing import parse_radon_cc_json
        radon_cc_output = json.dumps(self.radon_json_output)
        result = parse_radon_cc_json(radon_cc_output, self.test_config)
        
        # Assert the structure is correct
        self.assertIn('grade_counts', result)
        self.assertIn('functions', result)
        self.assertIn('files', result)
        
        # Check functions - we should have all 5 functions from the test data
        functions = result['functions']
        self.assertEqual(len(functions), 5, "Should have 5 functions/methods")
        
        # Verify we can find the complex function with highest complexity
        complex_function = None
        for func in functions:
            if func['function'] == 'complex_function':
                complex_function = func
                break
                
        self.assertIsNotNone(complex_function, "Should find complex_function")
        self.assertEqual(complex_function['complexity'], 16)
        self.assertEqual(complex_function['grade'], 'C')
        
        # Verify the functions are sorted by complexity (highest first)
        self.assertTrue(functions[0]['complexity'] >= functions[1]['complexity'],
                      "Functions should be sorted by complexity (highest first)")
                      
    @patch('json.loads')
    @patch('codeqa.metrics.is_project_file', return_value=True)
    def test_radon_cc_json_parsing_with_string_entries(self, mock_is_project_file, mock_json_loads):
        """Test that radon CC JSON output with string entries is handled correctly (fix for v0.1.5)."""
        # Set up the mock to return our sample data with string entries
        mock_json_loads.return_value = self.radon_json_with_strings
        
        # Call the function under test
        from codeqa.metrics_parsing import parse_radon_cc_json
        radon_cc_output = json.dumps(self.radon_json_with_strings)
        
        # This should not raise an AttributeError anymore
        result = parse_radon_cc_json(radon_cc_output, self.test_config)
        
        # Assert the structure is correct
        self.assertIn('grade_counts', result)
        self.assertIn('functions', result)
        self.assertIn('files', result)
        
        # Check functions - we should have 3 entries (2 functions + 1 string that gets default values)
        functions = result['functions']
        self.assertEqual(len(functions), 3, "Should have 3 entries including the string one")
        
        # Verify the string entry was handled with default values
        string_entry = None
        for func in functions:
            if func['function'] == 'Unknown':
                string_entry = func
                break
                
        self.assertIsNotNone(string_entry, "Should have an 'Unknown' function from the string entry")
        self.assertEqual(string_entry['complexity'], 0, "String entry should have default complexity of 0")
        self.assertEqual(string_entry['grade'], 'X', "String entry should have default grade of 'X'")


class TestRuffParsing(unittest.TestCase):
    """Test case for Ruff output parsing."""

    def setUp(self):
        """Set up test case with sample Ruff outputs."""
        # Sample text output from ruff check
        self.ruff_text_output = """test_file.py:1:8: F401 `os` imported but unused
test_file.py:1:12: F401 `sys` imported but unused
test_file.py:1:17: F401 `math` imported but unused
test_file.py:1:1: E401 Multiple imports on one line"""

        # Sample JSON output from ruff check --output-format json
        self.ruff_json_output = [
            {
                "cell": None,
                "code": "F401",
                "filename": "test_file.py",
                "location": {"column": 8, "row": 1},
                "message": "`os` imported but unused"
            },
            {
                "cell": None,
                "code": "F401",
                "filename": "test_file.py",
                "location": {"column": 12, "row": 1},
                "message": "`sys` imported but unused"
            },
            {
                "cell": None,
                "code": "F401",
                "filename": "test_file.py",
                "location": {"column": 17, "row": 1},
                "message": "`math` imported but unused"
            },
            {
                "cell": None,
                "code": "E401",
                "filename": "test_file.py",
                "location": {"column": 1, "row": 1},
                "message": "Multiple imports on one line"
            }
        ]

        # Config for testing
        self.test_config = {
            "include_paths": ["test"],
            "exclude_patterns": ["__pycache__"]
        }

    @patch('json.loads')
    @patch('codeqa.metrics.is_project_file', return_value=True)
    def test_ruff_json_parsing(self, mock_is_project_file, mock_json_loads):
        """Test that ruff JSON output is correctly parsed."""
        # Set up the mock to return our sample data
        mock_json_loads.return_value = self.ruff_json_output
        
        # Call the function under test
        from codeqa.metrics_parsing import parse_ruff_json
        ruff_output = json.dumps(self.ruff_json_output)
        result = parse_ruff_json(ruff_output, self.test_config)
        
        # Assert we got the expected issues
        self.assertEqual(len(result), 4, "Should have 4 linting issues")
        
        # Check structure of first issue
        issue = result[0]
        self.assertEqual(issue['file'], 'test_file.py')
        self.assertEqual(issue['line'], 1)
        self.assertEqual(issue['column'], 8)
        self.assertEqual(issue['code'], 'F401')
        self.assertEqual(issue['message'], "`os` imported but unused")


class TestClocParsing(unittest.TestCase):
    """Test case for cloc output parsing."""

    def setUp(self):
        """Set up test case with sample cloc outputs."""
        # Sample text output from cloc
        self.cloc_text_output = """github.com/AlDanial/cloc v 2.04  T=0.01 s (76.0 files/s, 2279.0 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
Python                           1              4              0             26
-------------------------------------------------------------------------------
SUM:                             1              4              0             26
-------------------------------------------------------------------------------"""

        # Sample JSON output from cloc --json
        self.cloc_json_output = {
            "header": {
                "cloc_url": "github.com/AlDanial/cloc",
                "cloc_version": "2.04",
                "elapsed_seconds": 0.0119068622589111,
                "n_files": 1,
                "n_lines": 30,
                "files_per_second": 83.9851825153681,
                "lines_per_second": 2519.55547546104
            },
            "Python": {
                "nFiles": 1,
                "blank": 4,
                "comment": 0,
                "code": 26
            },
            "SUM": {
                "blank": 4,
                "comment": 0,
                "code": 26,
                "nFiles": 1
            }
        }

        # Config for testing
        self.test_config = {
            "include_paths": ["test"],
            "exclude_patterns": ["__pycache__"]
        }

    @patch('json.loads')
    def test_cloc_json_parsing(self, mock_json_loads):
        """Test that cloc JSON output is correctly parsed."""
        # Set up the mock to return our sample data
        mock_json_loads.return_value = self.cloc_json_output
        
        # Call the function under test
        from codeqa.metrics_parsing import parse_cloc_json
        cloc_output = json.dumps(self.cloc_json_output)
        result = parse_cloc_json(cloc_output)
        
        # Assert the structure is correct
        self.assertIn('total', result)
        self.assertIn('by_language', result)
        
        # Check the total stats
        self.assertEqual(result['total']['files'], 1)
        self.assertEqual(result['total']['blank'], 4)
        self.assertEqual(result['total']['comment'], 0)
        self.assertEqual(result['total']['code'], 26)
        
        # Check language breakdown
        self.assertIn('Python', result['by_language'])
        self.assertEqual(result['by_language']['Python']['files'], 1)
        self.assertEqual(result['by_language']['Python']['code'], 26)


if __name__ == '__main__':
    unittest.main()