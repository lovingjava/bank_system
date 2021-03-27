import os
import time

bakup_dir = "E:\\桌面\\Python\\pycharm_bank\\bank_system\\"
current_time = time.strftime('%Y%m%d%H%M%S')
user = 'root'
password = '564445'
database = ['mysql', 'bank_system']
if os.path.exists(bakup_dir):
    print("The path %s exists" % bakup_dir)
else:
    os.makedirs(bakup_dir)
    print("The path %s create sucessful" % bakup_dir)
os.chdir(bakup_dir)
for i in range(len(database)):
    a = database[i]
mysqlbak_cmd = "mysqldump -u%s -p%s --default-character-set=utf8  %s > %s%s.sql" % (user, password, a, current_time, a)
os.system(mysqlbak_cmd)
print("backup sucessful")
