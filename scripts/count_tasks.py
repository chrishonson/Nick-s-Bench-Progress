import re
import json
import datetime
import urllib.parse
import argparse
from typing import Tuple, Optional, List, Dict

def count_tasks_from_readme(file_path="README.md"):
    """Count completed and total tasks from README.md file."""
    total_tasks = 0
    completed_tasks = 0
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Regex to find lines starting with "- [ ]" or "- [✅]" or "- [x]" (case-insensitive for x)
                if re.match(r"^- \[[xX✅]\]", line):
                    completed_tasks += 1
                    total_tasks += 1
                elif re.match(r"^- \[[ ]\]", line):
                    total_tasks += 1
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None
    return total_tasks, completed_tasks

def count_tasks_by_date(file_path="README.md") -> Dict[str, Tuple[int, int]]:
    """Count tasks by date section in README.md file."""
    tasks_by_date = {}
    current_date = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # Look for date headers like "## Fri May 2" or "## May 2"
                date_match = re.match(r"^## (?:\w+ )?((?:May|Jun) \d+)", line)
                if date_match:
                    current_date = date_match.group(1).strip()
                    # Don't initialize here - only add when we find actual tasks
                
                # Count tasks under current date
                elif current_date and re.match(r"^- \[", line):
                    # Initialize if not exists
                    if current_date not in tasks_by_date:
                        tasks_by_date[current_date] = (0, 0)
                    total, completed = tasks_by_date[current_date]
                    if re.match(r"^- \[[xX✅]\]", line):
                        tasks_by_date[current_date] = (total + 1, completed + 1)
                    elif re.match(r"^- \[[ ]\]", line):
                        tasks_by_date[current_date] = (total + 1, completed)
    
                # Reset current_date when hitting a non-date header
                elif re.match(r"^##", line) and not date_match:
                    current_date = None
                        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return {}
    
    return tasks_by_date

def update_progress_header(readme_content, completed_tasks, total_tasks):
    """Update the main progress line in README content."""
    new_progress_line = f"## Progress: {completed_tasks}/{total_tasks} tasks completed"
    updated_content = re.sub(r"^## Progress: \d+/\d+ tasks completed", new_progress_line, readme_content, flags=re.MULTILINE)
    return updated_content

def update_progress_bar(readme_content, percentage_completed):
    """Update the progress bar URL in README content."""
    new_progress_bar_url = f"![Progress](https://progress-bar.xyz/{percentage_completed}/?scale=100&width=500&color=2EA043&suffix=%25)"
    updated_content = re.sub(r"^!\[Progress\]\(https://progress-bar\.xyz/.*?%25\)", new_progress_bar_url, readme_content, flags=re.MULTILINE)
    return updated_content

def extract_chart_config(readme_content):
    """Extract chart URL and config from README content."""
    chart_url_match = re.search(r"(https?://quickchart\.io/chart\?w=\d+&h=\d+&c=(.*))\)", readme_content, re.DOTALL)
    if not chart_url_match:
        return None, None
    
    original_chart_url = chart_url_match.group(1)
    chart_config_str = chart_url_match.group(2)
    return original_chart_url, chart_config_str

def parse_chart_labels(chart_config_str):
    """Parse labels array from chart config string."""
    labels_start = chart_config_str.find('labels:[')
    if labels_start == -1:
        return None
    
    labels_start += len('labels:[')
    labels_end = chart_config_str.find(']', labels_start)
    if labels_end == -1:
        return None
    
    labels_str_raw = chart_config_str[labels_start:labels_end]
    decoded_labels = urllib.parse.unquote(labels_str_raw)
    labels_list = [label.strip("'") for label in decoded_labels.split(',')]
    return labels_list

def parse_actual_data(chart_config_str):
    """Parse actual data series from chart config string."""
    actual_data_match = re.search(r"label:%27Actual%27,data:(\[.*?\])", chart_config_str, re.DOTALL)
    if not actual_data_match:
        actual_data_match = re.search(r"label:'Actual',data:(\[.*?\])", chart_config_str, re.DOTALL)
    if not actual_data_match:
        return None
    
    actual_data_str_raw = actual_data_match.group(1)
    actual_data_decoded = urllib.parse.unquote(actual_data_str_raw.strip('[]'))
    actual_data_list_str = [val.strip() for val in actual_data_decoded.split(',')]
    actual_data_list = [int(x) if x != 'null' and x != '' else None for x in actual_data_list_str]
    return actual_data_list, actual_data_str_raw

def calculate_burndown_progress(tasks_by_date: Dict[str, Tuple[int, int]], start_tasks: int = 54) -> Dict[str, int]:
    """Calculate actual burndown progress based on task completion by date."""
    burndown_data = {"Start": start_tasks}
    remaining_tasks = start_tasks
    
    # Sort dates chronologically (simplified - assumes format like "May 2", "May 6", etc.)
    def date_sort_key(date_str):
        try:
            # Handle different date formats
            if "May" in date_str:
                day = int(date_str.replace("May", "").strip())
                return (5, day)  # May = month 5
            elif "Jun" in date_str:
                day = int(date_str.replace("Jun", "").strip())
                return (6, day)  # June = month 6
            else:
                return (0, 0)  # Unknown format
        except:
            return (0, 0)
    
    sorted_dates = sorted([d for d in tasks_by_date.keys() if tasks_by_date[d][1] > 0], key=date_sort_key)
    
    for date in sorted_dates:
        total_tasks, completed_tasks = tasks_by_date[date]
        if completed_tasks > 0:
            remaining_tasks -= completed_tasks
            burndown_data[date] = remaining_tasks
    
    return burndown_data

