#!/usr/bin/env python3
"""
Snapshot management functionality for CodeQA.

This module handles snapshot creation, comparison, and reporting.
It was extracted from metrics.py to reduce function complexity.
"""

import glob
import json
import os
from typing import Dict, Any, Tuple, Optional


# Constants
METRICS_FILE = "CODE_METRICS.md"
METRICS_DIR = "generated/metrics"


def is_snapshot_unchanged(current_metrics: Dict[str, Any], previous_metrics: Optional[Dict[str, Any]]) -> bool:
    """
    Compare two snapshots to determine if there are any significant changes.
    
    Args:
        current_metrics: The current metrics snapshot
        previous_metrics: The previous metrics snapshot
        
    Returns:
        bool: True if the snapshots are essentially the same, False if there are changes
    """
    # If there's no previous snapshot, we consider this a change
    if previous_metrics is None:
        return False
        
    # Compare summary data fields that would indicate meaningful changes
    summary_fields = [
        'cloc.total',
        'ruff.issues_count',
        'radon_cc.grade_counts',
        'radon_mi.grade_counts'
    ]
    
    # Check each summary field
    for field in summary_fields:
        parts = field.split('.')
        
        # Navigate through nested dictionaries
        current_value = current_metrics
        previous_value = previous_metrics
        
        try:
            for part in parts:
                current_value = current_value[part]
                previous_value = previous_value[part]
                
            # Compare the values - if they differ, we have a change
            if current_value != previous_value:
                print(f"Change detected in {field}: {previous_value} -> {current_value}")
                return False
        except (KeyError, TypeError) as e:
            # If we can't compare the fields, assume there's a change
            print(f"Error comparing {field}: {str(e)}")
            return False
            
    # If we get here, all summary data matches
    return True


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


