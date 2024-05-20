# Forum Post System

This project implements a Forum System with a RESTful API that allows users to interact with topics, replies, categories, messages, and user management.

## Project Description

Design and implement a Forum System and provide RESTful API that can be consumed by different clients. High-level description:

- Users can read and create topics and message other users.
- Administrators manage users, topics, and categories.

## RESTful API Requirements

### MUST Requirements

- **Token Endpoint:** Accepts user login data and responds with an authentication token that can be used to access other endpoints.
- **Register User:** Accepts user registration data.
- **Create Topic:** Requires authentication token. Topic data must contain at least a title and a category.
- **Create Reply:** Requires authentication token. Reply data should contain at least text and is associated with a specific topic.
- **View Topics:** Responds with a list of topic resources. Consider adding search, sort, and pagination query params.
- **View Topic:** Responds with a single topic resource and a list of reply resources.
- **View Category:** Responds with a list of all topics that belong to that category. Consider adding search, sort, and pagination query params.
- **View Categories:** Responds with a list of all categories.
- **Create Message:** Requires authentication. Creates a message, should contain at least text as property.
- **View Conversation:** Requires authentication. Responds with a list of messages exchanged between the authenticated user and another user.
- **View Conversations:** Requires authentication. Responds with a list of all users with which the authenticated user has exchanged messages.
- **Upvote/Downvote a Reply:** Requires authentication. A user should be able to change their downvotes to upvotes and vice versa, but a reply can only be upvoted/downvoted once per user.
- **Choose Best Reply:** Requires authentication. Topic author can select one best reply to their topic.

### SHOULD Requirements

- **Create Category:** Requires admin authentication. Category data should contain at least a name.
- **Make Category Private / Non-private:** Requires admin authentication. Changes visibility to a category and all associated topics. Topics in a private category are only available to category members.
- **Give User a Category Read Access:** Requires admin authentication. A user can now view all topics and replies in the specific private category.
- **Give User a Category Write Access:** Requires admin authentication. A user can now view all topics and replies in the specific private category and post new topics and replies.
- **Revoke User Access:** Requires admin authentication. A user loses their read or write access to a category.
- **View Privileged Users:** Requires admin authentication. Responds with a list of all users for a specific private category along with their access level.
- **Lock Topic:** Requires admin authentication. A topic can no longer accept new replies.
- **Lock Category:** Requires admin authentication. A category can no longer accept new topics.

## Technologies Used
- FastAPI
- Python
- REST
- JWT
- JSON
- Uvicorn
- MariaDB
- MySQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/forum-post-system.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Start the server:
   ```bash
   uvicorn main:app --reload

Access the API endpoints at http://localhost:8000/docs.

## Credits

- **Project Creators:** Kaloyan Nikolov, Veselin Totev, Ina Ignatova.

