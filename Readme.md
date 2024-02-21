# Note Taking Backend

## Information
This repository contains APIs developed in Django for basic note taking functionalities

## Prerequisites
 1. Install the dependencies by running the below commands from the project's root directory in the command line:
```bash
$pip3 install -r requirements.txt
```
 or

 You can also use a virtual evnironement first to isolate the project's dependencies:
```bash
$python3 -m venv env
$source env/bin/activate
(env)$pip3 install -r requirements.txt
```

 2. Setup Database, the project uses SQLite as the database engine by default. The database can be setup by running the following commands (also creates the super user for Django administrative privileges):
```bash
$python3 notesapp/manage.py makemigrations
$python3 notesapp/manage.py migrate
$python3 notesapp/manage.py createsuperuser
```

## Starting the Process
To start the server:
```bash 
$python3 notesapp/manage.py runserver
```

## API Documentation

#### Signup
This will be used to create a new user

```http
POST /signup
```
Request Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Username for registering |
| `password` | `string` | **Required**. Password |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | Session Authentication token upon successfull registration for subsequent APIs usage|
| `message` | `string` | successfull registration message |

#### Logout
This will be used to logout the logged-in user

```http
POST /logout
```
Request Schema
| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | successfull registration message |

#### Login
This will be used to login a registered user

```http
POST /login
```
Request Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. Username for registering |
| `password` | `string` | **Required**. Password |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `token` | `string` | Session Authentication token upon successfull registration for subsequent APIs usage|
| `message` | `string` | successfull registration message |

#### Create Note
This will be used to create a new note

```http
POST /notes/create
```
Request Schema
| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `title` | `string` | **Required**. Title of the Note |
| `content` | `string` | **Required**. Note's content |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `number` | Id of the note created. **This will be used for note specific API usage**|
| `title` | `string` | Title of the Note |
| `content` | `string` | Note's content |
| `note_version` | `string` | Version of the note. In this case, it would be `1` for a newly created note |
| `owner` | `string` | Id of the user who created the note |
| `shared_with` | `list` | List of users who have access to this note besides the owner which would be empty during creation |

#### Read a Note
This will be used to read a note which is accessible by the user

```http
GET /notes/:id
```
Request Schema
| Path Parameter| Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. Id of the note|

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `title` | `string` | **Required**. Title of the Note |
| `content` | `string` | **Required**. Note's content |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `number` | Id of the note created. **This will be used for note specific API usage**|
| `title` | `string` | Title of the Note |
| `content` | `string` | Note's content |
| `note_version` | `string` | Version of the note. In this case, it would be `1` for a newly created note |
| `owner` | `string` | Id of the user who created the note |
| `shared_with` | `list` | List of users who have access to this note besides the owner. |

#### Share a Note
This will be used to share the access to a note with other users

```http
POST /notes/share
```
Request Schema
| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `note_id` | `number` | **Required**. Id of the note|
| `usernames` | `list` | **Required**. List of usernames in string value |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Successfull API invocation message|

#### Update Note
This will be used to update an existing note. **Note** Previous content of the note is required along with new one.

```http
POST /notes/update/:id
```
Request Schema
| Path Parameter| Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. Id of the note|

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `content` | `string` | **Required**. Note's new content **along with previous content** |

Response Schema
| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `message` | `string` | Note Successfully updated message|
| `note_version` | `string` | Updated version of the note |

#### Get Note Versions
This will be used to fetch history of all the updates made to the note

```http
POST /notes/version-history/:id
```
Request Schema
| Path Parameter| Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `string` | **Required**. Id of the note|

| Header | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `Authorization` | `string` | **Required**. Session Token which needs to be passed as `Token token_value` |

Response Schema
- A list of dictionaries containing information about every version of each note in the below format

| Body | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `id` | `number` | Id of the note version created. (Different from Note Id)|
| `content` | `string` | Note's content |
| `created_at` | `string` | Time when the update was made on the note |
| `note` | `number` | Id of the note |
| `note_version` | `string` | Version of the note when the update was made|
| `made_by` | `string` | Id of the user who updated the note |

## Testing
To run the basic test cases, use the below command from the project's root directory in the command line:
```bash 
$python3 notesapp/manage.py test notes
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.