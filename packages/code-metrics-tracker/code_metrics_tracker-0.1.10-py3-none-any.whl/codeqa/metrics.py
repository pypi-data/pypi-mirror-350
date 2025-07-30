#!/usr/bin/env python3
"""
Code quality metrics functionality for CodeQA.

This module provides tools to track and analyze code quality metrics using Ruff and Radon.
"""

import datetime
import glob
import json
import os
import re
import shutil
import subprocess
from collections import defaultdict
import pkg_resources


# Constants
METRICS_FILE = "CODE_METRICS.md"
METRICS_DIR = "generated/metrics"
CONFIG_FILE = "codeqa.json"

# Default configuration if no config file is found
DEFAULT_CONFIG = {
    "include_paths": ["src", "tests"],
    "exclude_patterns": ["migrations", ".coverage", "*.db", "*.log"]
}


def init_project(config_path=None):
    """
    Initialize a project with code quality tracking.
    
    Args:
        config_path: Optional path to a custom config file
    """
    # Create config file
    if not os.path.exists(CONFIG_FILE):
        config = DEFAULT_CONFIG
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Could not parse config file {config_path}. Using default config.")
                
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        print(f"Created configuration file: {CONFIG_FILE}")
    else:
        print(f"Configuration file already exists: {CONFIG_FILE}")
    
    # Create metrics directory
    os.makedirs(METRICS_DIR, exist_ok=True)
    print(f"Created metrics directory: {METRICS_DIR}")
    
    # Create CODE_METRICS.md if it doesn't exist
    if not os.path.exists(METRICS_FILE):
        # Get template from package
        template_path = pkg_resources.resource_filename('codeqa', 'templates/CODE_METRICS.md.template')
        
        if os.path.exists(template_path):
            shutil.copy(template_path, METRICS_FILE)
        else:
            # Fallback if template isn't found
            with open(METRICS_FILE, 'w') as f:
                f.write("""# Code Quality Metrics

This file tracks code quality metrics over time to help monitor and improve our codebase.

## Metrics Definitions

### Ruff Metrics

- **Issues Count**: Total number of linting issues detected by Ruff
- **Issues by Type**: Distribution of error types (unused imports, undefined names, etc.)

### Radon Complexity Metrics (CC)

- **A**: CC score 1-5 (low complexity)
- **B**: CC score 6-10 (moderate complexity)
- **C**: CC score 11-20 (high complexity)
- **D**: CC score 21-30 (very high complexity)
- **E**: CC score 31-40 (extremely high complexity)
- **F**: CC score 41+ (alarming complexity)

### Radon Maintainability Metrics (MI)

- **A**: MI score 20-100 (high maintainability)
- **B**: MI score 10-19 (medium maintainability)
- **C**: MI score 0-9 (low maintainability)

## Historical Snapshots

""")
        print(f"Created metrics file: {METRICS_FILE}")
    else:
        print(f"Metrics file already exists: {METRICS_FILE}")
    
    print("\nProject initialized successfully!")
    print("Run 'codeqa snapshot' to create your first code quality snapshot.")


