# Scripts Documentation

This folder contains scripts for managing and tracking progress in the Nick's Bench Progress project.

## count_tasks.py

A Python script that counts tasks and updates progress tracking in README.md files.

### Features

- **Task Counting**: Counts completed and total tasks from markdown files
- **Progress Updates**: Updates progress headers and progress bars
- **Burndown Chart Integration**: Updates QuickChart burndown charts with current progress
- **Date-aware**: Automatically determines the correct date for chart updates
- **URL Encoding Support**: Handles both plain and URL-encoded chart configurations

### Usage

```bash
# Count tasks only (no modifications)
python3 scripts/count_tasks.py

# Count tasks and update README.md with current progress
python3 scripts/count_tasks.py --update
```

### Architecture

The script has been refactored from a monolithic function into smaller, focused functions:

#### Core Functions

- `count_tasks_from_readme(file_path)` - Counts tasks from markdown file
- `update_readme_progress(file_path)` - Main orchestration function

#### Progress Update Functions

- `update_progress_header(content, completed, total)` - Updates progress header
- `update_progress_bar(content, percentage)` - Updates progress bar URL
- `update_burndown_chart(content, completed, total)` - Updates burndown chart

#### Chart Processing Functions

- `extract_chart_config(content)` - Extracts chart URL and config
- `parse_chart_labels(config)` - Parses date labels from chart
- `parse_actual_data(config)` - Parses actual progress data
- `determine_update_index(labels, data)` - Finds correct date index
- `update_actual_data(data, index, value)` - Updates progress data
- `build_new_chart_url(url, config, data, raw)` - Constructs new chart URL

#### Utility Functions

- `find_best_date_match(labels, current_date)` - Finds best date match
- `should_use_best_fit(...)` - Determines date fallback logic

### Task Format Support

The script recognizes these task completion markers:

- `[✅]` - Checkmark (completed)
- `[x]` - Lowercase x (completed)  
- `[X]` - Uppercase X (completed)
- `[ ]` - Empty (incomplete)

### Example Output

```
Total tasks: 57
Completed tasks: 28
Percentage completed: 49.12%
```

With `--update` flag:
```
Updating burndown chart for 'May 23' with 26 tasks remaining.
Burndown chart URL updated.
Updated progress header to: 28/57 (49%)
'README.md' updated successfully.
```

## test_count_tasks.py

Comprehensive test suite for the count_tasks.py script.

### Test Coverage

- **Unit Tests**: 24 individual function tests
- **Integration Tests**: 2 end-to-end workflow tests
- **Edge Cases**: File not found, empty files, missing data
- **Mocking**: Proper isolation of external dependencies

### Running Tests

```bash
cd scripts
python3 test_count_tasks.py
```

### Test Categories

#### Task Counting Tests
- Basic task counting functionality
- Different completion markers
- Empty files and missing files
- Files without tasks

#### Progress Update Tests  
- Progress header updates
- Progress bar URL updates
- Various percentage scenarios

#### Chart Processing Tests
- Valid and invalid chart configurations
- URL-encoded vs plain text formats
- Missing chart components
- Date matching and fallback logic

#### Integration Tests
- Complete workflow with temporary files
- Date mocking for consistent results
- File I/O operations

### Test Results

All tests should pass:
```
Ran 26 tests in 0.007s

OK
```

## Benefits of Refactoring

### Reduced Complexity
- **Before**: Single function with 8+ levels of nesting
- **After**: 12 focused functions with 1-3 levels of nesting each

### Improved Testability  
- **Before**: Monolithic function difficult to test in isolation
- **After**: Each function can be tested independently

### Better Maintainability
- **Before**: Changes required navigating complex nested logic
- **After**: Clear separation of concerns, easy to modify individual features

### Enhanced Readability
- **Before**: 150+ lines in a single function
- **After**: Functions with clear names and single responsibilities

## File Structure

```
scripts/
├── README.md           # This documentation
├── count_tasks.py      # Main script (refactored)
└── test_count_tasks.py # Test suite
``` 