def format_snapshot_markdown(metrics_data, previous_metrics=None):
    """
    Format snapshot data into markdown.
    
    Args:
        metrics_data: Dictionary with current metrics data
        previous_metrics: Optional dictionary with previous metrics data for trends
        
    Returns:
        Markdown text for the snapshot
    """
    today = metrics_data.get('timestamp', 'unknown')
    root_dir = os.getcwd()
    
    # Extract metrics data
    code_stats = metrics_data.get('cloc', {})
    ruff_count = metrics_data.get('ruff', {}).get('issues_count', 0)
    cc_counts = metrics_data.get('radon_cc', {}).get('grade_counts', {})
    mi_counts = metrics_data.get('radon_mi', {}).get('grade_counts', {})
    
    # Calculate trends
    trends = {}
    if previous_metrics:
        # LOC trends
        prev_loc = previous_metrics.get('cloc', {}).get('total', {}).get('code', 0)
        curr_loc = code_stats.get('total', {}).get('code', 0)
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
    
    # Prepare the top files and functions lists
    top_complex_files = get_top_complex_files(metrics_data, root_dir)
    top_complex_functions = get_top_complex_functions(metrics_data, root_dir)
    top_lint_files = get_top_lint_files(metrics_data, root_dir)
    top_low_mi_files = get_top_low_mi_files(metrics_data, root_dir)
    
    # Create table for code stats by language
    code_stats_table = format_code_stats_table(code_stats)
    
    # Create table for complex files
    complex_files_table = format_complex_files_table(top_complex_files)
    
    # Create table for complex functions
    complex_funcs_table = format_complex_functions_table(top_complex_functions)
    
    # Create table for lint files
    lint_files_table = format_lint_files_table(top_lint_files)
    
    # Create table for low maintainability files
    mi_files_table = format_mi_files_table(top_low_mi_files)
    
    # Trend data
    trend_section = format_trend_section(trends) if trends else ""
    
    # Generate markdown
    markdown = f"""### {metrics_data['date']}

#### Summary

| Metric | Value | 
|--------|-------|
| Lines of Code | {code_stats.get('total', {}).get('code', 0):,} |
| Files | {code_stats.get('total', {}).get('files', 0):,} |
| Comments | {code_stats.get('total', {}).get('comment', 0):,} |
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
    
    return markdown


def get_top_complex_files(metrics_data, root_dir, limit=10):
    """Extract top complex files from metrics data."""
    top_complex_files = []
    if 'files' in metrics_data.get('radon_cc', {}):
        complex_files = list(metrics_data['radon_cc']['files'].items())
        for file_path, data in sorted(complex_files, key=lambda x: x[1]['max_complexity'], reverse=True)[:limit]:
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
    return top_complex_files


def get_top_complex_functions(metrics_data, root_dir, limit=10):
    """Extract top complex functions from metrics data."""
    top_complex_functions = []
    if 'functions' in metrics_data.get('radon_cc', {}):
        complex_funcs = metrics_data['radon_cc']['functions'][:limit]
        for func in complex_funcs:
            rel_path = os.path.relpath(func['file'], root_dir)
            top_complex_functions.append({
                'file': rel_path, 
                'function': func['function'],
                'grade': func['grade'],
                'complexity': func['complexity']
            })
    return top_complex_functions


def get_top_lint_files(metrics_data, root_dir, limit=10):
    """Extract top files with linting issues from metrics data."""
    top_lint_files = []
    if 'files_count' in metrics_data.get('ruff', {}):
        lint_files = list(metrics_data['ruff']['files_count'].items())
        for file_path, count in sorted(lint_files, key=lambda x: x[1], reverse=True)[:limit]:
            rel_path = os.path.relpath(file_path, root_dir)
            top_lint_files.append({
                'file': rel_path,
                'issues': count
            })
    return top_lint_files


def get_top_low_mi_files(metrics_data, root_dir, limit=10):
    """Extract top files with low maintainability from metrics data."""
    top_low_mi_files = []
    if 'files' in metrics_data.get('radon_mi', {}):
        low_mi_files = metrics_data['radon_mi']['files']
        for data in sorted(low_mi_files, key=lambda x: x['score'])[:limit]:
            rel_path = os.path.relpath(data['file'], root_dir)
            top_low_mi_files.append({
                'file': rel_path,
                'grade': data['grade'],
                'score': data['score']
            })
    return top_low_mi_files


def format_code_stats_table(code_stats):
    """Format code statistics as a markdown table."""
    table = "| Language | Files | Code | Comment | Blank |\n"
    table += "|----------|-------|------|---------|-------|\n"
    for lang, data in code_stats.get('by_language', {}).items():
        table += f"| {lang} | {data['files']:,} | {data['code']:,} | {data['comment']:,} | {data['blank']:,} |\n"
    return table


def format_complex_files_table(top_complex_files):
    """Format complex files as a markdown table."""
    table = "| File | Grade | Complexity | Most Complex Function |\n"
    table += "|------|-------|------------|----------------------|\n"
    for file_data in top_complex_files:
        table += f"| {file_data['file']} | {file_data['grade']} | {file_data['complexity']} | {file_data['function']} |\n"
    return table


def format_complex_functions_table(top_complex_functions):
    """Format complex functions as a markdown table."""
    table = "| File | Function | Grade | Complexity |\n"
    table += "|------|----------|-------|------------|\n"
    for func_data in top_complex_functions:
        table += f"| {func_data['file']} | {func_data['function']} | {func_data['grade']} | {func_data['complexity']} |\n"
    return table


def format_lint_files_table(top_lint_files):
    """Format files with linting issues as a markdown table."""
    table = "| File | Issues |\n"
    table += "|------|--------|\n"
    for file_data in top_lint_files:
        table += f"| {file_data['file']} | {file_data['issues']} |\n"
    return table


def format_mi_files_table(top_low_mi_files):
    """Format files with low maintainability as a markdown table."""
    table = "| File | Grade | Score |\n"
    table += "|------|-------|-------|\n"
    for file_data in top_low_mi_files:
        table += f"| {file_data['file']} | {file_data['grade']} | {file_data['score']:.2f} |\n"
    return table


def format_trend_section(trends):
    """Format trend data as a markdown section."""
    trend_section = """
#### Trends Since Last Snapshot
| Metric | Change |
|--------|--------|
"""
    trend_section += f"| Lines of Code | {trends.get('loc', 'N/A')} |\n"
    trend_section += f"| Linting Issues | {trends.get('ruff', 'N/A')} |\n"
    trend_section += f"| Complex Functions | {trends.get('cc', 'N/A')} |\n"
    trend_section += f"| Low Maintainability | {trends.get('mi', 'N/A')} |\n"
    return trend_section


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