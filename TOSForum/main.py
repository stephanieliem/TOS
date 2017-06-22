import os
from flask import Flask, session, redirect, url_for, render_template, request, escape
import sqlite3 as sql
from datetime import datetime, date, time
app = Flask(__name__)
app.secret_key = 'albert edwillian pratomo'
app.config['UPLOAD_FOLDER'] = '/home/m26415175/TOSForum/static/images'

@app.route('/')
@app.route('/index')
def index():
   # con = sql.connect("database.db")
   # con.row_factory = sql.Row
   # cur = con.cursor()
   # cur.execute("select * from hotels")
   # rows = cur.fetchall();

   return render_template("signin.html")

@app.route('/indexx')
def indexx():
    with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT * from threads join users on threads.userId = users.userId ORDER BY threads.postDate DESC")
         rows = cur.fetchall();
         return render_template('index.html',threads = rows)
         con.close()

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/signup')
def signup():
   return render_template('signup.html')

@app.route('/goeditthread/<name>')
def goeditthread(name):
	with sql.connect("database.db") as con:
		con.row_factory = sql.Row
		cur = con.cursor()
		cur.execute("SELECT * from threads where threadId=?", (name,))
		rows = cur.fetchone();   
		return render_template('editthread.html', thread = rows)
		con.close()

@app.route('/notif')
def notif():
   with sql.connect("database.db") as con:
      con.row_factory = sql.Row
      cur = con.cursor()
      cur.execute("SELECT * from users where username=?", (session['username'],))
      rows = cur.fetchone();   
      userId = rows[0]

      cur.execute("SELECT * from users u join comments c on u.userId = c.userId join threads t on t.threadId = c.threadId where t.userId= ? ORDER BY c.commentDate DESC", (userId,))
      rows = cur.fetchall();   

      return render_template('notifications.html', notifs = rows, userId = userId)

@app.route('/signin')
def signin():
   return render_template('signin.html')

@app.route('/profile')
def profile():
	with sql.connect("database.db") as con:
         con.row_factory = sql.Row
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         rows = cur.fetchone();
         userId = rows['userId']
         date1 = datetime.strptime(rows['joinDate'], '%Y-%m-%d %H:%M:%S')
         date = date1.strftime("%d %B %Y")
         cur.execute("SELECT COUNT(*) from threads t join users u on t.userId = u.userId where u.userId = ?", (userId,))
         thr = cur.fetchone();
         cur.execute("SELECT * from threads join users on threads.userId = users.userId where users.userId = ? ORDER BY threads.postDate DESC", (userId,))
         threads = cur.fetchall();
         
         return render_template('profile.html',user = rows, thr = thr[0], threads = threads, date = date)
         con.close()

@app.route('/adduser',methods = ['POST', 'GET'])
def adduser():
   if request.method == 'POST':
      email = request.form['postEmail']
      username = request.form['postUsername']
      password = request.form['postPassword']
      f = request.files['file']
      extension=f.filename.split(".")
      extension=str(extension[1])

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT COUNT(*) from users where email = ? or username = ?",(email,username))
         cek = cur.fetchone()

         if cek[0] > 0:
            info = "Email/Username is already used"
            return render_template('wrongsignup.html',info = info)
         else:
            cur.execute("SELECT MAX(UserId) FROM users")
            res = cur.fetchone();
            cur.execute("SELECT * FROM users where userId = ?", res)
            row = cur.fetchone();
            filename = str(row[0])+"."+extension
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("INSERT INTO users (email,username,password, joinDate, imageUrl) VALUES (?,?,?,?,?)",(email,username,password,datetime.now().strftime("%Y-%m-%d %H:%M:%S"), filename) )
            con.commit()

            info = "Sign up success! Please sign in to continue"
            return render_template('oksignin.html',info = info)
         
         con.close()

@app.route('/addthread',methods = ['POST', 'GET'])
def addthread():
   if request.method == 'POST':
      title = request.form['postTitle']
      content = request.form['postContent']

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         rows = cur.fetchone();   
         userId = rows[0]

         cur.execute("INSERT INTO threads (title,content,postDate,userId) VALUES (?,?,?,?)",(title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),userId) )
         con.commit()
         return redirect(url_for('indexx'))
         con.close()

@app.route('/edituser/')
def edituser():
         con = sql.connect("database.db")
         con.row_factory = sql.Row
   
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         hsl = cur.fetchone();   
       
         return render_template("editprofile.html",user = hsl)

@app.route('/thread/<name>')
def thread(name):
         con = sql.connect("database.db")
         con.row_factory = sql.Row
   
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         hsl = cur.fetchone();   
         userId = hsl['userId']

         cur.execute("SELECT * from threads join users on threads.userId = users.userId where threads.threadId = ?",(name,))
         rows = cur.fetchone();
         date1 = datetime.strptime(rows['postDate'], '%Y-%m-%d %H:%M:%S')
         date = date1.strftime("%d %B %Y %I:%M %p")

         cur.execute("SELECT * from comments join users on comments.userId = users.userId where comments.threadId = ? ORDER BY comments.commentDate ASC",(name,))
         com = cur.fetchall();
       
	 return render_template("thread.html",thread = rows, comments = com, date = date, userId = userId)
