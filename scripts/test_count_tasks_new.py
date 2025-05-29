import unittest
import tempfile
import os
from unittest.mock import patch, mock_open
from count_tasks import (
    count_tasks_from_readme,
    count_tasks_by_date,
    calculate_burndown_progress,
    update_progress_header,
    update_progress_bar,
    extract_chart_config,
    parse_chart_labels,
    parse_actual_data,
    update_burndown_chart_accurate,
    update_readme_progress
)

class TestCountTasks(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_readme_content = """# Nick's Bench Progress

## Progress: 28/57 tasks completed
![Progress](https://progress-bar.xyz/49/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27],datasets:[{label:%27Actual%27,data:[54%2C51%2C47]}]}})

## Fri May 2 — Start
- [✅] 1. **Read the AWS Developer Guide**
- [✅] 2. **Udemy kick-off**
- [✅] 3. Create a **Gap List**

## Mon May 5 — Vacation
*Vacation Day*

## Tue May 6 — Storage Focus
- [✅] 1. Udemy Section 4 – IAM & CLI
- [✅] 2. Udemy Section 5 - EC2 Storage
- [ ] 3. Udemy Section 6 – EC2 Storage
- [ ] 4. Complete quizzes

## Wed May 7 — Testing
- [✅] 1. **Udemy Section 10 – VPC**
- [ ] 2. **Udemy Section 7 – ELB**
"""

    def test_count_tasks_from_readme(self):
        """Test basic task counting from README content."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(self.sample_readme_content)
            f.flush()
            
            total, completed = count_tasks_from_readme(f.name)
            
            # Should count: 3 completed + 2 completed + 1 completed = 6 completed
            # Should count: 3 + 4 + 2 = 9 total
            self.assertEqual(completed, 6)
            self.assertEqual(total, 9)
            
        os.unlink(f.name)

    def test_count_tasks_from_readme_file_not_found(self):
        """Test handling of missing file."""
        total, completed = count_tasks_from_readme("nonexistent.md")
        self.assertIsNone(total)
        self.assertIsNone(completed)

    def test_count_tasks_by_date(self):
        """Test counting tasks by date sections."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(self.sample_readme_content)
            f.flush()
            
            tasks_by_date = count_tasks_by_date(f.name)
            
            # Should parse dates correctly
            self.assertIn("May 2", tasks_by_date)
            self.assertIn("May 6", tasks_by_date)
            self.assertIn("May 7", tasks_by_date)
            
            # Check counts for each date
            self.assertEqual(tasks_by_date["May 2"], (3, 3))  # 3 total, 3 completed
            self.assertEqual(tasks_by_date["May 6"], (4, 2))  # 4 total, 2 completed  
            self.assertEqual(tasks_by_date["May 7"], (2, 1))  # 2 total, 1 completed
            
            # May 5 should not have tasks (vacation day)
            self.assertNotIn("May 5", tasks_by_date)
            
        os.unlink(f.name)

    def test_count_tasks_by_date_no_file(self):
        """Test count_tasks_by_date with missing file."""
        result = count_tasks_by_date("nonexistent.md")
        self.assertEqual(result, {})

    def test_calculate_burndown_progress(self):
        """Test burndown progress calculation."""
        tasks_by_date = {
            "May 2": (3, 3),   # 3 completed -> 54-3=51 remaining
            "May 6": (4, 2),   # 2 completed -> 51-2=49 remaining
            "May 7": (2, 1),   # 1 completed -> 49-1=48 remaining
            "May 5": (0, 0),   # No tasks (vacation day)
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=54)
        
        expected = {
            "Start": 54,
            "May 2": 51,
            "May 6": 49, 
            "May 7": 48
        }
        
        self.assertEqual(burndown, expected)
        # May 5 should not appear (no completed tasks)
        self.assertNotIn("May 5", burndown)

    def test_calculate_burndown_progress_empty_input(self):
        """Test burndown calculation with no completed tasks."""
        burndown = calculate_burndown_progress({}, start_tasks=54)
        self.assertEqual(burndown, {"Start": 54})

    def test_calculate_burndown_progress_june_dates(self):
        """Test burndown calculation with June dates."""
        tasks_by_date = {
            "May 30": (2, 2),   # 2 completed
            "Jun 1": (1, 1),    # 1 completed 
            "Jun 3": (3, 3),    # 3 completed
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=54)
        
        expected = {
            "Start": 54,
            "May 30": 52,  # 54-2=52
            "Jun 1": 51,   # 52-1=51
            "Jun 3": 48    # 51-3=48
        }
        
        self.assertEqual(burndown, expected)

    def test_update_progress_header(self):
        """Test updating the progress header."""
        content = "## Progress: 10/20 tasks completed\nOther content"
        updated = update_progress_header(content, 15, 25)
        self.assertIn("## Progress: 15/25 tasks completed", updated)
        self.assertNotIn("## Progress: 10/20 tasks completed", updated)

    def test_update_progress_bar(self):
        """Test updating the progress bar URL."""
        content = "![Progress](https://progress-bar.xyz/50/?scale=100&width=500&color=2EA043&suffix=%25)"
        updated = update_progress_bar(content, 75)
        self.assertIn("https://progress-bar.xyz/75/?scale=100&width=500&color=2EA043&suffix=%25", updated)
        self.assertNotIn("https://progress-bar.xyz/50/", updated)

    def test_extract_chart_config(self):
        """Test extracting chart configuration from README."""
        content = "![Chart](https://quickchart.io/chart?w=800&h=400&c={test:config})"
        url, config = extract_chart_config(content)
        
        self.assertEqual(url, "https://quickchart.io/chart?w=800&h=400&c={test:config}")
        self.assertEqual(config, "{test:config}")

    def test_extract_chart_config_not_found(self):
        """Test handling when chart config is not found."""
        content = "No chart here"
        url, config = extract_chart_config(content)
        
        self.assertIsNone(url)
        self.assertIsNone(config)

    def test_parse_chart_labels(self):
        """Test parsing chart labels from config string."""
        config = "labels:[%27Start%27,%27May%202%27,%27May%206%27]"
        labels = parse_chart_labels(config)
        
        self.assertEqual(labels, ["Start", "May 2", "May 6"])

    def test_parse_chart_labels_not_found(self):
        """Test handling when labels are not found."""
        config = "no labels here"
        labels = parse_chart_labels(config)
        
        self.assertIsNone(labels)

    def test_parse_actual_data(self):
        """Test parsing actual data from config string."""
        config = "label:%27Actual%27,data:[54%2C51%2C47]"
        result = parse_actual_data(config)
        
        self.assertIsNotNone(result)
        actual_data, raw_data = result
        self.assertEqual(actual_data, [54, 51, 47])

    def test_parse_actual_data_with_nulls(self):
        """Test parsing actual data with null values."""
        config = "label:%27Actual%27,data:[54%2C51%2Cnull%2C47]"
        result = parse_actual_data(config)
        
        self.assertIsNotNone(result)
        actual_data, raw_data = result
        self.assertEqual(actual_data, [54, 51, None, 47])

    def test_parse_actual_data_not_found(self):
        """Test handling when actual data is not found."""
        config = "no actual data here"
        result = parse_actual_data(config)
        
        self.assertIsNone(result)

    def test_update_burndown_chart_accurate(self):
        """Test the accurate burndown chart update function."""
        content = """![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27,%27May%207%27],datasets:[{label:%27Actual%27,data:[54%2C51%2Cnull%2Cnull]}]}})"""
        
        tasks_by_date = {
            "May 2": (3, 3),  # 3 completed
            "May 6": (2, 2),  # 2 completed  
        }
        
        updated_content = update_burndown_chart_accurate(content, tasks_by_date)
        
        # Should update with accurate data: Start=54, May 2=51, May 6=49
        self.assertIn("54%2C51%2Cnull%2C49", updated_content)

    def test_update_burndown_chart_accurate_no_chart(self):
        """Test accurate burndown update when no chart is present."""
        content = "No chart here"
        tasks_by_date = {"May 2": (3, 3)}
        
        result = update_burndown_chart_accurate(content, tasks_by_date)
        self.assertEqual(result, content)  # Should return unchanged

    def test_update_burndown_chart_accurate_complex_labels(self):
        """Test burndown update with more complex label matching."""
        content = """![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27,%27May%207%27,%27May%2010%27],datasets:[{label:%27Actual%27,data:[54%2Cnull%2Cnull%2Cnull%2Cnull]}]}})"""
        
        tasks_by_date = {
            "May 2": (3, 3),   # 3 completed -> 54-3=51
            "May 7": (1, 1),   # 1 completed -> 51-1=50  
            # Note: May 6 has no completed tasks, May 10 not in tasks_by_date
        }
        
        updated_content = update_burndown_chart_accurate(content, tasks_by_date)
        
        # Should have: Start=54, May 2=51, May 6=null, May 7=50, May 10=null
        self.assertIn("54%2C51%2Cnull%2C50%2Cnull", updated_content)

class TestDateSorting(unittest.TestCase):
    """Test the date sorting logic in calculate_burndown_progress."""
    
    def test_date_sorting_may_dates(self):
        """Test that May dates are sorted correctly."""
        tasks_by_date = {
            "May 15": (1, 1),
            "May 2": (1, 1), 
            "May 23": (1, 1),
            "May 7": (1, 1),
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=58)
        
        # Check that dates are processed in correct order
        expected_remaining = [58, 57, 56, 55, 54]  # Start, then decreasing by 1 each date
        actual_remaining = list(burndown.values())
        
        self.assertEqual(actual_remaining, expected_remaining)

    def test_date_sorting_mixed_months(self):
        """Test sorting across May and June."""
        tasks_by_date = {
            "Jun 2": (1, 1),
            "May 30": (1, 1),
            "Jun 1": (1, 1),
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=57)
        
        # Should be: Start=57, May 30=56, Jun 1=55, Jun 2=54
        expected_keys = ["Start", "May 30", "Jun 1", "Jun 2"]
        self.assertEqual(list(burndown.keys()), expected_keys)

    def test_date_sorting_edge_cases(self):
        """Test edge cases in date sorting."""
        tasks_by_date = {
            "May 9": (2, 2),
            "May 10": (1, 1),
            "May 1": (3, 3),
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=50)
        
        # Should be sorted: May 1, May 9, May 10
        expected_keys = ["Start", "May 1", "May 9", "May 10"]
        self.assertEqual(list(burndown.keys()), expected_keys)
        
        # Check values
        self.assertEqual(burndown["May 1"], 47)   # 50-3=47
        self.assertEqual(burndown["May 9"], 45)   # 47-2=45
        self.assertEqual(burndown["May 10"], 44)  # 45-1=44

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_full_workflow(self):
        """Test the complete update workflow."""
        readme_content = """# Test Progress

## Progress: 5/10 tasks completed
![Progress](https://progress-bar.xyz/50/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart  
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27],datasets:[{label:%27Actual%27,data:[10%2Cnull%2Cnull]}]}})

## May 2 — First Day
- [✅] 1. Task 1
- [✅] 2. Task 2

## May 6 — Second Day
- [✅] 1. Task 3
- [ ] 2. Task 4
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(readme_content)
            f.flush()
            
            # Test the complete workflow functions
            total, completed = count_tasks_from_readme(f.name)
            tasks_by_date = count_tasks_by_date(f.name)
            burndown = calculate_burndown_progress(tasks_by_date, start_tasks=10)
            
            # Verify results
            self.assertEqual(total, 4)
            self.assertEqual(completed, 3)
            self.assertEqual(tasks_by_date["May 2"], (2, 2))
            self.assertEqual(tasks_by_date["May 6"], (2, 1))
            self.assertEqual(burndown["May 2"], 8)  # 10 - 2 = 8
            self.assertEqual(burndown["May 6"], 7)  # 8 - 1 = 7
            
        os.unlink(f.name)

    def test_update_readme_progress_integration(self):
        """Test the main update function with a realistic example."""
        readme_content = """# Test Progress

## Progress: 2/6 tasks completed
![Progress](https://progress-bar.xyz/33/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart  
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27],datasets:[{label:%27Actual%27,data:[6%2Cnull%2Cnull]}]}})

