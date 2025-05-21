from typing import List, Dict, Any

# Function schemas that Gemini can call
FUNCTION_SCHEMAS = [
    {
        "name": "create_appointment",
        "description": "Create a new appointment with specified details",
        "parameters": {
            "type": "object",
            "properties": {
                "loggedin_user_id": {
                    "type": "string",
                    "description": "ID of the user creating the appointment"
                },
                "target_user_id": {
                    "type": "string",
                    "description": "ID of the person being met with"
                },
                "client_id": {
                    "type": "string",
                    "description": "ID of the client organization"
                },
                "department_id": {
                    "type": "string",
                    "description": "ID of the department"
                },
                "location_id": {
                    "type": "string",
                    "description": "ID of the location"
                },
                "user_availability_id": {
                    "type": "string",
                    "description": "ID of the user's availability slot"
                },
                "date": {
                    "type": "string",
                    "description": "Date of the appointment (YYYY-MM-DD)"
                },
                "time": {
                    "type": "string",
                    "description": "Time slot of the appointment (HH:MM-HH:MM)"
                },
                "duration": {
                    "type": "integer",
                    "description": "Duration of the appointment in minutes"
                },
                "appointment_agenda": {
                    "type": "string",
                    "description": "Agenda or purpose of the appointment"
                },
                "creator_name": {
                    "type": "string",
                    "description": "Name of the appointment creator"
                },
                "status": {
                    "type": "string",
                    "description": "Status of the appointment"
                },
                "notes": {
                    "type": "string",
                    "description": "Additional notes for the appointment"
                },
                "reason": {
                    "type": "string",
                    "description": "Reason for the appointment"
                },
                "location_name": {
                    "type": "string",
                    "description": "Name of the location"
                },
                "is_virtual": {
                    "type": "boolean",
                    "description": "Whether the appointment is virtual"
                },
                "meeting_link": {
                    "type": "string",
                    "description": "Link for virtual meeting"
                }
            },
            "required": ["loggedin_user_id", "target_user_id", "client_id", "department_id", "location_id", "date", "time", "duration", "appointment_agenda", "creator_name", "status"]
        }
    },
    {
        "name": "create_task",
        "description": "Create a new task with specified details",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Title of the task"
                },
                "task_type": {
                    "type": "string",
                    "description": "Type of the task"
                },
                "task_description": {
                    "type": "string",
                    "description": "Detailed description of the task"
                },
                "assigned_to": {
                    "type": "string",
                    "description": "ID of the person assigned to the task"
                },
                "start_date": {
                    "type": "string",
                    "description": "Start date and time (ISO format)"
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date and time (ISO format)"
                },
                "status": {
                    "type": "string",
                    "description": "Status of the task"
                },
                "priority": {
                    "type": "string",
                    "description": "Priority level of the task"
                },
                "project": {
                    "type": "string",
                    "description": "Project name"
                },
                "milestone": {
                    "type": "string",
                    "description": "Milestone name"
                },
                "parent_task": {
                    "type": "string",
                    "description": "ID of the parent task"
                },
                "tags": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "description": "Tags associated with the task"
                },
                "client_id": {
                    "type": "string",
                    "description": "ID of the client organization"
                },
                "department_id": {
                    "type": "string",
                    "description": "ID of the department"
                },
                "location_id": {
                    "type": "string",
                    "description": "ID of the location"
                },
                "created_by": {
                    "type": "string",
                    "description": "ID of the task creator"
                }
            },
            "required": ["title", "task_type", "task_description", "assigned_to", "start_date", "due_date", "status", "priority", "client_id", "department_id", "location_id", "created_by"]
        }
    }
] 