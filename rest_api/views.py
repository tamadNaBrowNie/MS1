from django.shortcuts import render

# Create your views here.
raws = {
    'validate': """SELECT pw FROM user WHERE user.username = ? AND user.pw = ?; """,
    'add': """INSERT INTO user (username, email,leval_name,pfp,phone,pw)""",
}