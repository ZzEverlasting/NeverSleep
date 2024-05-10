import csv
import os
import json

USER_DATA_FILE = 'user_data.csv'

def initialize_user_data():
    """ Initialize CSV file to store user data if it doesn't exist """
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'username', 'password', 'customization_data'])

def register_user(username, password, customization_data=None):
    """ Register a new user with hashed password and optional customization data """
    initialize_user_data()  # Ensure the user data file is initialized
    new_customization = json.dumps(customization_data) if customization_data else '{}'

    # Read existing data to determine the next user_id
    with open(USER_DATA_FILE, 'r', newline='') as file:
        reader = csv.DictReader(file)
        existing_users = list(reader)
        user_id = max([int(user['user_id']) for user in existing_users] or [0]) + 1

    # Append the new user to the file
    with open(USER_DATA_FILE, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['user_id', 'username', 'password', 'customization_data'])
        writer.writerow({
            'user_id': user_id,
            'username': username,
            'password': password,  # Consider hashing this password
            'customization_data': new_customization
        })

    return f'User {username} registered successfully with user ID {user_id}.'


def login_user(username, password, file_path=USER_DATA_FILE):
    """ Authenticate user by comparing the hashed password """
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['username'] == username and row['password'] == password:
                return {
                    'success': True,
                    'message': 'Login successful',
                    'session_data': {
                        'user_id': row['user_id'],
                        'username': row['username'],
                        'password': row['password'],
                        'customization_data': row.get('customization_data', '')
                    }
                    }
    return {'success': False, 'message': 'Username or Password is INVALID, Try Again!'}

def update_user_customization(username, customization_data, file_path=USER_DATA_FILE):
    """ Update customization data for an existing user """
    updated = False
    temp_file = file_path + '.tmp'
    try:
        with open(file_path, 'r', newline='') as csvfile, open(temp_file, 'w', newline='') as tmpfile:
            reader = csv.DictReader(csvfile)
            writer = csv.DictWriter(tmpfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            for row in reader:
                if row['username'] == username:
                    row['customization_data'] = json.dumps(customization_data)
                    updated = True
                writer.writerow(row)
        os.replace(temp_file, file_path)
        return 'Customization updated successfully.' if updated else 'User not found.'
    except Exception as e:
        return f"Error updating customization: {str(e)}"
