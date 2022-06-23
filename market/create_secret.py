import random
import json
import os

SYMBOLS = "1234567890qwertyuiopasdfghjklzxcvbnm-=[];'\./,_+()*&^%$#@!}{|:?><~ZXCVBNMASDFGHJKLQWERTYUIOP"
N = 128
FILE = '/var/www/html/secrets/secret.env'

try:
    with open(FILE, 'r') as fp:
        d = json.load(fp)
        if d.get("SECRET_KEY", None) is not None:
            pass
        else:
            raise AttributeError()
except:
    with open(FILE, 'w') as fp:
        s = ''.join(random.choices(SYMBOLS, k=N))
        json.dump({'SECRET_KEY': s}, fp)
