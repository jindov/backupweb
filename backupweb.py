##########################################################

import os
import time
import datetime
from datetime import datetime, timedelta

DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = 'xxxx'
DB_NAME = 'dbname'
BACKUP_PATH = '/home/user/backup/mysql-'

DATETIME = time.strftime('%d%m%Y')

TODAYBACKUPPATH = BACKUP_PATH + DATETIME

print "creating backup folder"
if not os.path.exists(TODAYBACKUPPATH):
    os.makedirs(TODAYBACKUPPATH)

print "checking for databases names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in file " + DB_NAME
else:
    print "Databases file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0

if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()
       db = db[:-1]
       dumpcmd = "mysqldump -u " + DB_USER + " -p'" + DB_USER_PASSWORD +"'"+ " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
       os.system(dumpcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -u " + DB_USER + " -p'" + DB_USER_PASSWORD +"'"+ " " + db + " > " + TODAYBACKUPPATH + "/" + db + ".sql"
   os.system(dumpcmd)
##### end of backup db #####

#### backup source code ####
TAR_PATH = '/home/user/backup/website.com-'
TAR_NAME = TAR_PATH + DATETIME + ".tar.gz"
CODE_NAME = 'website.com'
HOME = '/home/user/backup/'
SOURCE_PATH = '/webapps/'
if os.path.exists(CODE_NAME):
   remove_exist = "rm -rf " + HOME + "website.com"
   os.system(remove_exist)
   copy_new = "cp -rfa " + SOURCE_PATH + "website.com " + HOME
   os.system(copy_new)
else:
   copy_new = "cp -rfa " + SOURCE_PATH + "website.com " + HOME
   os.system(copy_new)
##### end of backup sc #####

####  start of zip and remove old one ####
zipfile = "tar -cf " + TAR_NAME + " website.com mysql-" + DATETIME
os.system(zipfile)
remove_db = "rm -rf " + TODAYBACKUPPATH
os.system(remove_db)
pushgdrive = "python /opt/Backup-To-Google-Drive/backup.py /opt/Backup-To-Google-Drive/config/config.json /home/user/backup/website.com-" + DATETIME +".tar.gz"
os.system(pushgdrive)
YESTERDAY = datetime.now() - timedelta(days=1)
OLD_ZIP = TAR_PATH + YESTERDAY.strftime('%d%n%Y') + ".tar.gz"
if os.path.isfile(OLD_ZIP):
   remove_old = "rm -rf " + TAR_PATH + "-" + YESTERDAY.strftime('%d%n%Y') + ".tar.gz"