#!/usr/bin/env python3
"""Simple tests for the fixed count_tasks.py script."""

import unittest
import tempfile
import os
from count_tasks import count_tasks_by_date, calculate_burndown_progress

class TestSimple(unittest.TestCase):
    
    def test_no_empty_dates(self):
        """Test that dates with no tasks are not included."""
        readme_content = """
## May 2 — Work Day
- [✅] 1. Task A

## May 5 — Vacation Day
*No work*

## May 6 — More Work
- [✅] 1. Task B
"""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md') as f:
            f.write(readme_content)
            f.flush()
            
            tasks_by_date = count_tasks_by_date(f.name)
            
            # Should only include dates with actual tasks
            self.assertIn("May 2", tasks_by_date)
            self.assertIn("May 6", tasks_by_date)
            self.assertNotIn("May 5", tasks_by_date)  # No tasks on vacation day
            
        os.unlink(f.name)

    def test_burndown_calculation(self):
        """Test basic burndown calculation."""
        tasks_by_date = {
            "May 2": (2, 2),   # 2 completed
            "May 6": (1, 1),   # 1 completed
        }
        
        burndown = calculate_burndown_progress(tasks_by_date, start_tasks=10)
        
        expected = {
            "Start": 10,
            "May 2": 8,    # 10 - 2 = 8
            "May 6": 7     # 8 - 1 = 7
        }
        
        self.assertEqual(burndown, expected)

if __name__ == '__main__':
    unittest.main(verbosity=2) 