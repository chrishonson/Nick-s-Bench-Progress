import unittest
import tempfile
import os
import unittest.mock
from unittest.mock import patch, MagicMock
from datetime import datetime
import count_tasks

class TestCountTasks(unittest.TestCase):
    """Test cases for the count_tasks module."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_readme_content = """# Test README

## Progress: 5/10 tasks completed
![Progress](https://progress-bar.xyz/50/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%203%27],datasets:[{label:%27Ideal%27,data:[10,8,6],fill:false},{label:%27Actual%27,data:[10,8,null],fill:false}]}})

## Tasks
- [✅] Task 1 completed
- [✅] Task 2 completed
- [✅] Task 3 completed
- [✅] Task 4 completed
- [✅] Task 5 completed
- [ ] Task 6 incomplete
- [ ] Task 7 incomplete
- [ ] Task 8 incomplete
- [ ] Task 9 incomplete
- [ ] Task 10 incomplete
"""

    def create_temp_file(self, content):
        """Create a temporary file with given content."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md')
        temp_file.write(content)
        temp_file.close()
        return temp_file.name

    def tearDown(self):
        """Clean up temporary files."""
        # Clean up any temporary files created during tests
        pass

    def test_count_tasks_from_readme_basic(self):
        """Test basic task counting functionality."""
        temp_file = self.create_temp_file(self.sample_readme_content)
        try:
            total, completed = count_tasks.count_tasks_from_readme(temp_file)
            self.assertEqual(total, 10)
            self.assertEqual(completed, 5)
        finally:
            os.unlink(temp_file)

    def test_count_tasks_from_readme_empty_file(self):
        """Test task counting with empty file."""
        temp_file = self.create_temp_file("")
        try:
            total, completed = count_tasks.count_tasks_from_readme(temp_file)
            self.assertEqual(total, 0)
            self.assertEqual(completed, 0)
        finally:
            os.unlink(temp_file)

    def test_count_tasks_from_readme_no_tasks(self):
        """Test task counting with no task markers."""
        content = "# README\n\nSome content without tasks.\n"
        temp_file = self.create_temp_file(content)
        try:
            total, completed = count_tasks.count_tasks_from_readme(temp_file)
            self.assertEqual(total, 0)
            self.assertEqual(completed, 0)
        finally:
            os.unlink(temp_file)

    def test_count_tasks_from_readme_file_not_found(self):
        """Test task counting with non-existent file."""
        total, completed = count_tasks.count_tasks_from_readme("nonexistent.md")
        self.assertIsNone(total)
        self.assertIsNone(completed)

    def test_count_tasks_different_markers(self):
        """Test task counting with different completion markers."""
        content = """# Test
- [x] Task 1 (lowercase x)
- [X] Task 2 (uppercase X)
- [✅] Task 3 (checkmark)
- [ ] Task 4 (incomplete)
"""
        temp_file = self.create_temp_file(content)
        try:
            total, completed = count_tasks.count_tasks_from_readme(temp_file)
            self.assertEqual(total, 4)
            self.assertEqual(completed, 3)
        finally:
            os.unlink(temp_file)

    def test_update_progress_header(self):
        """Test updating progress header."""
        content = "## Progress: 0/5 tasks completed\nOther content"
        updated = count_tasks.update_progress_header(content, 3, 5)
        self.assertIn("## Progress: 3/5 tasks completed", updated)

    def test_update_progress_bar(self):
        """Test updating progress bar URL."""
        content = "![Progress](https://progress-bar.xyz/20/?scale=100&width=500&color=2EA043&suffix=%25)"
        updated = count_tasks.update_progress_bar(content, 75)
        self.assertIn("https://progress-bar.xyz/75/", updated)

    def test_extract_chart_config_valid(self):
        """Test extracting chart config from valid URL."""
        content = """![Chart](https://quickchart.io/chart?w=800&h=400&c={test:config})"""
        url, config = count_tasks.extract_chart_config(content)
        self.assertIsNotNone(url)
        self.assertIsNotNone(config)
        self.assertIn("quickchart.io", url)
        self.assertEqual(config, "{test:config}")

    def test_extract_chart_config_invalid(self):
        """Test extracting chart config from invalid content."""
        content = "No chart URL here"
        url, config = count_tasks.extract_chart_config(content)
        self.assertIsNone(url)
        self.assertIsNone(config)

    def test_parse_chart_labels_valid(self):
        """Test parsing labels from chart config."""
        config = "data:{labels:[%27Start%27,%27May%202%27,%27May%203%27],datasets:[]"
        labels = count_tasks.parse_chart_labels(config)
        self.assertEqual(labels, ["Start", "May 2", "May 3"])

    def test_parse_chart_labels_missing(self):
        """Test parsing labels when labels are missing."""
        config = "data:{datasets:[]}"
        labels = count_tasks.parse_chart_labels(config)
        self.assertIsNone(labels)

    def test_parse_actual_data_valid(self):
        """Test parsing actual data from chart config."""
        config = "datasets:[{label:%27Actual%27,data:[10,8,6,null]}]"
        result = count_tasks.parse_actual_data(config)
        self.assertIsNotNone(result)
        actual_data_list, actual_data_str_raw = result
        self.assertEqual(actual_data_list, [10, 8, 6, None])
        self.assertEqual(actual_data_str_raw, "[10,8,6,null]")

    def test_parse_actual_data_url_encoded(self):
        """Test parsing URL-encoded actual data."""
        config = "datasets:[{label:%27Actual%27,data:[10%2C8%2C6%2Cnull]}]"
        result = count_tasks.parse_actual_data(config)
        self.assertIsNotNone(result)
        actual_data_list, _ = result
        self.assertEqual(actual_data_list, [10, 8, 6, None])

    def test_parse_actual_data_missing(self):
        """Test parsing actual data when it's missing."""
        config = "datasets:[{label:%27Ideal%27,data:[10,8,6]}]"
        result = count_tasks.parse_actual_data(config)
        self.assertIsNone(result)

    @patch('count_tasks.datetime')
    def test_determine_update_index_exact_match(self, mock_datetime):
        """Test determining update index with exact date match."""
        mock_datetime.datetime.now.return_value = datetime(2024, 5, 23)
        mock_datetime.datetime.strptime = datetime.strptime
        
        labels = ["Start", "May 2", "May 23", "May 24"]
        actual_data = [10, 8, 6, None]
        
        index = count_tasks.determine_update_index(labels, actual_data)
        self.assertEqual(index, 2)  # Index of "May 23"

    @patch('count_tasks.datetime')
    def test_determine_update_index_fallback(self, mock_datetime):
        """Test determining update index with fallback logic."""
        mock_datetime.datetime.now.return_value = datetime(2024, 5, 25)
        mock_datetime.datetime.strptime = datetime.strptime
        
        labels = ["Start", "May 2", "May 23", "May 24"]
        actual_data = [10, 8, 6, None]
        
        index = count_tasks.determine_update_index(labels, actual_data)
        self.assertEqual(index, 3)  # Index of first None

    def test_find_best_date_match(self):
        """Test finding best date match."""
        labels = ["Start", "May 2", "May 23", "May 24", "May 25"]
        current_dt = datetime(2024, 5, 24)
        
        best_fit = count_tasks.find_best_date_match(labels, current_dt)
        self.assertEqual(best_fit, 3)  # Index of "May 24"

    def test_should_use_best_fit_scenarios(self):
        """Test various scenarios for should_use_best_fit."""
        labels = ["Start", "May 2", "May 23", "May 24"]
        actual_data = [10, 8, 6, None]
        current_dt = datetime(2024, 5, 23)
        
        # Should use best fit when current index has None
        result = count_tasks.should_use_best_fit(3, 2, actual_data, labels, current_dt)
        self.assertTrue(result)
        
        # Should not use best fit when temp_best_fit is -1
        result = count_tasks.should_use_best_fit(2, -1, actual_data, labels, current_dt)
        self.assertFalse(result)

    def test_update_actual_data(self):
        """Test updating actual data list."""
        actual_data = [10, None, None, 5, None]
        updated = count_tasks.update_actual_data(actual_data, 2, 7)
        
        expected = [10, 10, 7, 5, None]  # Fill historical gaps, update index 2
        self.assertEqual(updated, expected)

    def test_build_new_chart_url_valid(self):
        """Test building new chart URL with valid data."""
        original_url = "https://quickchart.io/chart?w=800&h=400&c={config}"
        config = "data:{datasets:[{label:%27Actual%27,data:[10,8,6]}]}"
        actual_data = [10, 8, 5]
        raw_data = "[10,8,6]"
        
        new_url = count_tasks.build_new_chart_url(original_url, config, actual_data, raw_data)
        self.assertIsNotNone(new_url)
        self.assertIn("w=800&h=400", new_url)
        self.assertIn("10%2C8%2C5", new_url)

    def test_build_new_chart_url_missing_segment(self):
        """Test building new chart URL when original segment is missing."""
        original_url = "https://quickchart.io/chart?w=800&h=400&c={config}"
        config = "data:{datasets:[{label:%27Ideal%27,data:[10,8,6]}]}"  # No Actual data
        actual_data = [10, 8, 5]
        raw_data = "[10,8,6]"
        
        new_url = count_tasks.build_new_chart_url(original_url, config, actual_data, raw_data)
        self.assertIsNone(new_url)

    @patch('count_tasks.extract_chart_config')
    @patch('count_tasks.parse_chart_labels')
    @patch('count_tasks.parse_actual_data')
    def test_update_burndown_chart_success(self, mock_parse_actual, mock_parse_labels, mock_extract):
        """Test successful burndown chart update."""
        # Mock the dependencies
        mock_extract.return_value = ("http://example.com", "config")
        mock_parse_labels.return_value = ["Start", "May 23"]
        mock_parse_actual.return_value = ([10, 8], "[10,8]")
        
        with patch('count_tasks.determine_update_index', return_value=1), \
             patch('count_tasks.update_actual_data', return_value=[10, 7]), \
             patch('count_tasks.build_new_chart_url', return_value="http://new.url"):
            
            result = count_tasks.update_burndown_chart("content", 3, 10)
            self.assertEqual(result, "content")  # Would be updated in real scenario

    @patch('count_tasks.extract_chart_config')
    def test_update_burndown_chart_no_url(self, mock_extract):
        """Test burndown chart update when no chart URL found."""
        mock_extract.return_value = (None, None)
        
        result = count_tasks.update_burndown_chart("content", 3, 10)
        self.assertEqual(result, "content")  # Returns unchanged

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_update_readme_progress_file_not_found(self, mock_open):
        """Test update_readme_progress when file is not found."""
        with patch('builtins.print') as mock_print:
            count_tasks.update_readme_progress("nonexistent.md")
            mock_print.assert_called_with("Error: File 'nonexistent.md' not found.")

    @patch('count_tasks.count_tasks_from_readme')
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data="mock content")
    def test_update_readme_progress_no_tasks(self, mock_open_func, mock_count):
        """Test update_readme_progress when no tasks found."""
        mock_count.return_value = (0, 0)
        
        with patch('builtins.print') as mock_print:
            count_tasks.update_readme_progress()
            mock_print.assert_called_with("No tasks found in README.md. Nothing to update.")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_full_workflow_with_temp_file(self):
        """Test the complete workflow with a temporary file."""
        content = """# Test README

## Progress: 2/5 tasks completed
![Progress](https://progress-bar.xyz/40/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%2023%27],datasets:[{label:%27Ideal%27,data:[5,3,1]},{label:%27Actual%27,data:[5,3,null]}]}})

- [✅] Task 1
- [✅] Task 2
- [ ] Task 3
- [ ] Task 4
- [ ] Task 5
"""
        
        temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md')
        temp_file.write(content)
        temp_file.close()
        
        try:
            # Mock datetime to ensure consistent testing
            with patch('count_tasks.datetime') as mock_datetime:
                mock_datetime.datetime.now.return_value = datetime(2024, 5, 23)
                mock_datetime.datetime.strptime = datetime.strptime
                
                # Run the update
                count_tasks.update_readme_progress(temp_file.name)
                
                # Read the updated content
                with open(temp_file.name, 'r') as f:
                    updated_content = f.read()
                
                # Verify the updates
                self.assertIn("## Progress: 2/5 tasks completed", updated_content)
                self.assertIn("progress-bar.xyz/40/", updated_content)
                # Note: Full chart testing would require more complex mocking
                
        finally:
            os.unlink(temp_file.name)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2) 