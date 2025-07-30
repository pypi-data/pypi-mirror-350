#!/usr/bin/env python3
"""
Parsers for code quality tools output in the CodeQA metrics module.

This module provides JSON parsers for:
- radon (cyclomatic complexity)
- ruff (linting)
- cloc (code statistics)

Each parser converts tool JSON output into a structured, typed format.
"""

import json
from typing import Dict, List, Any, TypedDict


# Type definitions for parsed data
class ClocLanguageStats(TypedDict):
    """Type for language statistics from cloc."""
    files: int
    blank: int
    comment: int
    code: int


class ClocStats(TypedDict):
    """Type for overall code statistics from cloc."""
    total: Dict[str, int]
    by_language: Dict[str, ClocLanguageStats]


class RuffIssue(TypedDict):
    """Type for a single linting issue from ruff."""
    file: str
    line: int
    column: int
    code: str
    message: str


class RadonCCFunction(TypedDict):
    """Type for a function's cyclomatic complexity metrics from radon."""
    file: str
    function: str
    grade: str
    complexity: int
    type: str


class RadonCCFile(TypedDict):
    """Type for a file's cyclomatic complexity metrics from radon."""
    count: int
    max_complexity: int
    max_grade: str
    function: str


# Parser functions
def parse_cloc_json(output: str) -> ClocStats:
    """
    Parse JSON output from cloc command.
    
    Args:
        output: JSON output string from cloc --json
        
    Returns:
        Structured code statistics from cloc
    """
    data = json.loads(output)
    
    # Initialize the result structure
    stats: ClocStats = {
        'total': {'code': 0, 'blank': 0, 'comment': 0, 'files': 0},
        'by_language': {}
    }
    
    # Process the SUM entry for totals
    if 'SUM' in data:
        sum_data = data['SUM']
        stats['total'] = {
            'files': sum_data.get('nFiles', 0),
            'blank': sum_data.get('blank', 0),
            'comment': sum_data.get('comment', 0),
            'code': sum_data.get('code', 0)
        }
    
    # Process language-specific entries
    for key, value in data.items():
        # Skip non-language entries
        if key in ('header', 'SUM'):
            continue
            
        # Add language entry
        lang_stats: ClocLanguageStats = {
            'files': value.get('nFiles', 0),
            'blank': value.get('blank', 0),
            'comment': value.get('comment', 0),
            'code': value.get('code', 0)
        }
        stats['by_language'][key] = lang_stats
    
    return stats


def parse_ruff_json(output: str, config: Dict[str, Any]) -> List[RuffIssue]:
    """
    Parse JSON output from ruff check command.
    
    Args:
        output: JSON output string from ruff check --output-format json
        config: Configuration dictionary with include/exclude paths
        
    Returns:
        List of linting issues found
    """
    # Parse the JSON output
    issues_data = json.loads(output)
    results: List[RuffIssue] = []
    
    for issue in issues_data:
        file_path = issue.get('filename', '')
            
        # Create structured issue data
        issue_data: RuffIssue = {
            'file': file_path,
            'line': issue.get('location', {}).get('row', 0),
            'column': issue.get('location', {}).get('column', 0),
            'code': issue.get('code', ''),
            'message': issue.get('message', '')
        }
        results.append(issue_data)
    
    return results


def parse_radon_cc_json(output: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse JSON output from radon cc command.
    
    Args:
        output: JSON output string from radon cc --json
        config: Configuration dictionary with include/exclude paths
        
    Returns:
        Dictionary with complexity metrics
    """
    # Parse the JSON output
    cc_data = json.loads(output)
    cc_results: List[RadonCCFunction] = []
    
    # Process each file
    for file_path, functions in cc_data.items():
        # Process each function in the file
        for func in functions:
            # Handle both string and dict inputs
            if isinstance(func, str):
                # For string entries, use defaults
                function_name = "Unknown"
                complexity = 0
                grade = "X" 
                func_type = "function"
            else:
                # Extract data directly from the JSON structure
                function_name = func.get('name', 'Unknown')
                complexity = func.get('complexity', 0)
                grade = func.get('rank', 'X')
                func_type = func.get('type', 'function')
            
            # Create a structured entry for this function
            cc_results.append({
                'file': file_path,
                'function': function_name,
                'grade': grade,
                'complexity': complexity,
                'type': func_type
            })
    
    # Sort by complexity (highest first)
    cc_results = sorted(cc_results, key=lambda x: x['complexity'], reverse=True)
    
    # Count by grade
    cc_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0}
    for result in cc_results:
        if result['grade'] in cc_counts:
            cc_counts[result['grade']] += 1
    
    # Count by file
    cc_files = {}
    for result in cc_results:
        file_path = result['file']
        if file_path not in cc_files:
            cc_files[file_path] = {
                'count': 0,
                'max_complexity': 0,
                'max_grade': 'A',
                'function': ''
            }
        
        cc_files[file_path]['count'] += 1
        
        # Update max complexity for this file if needed
        if result['complexity'] > cc_files[file_path]['max_complexity']:
            cc_files[file_path]['max_complexity'] = result['complexity']
            cc_files[file_path]['max_grade'] = result['grade']
            cc_files[file_path]['function'] = result['function']
    
    # Sort files by max complexity
    cc_files = dict(sorted(cc_files.items(), key=lambda x: x[1]['max_complexity'], reverse=True))
    
    # Return structured data
    return {
        'grade_counts': cc_counts,
        'functions': cc_results,
        'files': cc_files
    }


def parse_radon_mi(output: str, config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse output from radon mi command.
    
    Args:
        output: Output string from radon mi -s
        config: Configuration dictionary with include/exclude paths
        
    Returns:
        List of maintainability metrics for files
    """
    import re
    
    results = []
    
    for line in output.strip().split('\n'):
        if not line.strip():
            continue
            
        parts = line.strip().split(' - ')
        if len(parts) == 2:
            file_path = parts[0].strip()
                
            mi_info = parts[1].strip()
            grade = mi_info[0]
            match = re.search(r'(\d+\.\d+)', mi_info)
            if match:
                score = float(match.group(1))
                results.append({
                    'file': file_path,
                    'grade': grade,
                    'score': score
                })
    
    return sorted(results, key=lambda x: x['score'])