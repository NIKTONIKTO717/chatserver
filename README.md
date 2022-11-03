# INF226 - Assignment 2+3

developed by Samuel Krempaský alone

<aside>
📑 I worked out this assignment myself. I don’t fully understand, how big difference is expected between 1 person group and 3 people group, so I hope this will be enough. I'll be thrilled for the bonus points 😀

</aside>

## Brief overview of your design considerations from Part A

A few thinks were (in my opinion) problematic because of not the best security design. 

- SQL commands were composed just from string. They definitely should by executed by prepared statement function.
- everything was in one file - e.g. if unhappily became [app.py](http://app.py) available publicly, would be possible to see everything including db info… Should be separated and defactored
- API (initially /search, /send → in my implementation /message, /new) is not restricted, neither for unlogged users and neither for sending/viewing messages of somebody else
- It was possible to pass html (e.g. iframe or script) to the message input. It definitely have to be checked on backend.
- password should be stored in database not as plain text but as hash
- Errors should not be printed so descriptive
- Secret key `app.secret_key` should be secret, and not ‘foo’ or ‘key’…

### Security design considerations

- All SQL commands are executed with preparing statement. This is n.1 of preventing SQL injection.
- All inserts into database (message-to, message) have to be cleaned from HTML tags before inserting into database
- All API request are authorised (I’m using flask functions), so identificator is not passed as argument to URL and authorization is handled by flask
- I’m using string without spaces as unique identificator of user
- Passwords are encrypted by bcrypt ([https://bcrypt-generator.com/](https://bcrypt-generator.com/)) (thanks to: [https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python](https://stackoverflow.com/questions/9594125/salt-and-hash-a-password-in-python))
- I was doing assigment alone, so I did not implemented everything, so now is possible to send message to anyone, without banning, checking for user existance…

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

## Answers to the questions

- [Threat model](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
    - who might attack the application?
        - administrator of app - person who have access to .py files and database.
        - hosting provider - if hosting is not encrypted
        - logged users - sending a message, cross-site scripting…
        - everyone - trying to drop database with login and password form
    - What can an attacker do?
        - DDoS attack
        - 
    - What damage could be done (in terms of *confidentiality*, *integrity*, *availability*)?
        - *confidentiality -* damage from inside, from person who is administrating app
        - *availability -* depends on hosting provider, maybe DDoS if the don’t have any secure defence
    - Are there limits to what an attacker can do?
        - 
    - Are there limits to what we can sensibly protect against?
        - We can protect against DDoS by choosing good hosting provider or using some security tools against it.
        - There are limits, we always need some person to administrate and take care, and no one is infallible.
- What are the main attack vectors for the application?
- What should we do (or what have you done) to protect against attacks? In every part of app are some best practices. E.g. for communication with database it is using prepared statement. For API it is correct usage of authorization framework (in my case flask). Also it is important to be aware of cross-site scripting and requests forgery. Maybe a few other things which I think are very easy to understand and apply and som important: Using correct SSL (no http anymore 🙂) and have on mind what is done on backend and what on frontend (E.g. we cannot check input for cross-site scripting on frontend by js, but on backend without any possibility to bypass it…) an maybe what I didn’t do in this project is try to have as little frontend-backend communication as possible and have a fat client. For example, if I want to search in the messages that I have loaded on the frontend for messages that contain some typed text, I can do it on already received data only using js and hide those that do not contain text / highlight them with some css class…
- *What is the access control model?* ReBAC - the only permission grant process is during using API. All endpoints are permitted only for logged users and in response for messages endpoints are only messages with which have user relationship - sender or recipient.

- How can you know that you security is good enough? At first we can use some security tools. I used Snyk plugin in PyCharm. On the right you can see the result. All of them I resolved. Next point should be logging. I know it as rule of 4W - who, what, where, when. But I think the main idea is to have all reasonable data about using, which we can analyze. E.g. our app is online and server stops responding. If we have logging, we can find that it could be DoS because many different IP address are trying to load the page every second… Without logging we are helpless.

![Untitled 1](https://user-images.githubusercontent.com/36561335/199746367-9b136b90-6e80-48f0-a599-6f8671369be4.png)
