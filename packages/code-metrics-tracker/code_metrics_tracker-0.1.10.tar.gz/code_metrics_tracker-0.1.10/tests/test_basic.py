#!/usr/bin/env python3
"""
Basic test script for the Code Metrics Tracker.
This script tests the main functionality of the codeqa tool by running it on a test directory.
"""

import os
import shutil
import subprocess
import tempfile
import json
from pathlib import Path


class TestCodeMetricsTracker:
    """Tests for Code Metrics Tracker."""

    def setup_method(self):
        """Set up a temporary test directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_dir = os.getcwd()
        
        # Create a sample Python file to analyze
        sample_code_dir = os.path.join(self.temp_dir, "src")
        os.makedirs(sample_code_dir)
        
        # Create a sample Python file with some code
        with open(os.path.join(sample_code_dir, "sample.py"), "w") as f:
            f.write("""#!/usr/bin/env python3
'''Sample module for testing code metrics.'''

def function_a():
    '''A simple function.'''
    x = 10
    y = 20
    return x + y

def function_b(a, b, c):
    '''A function with high cyclomatic complexity.'''
    if a > b:
        if b > c:
            return a
        elif a > c:
            return b
        else:
            return c
    elif b > a:
        if a > c:
            return b
        elif b > c:
            return a
        else:
            return c
    else:
        return a
""")
        
        # Change to the temporary directory
        os.chdir(self.temp_dir)
        
        # Create a configuration file
        with open("codeqa.json", "w") as f:
            json.dump({
                "include_paths": ["src"],
                "exclude_patterns": ["venv", "site-packages", "__pycache__", ".pyc"]
            }, f)

    def teardown_method(self):
        """Clean up after the test."""
        os.chdir(self.original_dir)
        shutil.rmtree(self.temp_dir)

    def run_command(self, command):
        """Run a command and return stdout, stderr, and return code."""
        process = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        return process.stdout, process.stderr, process.returncode

    def test_init(self):
        """Test the init command."""
        # Remove the config file we created in setup_method
        os.remove("codeqa.json")
        
        stdout, stderr, returncode = self.run_command("codeqa init")
        
        assert returncode == 0
        assert "Project initialized successfully" in stdout
        assert os.path.exists("codeqa.json")
        assert os.path.exists("CODE_METRICS.md")
        assert os.path.exists("generated/metrics")

    def test_snapshot(self):
        """Test the snapshot command."""
        # First make sure we have initialized properly
        self.run_command("codeqa init")
        
        # Now create a snapshot
        stdout, stderr, returncode = self.run_command("codeqa snapshot")
        
        # Print out stderr to help diagnose issues
        if returncode != 0:
            print(f"Error running snapshot: {stderr}")
        
        assert returncode == 0
        assert "Snapshot added to CODE_METRICS.md" in stdout
        assert "Detailed metrics saved to" in stdout
        assert os.path.exists("CODE_METRICS.md")
        
        # Check if metrics directory contains a JSON file
        metrics_files = list(Path("generated/metrics").glob("metrics_*.json"))
        assert len(metrics_files) > 0
        
        # Verify the content of the CODE_METRICS.md file
        with open("CODE_METRICS.md", "r") as f:
            content = f.read()
            assert "Lines of Code" in content
            assert "Linting Issues" in content
            assert "Cyclomatic Complexity" in content

    def test_list(self):
        """Test the list command."""
        # First initialize and create a snapshot
        self.run_command("codeqa init")
        self.run_command("codeqa snapshot")
        
        # Now list the snapshots
        stdout, stderr, returncode = self.run_command("codeqa list")
        
        if returncode != 0:
            print(f"Error running list: {stderr}")
            
        assert returncode == 0
        assert "Available snapshots:" in stdout
        assert "metrics_" in stdout

    def test_report(self):
        """Test the report command."""
        # First initialize and create a snapshot
        self.run_command("codeqa init")
        self.run_command("codeqa snapshot")
        
        # Now generate a report using the snapshot index
        stdout, stderr, returncode = self.run_command("codeqa report --snapshot 1")
        
        if returncode != 0:
            print(f"Error running report: {stderr}")
            
        assert returncode == 0
        assert "Code Quality Report" in stdout
        assert "Summary" in stdout

    def test_compare(self):
        """Test the compare command with two snapshots."""
        # First initialize
        self.run_command("codeqa init")
        
        # Create first snapshot
        self.run_command("codeqa snapshot")
        
        # Modify the sample.py file to change metrics
        with open("src/sample.py", "a") as f:
            f.write("""
def new_function():
    '''A new function for the second snapshot.'''
    return 42
""")
        
        # Create second snapshot
        self.run_command("codeqa snapshot")
        
        # Compare the snapshots
        stdout, stderr, returncode = self.run_command("codeqa compare --first 2 --second 1")
        
        if returncode != 0:
            print(f"Error running compare: {stderr}")
        
        assert returncode == 0
        assert "Comparison" in stdout
        assert "Lines of Code" in stdout
        assert "Change" in stdout


def check_cloc_installed():
    """Check if cloc is installed and available."""
    try:
        process = subprocess.run("which cloc", shell=True, capture_output=True, text=True)
        return process.returncode == 0
    except Exception:
        return False

def run_tests():
    """Run all tests."""
    print("Running Code Metrics Tracker tests...")
    
    # Check if cloc is installed
    if not check_cloc_installed():
        print("WARNING: 'cloc' is not installed. Please install cloc before running tests.")
        print("On macOS: brew install cloc")
        print("On Ubuntu/Debian: sudo apt-get install cloc")
        return
    
    test = TestCodeMetricsTracker()
    
    try:
        test.setup_method()
        print("\nTesting 'init' command:")
        test.test_init()
        print("✓ 'init' command test passed")
        
        test.setup_method()  # Reset for the next test
        print("\nTesting 'snapshot' command:")
        test.test_snapshot()
        print("✓ 'snapshot' command test passed")
        
        test.setup_method()
        print("\nTesting 'list' command:")
        test.test_list()
        print("✓ 'list' command test passed")
        
        test.setup_method()
        print("\nTesting 'report' command:")
        test.test_report()
        print("✓ 'report' command test passed")
        
        test.setup_method()
        print("\nTesting 'compare' command:")
        test.test_compare()
        print("✓ 'compare' command test passed")
        
        print("\nAll tests passed successfully!")
    
    except Exception as e:
        print(f"Test failed: {str(e)}")
        raise
    finally:
        test.teardown_method()


if __name__ == "__main__":
    run_tests()