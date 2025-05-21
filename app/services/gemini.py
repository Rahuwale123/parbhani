import requests
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from ..config import settings
from .function_schemas import FUNCTION_SCHEMAS
from .functions import FUNCTION_IMPLEMENTATIONS
from .system_prompt import SYSTEM_PROMPT

class GeminiService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        self.headers = {
            "Content-Type": "application/json"
        }
        # Store conversation history for each user
        self.conversation_history: Dict[str, List[Dict[str, str]]] = {}
        # Store user context (name, preferred language, etc.)
        self.user_context: Dict[str, Dict[str, str]] = {}

    def _get_user_history(self, userid: str) -> List[Dict[str, str]]:
        """Get conversation history for a user"""
        return self.conversation_history.get(userid, [])

    def _add_to_history(self, userid: str, role: str, content: str):
        """Add a message to user's conversation history"""
        if userid not in self.conversation_history:
            self.conversation_history[userid] = []
        self.conversation_history[userid].append({"role": role, "content": content})
        # Keep only last 10 messages to prevent context window issues
        self.conversation_history[userid] = self.conversation_history[userid][-10:]

    def _update_user_context(self, userid: str, message: str):
        """Update user context based on the message"""
        if userid not in self.user_context:
            self.user_context[userid] = {
                "name": None,
                "preferred_language": None
            }
        
        # Detect language
        if any(char in message for char in ['ा', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']):
            self.user_context[userid]["preferred_language"] = "Marathi"
        elif any(char in message for char in ['ा', 'ी', 'ु', 'ू', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः', '़']):
            self.user_context[userid]["preferred_language"] = "Hindi"
        else:
            self.user_context[userid]["preferred_language"] = "English"

        # Try to extract name if not already set
        if not self.user_context[userid]["name"]:
            # Look for name in conversation history
            for msg in self._get_user_history(userid):
                if "my name is" in msg["content"].lower() or "माझं नाव" in msg["content"] or "मेरा नाम" in msg["content"]:
                    # Extract name from the message
                    words = msg["content"].split()
                    for i, word in enumerate(words):
                        if word.lower() in ["is", "नाव", "नाम"] and i + 1 < len(words):
                            self.user_context[userid]["name"] = words[i + 1]
                            break

    def _get_smart_defaults(self, function_name: str, userid: str, message: str) -> Dict[str, Any]:
        """Generate smart defaults for tasks and appointments"""
        user_context = self.user_context.get(userid, {})
        user_name = user_context.get("name", "User")
        
        if function_name == "create_task":
            return {
                "assigned_to": user_name,
                "created_by": user_name,
                "status": "pending"
            }

        elif function_name == "create_appointment":
            return {
                "client_name": user_name,
                "status": "scheduled"
            }

        return {}

    def process_message(self, message: str, userid: str) -> str:
        """
        Process a message and return a response
        """
        try:
            # Print user message
            print(f"\nUser {userid}: {message}")

            # Update user context
            self._update_user_context(userid, message)

            # Add user message to history
            self._add_to_history(userid, "user", message)

            # Get user's conversation history
            history = self._get_user_history(userid)
            
            # Prepare conversation context
            conversation_context = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in history
            ])

            # Get user context
            user_context = self.user_context.get(userid, {})
            user_name = user_context.get("name", "User")
            preferred_language = user_context.get("preferred_language", "English")

            # Prepare the request payload
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"{SYSTEM_PROMPT}\n\nUser Context:\n- Name: {user_name}\n- Preferred Language: {preferred_language}\n\nConversation History:\n{conversation_context}\n\nUser (ID: {userid}): {message}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 1024,
                },
                "tools": [{
                    "functionDeclarations": FUNCTION_SCHEMAS
                }]
            }

            # Make the API request
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=self.headers,
                json=payload
            )

            if response.status_code != 200:
                error_response = "I apologize, but I'm having trouble processing your request right now. Please try again later."
                self._add_to_history(userid, "assistant", error_response)
                print(f"Assistant: {error_response}")
                return error_response

            response_data = response.json()
            
            # Check for function calls in the response
            if "candidates" in response_data and response_data["candidates"]:
                candidate = response_data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "functionCall" in part:
                            function_call = part["functionCall"]
                            function_name = function_call["name"]
                            function_args = function_call["args"]
                            
                            # Get smart defaults and merge with provided args
                            defaults = self._get_smart_defaults(function_name, userid, message)
                            function_args = {**defaults, **function_args}
                            
                            # Execute the function if it exists
                            if function_name in FUNCTION_IMPLEMENTATIONS:
                                function_result = FUNCTION_IMPLEMENTATIONS[function_name](**function_args)
                                
                                # Special handling for nearby services
                                if function_name == "get_nearby_services":
                                    # Pass the function result back to Gemini for formatting
                                    format_payload = {
                                        "contents": [{
                                            "parts": [{
                                                "text": f"""{SYSTEM_PROMPT}

Here is the raw function response for nearby services. Please format it into a natural, empathetic response that:
1. Shows concern for the user's condition
2. Provides immediate self-care advice
3. Suggests ONLY ONE most relevant service (usually the closest or most specialized)
4. Offers to help book an appointment
5. Uses appropriate emojis and friendly tone

IMPORTANT: 
- NEVER list multiple services unless the user specifically asks for more options
- ALWAYS choose the single most relevant service based on:
  * Closest distance
  * Most appropriate specialization
  * Best availability
  * Highest rating (if available)
- If multiple services are found, only mention the best one

For example, if the user has a stomach pain, format it like:
"Oh no, stomach pains can be from stress, dehydration, or even eye strain. Try drinking some water, resting in a quiet place, and maybe massaging your temples. If it's still bothering you, I found a neurologist nearby — Dr. Sneha Patil at Shivaji Nagar Clinic, Parbhani (9823111122). Want me to book an appointment for you? 😊"

If the user says yes to booking an appointment, first ask for their details like:
"I'll help you book an appointment. First, I need a few details:
1. What's your name?
2. Which day would you prefer? The doctor is available on:
   - Monday: 10 AM to 2 PM
   - Wednesday: 2 PM to 6 PM
   - Friday: 11 AM to 3 PM
3. What time would work best for you?"

After getting the details, then confirm the appointment like:
"🎉 Perfect! I'll book your appointment with Dr. [Name] at [Hospital] for [Date] at [Time]. Just to confirm:
- Your name: [User's name]
- Date: [Selected date]
- Time: [Selected time]
- Purpose: [User's condition]

Is this correct? I can proceed with the booking once you confirm. 😊"

Here is the raw function response to format:
{json.dumps(function_result, indent=2)}"""
                                            }]
                                        }],
                                        "generationConfig": {
                                            "temperature": 0.7,
                                            "topK": 40,
                                            "topP": 0.95,
                                            "maxOutputTokens": 1024,
                                        }
                                    }
                                else:
                                    # For other functions, use the original response
                                    format_payload = {
                                        "contents": [{
                                            "parts": [{
                                                "text": f"Here is the raw function response. Please format it into a natural, user-friendly response with emojis and clear formatting:\n\n{json.dumps(function_result, indent=2)}"
                                            }]
                                        }],
                                        "generationConfig": {
                                            "temperature": 0.7,
                                            "topK": 40,
                                            "topP": 0.95,
                                            "maxOutputTokens": 1024,
                                        }
                                    }
                                
                                # Get formatted response from Gemini
                                format_response = requests.post(
                                    f"{self.api_url}?key={self.api_key}",
                                    headers=self.headers,
                                    json=format_payload
                                )
                                
                                if format_response.status_code == 200:
                                    format_data = format_response.json()
                                    if "candidates" in format_data and format_data["candidates"]:
                                        formatted_text = format_data["candidates"][0]["content"]["parts"][0].get("text", str(function_result))
                                        self._add_to_history(userid, "assistant", formatted_text)
                                        print(f"Assistant: {formatted_text}")
                                        return formatted_text
                                
                                # Fallback to raw function result if formatting fails
                                self._add_to_history(userid, "assistant", str(function_result))
                                print(f"Assistant: {function_result}")
                                return str(function_result)
            
            # If no function call, return the text response
            if "candidates" in response_data and response_data["candidates"]:
                candidate = response_data["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    response = candidate["content"]["parts"][0].get("text", "I apologize, but I couldn't generate a proper response.")
                    self._add_to_history(userid, "assistant", response)
                    print(f"Assistant: {response}")
                    return response
            
            error_response = "I apologize, but I couldn't generate a proper response."
            self._add_to_history(userid, "assistant", error_response)
            print(f"Assistant: {error_response}")
            return error_response

        except Exception as e:
            error_response = "I apologize, but I encountered an error while processing your request. Please try again later."
            self._add_to_history(userid, "assistant", error_response)
            print(f"Assistant: {error_response}")
            return error_response

gemini_service = GeminiService() 