from typing import Dict, Any, List
import requests
from datetime import datetime

def create_appointment(
    loggedin_user_id: str,
    target_user_id: str,
    client_id: str,
    department_id: str,
    location_id: str,
    date: str,
    time: str,
    duration: int,
    appointment_agenda: str,
    creator_name: str,
    status: str,
    user_availability_id: str = None,
    notes: str = None,
    reason: str = None,
    location_name: str = None,
    is_virtual: bool = False,
    meeting_link: str = None
) -> Dict[str, Any]:
    """Create a new appointment"""
    url = 'https://dt1wp7hrm9.execute-api.ap-south-1.amazonaws.com/auth/api/appointment/'
    payload = {
        "loggedin_user_id": loggedin_user_id,
        "target_user_id": target_user_id,
        "client_id": client_id,
        "department_id": department_id,
        "location_id": location_id,
        "date": date,
        "time": time,
        "duration": duration,
        "appointment_agenda": appointment_agenda,
        "creator_name": creator_name,
        "status": status,
        "user_availability_id": user_availability_id,
        "notes": notes,
        "reason": reason,
        "location_name": location_name,
        "is_virtual": is_virtual,
        "meeting_link": meeting_link,
        "is_approved": False,
        "approved_by": None,
        "approved_at": None,
        "tags": [],
        "created_by": loggedin_user_id,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN_HERE'  # This should be replaced with actual token
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def create_task(
    title: str,
    task_type: str,
    task_description: str,
    assigned_to: str,
    start_date: str,
    due_date: str,
    status: str,
    priority: str,
    client_id: str,
    department_id: str,
    location_id: str,
    created_by: str,
    project: str = None,
    milestone: str = None,
    parent_task: str = None,
    tags: List[str] = None,
    observers: List[str] = None,
    attachments: List[str] = None,
    custom_field: Dict[str, Any] = None
) -> Dict[str, Any]:
    """Create a new task"""
    url = 'https://dt1wp7hrm9.execute-api.ap-south-1.amazonaws.com/auth/api/task/'
    payload = {
        "title": title,
        "task_type": task_type,
        "task_description": task_description,
        "assigned_to": assigned_to,
        "start_date": start_date,
        "due_date": due_date,
        "status": status,
        "priority": priority,
        "project": project,
        "milestone": milestone,
        "parent_task": parent_task,
        "tags": tags or [],
        "observers": observers or [],
        "attachments": attachments or [],
        "client_id": client_id,
        "department_id": department_id,
        "location_id": location_id,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "custom_field": custom_field or {}
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_TOKEN_HERE'  # This should be replaced with actual token
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Dictionary mapping function names to their implementations
FUNCTION_IMPLEMENTATIONS = {
    "create_appointment": create_appointment,
    "create_task": create_task
} 