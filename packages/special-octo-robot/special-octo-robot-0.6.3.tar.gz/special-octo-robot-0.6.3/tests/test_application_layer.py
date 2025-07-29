import os
import unittest
from app.constants import path, db_path
from app.utility import convert_time_to_epoch, get_relative_date_string
from app.database import initialize, insert_into_table
from app.application import list_tasks, add_tasks, search_task, get_subtasks, handle_delete, update_task
from datetime import datetime, timedelta

def create_db():
    os.makedirs(path, exist_ok=True)
    if os.path.exists(db_path):
        os.remove(db_path)
    initialize("tasks")

def fill_db():
    add_tasks(title = "Task 1", description="Description 1", priority=1)
    add_tasks(title = "Task 2", description="Description 2", priority=4, today=True)
    add_tasks(title = "Task 3", description="Description 3", priority=2, week=True)
    future_date = datetime.now() + timedelta(days=10)
    add_tasks(title = "Task 4", description="Description 4", priority=3, deadline=future_date.strftime("%Y-%m-%d"))
    add_tasks(title = "Task 5", description="Description 5", priority=5, completed=True)
    add_tasks(title = "Task 6", description="Description 6", inprogress=True)
    add_tasks(title = "Task 7", description="Description 7", pending=True)
    add_tasks(title = "Task 8", priority=3, deadline='2000-09-11')
    add_tasks(title='Child of task 1', parent={"id":1}, label='Label1')
    add_tasks(title='Child of child task 1', parent={"id": 9}, week=True)
    insert_into_table(table="tasks", columns=["title", "completed", "status"], values=["'Task 9'", str(convert_time_to_epoch("2024-08-25")), "'Completed'"])