@app.route('/thread1/<name>')
def thread1(name):
         con = sql.connect("database.db")
         con.row_factory = sql.Row
   
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         hsl = cur.fetchone();   
         userId = hsl['userId']

         cur.execute("SELECT * from threads join users on threads.userId = users.userId where threads.threadId = ?",(name,))
         rows = cur.fetchone();
         date1 = datetime.strptime(rows['postDate'], '%Y-%m-%d %H:%M:%S')
         date = date1.strftime("%d %B %Y %I:%M %p")

         cur.execute("SELECT * from comments join users on comments.userId = users.userId where comments.threadId = ? ORDER BY comments.commentDate ASC",(name,))
         com = cur.fetchall();
         return render_template("thread1.html",thread = rows, comments = com, date = date, userId = userId)
@app.route('/addcomment',methods = ['POST', 'GET'])
def addcomment():
   if request.method == 'POST':
      comment = request.form['postComment']
      threadId = request.form['threadId']

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT * from users where username=?", (session['username'],))
         rows = cur.fetchone();   
         userId = rows[0]

         cur.execute("INSERT INTO comments (comment,commentDate,userId,threadId) VALUES (?,?,?,?)",(comment,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),userId,threadId))
         con.commit()
         info = "Comment berhasil ditambahkan."
         # return render_template('info.html',info = info)
         return redirect(url_for('thread',name = threadId))
         con.close()

@app.route('/search',methods = ['POST', 'GET'])                
def search():
   if request.method == 'POST':
      keyword = request.form['keyword']
      nkeyword = "%"+keyword+"%"

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT * from threads join users on threads.userId = users.userId where (title like ? or UPPER(title) like ?) or (content like ?  or UPPER(content) like ?) ORDER BY threads.postDate DESC", (nkeyword, nkeyword, nkeyword, nkeyword))
         rows = cur.fetchall();   

         return render_template("search.html",threads = rows, keyword = keyword)
         con.close()

@app.route('/editthread',methods = ['POST', 'GET'])
def editthread():
   if request.method == 'POST':
      title = request.form['postTitle']
      content = request.form['postContent']
      threadId = request.form['threadId']

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("UPDATE threads SET title = ?, content = ?, postDate = ? where threadId = ?",(title,content,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),threadId))
         con.commit()
         
         return redirect(url_for('thread',name = threadId))

@app.route('/edituserr',methods = ['POST', 'GET'])
def edituserr():
   if request.method == 'POST':
      userId = request.form['userId']
      email = request.form['postEmail']
      username = request.form['postUsername']
      password = request.form['postPassword']
      f = request.files['file']
      extension=f.filename.split(".")
      extension=str(extension[1])

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT COUNT(*) from users where email = ? or username = ?",(email,username))
         cek = cur.fetchone()

         if cek[0] > 1:
            cur.execute("SELECT * from users where username=?", (session['username'],))
            hsl = cur.fetchone();   
            info = "Email/Username is already used"
            return render_template('wrongedit.html',user = hsl, info = info)
         else:
            filename = str(userId)+"."+extension
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cur.execute("UPDATE users SET email= ?, username=?, password=?, imageUrl=? where userId = ?",(email,username,password,filename, userId) )
            con.commit()
            
            return redirect(url_for('profile'))
         
         con.close()

@app.route('/editcomment',methods = ['POST', 'GET'])
def editcomment():
   if request.method == 'POST':
      comment = request.form['postComment']
      commentId = request.form['commentId']
      threadId = request.form['threadId']

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("UPDATE comments SET comment = ?, commentDate = ? where commentId = ?",(comment,datetime.now().strftime("%Y-%m-%d %H:%M:%S"),commentId))
         con.commit()
         # info = "Comment berhasil diupdate."
         # return render_template('info.html',info = info)
         return redirect(url_for('thread',name = threadId))
         con.close()

@app.route('/deletethread/<name>')
def deletethread(name):
      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("DELETE FROM comments where threadId = ?",(name,))
         cur.execute("DELETE FROM threads where threadId = ?",(name,))
         con.commit()
         return redirect(url_for('indexx'))
         con.close()

@app.route('/deletethread1/<name>')
def deletethread1(name):
      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("DELETE FROM comments where threadId = ?",(name,))
         cur.execute("DELETE FROM threads where threadId = ?",(name,))
         con.commit()
         return redirect(url_for('profile'))
         con.close()

@app.route('/deletecomment/<name>/<tid>')
def deletecomment(name,tid):
      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("DELETE FROM comments where commentId = ?",(name,))
         con.commit()
         return redirect(url_for('thread',name = tid))
         con.close()

@app.route('/logincek',methods = ['POST', 'GET'])
def logincek():
   if request.method == 'POST':
      username = request.form['postUsername']
      password = request.form['postPassword']

      with sql.connect("database.db") as con:
         cur = con.cursor()
         cur.execute("SELECT COUNT(*) from users where username = ? and password = ?",(username,password))
         cek = cur.fetchone()

         if cek[0] > 0:
            session['username'] = username
            return redirect(url_for('indexx'))
         else:
            info = "Username/password Invalid"
            return render_template('wrongsignin.html',info = info)
         con.close()

if __name__ == '__main__':
   app.debug = True
   app.run('0.0.0.0',5005) 
