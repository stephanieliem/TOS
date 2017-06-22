import sqlite3

conn = sqlite3.connect('database.db')
print "Opened database successfully";

conn.execute('CREATE TABLE users (userId INTEGER PRIMARY KEY AUTOINCREMENT, username varchar(128) NOT NULL, password varchar(128) NOT NULL, email varchar(128) NOT NULL, joinDate DATETIME NOT NULL, imageUrl varchar(512) NOT NULL)')
print "Table USERS created successfully";

conn.execute('CREATE TABLE threads (threadId INTEGER PRIMARY KEY AUTOINCREMENT, title varchar(128) NOT NULL, content varchar(512) NOT NULL, postDate DATETIME NOT NULL, userId varchar(12) NOT NULL)')
print "Table THREADS created successfully";

conn.execute('CREATE TABLE comments (commentId INTEGER PRIMARY KEY AUTOINCREMENT, comment varchar(128) NOT NULL, commentDate DATETIME NOT NULL, userId varchar(12) NOT NULL, threadId varchar(12) NOT NULL)')
print "Table COMMENTS created successfully";

conn.close()
