# Shareable ToDo List API

## Overview
This project is a Flask-based API for a shareable todo list application. It allows users to manage todo lists and tasks, and includes functionality for sharing lists with other users. The API supports user authentication and authorization using JSON Web Tokens (JWT).

## Features
- User authentication.
- CRUD operations for todo lists and tasks.
- Sharing todo lists with different permissions.
- *Upcoming Feature*: Real-time notifications on updates.


## API Endpoints

### Authentication
- `POST /auth/login`: User login.
- `POST /auth/register`: User registration.

### ToDo Lists
- `POST /todolists`: Create a new todo list.
- `GET /todolists`: Retrieve all todo lists.
- `GET /todolists/<int:list_id>`: Retrieve a specific todo list.
- `PUT /todolists/<int:list_id>`: Update a specific todo list.
- `DELETE /todolists/<int:list_id>`: Delete a specific todo list.

### Tasks
- `POST /tasks`: Create a new task in a todo list.
- `PUT /tasks/<int:task_id>`: Update a specific task.

### Sharing
- `POST /share_todo_list`: Share a todo list with another user.

## Future Enhancements
- I plan to add a real-time notification system. This will allow users to receive updates whenever a shared todo list is modified.
- I am currently working on the frontend aspect of this project using React JS.




