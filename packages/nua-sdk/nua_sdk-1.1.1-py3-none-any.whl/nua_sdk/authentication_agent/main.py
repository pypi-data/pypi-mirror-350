import os
from langgraph_sdk import get_sync_client
from dotenv import load_dotenv

load_dotenv()



class AuthenticationAgent:
    def __init__(self, message: str, pentest_uuid: str):
        self.auth_agent = get_sync_client(url=os.getenv("AUTH_AGENT_URL"))
        self.message = message
        self.pentest_uuid = pentest_uuid
    
    def authenticate(self):
        session_details = None
        thread_id = self.auth_agent.threads.create().get("thread_id")
        response = self.auth_agent.runs.stream(
            thread_id=thread_id,
            assistant_id="agent",
            input={
                "messages": [self.message],
                "pentest_uuid": self.pentest_uuid
            },
            stream_mode="values"
        )
        for chunk in response:
            if chunk.data.get("session_details") != None:
                session_details = chunk.data.get("session_details")
                break
        return session_details

