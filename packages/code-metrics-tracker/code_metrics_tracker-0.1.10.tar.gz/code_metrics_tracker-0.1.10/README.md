# Code Metrics Tracker

[![PyPI Version](https://img.shields.io/pypi/v/code-metrics-tracker.svg)](https://pypi.org/project/code-metrics-tracker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/code-metrics-tracker.svg)](https://pypi.org/project/code-metrics-tracker/)

## Why We Built Code Metrics Tracker

Most code quality tools fall into two categories: simple analyzers that provide point-in-time metrics without historical tracking, or complex enterprise platforms that require servers, cloud accounts, and extensive configuration. We built Code Metrics Tracker to fill the gap in between.

### The Problem We Solved

Python developers needed a tool that could:
- Track code quality metrics over time locally without cloud dependencies
- Work seamlessly with git workflows for version-controlled metrics
- Setup in minutes with sensible defaults
- Integrate effortlessly with CI/CD pipelines like GitHub Actions
- Generate reports that live alongside the code

### What Makes Us Different

Unlike enterprise platforms, Code Metrics Tracker:
- **Runs entirely locally** - your code never leaves your machine
- **Zero configuration** - works out of the box with smart defaults
- **Git-native** - metrics are stored in your repository
- **CI/CD ready** - includes GitHub Actions templates
- **Developer-friendly** - simple CLI, markdown reports

Unlike simple analyzers, Code Metrics Tracker:
- **Tracks history** - see how metrics change over time
- **Unified reporting** - combines multiple tools into one view
- **Manages snapshots** - compare any two points in time
- **Automated workflows** - updates metrics on every commit

## What It Does

Code Metrics Tracker combines three industry-standard tools to provide comprehensive analysis:

- **cloc**: Counts lines of code, comments, and blank lines across programming languages
- **Ruff**: Identifies linting issues, code style violations, and potential bugs with fast performance
- **Radon**: Analyzes code complexity (cyclomatic complexity) and maintainability

## What's New in 0.1.10 (May 2025)

- **GitHub Actions**: Updated workflows to use latest action versions (checkout@v4, setup-python@v5, git-auto-commit-action@v5)
- **Documentation**: Added warnings about deprecated GitHub Actions versions that cause workflow failures
- **Installation**: Updated GitHub Actions integration examples with latest versions

## What's New in 0.1.9 (May 2025)

- **Bug Fix**: Fixed cloc command failure when exclude patterns contain wildcards (e.g., `*.db`, `config/*.yaml`)
- **GitHub Actions**: Resolved "cannot specify directory paths" error in CI/CD workflows
- **Pattern Handling**: Improved exclude pattern logic to correctly handle wildcards and file extensions

## What's New in 0.1.6 (May 2025)

- **Improved Detection**: Fixed `--only-on-changes` flag to correctly identify meaningful changes
- **Better Feedback**: Added debug output showing which metrics changed between snapshots
- **Developer UX**: Clear messages when no changes are detected in snapshots
- **JSON Files**: Added "_unchanged" suffix to metrics files when no changes are detected

## What's New in 0.1.5 (May 2025)

- **New Feature**: Added `--only-on-changes` flag to prevent redundant CODE_METRICS.md updates
- **GitHub Actions Efficiency**: Improved GitHub workflow to avoid empty commits
- **Bug Fix**: Fixed an issue with Radon CC JSON parsing where string entries caused errors
- **Improved Stability**: Enhanced parser to handle different formats of Radon output
- **Better Error Handling**: Added specific type checking to prevent AttributeError

## What's New in 0.1.4 (May 2023)

- **Improved JSON Parsing**: All tools now use structured JSON output for better accuracy
- **Accurate Complexity Reporting**: Fixed function complexity display in reports
- **Enhanced Modularity**: New dedicated modules for parsing and snapshot management
- **Type Safety**: Added TypedDict definitions for all metrics data

See the [CHANGELOG.md](CHANGELOG.md) for full details.

## Features

The tracker generates detailed reports focusing on:

- **Lines of code statistics**: Track code volume and distribution by language
- **Linting issues**: Detect and monitor code style, potential bugs, and anti-patterns
- **Cyclomatic complexity**: Identify complex functions and methods that need refactoring
- **Maintainability index**: Measure how maintainable your code is over time

Results are stored in two complementary formats:
1. **JSON snapshots**: Detailed metrics data stored in versioned JSON files for programmatic analysis
2. **Markdown reports**: Human-readable CODE_METRICS.md file that tracks metrics over time with trend indicators

### Perfect For

- **Python teams** who want local control over their metrics
- **Open source projects** that need transparent quality tracking
- **Private codebases** where cloud solutions aren't an option
- **CI/CD workflows** that need automated quality gates
- **Developers** who prefer simplicity over complexity

Key benefits:
- Track code quality trends over time
- Identify problematic areas in the codebase
- Make data-driven refactoring decisions
- Establish quality standards with measurable metrics
- Integrate metrics tracking into CI/CD pipelines

## Installation

### Install from PyPI

```bash
pip install code-metrics-tracker
```

### Install Required Dependencies

The tool relies on three external tools that need to be installed separately:

#### 1. Install cloc

```bash
# macOS
brew install cloc

# Ubuntu/Debian
sudo apt-get install cloc

# Windows
choco install cloc
```

#### 2. Install Ruff and Radon

These are automatically installed as dependencies when you install code-metrics-tracker, but you can also install them directly:

```bash
pip install ruff radon
```

## Quick Start

1. Initialize code quality tracking in your project:

```bash
codeqa init
```

2. Create a code quality snapshot:

```bash
codeqa snapshot
```

3. View the generated CODE_METRICS.md file for detailed metrics.

## Commands

### Command Overview

- `codeqa init` - Initialize code quality tracking in your project
- `codeqa snapshot` - Create a new code quality snapshot and update CODE_METRICS.md
- `codeqa list` - List all available snapshots
- `codeqa compare` - Compare two snapshots to see trends
- `codeqa report` - Generate a standalone report from a snapshot

### Detailed Usage Examples

#### Initialize a Project

The `init` command sets up your project for code quality tracking by:
- Creating a configuration file (`codeqa.json`)
- Creating a metrics storage directory
- Adding a CODE_METRICS.md file if it doesn't exist

```bash
# Basic initialization with default settings
codeqa init

# After initialization, you can edit codeqa.json to customize
# which directories to include/exclude
```

#### Create Metrics Snapshots

The `snapshot` command analyzes your codebase and:
- Runs code statistics with cloc
- Performs linting checks with Ruff
- Analyzes complexity and maintainability with Radon
- Updates CODE_METRICS.md with the latest metrics
- Stores detailed metrics data as a JSON file

```bash
# Create a snapshot with default settings
codeqa snapshot

# Create a snapshot with a custom report title
codeqa snapshot --title "Post-Refactoring Metrics"

# Create a snapshot but only update CODE_METRICS.md if there are meaningful changes
codeqa snapshot --only-on-changes
```

#### List Available Snapshots

The `list` command shows all available snapshots:

```bash
# List all snapshots with their dates and filenames
codeqa list
```

Example output:
```
Available snapshots:
- May 13, 2025 (metrics_20250513_164444.json)
- April 19, 2025 (metrics_20250419_150845.json)
- April 18, 2025 (metrics_20250418_183327.json)
```

#### Compare Snapshots

The `compare` command allows you to track changes between two snapshots:

```bash
# Compare by using snapshot filenames
codeqa compare --first generated/metrics/metrics_20250418_183327.json --second generated/metrics/metrics_20250513_164444.json

# Compare and save the report to a file
codeqa compare --first generated/metrics/metrics_20250418_183327.json --second generated/metrics/metrics_20250513_164444.json --output comparison_report.md

# Compare using indexes from the list command (1-based)
codeqa compare --first 2 --second 1 --output comparison_report.md
```

The comparison report highlights:
- Changes in lines of code
- Changes in linting issues
- Changes in complex functions
- Changes in maintainability
- Trend analysis with percentage changes

#### Generate Standalone Reports

The `report` command generates a standalone report from a specific snapshot:

```bash
# Generate a report from a specific snapshot
codeqa report --snapshot generated/metrics/metrics_20250513_164444.json

# Save the report to a specific file
codeqa report --snapshot generated/metrics/metrics_20250513_164444.json --output quality_report.md

# Generate a report using the snapshot index from the list command (1-based)
codeqa report --snapshot 1 --output quality_report.md
```

The standalone report includes:
- Summary statistics
- Code distribution by language
- Top complex files and functions
- Files with linting issues
- Files with low maintainability

## Output Formats

### CODE_METRICS.md

The main output file is `CODE_METRICS.md`, which contains:

- A header section explaining the metrics
- Historical snapshots with dates
- Summary statistics for each snapshot
- Code statistics by language
- Lists of complex files and functions
- Files with linting issues
- Files with low maintainability
- Trend analysis compared to the previous snapshot
- Analysis of critical issues to address

#### Sample CODE_METRICS.md Excerpt

```markdown
# Code Quality Metrics

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

## Historical Snapshots

### May 13, 2025

#### Summary

| Metric | Value | 
|--------|-------|
| Lines of Code | 123,739 |
| Files | 699 |
| Comments | 35,493 |
| Linting Issues | 376 |
| Cyclomatic Complexity | A:751 B:102 C:253 D:8 E:3 F:346 |
| Maintainability Index | A:215 B:1 C:3 |

#### Analysis
- Critical issues to address:
  - 376 linting issues
  - 610 high complexity functions
  - 3 files with low maintainability
```

### Comparison Reports

Comparison reports highlight changes between snapshots:

```markdown
## Comparison: April 19, 2025 vs May 13, 2025

### Summary

| Metric | April 19, 2025 | May 13, 2025 | Change |
|--------|---------|---------|--------|
| Lines of Code | 26,423 | 123,739 | ↑ 97316 (368.3%) |
| Linting Issues | 296 | 376 | ↑ 80 (27.0%) |
| Complex Functions (C-F) | 474 | 610 | ↑ 136 (28.7%) |
| Low Maintainability Files | 3 | 3 | ↑ 0 (0.0%) |

### Analysis

- Code Size: Increased by 97,316 lines
- Code Quality: Mixed changes
- Most Significant Change: Complex Functions
```

### JSON Data Files

Each snapshot also produces a detailed JSON file containing:

- Complete metrics data
- Timestamp information
- Raw data from all tools (cloc, Ruff, Radon)
- Detailed breakdowns by file and function
- Language statistics

These JSON files can be used for:
- Custom analysis scripts
- Integration with other tools
- Historical data processing
- Visualization dashboards

## Configuration

**Important Note:** Many common patterns are already excluded by the tools themselves (like `.git`, `.venv`, `__pycache__`), so you only need to specify project-specific exclusions.

The tool uses a `codeqa.json` configuration file to control which files and directories are analyzed. Understanding how include and exclude patterns work is crucial for getting accurate metrics that reflect only your project's code.

### Basic Configuration Structure

```json
{
  "include_paths": ["src", "tests"],
  "exclude_patterns": ["migrations", ".coverage", "*.db", "*.log"]
}
```

### How Include and Exclude Patterns Work

Code Metrics Tracker ensures consistent pattern application across all three analysis tools (cloc, Ruff, and Radon) by converting the configuration patterns to each tool's specific format:

#### Pattern Application by Tool

1. **cloc (Code Statistics)**
   - Include paths: Analyzes only the specified directories
   - Exclude patterns are converted to:
     - `--exclude-dir` for directory patterns (e.g., `venv`, `__pycache__`)
     - `--exclude-ext` for file extensions (e.g., `.pyc` becomes `pyc`)

2. **Ruff (Linting)**
   - Include paths: Analyzes only the specified directories
   - Exclude patterns are converted to glob patterns:
     - Directory names become `**/{dir}/**` to match anywhere in the tree
     - File extensions become `*.ext` patterns

3. **Radon (Complexity & Maintainability)**
   - Include paths: Analyzes only the specified directories
   - Exclude patterns are converted to glob patterns:
     - Directory names become `*/{dir}/*` for matching
     - File extensions become `*.ext` patterns

### Pattern Format Guidelines

When creating your configuration, follow these guidelines for effective pattern matching:

1. **Include Paths**
   - Use relative paths from the project root
   - List only the directories containing your source code
   - Common examples: `src`, `lib`, `tests`, `app`

2. **Exclude Patterns**
   - **Simple directory names**: Use just the name (e.g., `venv`, `migrations`)
   - **File extensions**: Include the dot (e.g., `.db`, `.log`)
   - **Specific paths**: Use forward slashes (e.g., `docs/build`)
   - **Complex patterns**: Use standard glob syntax

### What's Already Excluded by Default

Each tool has built-in exclusions, so you don't need to exclude these:

**cloc automatically excludes:**
- Version control directories: `.git`, `.svn`, `.hg`, `.bzr`, `.cvs`
- The `.snapshot` directory
- Many auto-generated files (configure, Makefile.in, etc.)

**Ruff automatically excludes:**
- Version control: `.git`, `.svn`, `.hg`, `.bzr`
- Virtual environments: `.venv`, `venv`, `.direnv`
- Python caches: `__pycache__`, `.mypy_cache`, `.pytype`, `.ruff_cache`
- Build directories: `dist`, `build`, `.eggs`, `__pypackages__`
- Test environments: `.tox`, `.nox`
- Other: `node_modules`, `.pants.d`
- Respects `.gitignore` files by default

**Radon automatically excludes:**
- Hidden directories (starting with `.`)

**You only need to exclude:**
- Project-specific directories (e.g., `migrations`, `static`, `uploads`)
- Non-default virtual environments (e.g., `env`, `.env`)
- Generated files not covered by defaults (e.g., `.coverage`, `htmlcov`)
- Large data files (e.g., `.db`, `.sqlite`, `.pkl`)

### Best Practices for Configuration

#### Effective Configuration Examples

**Standard Python Project:**
```json
{
  "include_paths": [
    "src",
    "tests"
  ],
  "exclude_patterns": [
    "env",           // Non-default virtual env name
    ".env",          // Non-default virtual env name
    ".pytest_cache", // Testing artifacts
    ".coverage",     // Coverage data
    "htmlcov",       // Coverage reports
    "*.egg-info"     // Package metadata
  ]
}
```

**Complex Multi-Package Project:**
```json
{
  "include_paths": [
    "packages/core/src",
    "packages/cli/src",
    "packages/api/src",
    "shared/utils",
    "tests"
  ],
  "exclude_patterns": [
    // Non-default environments
    "env",
    
    // Project-specific
    "site-packages", // Vendored packages
    ".idea",        // IDE files
    ".vscode",      // IDE files
    ".coverage",    // Test coverage
    "docs/_build",  // Built docs
    "htmlcov",      // Coverage reports
    
    // Test data
    "test_data",
    "fixtures",
    "*.db",
    "*.log"
  ]
}
```

### Tips for Accurate Metrics

1. **Start Narrow, Expand Gradually**
   - Begin with your core source directories
   - Add additional paths as needed
   - Monitor the first few snapshots to ensure accuracy

2. **Exclude Generated Code**
   - Migration files (`migrations/`)
   - Auto-generated API clients
   - Compiled or transpiled output
   - Protocol buffer generated files

3. **Exclude Third-Party Code**
   - Vendored dependencies
   - Copied libraries
   - Framework boilerplate
   - Template code

4. **Use Specific Patterns When Needed**
   - For partial exclusions: `tests/fixtures` instead of all `tests`
   - For specific file types: `.spec.js` for test files
   - For nested exclusions: `src/generated` to exclude only generated code in src

5. **Validate Your Configuration**
   - Run `codeqa snapshot --verbose` to see which directories are analyzed
   - Check the first snapshot's file count and language distribution
   - Adjust patterns based on the results

### Common Configuration Patterns

**Python Projects (minimal, non-redundant):**
```json
{
  "exclude_patterns": [
    // Non-default virtual environments
    "env", ".env",
    
    // Project-specific artifacts
    ".pytest_cache", ".coverage", "htmlcov",
    "wheelhouse",    // Wheel storage
    
    // Data files
    "*.db", "*.sqlite", "*.log"
  ]
}
```

**JavaScript/TypeScript Projects:**
```json
{
  "exclude_patterns": [
    // Dependencies (node_modules already excluded by Ruff)
    "bower_components",  // If using Bower
    
    // Build outputs (dist/build already excluded)
    "out", ".next",      // Framework-specific
    
    // Testing
    "coverage", ".nyc_output",
    
    // Caches
    ".cache", ".parcel-cache"
  ]
}
```

### Common Pitfalls to Avoid

1. **Over-broad Exclusions**
   - Don't exclude entire directories if you only need to exclude subdirectories
   - Be specific with patterns to avoid missing important code

2. **Missing Project-Specific Patterns**
   - Don't forget non-default virtual environments (`env`, `.env` if used)
   - Remember project-specific generated files (`.coverage`, `htmlcov`)
   - Include custom build/data directories specific to your project
   - Note: Most common patterns (`.git`, `.venv`, `__pycache__`) are already excluded by the tools

3. **Incorrect Pattern Syntax**
   - File extensions need the dot: `.pyc` not `pyc` in exclude_patterns
   - Use forward slashes (`/`) even on Windows
   - Patterns are case-sensitive

4. **Not Testing Configuration Changes**
   - Always run a snapshot after changing configuration
   - Use the `--verbose` flag to see what's being analyzed
   - Verify metrics match your expectations

### Debugging Configuration Issues

If your metrics seem incorrect:

1. Run with verbose output: `codeqa snapshot --verbose`
2. Check which directories are being analyzed
3. Verify exclude patterns are working correctly
4. Look at the generated JSON file for detailed file lists
5. Adjust patterns and re-run until accurate
```json
{
  "include_paths": ["src", "notebooks", "pipelines", "tests"],
  "exclude_patterns": [
    "data", "models", "outputs", "*.ipynb_checkpoints",
    "*.pkl", "*.h5", "*.parquet", "venv"
  ]
}
```

### Common Pitfalls to Avoid

#### 1. Over-Inclusive Patterns

❌ **Avoid:**
```json
{
  "include_paths": ["."],  // Includes everything, even virtual environments
  "exclude_patterns": []
}
```

✅ **Better:**
```json
{
  "include_paths": ["src", "tests"],
  "exclude_patterns": ["venv", "*.pyc", "__pycache__"]
}
```

#### 2. Missing Virtual Environment Exclusions

❌ **Problem:**
```json
{
  "exclude_patterns": ["pycache"]  // Missing __ prefix
}
```

✅ **Correct:**
```json
{
  "exclude_patterns": ["__pycache__", "venv", ".venv"]
}
```

#### 3. Conflicting Include/Exclude Patterns

❌ **Confusing:**
```json
{
  "include_paths": ["src", "tests"],
  "exclude_patterns": ["src/generated", "tests/fixtures"]
}
```

✅ **Clearer:**
```json
{
  "include_paths": ["src", "tests"],
  "exclude_patterns": ["*/generated", "*/fixtures", "*/test_data"]
}
```

#### 4. Platform-Specific Paths

❌ **Windows-specific:**
```json
{
  "exclude_patterns": ["src\\temp", "tests\\data"]
}
```

✅ **Cross-platform:**
```json
{
  "exclude_patterns": ["src/temp", "tests/data", "*/temp", "*/data"]
}
```

### Examples of Effective Configurations

#### Monorepo with Multiple Services

```json
{
  "include_paths": [
    "services/api",
    "services/worker",
    "services/gateway",
    "shared/lib",
    "shared/utils"
  ],
  "exclude_patterns": [
    "*/coverage",           // Test coverage reports
    "*.log",                // Log files
    "services/deprecated",  // Deprecated code
    "*/migrations",         // Database migrations
    "*/uploads",            // User uploads
    "*.db"                  // Database files
  ]
}
```

#### Library with Examples and Docs

```json
{
  "include_paths": [
    "src",
    "tests"
  ],
  "exclude_patterns": [
    "examples",      // Example code not part of the library
    "docs",          // Documentation
    "benchmarks",    // Performance testing
    "scripts",       // Build/deploy scripts
    "*.egg-info",    // Package metadata
    ".coverage",     // Test coverage data
    "htmlcov"        // Coverage reports
  ]
}
```

#### Microservice with Docker

```json
{
  "include_paths": [
    "app",
    "tests",
    "migrations"
  ],
  "exclude_patterns": [
    "docker",        // Docker configurations
    "k8s",           // Kubernetes manifests
    ".dockerignore",
    "volumes",       // Docker volumes
    "*.log",         // Log files
    "coverage.xml",  // Coverage report
    ".coverage",     // Coverage data
    "*.db",          // Database files
    "uploads"        // User uploaded files
  ]
}
```

### Debugging Pattern Matching

If you're unsure whether your patterns are working correctly:

1. **Check Generated Metrics**: Look at the files being analyzed in the JSON output
2. **Use Verbose Mode**: Some tools provide verbose output showing excluded files
3. **Test Incrementally**: Start with minimal patterns and add exclusions as needed
4. **Review Tool Documentation**: Each tool may have specific pattern syntax requirements

### Pattern Precedence

When there's a conflict between include and exclude patterns:
- **Exclude patterns generally take precedence** over include patterns
- More specific patterns override more general ones
- Tool-specific behaviors may vary (check individual tool documentation)

By carefully configuring your include and exclude patterns, you can ensure that codeqa provides accurate metrics that truly reflect your project's code quality, excluding third-party dependencies and generated files that might skew the results.

## GitHub Actions Integration

Add this to your GitHub Actions workflow to automatically track code quality metrics:

```yaml
name: Code Quality Metrics

on:
  push:
    branches: [ main ]

jobs:
  code-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - name: Install cloc
        run: sudo apt-get install -y cloc
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install code-metrics-tracker
      - name: Generate code quality snapshot
        run: codeqa snapshot --only-on-changes  # Only update if there are meaningful changes
      - name: Commit updated CODE_METRICS.md
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "Update code quality metrics"
          file_pattern: CODE_METRICS.md generated/metrics/*
```

### Important: Use Latest Action Versions

**Always use the latest versions of GitHub Actions** to avoid deprecation warnings and security issues:

- ✅ `actions/checkout@v4` (not v3)
- ✅ `actions/setup-python@v5` (not v4) 
- ✅ `stefanzweifel/git-auto-commit-action@v5` (not v4)

Using deprecated versions like `actions/checkout@v3` or `actions/upload-artifact@v3` will cause workflow failures with messages like:
```
This request has been automatically failed because it uses a deprecated version of `actions/upload-artifact: v3`.
```

The template above uses the latest stable versions as of 2025.

## Development Guide

### Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/AgileWorksZA/codeqa.git
cd codeqa
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install build twine
```

### Creating a New Release

1. Update version numbers in both files:
   - `setup.py` - Update the `version` parameter
   - `codeqa/__init__.py` - Update the `__version__` variable

2. Update the README.md with any new features or changes

3. Build the package:
```bash
rm -rf dist/ build/ *.egg-info/
python -m build
```

4. Test the package locally:
```bash
pip install dist/*.whl
```

### Publishing to PyPI

1. Install publishing tools if you haven't already:
```bash
pip install twine
```

2. Create a `.pypirc` file in your home directory with your PyPI credentials:
```ini
[pypi]
username = your_username
password = your_password
```

3. Upload to PyPI:
```bash
python -m twine upload dist/*
```

4. Alternatively, use a token for authentication:
```bash
python -m twine upload --username __token__ --password your-pypi-token dist/*
```

5. Verify the package is available on PyPI:
https://pypi.org/project/code-metrics-tracker/

## License

MIT