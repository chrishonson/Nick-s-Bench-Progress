#!/usr/bin/env python3
"""
Tests for the fixed count_tasks.py script.
Focuses on the core functionality with realistic test cases.
"""

import unittest
import tempfile
import os
from count_tasks import (
    count_tasks_from_readme,
    count_tasks_by_date,
    calculate_burndown_progress,
    update_burndown_chart_accurate
)

class TestFixedScript(unittest.TestCase):
    
    def test_count_tasks_by_date_realistic(self):
        """Test date parsing with realistic README content."""
        readme_content = """# Progress

## Fri May 2 — Start  
- [✅] 1. Task A
- [✅] 2. Task B
- [ ] 3. Task C

## Mon May 5 — Vacation
*No work*

## Tue May 6 — Focus Day
- [✅] 1. Task D
- [✅] 2. Task E

## May 23 — No Day Name
- [✅] 1. Task F
- [ ] 2. Task G

## Not a Date Header
- [ ] 1. Should not count
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(readme_content)
            f.flush()
            
            tasks_by_date = count_tasks_by_date(f.name)
            
            # Verify correct date parsing
            self.assertIn("May 2", tasks_by_date)
            self.assertIn("May 6", tasks_by_date)  
            self.assertIn("May 23", tasks_by_date)
            
            # Verify task counts
            self.assertEqual(tasks_by_date["May 2"], (3, 2))  # 3 total, 2 completed
            self.assertEqual(tasks_by_date["May 6"], (2, 2))  # 2 total, 2 completed
            self.assertEqual(tasks_by_date["May 23"], (2, 1)) # 2 total, 1 completed
            
            # Should not include vacation day or invalid headers
            self.assertNotIn("May 5", tasks_by_date)
            self.assertNotIn("Not a Date Header", tasks_by_date)
            
        os.unlink(f.name)

    def test_calculate_burndown_progress_realistic(self):
        """Test burndown calculation with realistic AWS study progress."""
        tasks_by_date = {
            "May 2": (3, 3),   # 3 completed
            "May 6": (4, 4),   # 4 completed  
            "May 7": (2, 2),   # 2 completed
            "May 16": (2, 2),  # 2 completed
            "May 23": (2, 2),  # 2 completed
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=54)
        
        expected = {
            "Start": 54,
            "May 2": 51,    # 54 - 3 = 51
            "May 6": 47,    # 51 - 4 = 47  
            "May 7": 45,    # 47 - 2 = 45
            "May 16": 43,   # 45 - 2 = 43
            "May 23": 41    # 43 - 2 = 41
        }
        
        self.assertEqual(burndown, expected)

    def test_date_sorting_order(self):
        """Test that dates are sorted chronologically."""
        tasks_by_date = {
            "May 23": (2, 2),
            "May 2": (3, 3),
            "May 16": (1, 1),
            "May 7": (2, 2),
            "Jun 1": (1, 1),
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=50)
        
        # Should be chronological order
        expected_keys = ["Start", "May 2", "May 7", "May 16", "May 23", "Jun 1"]
        self.assertEqual(list(burndown.keys()), expected_keys)
        
        # Check decreasing values
        expected_values = [50, 47, 45, 44, 42, 41]  # Each date subtracts completed tasks
        self.assertEqual(list(burndown.values()), expected_values)

    def test_update_burndown_chart_accurate_simple(self):
        """Test burndown chart update with simple, controlled data."""
        chart_content = """
![Burndown Chart](https://quickchart.io/chart?w=800&h=400&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27],datasets:[{label:%27Actual%27,data:[10%2Cnull%2Cnull]}]}})
"""
        
        tasks_by_date = {
            "May 2": (2, 2),  # 2 completed -> 10-2=8 remaining
            "May 6": (1, 1),  # 1 completed -> 8-1=7 remaining
        }
        
        updated_content = update_burndown_chart_accurate(chart_content, tasks_by_date)
        
        # Should have: Start=10, May 2=8, May 6=7
        self.assertIn("10%2C8%2C7", updated_content)

    def test_edge_case_no_completed_tasks(self):
        """Test behavior when no tasks are completed."""
        tasks_by_date = {
            "May 2": (3, 0),  # No completed tasks
            "May 6": (2, 0),  # No completed tasks
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=54)
        
        # Should only have Start value since no tasks completed
        self.assertEqual(burndown, {"Start": 54})

    def test_mixed_completion_dates(self):
        """Test realistic mixed completion pattern."""
        tasks_by_date = {
            "May 2": (3, 3),   # Full completion
            "May 6": (4, 2),   # Partial completion  
            "May 7": (2, 2),   # Full completion
            "May 10": (3, 0),  # No completion
            "May 15": (1, 1),  # Full completion
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=54)
        
        # Only dates with completed tasks should appear
        expected_keys = ["Start", "May 2", "May 6", "May 7", "May 15"]
        self.assertEqual(list(burndown.keys()), expected_keys)
        
        # Values should decrease by completed count
        expected = {
            "Start": 54,
            "May 2": 51,    # 54 - 3 = 51
            "May 6": 49,    # 51 - 2 = 49
            "May 7": 47,    # 49 - 2 = 47
            "May 15": 46    # 47 - 1 = 46
        }
        self.assertEqual(burndown, expected)

class TestIntegration(unittest.TestCase):
    """Integration tests with realistic AWS study scenarios."""
    
    def test_aws_study_progress_realistic(self):
        """Test with realistic AWS certification study data."""
        readme_content = """# AWS Study Progress

## Progress: 15/30 tasks completed

## Fri May 2 — AWS Basics
- [✅] 1. Read AWS Developer Guide  
- [✅] 2. Setup AWS CLI
- [✅] 3. Create IAM user

## Tue May 6 — EC2 Deep Dive
- [✅] 1. EC2 Instance Types
- [✅] 2. Security Groups
- [ ] 3. Load Balancers
- [ ] 4. Auto Scaling

## Fri May 9 — Lambda Focus
- [✅] 1. Create Hello World Lambda
- [ ] 2. API Gateway Integration

## Mon May 12 — Practice
- [✅] 1. Practice Exam #1
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(readme_content)
            f.flush()
            
            # Test the workflow
            total, completed = count_tasks_from_readme(f.name)
            tasks_by_date = count_tasks_by_date(f.name)
            burndown = calculate_burndown_progress(tasks_by_date, start_tasks=30)
            
                        # Verify counts
            self.assertEqual(total, 10)
            self.assertEqual(completed, 7)  # Fixed: 3+2+1+1 = 7 completed
            
            # Verify date parsing
            expected_dates = ["May 2", "May 6", "May 9", "May 12"]
            for date in expected_dates:
                self.assertIn(date, tasks_by_date)
            
            # Verify burndown progression
            expected_burndown = {
                "Start": 30,
                "May 2": 27,    # 30 - 3 = 27
                "May 6": 25,    # 27 - 2 = 25  
                "May 9": 24,    # 25 - 1 = 24
                "May 12": 23    # 24 - 1 = 23
            }
            self.assertEqual(burndown, expected_burndown)
            
        os.unlink(f.name)

def run_all_tests():
    """Run all tests and print results."""
    print("🧪 Running tests for fixed count_tasks.py script...\n")
    
    # Run tests
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n📊 Test Results:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")  
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("🎉 All tests passed! The script is working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    exit(0 if success else 1) 