# -*- coding: utf-8 -*-


import bcrypt

passwd = '123456'

# 加密过程
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(passwd.encode(), salt)
print(hashed)