class ListTasks(unittest.TestCase):
    def test_list_task_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        # Test with no entries in table
        self.assertEqual(list_tasks(), [])

    def test_list_task_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(), [
            {
                    "id": 6,
                    "title": "Task 6",
                    "parent_id": None,
                    "status": "In Progress",
                    "deadline": "None",
                    "priority": 0,
                    "label": "None",
                    "description": "Description 6",
                    "subtasks": 0,
                },
                {
                    "id": 1,
                    "title": "Task 1",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 1,
                    "label": "None",
                    "description": "Description 1",
                    "subtasks": 1,
                },
                {
                    "id": 7,
                    "title": "Task 7",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 0,
                    "label": "None",
                    "description": "Description 7",
                    "subtasks": 0,
                },
                {
                    "id": 8,
                    "title": "Task 8",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "11-09-2000",
                    "priority": 3,
                    "label": "None",
                    "description": "None",
                    "subtasks": 0,
                },
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                },
                {
                    "id": 3,
                    "title": "Task 3",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 2,
                    "label": "None",
                    "description": "Description 3",
                    "subtasks": 0,
                },
                {
                    "id": 4,
                    "title": "Task 4",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "10-09-2024",
                    "priority": 3,
                    "label": "None",
                    "description": "Description 4",
                    "subtasks": 0,
                },
            ]
        )

    def test_list_task_with_priority_and_today(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(priority=1, today=True), [])

    def test_list_task_with_priority(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(priority=1),[
                {
                    "id": 1,
                    "title": "Task 1",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 1,
                    "label": "None",
                    "description": "Description 1",
                    "subtasks": 1,
                }
            ])

    def test_list_task_with_today(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(today=True), [
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                }
            ]
        )

    def test_list_task_with_week(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        self.maxDiff = None

        self.assertEqual(list_tasks(week=True, subtasks=True), [
                {
                    "id": 2,
                    "title": "Task 2",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "31-08-2024",
                    "priority": 4,
                    "label": "None",
                    "description": "Description 2",
                    "subtasks": 0,
                },
                {
                    "id": 3,
                    "title": "Task 3",
                    "parent_id": None,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 2,
                    "label": "None",
                    "description": "Description 3",
                    "subtasks": 0,
                },
                {
                    "id": 10,
                    "title": "Child of child task 1",
                    "parent_id": 9,
                    "status": "Pending",
                    "deadline": "01-09-2024",
                    "priority": 0,
                    "label": "None",
                    "description": "None",
                    "subtasks": 0,
                },
            ]
                         )

    def test_list_task_with_status(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        self.maxDiff = None

        self.assertEqual(list_tasks(inprogress=True, completed=True), [
            {
                "id": 6,
                "title": "Task 6",
                "parent_id": None,
                "status": "In Progress",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 6",
                "subtasks": 0,
            },
            {
                "id": 11,
                "title": "Task 9",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            },
            {
                "id": 5,
                "title": "Task 5",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 5,
                "label": "None",
                "description": "Description 5",
                "subtasks": 0,
            },
            ]
        )

    def test_list_task_with_label(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(list_tasks(label='Label1', subtasks=True), [
                {
                    "id": 9,
                    "title": "Child of task 1",
                    "parent_id": 1,
                    "status": "Pending",
                    "deadline": "None",
                    "priority": 0,
                    "label": "Label1",
                    "description": "None",
                    "subtasks": 1,
                }
            ]
        )
    
    def test_list_task_with_relative_deadline(self) -> None:
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        
        self.assertEqual(list_tasks(date=get_relative_date_string(-6), completed=True), [
                 {
                "id": 11,
                "title": "Task 9",
                "parent_id": None,
                "status": "Completed",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            }
            ]
        )

class AddTasks(unittest.TestCase):
    def test_adding_task_with_single_quotes_in_description(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(add_tasks(title='Dummy Task', description="'Description'"), None)

    def test_adding_task_with_special_characters(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(add_tasks(title='Dummy Task', description="$ / \ "), None)

class SearchTask(unittest.TestCase):
    def test_search_task_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(search_task(1, "tasks"), {})

    def test_search_task_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(search_task(1, "tasks"), {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "Pending",
                "deadline": "None",
                "priority": 1,
                "label": "None",
                "completed": "None",
                "parent_id": None,
                "subtasks": 1,
            }
        )

    def test_search_task_with_invalid_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(search_task(100, "tasks"), {})

class GetSubtasks(unittest.TestCase):
    def test_get_subtasks_with_empty_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()

        self.assertEqual(get_subtasks(1, "tasks"), [])

    def test_get_subtasks_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(
            get_subtasks(1, "tasks"),
            [
                {
                    'id': 9,
                    'title': 'Child of task 1',
                    'status': 'Pending',
                    'deadline': 'None',
                    'priority': 0,
                    'label': 'Label1',
                    'description': 'None',
                    'subtasks': 1,
                    'parent_id': 1
                }
            ]
        )

    def test_get_subtasks_with_invalid_id(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()

        self.assertEqual(get_subtasks(100, "tasks"), [])

class HandleDelete(unittest.TestCase):
    def test_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        # test with valid id
        handle_delete({"id": 1, "parent_id": None}, "tasks")
        self.assertEqual(list_tasks(), [
              {
                "id": 6,
                "title": "Task 6",
                "parent_id": None,
                "status": "In Progress",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 6",
                "subtasks": 0,
            },
            {
                "id": 7,
                "title": "Task 7",
                "parent_id": None,
                "status": "Pending",
                "deadline": "None",
                "priority": 0,
                "label": "None",
                "description": "Description 7",
                "subtasks": 0,
            },
            {
                "id": 8,
                "title": "Task 8",
                "parent_id": None,
                "status": "Pending",
                "deadline": "11-09-2000",
                "priority": 3,
                "label": "None",
                "description": "None",
                "subtasks": 0,
            },
            {
                "id": 2,
                "title": "Task 2",
                "parent_id": None,
                "status": "Pending",
                "deadline": "31-08-2024",
                "priority": 4,
                "label": "None",
                "description": "Description 2",
                "subtasks": 0,
            },
            {
                "id": 3,
                "title": "Task 3",
                "parent_id": None,
                "status": "Pending",
                "deadline": "01-09-2024",
                "priority": 2,
                "label": "None",
                "description": "Description 3",
                "subtasks": 0,
            },
            {
                "id": 4,
                "title": "Task 4",
                "parent_id": None,
                "status": "Pending",
                "deadline": "10-09-2024",
                "priority": 3,
                "label": "None",
                "description": "Description 4",
                "subtasks": 0,
            },
        ])
        self.assertEqual(list_tasks(week=True, subtasks=True), [
            {
                "id": 2,
                "title": "Task 2",
                "parent_id": None,
                "status": "Pending",
                "deadline": "31-08-2024",
                "priority": 4,
                "label": "None",
                "description": "Description 2",
                "subtasks": 0,
            },
            {
                "id": 3,
                "title": "Task 3",
                "parent_id": None,
                "status": "Pending",
                "deadline": "01-09-2024",
                "priority": 2,
                "label": "None",
                "description": "Description 3",
                "subtasks": 0,
            },
        ])

    def test_subtask_deletion(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        # test with subtask id
        handle_delete({"id": 9, "parent_id": 1}, "tasks")
        self.assertEqual(search_task(1, "tasks"), {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "status": "Pending",
                "deadline": "None",
                "priority": 1,
                "label": "None",
                "completed": "None",
                "parent_id": None,
                "subtasks": 0,
            })


class HandleModify(unittest.TestCase):
    def test_cascading_effect_with_filled_db(self):
        # check if DEBUG is set to True
        self.assertTrue(os.environ.get("DEBUG", "") == "True")
        # set test environment
        create_db()
        fill_db()
        task = search_task(1, "tasks")
        task['status'] = 'Completed'
        update_task(task, "tasks")   # cascading update
        self.assertEqual(search_task(1, "tasks"), {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'status': 'Completed', 'deadline': 'None', 'priority': 1, 'label': 'None', 'completed': '31-08-2024', 'parent_id': None, 'subtasks': 1})
        self.assertEqual(get_subtasks(1, "tasks"), [{'id': 9, 'title': 'Child of task 1', 'status': 'Completed', 'deadline': 'None', 'priority': 0, 'label': 'Label1', 'description': 'None', 'subtasks': 1, 'parent_id': 1}])
        self.assertEqual(get_subtasks(9, "tasks"), [{'id': 10, 'title': 'Child of child task 1', 'status': 'Completed', 'deadline': '01-09-2024', 'priority': 0, 'label': 'None', 'description': 'None', 'subtasks': 0, 'parent_id': 9}])


if __name__ == '__main__':
    unittest.main()
