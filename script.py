import time
import datetime

import requests
import pymysql
from bs4 import BeautifulSoup

# info mysql
hostname = '10.10.10.168'
username = 'html'
password = 'Admin123@'
database = 'DB_html'

# info telegram
token = "your tele-bot's token"
chat_id = "your telegram's chat_id"

def send_message(token, chat_id, text):
    requests.get("https://api.telegram.org/bot{}/sendMessage?chat_id={}&text='{}'".format(token, chat_id, text))

def getUser(line):
    user_name = line.find\
    (class_="wc-comment-author wcai-uname-info wcai-not-clicked").text
    return user_name

def getidComment(line):
    idCom = line.get('id')
    return idCom

def getComment(line):
    Comment = line.find(class_="wc-comment-text")
    Comment = Comment.text.strip()
    return Comment

def getURL(line_n):
    d1 = line_n.find('a')
    url = d1.get('href').strip()
    return url

def getTitle(line_n):
    d1 = line_n.find('a')
    title = d1.string.strip()
    return title

def mysql_query(myConnection, field, table):
    values = []
    mysql = myConnection.cursor()
    sql = "select {} from {}".format(field, table)
    mysql.execute(sql)
    queries = mysql.fetchall()
    for value in queries:
        value = value[0]
        values.append(value)
    return values

def mysql_write_user(myConnection, user_name):
    mysql = myConnection.cursor()
    sql = "insert into user (username) values ('{}')".format(user_name)
    mysql.execute(sql)
    myConnection.commit()

def mysql_write_comm(myConnection, idcomment, idsite, iduser, nd_comment, times):
    mysql = myConnection.cursor()
    sql = "insert into comment (idcomment, idsite, iduser, nd_comment, times) values ('{}', {}, {}, '{}', '{}')"\
    .format(idcomment, idsite, iduser, nd_comment, times)
    mysql.execute(sql)
    myConnection.commit()

def mysql_get_id(myConnection, id, table, field, value):
    mysql = myConnection.cursor()
    sql = "select {} from {} where {}='{}'".format(id, table, field, value)
    mysql.execute(sql)
    value = mysql.fetchall()
    id_value = value[0][0]
    return id_value

def mysql_write_new_info(url, idsite, token, chat_id):
    get_data = requests.get(url)
    soup = BeautifulSoup(get_data.text, "lxml")
    info = soup.find_all(class_="wc-comment-right")
    for line in info:
        user_name = getUser(line)
        idCom = getidComment(line)
        Comment = getComment(line)
        if user_name not in mysql_query(myConnection, "username", "user"):
            mysql_write_user(myConnection, user_name)
        if idCom not in mysql_query(myConnection, "idcomment", "comment"):
            times = datetime.datetime.now()
            id_user = mysql_get_id(myConnection, "iduser", "user", "username", user_name)
            mysql_write_comm(myConnection, idCom, idsite, id_user, Comment, times)
            send_message(token, chat_id, Comment)
    

def mysql_write_site(myConnection, url, tieude):
    mysql = myConnection.cursor()
    sql = "insert into site (links, tieude) values ('{}', '{}')"\
    .format(url, tieude)
    mysql.execute(sql)
    myConnection.commit()

myConnection = pymysql.connect\
(host=hostname, user=username, passwd=password, db=database)
url = 'https://canhme.com/nhan-hoa/'
get_data = requests.get(url)
soup = BeautifulSoup(get_data.text, "lxml")
info = soup.find_all(class_="entry-title")

for line_n in info:
    url_n = getURL(line_n)
    title = getTitle(line_n)
    if url_n not in mysql_query(myConnection, "links", "site"):
        mysql_write_site(myConnection, url_n, title)
    id_site = mysql_get_id(myConnection, "idsite", "site", "links", url_n)
    mysql_write_new_info(url_n, id_site, token, chat_id)

myConnection.close()
