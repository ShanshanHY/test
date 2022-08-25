import os
import yaml
cookie = os.environ["COOKIE"]
with open("5.txt", mode='w', encoding='utf-8') as f:
    f.write(cookie)
