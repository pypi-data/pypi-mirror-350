#!/usr/bin/env python3
"""
Main CLI entry point for the CodeQA tool.
"""

import argparse
import sys
from .metrics import (
    create_snapshot,
    update_metrics_file,
    list_snapshots,
    compare_snapshots,
    create_report,
    init_project
)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(description='Generate and analyze code quality metrics')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Init command
    init_parser = subparsers.add_parser('init', 
        help='Initialize code quality tracking in your project')
    init_parser.add_argument('--config', help='Path to a custom config file')
    
    # Snapshot command
    snapshot_parser = subparsers.add_parser('snapshot', 
        help='Create a new code quality snapshot and update CODE_METRICS.md')
    snapshot_parser.add_argument('--config', help='Path to a custom config file')
    snapshot_parser.add_argument('--verbose', action='store_true', help='Print detailed information during processing')
    snapshot_parser.add_argument('--only-on-changes', action='store_true', 
        help='Only update CODE_METRICS.md if significant changes detected since last snapshot')
    
    # List command
    subparsers.add_parser('list', 
        help='List all available snapshots')
    
    # Compare command
    compare_parser = subparsers.add_parser('compare', 
        help='Compare two snapshots to see changes')
    compare_parser.add_argument('--first', required=True, 
        help='First (older) snapshot file or index from list command (1-based)')
    compare_parser.add_argument('--second', required=True, 
        help='Second (newer) snapshot file or index from list command (1-based)')
    compare_parser.add_argument('--output', 
        help='Output file for comparison report (default: print to console)')
    
    # Report command
    report_parser = subparsers.add_parser('report', 
        help='Generate a standalone report from a snapshot')
    report_parser.add_argument('--snapshot', required=True, 
        help='Snapshot file or index from list command (1-based)')
    report_parser.add_argument('--output', 
        help='Output file for report (default: print to console)')
    
    args = parser.parse_args()
    
    # If no command is specified, print help and exit
    if args.command is None:
        parser.print_help()
        return 0
    
    if args.command == 'init':
        # Initialize project
        config_path = args.config if hasattr(args, 'config') else None
        init_project(config_path)
        return 0
    
    elif args.command == 'snapshot':
        # Create snapshot
        config_path = args.config if hasattr(args, 'config') else None
        only_on_changes = args.only_on_changes if hasattr(args, 'only_on_changes') else False
        
        snapshot, json_path, unchanged = create_snapshot(
            config_path=config_path,
            verbose=args.verbose if hasattr(args, 'verbose') else False,
            only_on_changes=only_on_changes
        )
        
        # Only update the metrics file if we have changes or if the flag is not set
        if unchanged and only_on_changes:
            print("Snapshot created but CODE_METRICS.md not updated (no significant changes)")
            return 0
        elif update_metrics_file(snapshot):
            print("Snapshot added to CODE_METRICS.md")
            print(f"Detailed metrics saved to {json_path}")
            return 0
        else:
            print("Failed to update metrics file")
            return 1
            
    elif args.command == 'list':
        # List snapshots
        list_snapshots()
        return 0
        
    elif args.command == 'compare':
        # Get snapshots list
        snapshots = list_snapshots(silent=True)
        
        # Resolve snapshot paths
        first_path = args.first
        second_path = args.second
        
        # Check if numeric indices were provided
        try:
            if first_path.isdigit() and int(first_path) <= len(snapshots):
                first_path = snapshots[int(first_path) - 1]['file']
            if second_path.isdigit() and int(second_path) <= len(snapshots):
                second_path = snapshots[int(second_path) - 1]['file']
        except (ValueError, IndexError):
            print("Invalid snapshot index")
            return 1
        
        # Generate comparison report
        report = compare_snapshots(first_path, second_path)
        if report is None:
            print("Failed to generate comparison report")
            return 1
        
        # Output report
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Comparison report saved to {args.output}")
        else:
            print(report)
        
        return 0
        
    elif args.command == 'report':
        # Get snapshots list
        snapshots = list_snapshots(silent=True)
        
        # Resolve snapshot path
        snapshot_path = args.snapshot
        
        # Check if numeric index was provided
        try:
            if snapshot_path.isdigit() and int(snapshot_path) <= len(snapshots):
                snapshot_path = snapshots[int(snapshot_path) - 1]['file']
        except (ValueError, IndexError):
            print("Invalid snapshot index")
            return 1
        
        # Generate report
        report = create_report(snapshot_path)
        if report is None:
            print("Failed to generate report")
            return 1
        
        # Output report
        if args.output:
            with open(args.output, 'w') as f:
                f.write(report)
            print(f"Report saved to {args.output}")
        else:
            print(report)
        
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())