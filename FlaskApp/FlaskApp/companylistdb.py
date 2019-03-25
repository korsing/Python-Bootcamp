import csv
import pymysql

mydb = pymysql.connect(host='localhost',
    user='root',
    passwd='skgkdlslrtm',
    db='Bootcamp',
    charset='utf8')
cursor = mydb.cursor()

ifile = open('datalist.csv', 'rb')
csv_data = csv.reader(ifile)
for row in csv_data:
    cursor.execute('INSERT INTO company(code, names) VALUES ("%s", "%s");', row)
#close the connection to the database.
mydb.commit()
cursor.close()
