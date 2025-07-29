import json

import click
import keyring
import requests
from requests.auth import HTTPBasicAuth

import jira.database
from app.application import add_tasks
from app.application import update_task
from app.utility import display_error_message


def update_issues(url, email, table):
    new_issues = fetch_issues(url, email)
    for issue in parse_issues(new_issues):
        old_issue = jira.database.search_task(issue["key"])
        parent = jira.database.search_task(issue["parent"])
        if old_issue:
            old_issue["title"] = issue["key"] + ": " + issue["title"]
            old_issue["priority"] = issue["priority"]
            old_issue["label"] = issue["label"]
            old_issue["parent_id"] = parent.get("id", None)
            old_issue["status"] = issue["status"]
            old_issue["deadline"] = issue["deadline"]
            old_issue["description"] = issue["description"]
            update_task(old_issue, table)

        else:
            add_tasks(
                title=issue["key"] + ": " + issue["title"],
                table=table,
                deadline=issue["deadline"],
                priority=issue["priority"],
                description=issue["description"],
                label=issue["label"],
                parent=parent,
                inprogress=(issue["status"] == "In Progress"),
                pending=(issue["status"] == "Pending"),
                completed=(issue["status"] == "Completed"),
            )


def parse_issues(issues):
    new_issues = []
    for issue in issues:
        issue_details = {
            "key": issue["key"],
            "title": issue["fields"]["summary"],
            "description": issue["fields"]["description"],
            "deadline": issue["fields"].get("duedate", None),
            "priority": int(issue["fields"]["priority"]["id"]),
            "label": issue["fields"]["issuetype"]["name"],
            "parent": issue["fields"].get("parent", {}).get("key", ""),
        }
        if issue["fields"]["status"]["name"] == "Open":
            issue_details["status"] = "Pending"
        elif issue["fields"]["status"]["name"] == "In Progress":
            issue_details["status"] = "In Progress"
        else:
            issue_details["status"] = "Completed"

        new_issues.append(issue_details)
    return new_issues


def fetch_issues(url, email) -> list:
    token = keyring.get_password("devcord", "token")
    if token is None:
        display_error_message(
            'Please provide token, run "devcord jira --token".',
        )
        exit(1)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    auth = HTTPBasicAuth(email, token)
    try:
        response = requests.get(
            url
            + "rest/api/2/search?jql=assignee=currentUser()&fields=summary,status,priority,issuetype,parent,description,duedate",
            headers=headers,
            auth=auth,
            timeout=30,
        )
    except Exception as e:
        display_error_message(
            f"While making request to Jira - {e}",
        )
        exit(1)
    if "application/json" in response.headers.get("Content-Type", ""):
        issues = json.loads(response.text)  # Parse JSON

    else:
        display_error_message(
            "Response from Jira was in-correct. Make sure the token is correct.",
        )
        exit(1)
    return issues["issues"]