def update_burndown_chart_accurate(readme_content, tasks_by_date: Dict[str, Tuple[int, int]]):
    """Update the burndown chart with accurate date-based progress."""
    original_chart_url, chart_config_str = extract_chart_config(readme_content)
    if not original_chart_url:
        print("Warning: Burndown chart URL not found. Skipping burndown update.")
        return readme_content
    
    labels_list = parse_chart_labels(chart_config_str)
    if not labels_list:
        print("Warning: Could not parse chart labels. Skipping burndown update.")
        return readme_content
    
    actual_data_result = parse_actual_data(chart_config_str)
    if not actual_data_result:
        print("Warning: Could not parse actual data. Skipping burndown update.")
        return readme_content
    
    actual_data_list, actual_data_str_raw = actual_data_result
    
    # Use the current Start value from the chart, or fall back to 54
    start_tasks = actual_data_list[0] if actual_data_list and actual_data_list[0] is not None else 54
    
    # Calculate accurate burndown progress
    burndown_progress = calculate_burndown_progress(tasks_by_date, start_tasks)
    
    # Update only the data points that correspond to actual completion dates
    updated_actual_data = [None] * len(labels_list)
    
    for i, label in enumerate(labels_list):
        if label in burndown_progress:
            updated_actual_data[i] = burndown_progress[label]
    
    # Build new chart URL
    new_actual_data_str_for_url = '%2C'.join([str(x) if x is not None else 'null' for x in updated_actual_data])
    
    original_actual_data_segment = f"label:%27Actual%27,data:{actual_data_str_raw}"
    new_actual_data_segment = f"label:%27Actual%27,data:[{new_actual_data_str_for_url}]"
    
    if original_actual_data_segment not in chart_config_str:
        print("Warning: Could not find original data segment for replacement.")
        return readme_content
    
    new_chart_config_str = chart_config_str.replace(original_actual_data_segment, new_actual_data_segment)
    
    # Preserve width and height parameters
    width_height_match = re.search(r"\?w=(\d+)&h=(\d+)", original_chart_url)
    if width_height_match:
        width = width_height_match.group(1)
        height = width_height_match.group(2)
        new_chart_url = f"https://quickchart.io/chart?w={width}&h={height}&c={new_chart_config_str}"
    else:
        new_chart_url = f"https://quickchart.io/chart?w=800&h=400&c={new_chart_config_str}"
    
    updated_content = readme_content.replace(original_chart_url, new_chart_url)
    print("Burndown chart updated with accurate date-based progress.")
    return updated_content

def update_burndown_chart(readme_content, completed_tasks, total_tasks):
    """Legacy function - kept for compatibility but now uses task-by-date logic."""
    # For now, fall back to the old logic but with improved validation
    # This should be replaced with calls to update_burndown_chart_accurate
    print("Warning: Using legacy burndown update. Consider using date-based updates.")
    return readme_content

def update_readme_progress(file_path="README.md", use_accurate_burndown=True):
    """Main function to update README progress and burndown chart."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    current_total_tasks, current_completed_tasks = count_tasks_from_readme(file_path)

    if current_total_tasks == 0:
        print("No tasks found in README.md. Nothing to update.")
        return

    percentage_completed = round((current_completed_tasks / current_total_tasks) * 100) if current_total_tasks > 0 else 0

    # Update progress components
    readme_content = update_progress_header(readme_content, current_completed_tasks, current_total_tasks)
    readme_content = update_progress_bar(readme_content, percentage_completed)
    
    if use_accurate_burndown:
        tasks_by_date = count_tasks_by_date(file_path)
        readme_content = update_burndown_chart_accurate(readme_content, tasks_by_date)
    else:
        readme_content = update_burndown_chart(readme_content, current_completed_tasks, current_total_tasks)
    
    print(f"Updated progress header to: {current_completed_tasks}/{current_total_tasks} ({percentage_completed}%)")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"'{file_path}' updated successfully.")
    except IOError:
        print(f"Error: Could not write to file '{file_path}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count tasks in README.md and optionally update it.")
    parser.add_argument("--update", action="store_true", help="Update README.md with current task counts, progress bar, and burndown chart.")
    args = parser.parse_args()

    if args.update:
        update_readme_progress()
    else:
        total, completed = count_tasks_from_readme()
        if total is not None:
            print(f"Total tasks: {total}")
            print(f"Completed tasks: {completed}")
            if total > 0:
                percentage = (completed / total) * 100
                print(f"Percentage completed: {percentage:.2f}%")
            else:
                print("No tasks found to calculate percentage.")
