import re
import json
import datetime
import urllib.parse
import argparse

def count_tasks_from_readme(file_path="README.md"):
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

def update_readme_progress(file_path="README.md"):
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

    # Update main progress line
    new_progress_line = f"## Progress: {current_completed_tasks}/{current_total_tasks} tasks completed"
    readme_content = re.sub(r"^## Progress: \d+/\d+ tasks completed", new_progress_line, readme_content, flags=re.MULTILINE)

    # Update progress bar URL
    new_progress_bar_url = f"![Progress](https://progress-bar.xyz/{percentage_completed}/?scale=100&width=500&color=2EA043&suffix=%25)"
    readme_content = re.sub(r"^!\[Progress\]\(https://progress-bar\.xyz/.*?%25\)", new_progress_bar_url, readme_content, flags=re.MULTILINE)
    print(f"Updated progress header to: {current_completed_tasks}/{current_total_tasks} ({percentage_completed}%)")

    # --- Update Burndown Chart --- 
    chart_url_match = re.search(r"(https?://quickchart\.io/chart\?c=([^{]*\{[^}]*\}))(?=\))", readme_content)
    if not chart_url_match:
        print("Warning: Burndown chart URL not found or in unexpected format in README.md. Skipping burndown update.")
    else:
        original_chart_url = chart_url_match.group(1)
        chart_config_str = chart_url_match.group(2) # The part after c=
        
        # Extract labels (dates)
        labels_match = re.search(r"labels:(\[[^\]]*?\])", chart_config_str)
        if not labels_match:
            print("Warning: Could not find 'labels' in chart URL. Skipping burndown update.")
        else:
            labels_str_raw = labels_match.group(1)
            # Convert URL encoded labels like ['%27Start%27%2C%27May%202%27...] to a Python list of strings
            labels_list = [urllib.parse.unquote(label.strip("\'")) for label in labels_str_raw.strip("[]").split("%2C")]

            # Extract 'Actual' data series
            actual_data_match = re.search(r"label:%27Actual%27,data:(\[[^\]]*?\])", chart_config_str)
            if not actual_data_match:
                print("Warning: Could not find 'Actual' data in chart URL. Skipping burndown update.")
            else:
                actual_data_str_raw = actual_data_match.group(1)
                actual_data_list_str = [val for val in actual_data_str_raw.strip("[]").split("%2C")]
                actual_data_list = [int(x) if x != 'null' and x else None for x in actual_data_list_str]

                if not actual_data_list:
                    print("Warning: 'Actual' data list is empty. Skipping burndown update.")
                else:
                    burndown_start_tasks_actual = actual_data_list[0] if actual_data_list[0] is not None else current_total_tasks # Fallback for safety
                    tasks_remaining_today = burndown_start_tasks_actual - current_completed_tasks

                    current_dt = datetime.datetime.now()
                    target_label_str = current_dt.strftime("%b %-d") # e.g., "May 24"
                    update_index = -1

                    try:
                        update_index = labels_list.index(target_label_str)
                    except ValueError:
                        print(f"Today's exact label '{target_label_str}' not found. Determining best index...")
                        # Fallback: find the first 'null' index, or the last index if no nulls.
                        try:
                            update_index = actual_data_list.index(None) 
                        except ValueError: # No None found
                            update_index = len(actual_data_list) - 1 # Update last point if chart is full
                        
                        # Try to find the latest past date if the chosen index seems too far ahead
                        temp_best_fit = -1
                        for i in range(1, len(labels_list)):
                            try:
                                label_dt = datetime.datetime.strptime(f"{labels_list[i]} {current_dt.year}", "%b %d %Y")
                                if label_dt.date() <= current_dt.date():
                                    temp_best_fit = i
                                else: # First future date
                                    if update_index > i and temp_best_fit != -1 : # If current update_index (e.g. first None) is beyond this first future date.
                                         pass # Keep first None if it makes sense, or use temp_best_fit
                                    break 
                            except ValueError:
                                continue
                        if temp_best_fit != -1 and (update_index == -1 or actual_data_list[update_index] is not None or update_index > temp_best_fit ) : # prefer last known date if current is not good
                           if update_index == -1 or actual_data_list[update_index] is not None or labels_list[update_index] == 'null' : # if update_index is bad
                                update_index = temp_best_fit
                           elif datetime.datetime.strptime(f"{labels_list[update_index]} {current_dt.year}", "%b %d %Y") > current_dt : #if first_none is too far in future
                                update_index = temp_best_fit

                    if update_index == -1 or update_index >= len(actual_data_list) or update_index < 0:
                        print(f"Error: Determined update_index ({update_index}) is invalid for labels list (len {len(labels_list)}). Skipping burndown update.")
                    else:
                        print(f"Updating burndown chart for label: '{labels_list[update_index]}' (index {update_index}) with {tasks_remaining_today} tasks remaining.")
                        
                        # Fill historical Nones and update today's value
                        last_known_val = actual_data_list[0] # Start with the initial value
                        for i in range(1, len(actual_data_list)):
                            if i < update_index:
                                if actual_data_list[i] is None:
                                    actual_data_list[i] = last_known_val
                                elif actual_data_list[i] is not None:
                                     last_known_val = actual_data_list[i]
                            elif i == update_index:
                                actual_data_list[i] = tasks_remaining_today
                                last_known_val = tasks_remaining_today # update for future potential Nones if any
                            elif i > update_index and actual_data_list[i] is None : # future points after today should remain None
                                 actual_data_list[i] = None # Explicitly ensure future points are None
                            # If i > update_index and actual_data_list[i] is not None, leave it as is (e.g. manually forecasted)

                        new_actual_data_str_for_url = '%2C'.join([str(x) if x is not None else 'null' for x in actual_data_list])
                        
                        # Replace only the data part of the 'Actual' series in the config string
                        # This is safer than replacing the whole config string if other parts are complex or change.
                        original_actual_data_segment = f"label:%27Actual%27,data:{actual_data_str_raw}"
                        new_actual_data_segment = f"label:%27Actual%27,data:[{new_actual_data_str_for_url}]"
                        
                        if original_actual_data_segment in chart_config_str:
                            new_chart_config_str = chart_config_str.replace(original_actual_data_segment, new_actual_data_segment)
                            new_chart_url = f"https://quickchart.io/chart?c={new_chart_config_str}" 
                            readme_content = readme_content.replace(original_chart_url, new_chart_url)
                            print("Burndown chart URL updated.")
                        else:
                            print("Warning: Could not find the exact original 'Actual' data segment in chart URL for replacement. Burndown chart not updated.")

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
