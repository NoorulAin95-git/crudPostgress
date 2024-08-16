from crud import Crud

table = Crud( table='user', primarykey='id')
table.connect()
table.insert(id=1, loginname="noorulain" , usergroup=2, username="NM", firstname='noor', lastname='ulain')
table.insert_many( columns=('id','loginname','usergroup','firstname', 'lastname','username'),
    rows=[
        [2,'ridaali',2,'rida', 'ali','RA'],
        [3,'rimshaali',2,'rimsha', 'ali','RA']
    ]
)
table.commit()
table.select_all()
table.select_all(primaryKey_value=1)
table.select(columns=['firstname'],primaryKey_value=1)
table.select( columns=['firstname'])
table.update(column='firstname', column_value='ZULANOO',primaryKey_value=1)

# Delete a record
table.delete(primaryKey_value=1)
# Select all records
table.select_all()
# Delete all records
table.delete_all()

# User creation and validation with password
table.create_user('new_user', 'password123')
table.validate_user('new_user', 'password123')

# Close the connection
table.close()

