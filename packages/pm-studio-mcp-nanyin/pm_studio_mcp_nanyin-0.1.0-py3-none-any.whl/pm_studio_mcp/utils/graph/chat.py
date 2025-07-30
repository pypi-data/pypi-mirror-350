import requests
import markdown
from .auth import AuthUtils

class ChatUtils:
    """Utilities for accessing Microsoft Teams chat data via MS Graph API"""

    @staticmethod
    def get_group_chat_id_by_name(topic: str):
        """
        Get the group chat ID by filtering the topic. 
        
        Args:
            topic (str): The topic to filter the chat.
        
        Returns:
            str: The chat ID if found, otherwise None.
        """
        print("Retrieving group chat ID...")
            
        access_token = AuthUtils().login()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        params = {
            "$top": 50  # Limit the number of chats to retrieve
        }
        
        # Get the list of chats
        chats_url = "https://graph.microsoft.com/v1.0/me/chats"

        #chat result is paginated, so we need to handle pagination
        while chats_url:

            # Make the request to get the chats
            chats_response = requests.get(chats_url, headers=headers, params=params)
            
            if chats_response.status_code != 200:
                print(f"Error retrieving chats: {chats_response.text}")
                return False
            
            # Check if the chat topic matches the provided topic
            for chat in chats_response.json().get("value", []):
                if  chat.get("topic") and topic in chat.get("topic", ""):
                    chat_id = chat.get("id")
                    print(chat_id)
                    return chat_id
                
            # get the next page of chats
            chats_url = chats_response.json().get("@odata.nextLink")
            params = None  # No need to pass $top parameter for subsequent requests
    
        print(f"Chat with topic '{topic}' not found.")
        return None

    def send_chat_with_id(chat_id: str, message:str):
        """
        Send a message to a chat in Microsoft Teams using MS Graph API.
        
        Args:
            chat_id (str): The ID of the chat to send the message to. If sending to myself, use "self".
            message (str): The message to send.
        
        Returns:
            dict: Dictionary containing status and response data
        """
        print("Sending message to chat...")
        
        # Ensure user is authenticated
        access_token = AuthUtils().login()
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        # Create the chat message payload
        payload = {
            "body": {
                "contentType": "html", # Set content type to HTML
                "content": message + "</br></br><p style=\"color: grey;\"> - Sent from PM Studio</p>"
                # to add "[PM Studio] " as a prefix to the note
            }
        }
        
        if chat_id == "self":
            print("Sending note to myself...")
            endpoint = "https://graph.microsoft.com/v1.0/me/chats/48:notes/messages"
        else:
            print(f"Sending note to group chat: {chat_id}")
            endpoint = f"https://graph.microsoft.com/v1.0/me/chats/{chat_id}/messages"
        
        try:
            response = requests.post(url=endpoint, headers=headers, json=payload)
            print(f"Response status code: {response.status_code}")

            if response is None:
                return {
                    "status": "error",
                    "message": "No response received from the API."
                }

            if response.status_code == 201:
                print("Note sent successfully.")
                return {
                    "status": "success",
                    "message": "Note sent successfully."
                }
            else:
                return {
                    "status": "error",
                    "message": f"Error sending note: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "status": "error",
                "message": f"Error sending note: {str(e)}"
            }


    

    @staticmethod
    def send_message_to_chat(type:str, topic: str, message: str):
        """
        Send a note to a group chat in Microsoft Teams using MS Graph API.
        
        Args:
            type (str): The type of chat to send the message to. Can be "myself" or "group".
            topic (str): The topic of the group chat. Only used if type is "group".
            message (str): The message to send. 
        
        Returns:
            dict: Dictionary containing status and response data
        """
        
        print("Sending note to group chat in Microsoft Teams...")
        
        messageHTML = markdown.markdown(message)

        if type == "myself":
            return ChatUtils.send_chat_with_id("self", messageHTML)
        if type == "group":
            chat_id = ChatUtils.get_group_chat_id_by_name(topic)
            if chat_id is None:
                print(f"Chat with topic '{topic}' not found.")
                return False
            
            # Send the message to the group chat
            return ChatUtils.send_chat_with_id(chat_id, messageHTML)
        else:   
            print(f"Invalid type '{type}'. Please use 'myself' or 'group'.")
            return {
                "status": "error",
                "message": "Invalid type. Please use 'myself' or 'group'."
            }