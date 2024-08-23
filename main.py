# main.py
from crud import Crud
from sessions import Sessions


def authenticate_user_and_create_session(username, password, remote_addr, remote_host):
    crud = Crud(table='user', primarykey='id') 
    crud.connect()

    authenticated_user_id = crud.validate_user( username=username, password=password)

    if authenticated_user_id:
     
        session_manager = Sessions()
        session_key = session_manager.create_or_update_session(
            user_id=authenticated_user_id,
            remote_addr=remote_addr,
            remote_host=remote_host
        )
        session_manager.close()
        crud.close()
        return session_key
    else:
        print("Authentication failed")
        crud.close()
        return None

if __name__ == "__main__":
    table = Crud(table='user', primarykey='id')
    table.connect()
    # User creation and validation
    table.create_user(id=11,username='new_user', password='password123')
    print("Validating 'new_user':")
    print(table.validate_user(username='new_user', password='password123'))


    username = "new_user"
    password = "password123"
    remote_addr = "192.168.1.1"
    remote_host = "hostname.com"

    session_key = authenticate_user_and_create_session(username, password, remote_addr, remote_host)

    if session_key:
        print(f"User authenticated. Session key: {session_key}")
    else:
        print("User authentication failed.")

    # Close the connection
    table.close()
