import re
import json
import datetime
import urllib.parse
import argparse

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

def determine_update_index(labels_list, actual_data_list):
    """Determine which index to update in the burndown chart."""
    current_dt = datetime.datetime.now()
    target_label_str = current_dt.strftime("%b %-d")  # e.g., "May 24"
    
    try:
        return labels_list.index(target_label_str)
    except ValueError:
        # Fallback: find the first 'null' index, or the last index if no nulls
        try:
            update_index = actual_data_list.index(None)
        except ValueError:
            update_index = len(actual_data_list) - 1
        
        # Try to find the latest past date
        temp_best_fit = find_best_date_match(labels_list, current_dt)
        if temp_best_fit != -1 and should_use_best_fit(update_index, temp_best_fit, actual_data_list, labels_list, current_dt):
            update_index = temp_best_fit
        
        return update_index

def find_best_date_match(labels_list, current_dt):
    """Find the best matching date index for today's date."""
    temp_best_fit = -1
    for i in range(1, len(labels_list)):
        try:
            label_dt = datetime.datetime.strptime(f"{labels_list[i]} {current_dt.year}", "%b %d %Y")
            if label_dt.date() <= current_dt.date():
                temp_best_fit = i
            else:
                break
        except ValueError:
            continue
    return temp_best_fit

def should_use_best_fit(update_index, temp_best_fit, actual_data_list, labels_list, current_dt):
    """Determine if we should use the best fit date instead of the current update index."""
    if temp_best_fit == -1:
        return False
    
    if update_index == -1 or actual_data_list[update_index] is not None or update_index > temp_best_fit:
        if update_index == -1 or actual_data_list[update_index] is not None or labels_list[update_index] == 'null':
            return True
        try:
            if datetime.datetime.strptime(f"{labels_list[update_index]} {current_dt.year}", "%b %d %Y") > current_dt:
                return True
        except ValueError:
            pass
    
    return False

def update_actual_data(actual_data_list, update_index, tasks_remaining_today):
    """Update the actual data list with today's progress and fill historical gaps."""
    last_known_val = actual_data_list[0]
    
    for i in range(1, len(actual_data_list)):
        if i < update_index:
            if actual_data_list[i] is None:
                actual_data_list[i] = last_known_val
            elif actual_data_list[i] is not None:
                last_known_val = actual_data_list[i]
        elif i == update_index:
            actual_data_list[i] = tasks_remaining_today
            last_known_val = tasks_remaining_today
        elif i > update_index and actual_data_list[i] is None:
            actual_data_list[i] = None
    
    return actual_data_list

def build_new_chart_url(original_chart_url, chart_config_str, actual_data_list, actual_data_str_raw):
    """Build the new chart URL with updated data."""
    new_actual_data_str_for_url = '%2C'.join([str(x) if x is not None else 'null' for x in actual_data_list])
    
    original_actual_data_segment = f"label:%27Actual%27,data:{actual_data_str_raw}"
    new_actual_data_segment = f"label:%27Actual%27,data:[{new_actual_data_str_for_url}]"
    
    if original_actual_data_segment not in chart_config_str:
        return None
    
    new_chart_config_str = chart_config_str.replace(original_actual_data_segment, new_actual_data_segment)
    
    # Preserve width and height parameters
    width_height_match = re.search(r"\?w=(\d+)&h=(\d+)", original_chart_url)
    if width_height_match:
        width = width_height_match.group(1)
        height = width_height_match.group(2)
        new_chart_url = f"https://quickchart.io/chart?w={width}&h={height}&c={new_chart_config_str}"
    else:
        new_chart_url = f"https://quickchart.io/chart?w=800&h=400&c={new_chart_config_str}"
    
    return new_chart_url

def update_burndown_chart(readme_content, completed_tasks, total_tasks):
    """Update the burndown chart in README content."""
    original_chart_url, chart_config_str = extract_chart_config(readme_content)
    if not original_chart_url:
        print("Warning: Burndown chart URL not found or in unexpected format in README.md. Skipping burndown update.")
        return readme_content
    
    labels_list = parse_chart_labels(chart_config_str)
    if not labels_list:
        print("Warning: Could not find 'labels' in chart URL. Skipping burndown update.")
        return readme_content
    
    actual_data_result = parse_actual_data(chart_config_str)
    if not actual_data_result:
        print("Warning: Could not find 'Actual' data in chart URL. Skipping burndown update.")
        return readme_content
    
    actual_data_list, actual_data_str_raw = actual_data_result
    
    if not actual_data_list:
        print("Warning: 'Actual' data list is empty. Skipping burndown update.")
        return readme_content
    
    burndown_start_tasks_actual = actual_data_list[0] if actual_data_list[0] is not None else total_tasks
    tasks_remaining_today = burndown_start_tasks_actual - completed_tasks
    
    update_index = determine_update_index(labels_list, actual_data_list)
    
    if update_index == -1 or update_index >= len(actual_data_list) or update_index < 0:
        print(f"Error: Determined update_index ({update_index}) is invalid for labels list (len {len(labels_list)}). Skipping burndown update.")
        return readme_content
    
    print(f"Updating burndown chart for '{labels_list[update_index]}' with {tasks_remaining_today} tasks remaining.")
    
    updated_actual_data = update_actual_data(actual_data_list, update_index, tasks_remaining_today)
    new_chart_url = build_new_chart_url(original_chart_url, chart_config_str, updated_actual_data, actual_data_str_raw)
    
    if not new_chart_url:
        print("Warning: Could not find the exact original 'Actual' data segment in chart URL for replacement. Burndown chart not updated.")
        return readme_content
    
    updated_content = readme_content.replace(original_chart_url, new_chart_url)
    print("Burndown chart URL updated.")
    return updated_content

def update_readme_progress(file_path="README.md"):
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
