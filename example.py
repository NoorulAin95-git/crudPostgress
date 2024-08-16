from crud import Crud

# Initialize Crud object
table = Crud(
    table='user',
    primarykey='id'
)

# Connect to the database
table.connect()

# Insert data
table.insert(
    id=1,
    loginname="noorulain",
    usergroup=2,
    username="NM",
    firstname='noor',
    lastname='ulain'
)

# Insert multiple rows
table.insert_many(
    columns=('id','loginname','usergroup','firstname', 'lastname','username'),
    rows=[
        [2,'ridaali',2,'rida', 'ali','RA'],
        [3,'rimshaali',2,'rimsha', 'ali','RA']
    ]
)


# Commit the transaction
table.commit()

# Select all records
table.select_all()

# Select records with specific primary key
table.select_all(
    primaryKey_value=1
)

# Select specific columns with a condition
table.select(
    columns=['firstname'],
    primaryKey_value=1
)

# Select specific columns
table.select(
    columns=['firstname']
)

# Update a record
table.update(
    column='firstname',
    column_value='ZULANOO',
    primaryKey_value=1
)


=

# Delete a record
table.delete(
    primaryKey_value=1
)

# Select all records to verify changes
table.select_all()

# Delete all records
table.delete_all()

# User creation and validation
table.create_user('new_user', 'password123')
table.validate_user('new_user', 'password123')

# Close the connection
table.close()