## May 2 — First
- [✅] 1. Task A
- [✅] 2. Task B
- [ ] 3. Task C

## May 6 — Second  
- [✅] 1. Task D
- [ ] 2. Task E  
- [ ] 3. Task F
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(readme_content)
            f.flush()
            
            # Test the main update function
            update_readme_progress(f.name, use_accurate_burndown=True)
            
            # Read the updated content
            with open(f.name, 'r') as updated_f:
                updated_content = updated_f.read()
            
            # Verify updates
            self.assertIn("## Progress: 3/6 tasks completed", updated_content)
            self.assertIn("https://progress-bar.xyz/50/", updated_content)  # 3/6 = 50%
            
            # Verify burndown chart has been updated
            # Should have: Start=6, May 2=4 (6-2), May 6=3 (4-1)
            self.assertIn("6%2C4%2C3", updated_content)
            
        os.unlink(f.name)

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases."""
    
    def test_count_tasks_empty_sections(self):
        """Test counting tasks with empty date sections."""
        content = """# Test

## May 2 — Empty
## May 6 — Has Tasks  
- [✅] 1. Task 1
- [ ] 2. Task 2
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(content)
            f.flush()
            
            tasks_by_date = count_tasks_by_date(f.name)
            
            # May 2 should not appear (no tasks)
            self.assertNotIn("May 2", tasks_by_date)
            # May 6 should appear
            self.assertIn("May 6", tasks_by_date)
            self.assertEqual(tasks_by_date["May 6"], (2, 1))
            
        os.unlink(f.name)

    def test_malformed_date_headers(self):
        """Test handling of malformed date headers."""
        content = """# Test

## Not A Date
- [✅] 1. Task 1

## May 6 — Valid
- [✅] 1. Task 2

## Another Invalid Header
- [ ] 1. Task 3
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(content)
            f.flush()
            
            tasks_by_date = count_tasks_by_date(f.name)
            
            # Only the valid date should be parsed
            self.assertEqual(len([k for k in tasks_by_date.keys() if tasks_by_date[k][1] > 0]), 1)
            self.assertIn("May 6", tasks_by_date)
            
        os.unlink(f.name)

if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2) 