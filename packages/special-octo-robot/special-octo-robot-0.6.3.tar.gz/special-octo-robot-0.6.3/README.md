# Devcord

Devcord is a CLI tool designed to help you quickly manage your tasks as well as
help you monitor your time usage. Along with all the essential to-do list functionalities, Devcord allows you to select a task and start a session on it.

During a session, your time-spent on each of your activity is monitored for you to view later. This is useful for people who want to find out where their time is spent.

None of the data is stored on any server, it is all stored locally on your machine.


# Installation

Install Devcord using pip  
``` bash 
pip install --upgrade special-octo-robot
``` 

# Post Installation

To avoid typing devcord repetitively, register an alias in your shell configuration file.

Register an alias for tasks            
``` bash 
alias tasks = "devcord tasks"          
alias task  = "devcord task"
```

# Usage

## For adding tasks

| Description                                 | Command                                  |
|:--------------------------------------------|:------------------------------------------|
| Add a simple task                               | `devcord tasks -a "task name"`<br/> `devcord tasks --add "task name"`                                      |
| Add a task with a description <br/> (Opens scrollable text box to enter description)| `devcord tasks -a "task name" -d` <br /> `devcord tasks --add "task name" --desc`                          |
| Add a task with a due date                      | `devcord tasks -a "task name" -dt "dd/mm/yyyy"`<br /> `devcord tasks --add "task name" --due "dd/mm/yyyy"` |
| Add a task to be completed by today             | `devcord tasks -a "task name" -t`<br /> `devcord tasks --add "task name" --today`                          |
| Add a task to be completed within the current week | `devcord tasks -a "task name" -w` <br /> `devcord tasks --add "task name" --week`                       |
| Add a task with priority (1-5)                  | `devcord tasks -a "task name" -p 3`  <br /> `devcord tasks --add "task name" --priority 3`                 |
| Add a task with labels                          | `devcord tasks -a "task name" -lb "label"` <br /> `devcord tasks --add "task name" --label "label"`        |
| Add a subtask                                   | `devcord tasks -a "task name" -st`<br /> `devcord tasks --add "task name" --subtask`                       |

## For listing tasks

By default, in-progress and pending tasks are listed, with in-progress first followed by pending tasks and completed tasks are skipped.


| Description                                      | Command                                  |
|:-------------------------------------------------|:------------------------------------------|
| Simple List tasks                  | `devcord tasks l`<br/> `devcord tasks --list` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
|List tasks with subtasks	                        |`devcord tasks -l -st` <br/> `devcord tasks --list --subtasks`|
| List tasks by priority                          | `devcord tasks -l -p 3` <br/>`devcord tasks --list --priority 3`               |
| List tasks by label                             | `devcord tasks -l -lb "label"` <br/> `devcord tasks --list --label "label"`    |
| List tasks due today                            | `devcord tasks -l -t` <br/>`devcord tasks --list --today`                      |
| List tasks due in the current week              | `devcord tasks -l -w` <br/> `devcord tasks --list --week`                      |
| List tasks by status                            | `devcord tasks -l -i`<br/>  `devcord tasks --list --completed` <br/> `devcord tasks -l --pending`|
| Specify output format as JSON                   | `devcord tasks -l -o json` <br/> `devcord tasks --list --output text`               |
| Specify output file path                        | `devcord tasks -l --path "path/to/file"` |


## For managing tasks

Pass the keyword to perform required action on the task. The command will then prompt you through a fuzzy finder to enter
the task title. The keyword action would be performed on the selected task.

| Description                                      | Command                                  |
|:-------------------------------------------------|:------------------------------------------|
| View task description <br/> (Opens a scrollable text box with description)| `devcord task -d` <br/>`devcord task --desc` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;                      |
| Show subtasks                                   | `devcord task -st`<br/> `devcord task --subtasks`                                   |
| Mark task as in-progress                        | `devcord task -i`<br/> `devcord task --inprogress`                                  |
| Mark task as complete                           | `devcord task -c` <br/>`devcord task --completed`                                   |
| Mark task as pending                            | `devcord task -pd`<br/> `devcord task --pending`                                    |
| Set deadline to this week                       | `devcord task -w` <br/>`devcord task --week`                                        |  
| Set deadline to today                           | `devcord task -t` <br/>`devcord task --today`                                       |
| Delete task                                     | `devcord task -dl`<br/> `devcord task --delete`                                     |
| Modify task title                               | `devcord task -n "new title"` <br/>`devcord task --name "new title"`                |
| Modify task priority                            | `devcord task -p 3`<br/>  `devcord task --priority 3`                               |
| Modify task deadline                            | `devcord task -dd "dd/mm/yyyy"` <br/>`devcord task --deadline "dd/mm/yyyy"`         |
| Modify task labels                              | `devcord task -lb "label"` <br/>`devcord task --label "label"`                      |
| Modify Completed Task         | `devcord task -ar -n "new title"` <br/>`devcord task --archive --name "new title"`  |


## Jira Integration

With Jira integration you can view all your issues on devcord itself and sync
them as when required with a single command. On your first use instead of the following commands,
you'd be asked to set up your configuration for Jira.

| Description                                      | Command                                  |
|:-------------------------------------------------|:------------------------------------------|
| Sync tasks with Jira                            | `devcord jira --sync`&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|
| Set organization URL for Jira                   | `devcord jira --url`                     |
| Set organization email for Jira                 | `devcord jira --email`                   |
| Set Jira access token                           | `devcord jira --token`                   |

## Miscellaneous

Use Rich Tree:
``` bash
devcord init --pretty_tree False
```

Use Pretty Tree:
``` bash
devcord init --pretty_tree True
```
