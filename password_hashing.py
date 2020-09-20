import base64
import pickle
import stdiomask
import json
import hashlib
import os
users = {} # 定义字典对象存储用户名,密码键值对
# 增加新用户

def adduser ():
    username= input('Please input your username: ')
    while True:
        password1=stdiomask.getpass(prompt='Please input your password: ', mask='*')
        password2=stdiomask.getpass(prompt='Please input your password again: ', mask='*')
        if password1==password2:
            password= password1
            break
        else:
            continue
    salt = os.urandom(32) # 为每个新用户生成盐值
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    users[username] = { # 存储key和salt值
    'salt': salt,
    'key': key}  #{'michael': {'key': b'E"\x90\xd2B\xeb\x9aq}Og\x9a\x11\xdb\x0e\xf5\xcdy\x03\xaa...\xe6\x0e\x12\x83\xd2\x14=1J0', 'salt': b'4\xc42\x85g\xee\x13Q\xd3mT\xf1"/E;\x07>Y\xfe...\x8bBy\xff\xf7\xfe,9\x89\xea'}}
    users_pickle = pickle.dumps(users) #用pickle导出字典,这里不能用json dump,因为用二进制数据
    data ={
        username:base64.b64encode(users_pickle).decode('ascii'),
    } #用base64 转换二进制为ascii码
    with open('password.json', 'w') as f:
        json.dump(data, f)
    #{"michael": "gASVZQAAAAAAAAB9lIwHbWljaGFlbJR9lCiMBHNhbHSUQyBV7+BG5WOrdcvmX1roJ8HTzmXmqTfq5FkcNWS+Zi/8t5SMA2tleZRDIGbMxlJV5kFTsq309wZ2oUk/Ke6apRukeIPZ4zBeNcRalHVzLg=="}

def verify_password():
    username= input('Please input your username: ')
    password=stdiomask.getpass(prompt='Please input your password: ', mask='*')
    
    with open('password.json', 'r') as f:
        data=json.load(f)
    users_pickle=base64.b64decode(data[username])
    users=pickle.loads(users_pickle)
    salt = users[username]['salt']
    key = users[username]['key']
    new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    if key == new_key:
        print ("welcome,",username)
    else:
        print ("your password is wrong")

while True:
    print ("1. Add a new user")
    print ("2. Verify password")
    option=input ("Please input yout action: ")
    if option =='1':
        adduser()

    elif option =='2':
        verify_password()
    else:
        break
        




