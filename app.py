from ast import Not
from curses import flash
from datetime import date
import os
import re
from urllib import request
from xml.etree.ElementTree import tostring
from flask import Flask, redirect, render_template , flash , session ,url_for,request,g,url_for
import sqlite3
import os
app = Flask(__name__)
app.secret_key = os.urandom(24);
conn = sqlite3.connect("bookshop.db",check_same_thread=False)
currentlocation = os.path.dirname(os.path.abspath(__file__))
@app.route('/',methods=["POST","GET"])
def index():
    cur = conn.cursor()
    query = "SELECT * FROM book;"
    cur.execute(query)
    data = cur.fetchall()
    return render_template("/index.html",book = data)


@app.route('/login',methods=['POST','GET'])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("/login.html")
    else:
        cur = conn.cursor()
        username = request.form['username']
        password = request.form['userpass']
        queryexist = "SELECT * FROM users WHERE username = '{a}' AND userpass = '{b}';".format(a=username,b=password)
        if not username:
            flash("enter Username", "403")
            return render_template("/singup.html")
        elif not password:
            flash("Enter password", "info")
            return render_template("/login.html")
        cur.execute(queryexist)
        data = cur.fetchone()

        if  not data:
            flash("User or password not found")
            return render_template("/login.html")
        if data:
            session['user']=username
            conn.close
            return redirect("/")




@app.route("/singup",methods=["POST","GET"])
def singup():
    if request.method == "GET":
        session.clear()
        return render_template("/singup.html")
    else:
        username = request.form['username']
        password = request.form['userpass']
        confirmpassword = request.form['conuserpass']
        cur = conn.cursor()
        queryexist = "SELECT * FROM users WHERE username = '{a}';".format(a=username)
        queryadd = "INSERT INTO users(username,userpass) VALUES('{a}','{b}');".format(a=username,b=password)
        if not username:
            flash("enter Username", "403")
            return render_template("/singup.html")
        elif not password:
            flash("Enter password", "info")
            return render_template("/singup.html")
        elif not confirmpassword:
            flash("Enter password confirmation", "info")
            return render_template("/singup.html")
        elif confirmpassword != password:
            flash("the password not be same", "info")
            return render_template("/singup.html")
        cur.execute(queryexist)
        data = cur.fetchone()
        if data:
            flash("the user already exist")
            return render_template("/singup.html")

        try:
            cur.execute(queryadd)
        except:
            flash("ERROR")
            return render_template("/singup.html")
        conn.commit()
        session['user']=username
        return redirect("/")



@app.route('/addbook',methods=["POST","GET"])
def addbook():
    if request.method == "GET":
        return render_template("/addbook.html")
    else:
        bookname = request.form['bookname']
        author = request.form['author']
        description= request.form['description']
        book_url = request.form['url']
        cur = conn.cursor()
        if not bookname:
            flash("enter name of book")
            return render_template("/addbook.html")
        elif not author:
            flash("enter name of author")
            return render_template("/addbook.html")
        elif not author:
            flash("enter name of author")
            return render_template("/addbook.html")
        elif session.get('user') is None:
            flash("FIRST LOGIN")
            return render_template("/addbook.html")
        elif session.get('user') is not None:
            user = session.get('user')
            queryadd = 'INSERT INTO book(name,author,description,image,user) VALUES("{a}","{b}","{c}","{d}","{e}");'.format(a=bookname,b=author,c=description,d=book_url,e=user)
            try:
                cur.execute(queryadd)
            except:
                flash("ERROR")
                return render_template("/addbook.html")
            conn.commit()
            return render_template("/tnks.html")

@app.route('/tnks')
def tnks():
    return render_template("/tnks.html")

@app.route('/info/<id>',methods=["POST","GET"])
def info(id):
    cur = conn.cursor()
    queryadd = "SELECT * FROM book WHERE id = '{a}';".format(a = id)
    cur.execute(queryadd)
    data = cur.fetchone()
    conn.commit()
    return render_template("/info.html",book=data)
@app.route('/aboutus')
def aboutus():
    return render_template("/aboutus.html")


@app.route('/history')
def history():
    if session.get('user') is None:
        flash("FIRST LOGIN")
        return redirect("/login")
    user = session.get('user')
    cur = conn.cursor()
    queryadd = "SELECT * FROM book WHERE user = '{a}';".format(a = user)
    cur.execute(queryadd)
    data = cur.fetchall()
    conn.commit()
    return render_template("/history.html",data=data)


@app.route('/<id>',methods=["POST","GET"])
def revbook(id):
    cur = conn.cursor()
    queryadd = "DELETE FROM book WHERE id = '{a}';".format(a = id)
    cur.execute(queryadd)
    data = cur.fetchall()
    conn.commit()
    return redirect("/")

if __name__ == '__main__':
    app.run()