def load_config(config_path=None):
    """
    Load configuration from the config file.
    
    Args:
        config_path: Optional path to a custom config file
    """
    path_to_check = config_path if config_path else CONFIG_FILE
    
    try:
        with open(path_to_check, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Warning: Could not load config file ({e}). Using default configuration.")
        return DEFAULT_CONFIG


def is_project_file(filepath, config):
    """
    Check if a file path belongs to the project based on configuration.
    
    Args:
        filepath: Path to the file
        config: Configuration dictionary
    """
    # Get relative path from project root
    root_dir = os.getcwd()
    if filepath.startswith(root_dir):
        rel_path = os.path.relpath(filepath, root_dir)
    else:
        rel_path = filepath
    
    # Check if the path matches any include pattern
    included = False
    for include_path in config["include_paths"]:
        if rel_path == include_path or rel_path.startswith(f"{include_path}/"):
            included = True
            break
    
    if not included:
        return False
    
    # Check if the path matches any exclude pattern
    for exclude_pattern in config["exclude_patterns"]:
        if exclude_pattern in rel_path:
            return False
    
    return True


def build_cloc_exclude_args(config):
    """
    Build exclude arguments for cloc based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        String with exclude arguments for cloc
    """
    exclude_dirs = []
    exclude_exts = []
    
    for pattern in config.get("exclude_patterns", []):
        if pattern.startswith("."):
            # File extension (e.g., .pyc)
            exclude_exts.append(pattern[1:])
        elif pattern.startswith("*."):
            # Wildcard file extension (e.g., *.db, *.log)
            exclude_exts.append(pattern[2:])
        elif "/" not in pattern and "." not in pattern:
            # Simple directory name
            exclude_dirs.append(pattern)
        elif "/" in pattern and "*" not in pattern:
            # Directory path without wildcards (e.g., src/temp, config/test)
            exclude_dirs.append(pattern)
        # Skip patterns with wildcards in paths (e.g., config/*.yaml) as cloc doesn't support them
    
    args = ""
    if exclude_dirs:
        args += f" --exclude-dir={','.join(exclude_dirs)}"
    if exclude_exts:
        args += f" --exclude-ext={','.join(exclude_exts)}"
    
    return args


def build_ruff_exclude_args(config):
    """
    Build exclude arguments for Ruff based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        String with exclude arguments for Ruff
    """
    exclude_patterns = []
    
    for pattern in config.get("exclude_patterns", []):
        if pattern.startswith("."):
            # File extension (e.g., .pyc) -> convert to glob
            exclude_patterns.append(f"*{pattern}")
        elif "/" not in pattern and "." not in pattern:
            # Simple directory name -> match anywhere
            exclude_patterns.append(f"**/{pattern}/**")
        else:
            # Already a pattern
            exclude_patterns.append(pattern)
    
    args = ""
    for pattern in exclude_patterns:
        args += f" --exclude '{pattern}'"
    
    return args


def build_radon_exclude_args(config):
    """
    Build exclude arguments for Radon based on configuration.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        String with exclude arguments for Radon
    """
    exclude_patterns = []
    
    for pattern in config.get("exclude_patterns", []):
        if pattern.startswith("."):
            # File extension (e.g., .pyc) -> convert to glob
            exclude_patterns.append(f"*{pattern}")
        elif "/" not in pattern and "." not in pattern:
            # Simple directory name -> match anywhere
            exclude_patterns.append(f"*/{pattern}/*")
        else:
            # Already a pattern
            exclude_patterns.append(pattern)
    
    args = ""
    for pattern in exclude_patterns:
        args += f" --exclude '{pattern}'"
    
    return args


def run_command(command):
    """
    Run a shell command and return its output.
    
    Args:
        command: Shell command to execute
        
    Returns:
        Command output (stdout or stderr) or None if an error occurred
    """
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Check for success (some commands like ruff might return non-zero when they find issues - that's ok)
    if result.returncode != 0:
        # If the command contains "|| true", we're explicitly allowing non-zero exit codes
        if "|| true" not in command and "Found no issues" not in result.stderr:
            print(f"Error running command: {command}")
            print(f"Exit code: {result.returncode}")
            if result.stderr:
                print(f"Error message: {result.stderr}")
            return None
    
    # Return combined output - for some tools like ruff, errors are reported on stdout
    output = result.stdout
    
    # If there's no stdout but there is stderr, use stderr (like when "no issues found")
    if not output and result.stderr:
        output = result.stderr
        
    return output


def get_code_stats(config):
    """
    Get code statistics using cloc.
    Returns a dictionary with language statistics and line counts.
    
    Args:
        config: Configuration dictionary containing paths to analyze
    """
    # Get paths from config
    root_dir = os.getcwd()
    include_paths = " ".join([os.path.join(root_dir, path) for path in config["include_paths"]])
    
    print(f"Running code statistics on: {include_paths}")
    
    # Build exclude arguments
    exclude_args = build_cloc_exclude_args(config)
    
    # Run cloc command with JSON output and exclude patterns
    cloc_output = run_command(f"cloc {include_paths} --json{exclude_args}")
    if cloc_output is None:
        return {
            'total': {'code': 0, 'blank': 0, 'comment': 0, 'files': 0},
            'by_language': {}
        }
    
    # Import and use the JSON parser
    from codeqa.metrics_parsing import parse_cloc_json
    
    # Check if output is JSON format
    if cloc_output and '{' in cloc_output and '}' in cloc_output:
        try:
            # Use the proper JSON parser
            return parse_cloc_json(cloc_output)
        except json.JSONDecodeError:
            print("Warning: Could not parse cloc JSON output, falling back to text parsing")
    
    # Fallback to text parsing for backward compatibility
    stats = {
        'total': {'code': 0, 'blank': 0, 'comment': 0, 'files': 0},
        'by_language': {}
    }
    
    # Skip header lines and empty lines
    lines = cloc_output.strip().split('\n')
    
    # Extract summary stats
    summary_line = None
    for i, line in enumerate(lines):
        if line.startswith('SUM:'):
            summary_line = i
            break
    
    if summary_line is not None:
        # Parse the summary line
        sum_parts = lines[summary_line].split()
        try:
            stats['total'] = {
                'files': int(sum_parts[1]) if len(sum_parts) > 1 else 0,
                'blank': int(sum_parts[2]) if len(sum_parts) > 2 else 0,
                'comment': int(sum_parts[3]) if len(sum_parts) > 3 else 0,
                'code': int(sum_parts[4]) if len(sum_parts) > 4 else 0
            }
        except (ValueError, IndexError):
            print("Warning: Could not parse cloc summary line")
    
    # Extract language stats
    for line in lines:
        # Skip header lines, separator lines, and the summary line
        if (not line or line.startswith('github') or line.startswith('---') 
            or line.startswith('SUM:') or line.startswith('Language')):
            continue
        
        # Parse language line
        parts = line.split()
        if len(parts) >= 5:
            # Handle multi-word language names
            if parts[0] == 'Fish' and parts[1] == 'Shell':
                lang = 'Fish Shell'
                values = parts[2:6]  # files, blank, comment, code
            else:
                lang = parts[0]
                values = parts[1:5]  # files, blank, comment, code
            
            try:
                stats['by_language'][lang] = {
                    'files': int(values[0]),
                    'blank': int(values[1]),
                    'comment': int(values[2]),
                    'code': int(values[3])
                }
            except (ValueError, IndexError):
                print(f"Warning: Could not parse language stats for {lang}")
    
    return stats




def parse_radon_mi(output, config):
    """Parse the output of radon mi command."""
    results = []
    
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
            
        parts = line.strip().split(' - ')
        if len(parts) == 2:
            file_path = parts[0].strip()
            if not is_project_file(file_path, config):
                continue
                
            mi_info = parts[1].strip()
            grade = mi_info[0]
            score = float(re.search(r'(\d+\.\d+)', mi_info).group(1))
            results.append({
                'file': file_path,
                'grade': grade,
                'score': score
            })
    
    return sorted(results, key=lambda x: x['score'])


def parse_ruff_output(output, config):
    """
    Parse the output of ruff check command.
    
    Args:
        output: String output from the ruff command
        config: Configuration dictionary with include/exclude paths
        
    Returns:
        List of linting issues found
    """
    # Import the new JSON parser
    from codeqa.metrics_parsing import parse_ruff_json
    
    # Check if output is in JSON format
    if output and output.strip().startswith('['): 
        # This appears to be JSON format
        return parse_ruff_json(output, config)
    
    # Handle empty output or "no issues" messages
    if not output or "Found no issues" in output or "No files to check" in output:
        return []
        
    # Legacy text parsing code - keep for backward compatibility
    results = []
    lines = output.strip().split('\n')
    for line in lines:
        if not line.strip():
            continue
        
        # Skip informational lines like "Found X errors in Y files"
        if line.strip().startswith("Found ") and " errors in " in line:
            continue
            
        # Match linting errors in format: file.py:10:5: E123 Error message
        match = re.match(r'([^:]+):(\d+):(\d+): ([A-Z]\d+) (.*)', line)
        if match:
            file_path, line_num, col, error_code, message = match.groups()
            if not is_project_file(file_path, config):
                continue
                
            results.append({
                'file': file_path,
                'line': int(line_num),
                'column': int(col),
                'code': error_code,
                'message': message
            })
    
    return results


def count_issues_by_file(issues):
    """Count the number of issues per file."""
    counts = defaultdict(int)
    for issue in issues:
        counts[issue['file']] += 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


def find_latest_metrics_file(current_timestamp):
    """Find the latest metrics file before the current one."""
    metrics_dir = METRICS_DIR
    if not os.path.exists(metrics_dir):
        os.makedirs(metrics_dir, exist_ok=True)
        return None
    
    files = glob.glob(os.path.join(metrics_dir, "metrics_*.json"))
    if not files:
        return None
    
    # Filter out the current timestamp and sort
    previous_files = [f for f in files if os.path.basename(f) != f"metrics_{current_timestamp}.json"]
    if not previous_files:
        return None
    
    # Sort by modification time (newest first)
    previous_files.sort(key=os.path.getmtime, reverse=True)
    return previous_files[0] if previous_files else None


def list_snapshots(silent=False):
    """
    List all available snapshots.
    
    Args:
        silent: If True, don't print snapshot information
        
    Returns:
        List of snapshot files sorted by date (newest first)
    """
    metrics_dir = METRICS_DIR
    if not os.path.exists(metrics_dir):
        os.makedirs(metrics_dir, exist_ok=True)
        if not silent:
            print("No snapshots found")
        return []
    
    files = glob.glob(os.path.join(metrics_dir, "metrics_*.json"))
    if not files:
        if not silent:
            print("No snapshots found")
        return []
    
    # Sort by modification time (newest first)
    files.sort(key=os.path.getmtime, reverse=True)
    
    if not silent:
        print("Available snapshots:")
    snapshots = []
    for file in files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                date = data.get('date', os.path.basename(file))
                timestamp = data.get('timestamp', 'unknown')
                if not silent:
                    print(f"- {date} ({os.path.basename(file)})")
                snapshots.append({'file': file, 'date': date, 'timestamp': timestamp})
        except Exception as e:
            if not silent:
                print(f"- {os.path.basename(file)} [Error: {str(e)}]")
            snapshots.append({'file': file, 'date': 'unknown', 'timestamp': 'error'})
    
    return snapshots


def compute_trend(current, previous, key):
    """Compute the trend between current and previous metrics."""
    if key not in current or key not in previous:
        return None, None
    
    current_value = current[key]
    previous_value = previous[key]
    
    if isinstance(current_value, dict) and isinstance(previous_value, dict):
        return None, None  # Complex structure, handle separately
    
    if previous_value == 0:
        return current_value - previous_value, None  # Avoid division by zero
    
    change = current_value - previous_value
    percent = (change / previous_value) * 100
    
    return change, percent


def get_formatted_trend(change, percent, higher_is_better=False):
    """Format trend with arrow and color indicator."""
    if change is None:
        return "N/A"
    
    # Determine if the change is good or bad
    is_good = (higher_is_better and change > 0) or (not higher_is_better and change < 0)
    
    # Format the change
    if percent is not None:
        if is_good:
            return f"↓ {abs(change)} ({abs(percent):.1f}%)" if not higher_is_better else f"↑ {change} ({percent:.1f}%)"
        else:
            return f"↑ {change} ({percent:.1f}%)" if not higher_is_better else f"↓ {abs(change)} ({abs(percent):.1f}%)"
    else:
        if is_good:
            return f"↓ {abs(change)}" if not higher_is_better else f"↑ {change}"
        else:
            return f"↑ {change}" if not higher_is_better else f"↓ {abs(change)}"


def create_snapshot(config_path=None, verbose=False, only_on_changes=False):
    """
    Create a snapshot of code quality metrics.
    
    This function runs various code analysis tools and generates a snapshot
    of the current code quality metrics. It saves the snapshot as a JSON file
    and returns a markdown report.
    
    Args:
        config_path: Optional path to a custom config file
        verbose: Whether to print detailed progress information
        only_on_changes: If True, only update CODE_METRICS.md if significant changes detected
        
    Returns:
        Tuple of (markdown_content, json_path, unchanged)
    """
    config = load_config(config_path)
    today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_data = {
        'date': datetime.datetime.now().strftime("%B %d, %Y"),
        'timestamp': today,
        'config': config
    }
    
    # Print included folders
    if verbose:
        print("\nAnalyzing the following directories:")
        for path in config["include_paths"]:
            print(f"  - {path}")
        print("\nExcluding patterns:")
        for pattern in config["exclude_patterns"]:
            print(f"  - {pattern}")
        print("")
    
    # Get code stats using cloc
    code_stats = get_code_stats(config)
    metrics_data['cloc'] = code_stats
    
    # Build the paths to analyze
    root_dir = os.getcwd()
    paths_to_analyze = [os.path.join(root_dir, path) for path in config["include_paths"]]
    paths_str = " ".join(paths_to_analyze)
    
    # Build exclude arguments for Ruff
    ruff_exclude_args = build_ruff_exclude_args(config)
    
    # Run Ruff with JSON output format and exclude patterns
    ruff_cmd = f"ruff check {paths_str} --output-format json --no-fix{ruff_exclude_args} || true"
    print(f"Running linting check: {ruff_cmd}")
    ruff_output = run_command(ruff_cmd)
    
    if ruff_output is None:
        metrics_data['ruff'] = {'error': 'Error running Ruff'}
        # Set default values in case of error
        ruff_issues = []
        metrics_data['ruff'] = {
            'issues_count': 0,
            'issues': [],
            'files_count': {}
        }
    else:
        # Parse using the improved parser that handles JSON
        ruff_issues = parse_ruff_output(ruff_output, config)
        metrics_data['ruff'] = {
            'issues_count': len(ruff_issues),
            'issues': ruff_issues,
            'files_count': count_issues_by_file(ruff_issues)
        }
    
    # Build exclude arguments for Radon
    radon_exclude_args = build_radon_exclude_args(config)
    
    # Run Radon CC with JSON output format and exclude patterns
    radon_cc_output = run_command(f"radon cc {paths_str} -a -s --json{radon_exclude_args}")
    if radon_cc_output is None:
        metrics_data['radon_cc'] = {'error': 'Error running Radon CC'}
    else:
        # Import parser function from metrics_parsing module
        from codeqa.metrics_parsing import parse_radon_cc_json
        try:
            # Use the proper JSON parser
            metrics_data['radon_cc'] = parse_radon_cc_json(radon_cc_output, config)
        except json.JSONDecodeError:
            metrics_data['radon_cc'] = {'error': 'Error parsing Radon CC JSON output'}
    
    # Run Radon MI with exclude patterns
    radon_mi_output = run_command(f"radon mi {paths_str} -s{radon_exclude_args}")
    if radon_mi_output is None:
        metrics_data['radon_mi'] = {'error': 'Error running Radon MI'}
    else:
        mi_results = parse_radon_mi(radon_mi_output, config)
        
        # Count by grade
        mi_counts = {'A': 0, 'B': 0, 'C': 0}
        for result in mi_results:
            mi_counts[result['grade']] += 1
        
        metrics_data['radon_mi'] = {
            'grade_counts': mi_counts,
            'files': mi_results
        }
    
    # Save detailed metrics to JSON
    # Ensure the metrics directory exists
    os.makedirs(METRICS_DIR, exist_ok=True)
    
    # Look up previous metrics for trends and to check for changes
    previous_metrics_file = find_latest_metrics_file(today)
    previous_metrics = None
    if previous_metrics_file:
        try:
            with open(previous_metrics_file, 'r') as f:
                previous_metrics = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load previous metrics ({e})")
    
    # Check if this snapshot is unchanged from the previous one
    from codeqa.snapshot_manager import is_snapshot_unchanged
    
    # Default to 'changed' for the first run
    unchanged = False
    
    # Only check for changes if the flag is set and there's a previous snapshot
    if only_on_changes and previous_metrics:
        unchanged = is_snapshot_unchanged(metrics_data, previous_metrics)
        
    # Add suffix to JSON filename if unchanged
    filename = f"metrics_{today}"
    if unchanged:
        filename += "_unchanged"
    
    json_path = os.path.join(METRICS_DIR, f"{filename}.json")
    with open(json_path, 'w') as f:
        json.dump(metrics_data, f, indent=2)
    
    # Generate markdown summary
    root_dir = os.getcwd()
    ruff_count = metrics_data['ruff'].get('issues_count', 0)
    cc_counts = metrics_data['radon_cc'].get('grade_counts', {})
    mi_counts = metrics_data['radon_mi'].get('grade_counts', {})
    
    # Calculate trends
    trends = {}
    if previous_metrics:
        # LOC trends
        prev_loc = previous_metrics.get('cloc', {}).get('total', {}).get('code', 0)
        curr_loc = code_stats['total']['code']
        loc_change, loc_percent = compute_trend({'code': curr_loc}, {'code': prev_loc}, 'code')
        trends['loc'] = get_formatted_trend(loc_change, loc_percent, higher_is_better=False)
        
        # Linting trends
        prev_ruff = previous_metrics.get('ruff', {}).get('issues_count', 0)
        ruff_change, ruff_percent = compute_trend({'count': ruff_count}, {'count': prev_ruff}, 'count')
        trends['ruff'] = get_formatted_trend(ruff_change, ruff_percent, higher_is_better=False)
        
        # Complexity trends
        prev_cc_high = sum([previous_metrics.get('radon_cc', {}).get('grade_counts', {}).get(g, 0) 
                            for g in ['C', 'D', 'E', 'F']])
        curr_cc_high = sum([cc_counts.get(g, 0) for g in ['C', 'D', 'E', 'F']])
        cc_change, cc_percent = compute_trend({'high': curr_cc_high}, {'high': prev_cc_high}, 'high')
        trends['cc'] = get_formatted_trend(cc_change, cc_percent, higher_is_better=False)
        
        # Maintainability trends
        prev_mi_low = previous_metrics.get('radon_mi', {}).get('grade_counts', {}).get('C', 0)
        curr_mi_low = mi_counts.get('C', 0)
        mi_change, mi_percent = compute_trend({'low': curr_mi_low}, {'low': prev_mi_low}, 'low')
        trends['mi'] = get_formatted_trend(mi_change, mi_percent, higher_is_better=False)
    
    # Get top 10 files by complexity with additional data
    top_complex_files = []
    if 'files' in metrics_data['radon_cc']:
        complex_files = list(metrics_data['radon_cc']['files'].items())
        for file_path, data in sorted(complex_files, key=lambda x: x[1]['max_complexity'], reverse=True)[:10]:
            rel_path = os.path.relpath(file_path, root_dir)
            grade = data['max_grade']
            complexity = data['max_complexity']
            most_complex_function = data.get('function', 'N/A')
            
            top_complex_files.append({
                'file': rel_path,
                'grade': grade,
                'complexity': complexity,
                'function': most_complex_function
            })
    
    # Get top 10 functions by complexity
    top_complex_functions = []
    if 'functions' in metrics_data['radon_cc']:
        complex_funcs = metrics_data['radon_cc']['functions'][:10]
        for func in complex_funcs:
            rel_path = os.path.relpath(func['file'], root_dir)
            # Fix the format - extract the actual function name from the JSON
            if "(" in func['function']:
                # Function name has complexity in it like "F (41)" - extract the name
                display_name = func['function'].split(" ", 1)[0]
                actual_complexity = int(func['function'].split("(")[1].split(")")[0])
            else:
                display_name = func['function']
                actual_complexity = func['complexity']
                
            top_complex_functions.append({
                'file': rel_path, 
                'function': display_name,
                'grade': func['grade'],
                'complexity': actual_complexity
            })
    
    # Get top 10 files by linting issues
    top_lint_files = []
    if 'files_count' in metrics_data['ruff']:
        lint_files = list(metrics_data['ruff']['files_count'].items())
        for file_path, count in sorted(lint_files, key=lambda x: x[1], reverse=True)[:10]:
            rel_path = os.path.relpath(file_path, root_dir)
            top_lint_files.append({
                'file': rel_path,
                'issues': count
            })
    
    # Get top 10 files by low maintainability
    top_low_mi_files = []
    if 'files' in metrics_data['radon_mi']:
        low_mi_files = metrics_data['radon_mi']['files']
        for data in sorted(low_mi_files, key=lambda x: x['score'])[:10]:
            rel_path = os.path.relpath(data['file'], root_dir)
            top_low_mi_files.append({
                'file': rel_path,
                'grade': data['grade'],
                'score': data['score']
            })
    
    # Create table for code stats by language
    code_stats_table = "| Language | Files | Code | Comment | Blank |\n"
    code_stats_table += "|----------|-------|------|---------|-------|\n"
    for lang, data in code_stats['by_language'].items():
        code_stats_table += f"| {lang} | {data['files']:,} | {data['code']:,} | {data['comment']:,} | {data['blank']:,} |\n"
    
    # Create table for complex files
    complex_files_table = "| File | Grade | Complexity | Most Complex Function |\n"
    complex_files_table += "|------|-------|------------|----------------------|\n"
    for file_data in top_complex_files:
        complex_files_table += f"| {file_data['file']} | {file_data['grade']} | {file_data['complexity']} | {file_data['function']} |\n"
    
    # Create table for complex functions
    complex_funcs_table = "| File | Function | Grade | Complexity |\n"
    complex_funcs_table += "|------|----------|-------|------------|\n"
    
        # With the proper JSON parsing, we no longer need the function name mapping
    # The data is already in the correct format with proper function names and complexity values
    for func_data in top_complex_functions:
        # The function name, complexity and grade are now correctly extracted from the JSON
        function_name = func_data.get('function', 'Unknown')
        complexity = func_data.get('complexity', 0)
        grade = func_data.get('grade', 'X')
        
        complex_funcs_table += f"| {func_data['file']} | {function_name} | {grade} | {complexity} |\n"
    
    # Create table for lint files
    lint_files_table = "| File | Issues |\n"
    lint_files_table += "|------|--------|\n"
    for file_data in top_lint_files:
        lint_files_table += f"| {file_data['file']} | {file_data['issues']} |\n"
    
    # Create table for low maintainability files
    mi_files_table = "| File | Grade | Score |\n"
    mi_files_table += "|------|-------|-------|\n"
    for file_data in top_low_mi_files:
        mi_files_table += f"| {file_data['file']} | {file_data['grade']} | {file_data['score']:.2f} |\n"
    
    # Trend data
    trend_section = ""
    if trends:
        trend_section = """
#### Trends Since Last Snapshot
| Metric | Change |
|--------|--------|
"""
        trend_section += f"| Lines of Code | {trends.get('loc', 'N/A')} |\n"
        trend_section += f"| Linting Issues | {trends.get('ruff', 'N/A')} |\n"
        trend_section += f"| Complex Functions | {trends.get('cc', 'N/A')} |\n"
        trend_section += f"| Low Maintainability | {trends.get('mi', 'N/A')} |\n"
    
    # Generate markdown
    markdown = f"""### {metrics_data['date']}

#### Summary

| Metric | Value | 
|--------|-------|
| Lines of Code | {code_stats['total']['code']:,} |
| Files | {code_stats['total']['files']:,} |
| Comments | {code_stats['total']['comment']:,} |
| Linting Issues | {ruff_count} |
| Cyclomatic Complexity | A:{cc_counts.get('A', 0)} B:{cc_counts.get('B', 0)} C:{cc_counts.get('C', 0)} D:{cc_counts.get('D', 0)} E:{cc_counts.get('E', 0)} F:{cc_counts.get('F', 0)} |
| Maintainability Index | A:{mi_counts.get('A', 0)} B:{mi_counts.get('B', 0)} C:{mi_counts.get('C', 0)} |
| Detailed Report | [metrics_{today}.json](metrics/metrics_{today}.json) |

#### Code Statistics by Language
{code_stats_table}

#### Top 10 Complex Files
{complex_files_table}

#### Top 10 Complex Functions/Methods
{complex_funcs_table}

#### Top 10 Files with Linting Issues
{lint_files_table if top_lint_files else "No linting issues found."}

#### Top 10 Files with Low Maintainability
{mi_files_table}
{trend_section}
#### Analysis
- {'Critical issues to address:' if ruff_count + cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0) + mi_counts.get('C', 0) > 0 else 'No critical issues.'}
  - {f"{ruff_count} linting issues" if ruff_count > 0 else "0 linting issues"}
  - {f"{cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0)} high complexity functions" if cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0) > 0 else "0 high complexity functions"}
  - {f"{mi_counts.get('C', 0)} files with low maintainability" if mi_counts.get('C', 0) > 0 else "0 files with low maintainability"}
"""
    
    # Print message if unchanged
    if unchanged:
        print("\nNo significant changes detected since the last snapshot.")
        print(f"The metrics file still contains the last meaningful update.")
        print(f"Metrics data saved to {json_path} (marked as unchanged).")
    
    return markdown, json_path, unchanged


def update_metrics_file(snapshot):
    """Update the CODE_METRICS.md file with the new snapshot."""
    if not os.path.exists(METRICS_FILE):
        print(f"Error: {METRICS_FILE} not found")
        return False
    
    try:
        with open(METRICS_FILE, 'r') as f:
            content = f.read()
        
        # Find the position after the "## Historical Snapshots" header
        pattern = r"## Historical Snapshots"
        if pattern not in content:
            print(f"Error: Could not find '{pattern}' section in {METRICS_FILE}")
            return False
        
        # Insert at the end of the section
        parts = content.split(pattern)
        if len(parts) != 2:
            print(f"Error: Unexpected format in {METRICS_FILE}")
            return False
        
        updated_content = parts[0] + pattern + parts[1].rstrip() + "\n\n" + snapshot + "\n"
        
        with open(METRICS_FILE, 'w') as f:
            f.write(updated_content)
        
        return True
    except Exception as e:
        print(f"Error updating metrics file: {e}")
        return False


def compare_snapshots(snapshot1, snapshot2):
    """
    Compare two snapshots and generate a comparison report.
    
    Args:
        snapshot1: Path to the first snapshot file (older)
        snapshot2: Path to the second snapshot file (newer)
        
    Returns:
        Markdown string with comparison report
    """
    try:
        with open(snapshot1, 'r') as f:
            data1 = json.load(f)
        with open(snapshot2, 'r') as f:
            data2 = json.load(f)
    except Exception as e:
        print(f"Error loading snapshots: {str(e)}")
        return None
    
    # Basic info
    date1 = data1.get('date', 'Unknown')
    date2 = data2.get('date', 'Unknown')
    
    # Compare code stats
    loc1 = data1.get('cloc', {}).get('total', {}).get('code', 0)
    loc2 = data2.get('cloc', {}).get('total', {}).get('code', 0)
    loc_change, loc_percent = compute_trend({'code': loc2}, {'code': loc1}, 'code')
    loc_trend = get_formatted_trend(loc_change, loc_percent, higher_is_better=False)
    
    # Compare linting issues
    ruff1 = data1.get('ruff', {}).get('issues_count', 0)
    ruff2 = data2.get('ruff', {}).get('issues_count', 0)
    ruff_change, ruff_percent = compute_trend({'count': ruff2}, {'count': ruff1}, 'count')
    ruff_trend = get_formatted_trend(ruff_change, ruff_percent, higher_is_better=False)
    
    # Compare complexity stats
    cc1 = data1.get('radon_cc', {}).get('grade_counts', {})
    cc2 = data2.get('radon_cc', {}).get('grade_counts', {})
    high_cc1 = sum([cc1.get(g, 0) for g in ['C', 'D', 'E', 'F']])
    high_cc2 = sum([cc2.get(g, 0) for g in ['C', 'D', 'E', 'F']])
    cc_change, cc_percent = compute_trend({'high': high_cc2}, {'high': high_cc1}, 'high')
    cc_trend = get_formatted_trend(cc_change, cc_percent, higher_is_better=False)
    
    # Compare maintainability stats
    mi1 = data1.get('radon_mi', {}).get('grade_counts', {})
    mi2 = data2.get('radon_mi', {}).get('grade_counts', {})
    low_mi1 = mi1.get('C', 0)
    low_mi2 = mi2.get('C', 0)
    mi_change, mi_percent = compute_trend({'low': low_mi2}, {'low': low_mi1}, 'low')
    mi_trend = get_formatted_trend(mi_change, mi_percent, higher_is_better=False)
    
    # Generate markdown
    markdown = f"""## Comparison: {date1} vs {date2}

### Summary

| Metric | {date1} | {date2} | Change |
|--------|---------|---------|--------|
| Lines of Code | {loc1:,} | {loc2:,} | {loc_trend} |
| Linting Issues | {ruff1} | {ruff2} | {ruff_trend} |
| Complex Functions (C-F) | {high_cc1} | {high_cc2} | {cc_trend} |
| Low Maintainability Files | {low_mi1} | {low_mi2} | {mi_trend} |

### Analysis

- Code Size: {"Increased by " + str(loc_change) + " lines" if loc_change > 0 else "Decreased by " + str(abs(loc_change)) + " lines" if loc_change < 0 else "Remained the same"}
- Code Quality: {"Improved overall" if ruff_change <= 0 and cc_change <= 0 and mi_change <= 0 else "Declined overall" if ruff_change > 0 and cc_change > 0 and mi_change > 0 else "Mixed changes"}
- Most Significant Change: {max([('Linting Issues', abs(ruff_percent or 0)), ('Complex Functions', abs(cc_percent or 0)), ('Low Maintainability', abs(mi_percent or 0))], key=lambda x: x[1])[0] if any([ruff_percent, cc_percent, mi_percent]) else "None"}
"""
    
    return markdown


def create_report(snapshot_path):
    """
    Generate a standalone report from an existing snapshot.
    
    Args:
        snapshot_path: Path to the snapshot file
        
    Returns:
        Markdown string with report
    """
    try:
        with open(snapshot_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading snapshot: {str(e)}")
        return None
    
    # Basic info
    date = data.get('date', 'Unknown')
    
    # Code stats
    code_stats = data.get('cloc', {})
    total_code = code_stats.get('total', {}).get('code', 0)
    total_files = code_stats.get('total', {}).get('files', 0)
    
    # Linting issues
    ruff_count = data.get('ruff', {}).get('issues_count', 0)
    
    # Complexity stats
    cc_counts = data.get('radon_cc', {}).get('grade_counts', {})
    
    # Maintainability stats
    mi_counts = data.get('radon_mi', {}).get('grade_counts', {})
    
    # Generate markdown
    markdown = f"""## Code Quality Report: {date}

### Summary

| Metric | Value | 
|--------|-------|
| Lines of Code | {total_code:,} |
| Files | {total_files:,} |
| Linting Issues | {ruff_count} |
| Cyclomatic Complexity | A:{cc_counts.get('A', 0)} B:{cc_counts.get('B', 0)} C:{cc_counts.get('C', 0)} D:{cc_counts.get('D', 0)} E:{cc_counts.get('E', 0)} F:{cc_counts.get('F', 0)} |
| Maintainability Index | A:{mi_counts.get('A', 0)} B:{mi_counts.get('B', 0)} C:{mi_counts.get('C', 0)} |

### Analysis
- {'Critical issues to address:' if ruff_count + cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0) + mi_counts.get('C', 0) > 0 else 'No critical issues.'}
  - {f"{ruff_count} linting issues" if ruff_count > 0 else "0 linting issues"}
  - {f"{cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0)} high complexity functions" if cc_counts.get('C', 0) + cc_counts.get('D', 0) + cc_counts.get('E', 0) + cc_counts.get('F', 0) > 0 else "0 high complexity functions"}
  - {f"{mi_counts.get('C', 0)} files with low maintainability" if mi_counts.get('C', 0) > 0 else "0 files with low maintainability"}
"""
    
    return markdown