# session_manager.py
import uuid
from datetime import datetime, timedelta
from crud import Crud

class Sessions:
    def __init__(self):
        self.crud = Crud(table='login', primarykey='id')
        self.crud.connect()

    def create_or_update_session(self, user_id, remote_addr, remote_host):
        print(f"user_id type: {type(user_id)}, value: {user_id}")
        current_time = datetime.now()
        expiry_time = current_time + timedelta(minutes=30)
        session_key = str(uuid.uuid4())

        # Check for existing session for the user
        existing_sessions = self.crud.select(
            columns=['session_key', 'session_expiry'],
            primaryKey_value=user_id
        )
        
        for session in existing_sessions:
            if session[1] > current_time:  # If session expiry is not reached
                # Update existing session expiry
                self.crud.update_multiple_columns(
                    columns=['session_expiry', 'session_key'],
                    columns_value=[expiry_time, session_key],
                    primaryKey_value=user_id
                )
                return session_key
        
        # If no valid session exists, create a new session
        self.crud.insert(
            user_id=user_id,
            session_key=session_key,
            remote_addr=remote_addr,
            remote_host=remote_host,
            logged_in=current_time,
            session_expiry=expiry_time,
            status=1,  # Example status
            origin=1   # Example origin
        )
        self.crud.commit()
        return session_key

    def close(self):
        self.crud.close()
