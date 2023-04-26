## Features of application

- Login with username and password
- Displaying all messages sended or received by logged in person
- Searching in messages (done on backend by api, see below API section)
- Sending a message to specific person/people or for all
- Refreshing messages (getting new one, just calling api point /messages)
- Logout
- Except salt in hash I also added a bit of salt to css 🙂 (at least to the message bubbles)

Originally I had API and DB info here, but eventually I add a [separate part](https://www.notion.so/INF226-Assignment-2-3-5e75064a53f44401b9c53c253397eb06).

## How to test/demo it

At first you need to clone this git.

After that install all required packages (`requirements.txt`)(probably a few of them are already pre-installed with python):

`pip install flask flask_wtf flask_login apsw markupspace pygments bcrypt werkzeug wtforms`

or run

`pip install -r .\requirements.txt`

Last command is to run flask:

`flask run` 

Note from login-server git: If the `flask` command doesn't exist, you can start use `python -m flask run` instead.

In database are created 2 users. Password are in bcrypt format, so if you want to change them, generate hash at [https://bcrypt-generator.com/](https://bcrypt-generator.com/)

Database is stored in `tiny.sqlite` file, so for adding users just open it in some SQLite editor and add them.

| username | password |
| --- | --- |
| alice | 123 |
| bob | 123 |

## Technical details of implementation

### API

- **POST** /new
    
    **Arguments**
    
    `recipients` - users id, separated by comma e.g. `alice,bob, anotherlogin` , if null means message for all users
    
    `message` - message content
    
    **Response**
    
    Response is array with sent message (message with last recipient in case if message have more recipients) in format `[[id,"sender","Message",timestamp,"recipient"|null]]`
    
    Example:
    
    `[[23,"alice","Message","2022-10-29 21:52:04",null]]`
    
- **GET** /messages
    
    **Arguments**
    
    `q` - search query. For all messages set to `null` or not provide
    
    `sent` - `true` / `false` , default `false` - include sent messages of user
    
    **Response**
    
    Response is array with messages.
    
    Example: 
    
    `[[1,"alice","A message...","2022-10-29 09:00:03","bob"],[2,"alice","A message to all","2022-10-29 09:00:14",null]`
    
- **GET** /messages/<ID>
    
    **Arguments**
    
    **Response**
    
    Response is array with one message, or nothing if ID not exist or you are not authorized
    
    Example:
    
    `[[23,"alice","Message","2022-10-29 21:52:04",null]]`
    

### Database model

![Untitled](https://user-images.githubusercontent.com/36561335/199746272-1ee36fac-378e-4bdb-ac77-85381518c523.png)


A SQLite Database is used.