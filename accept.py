import mysql.connector
from mysql.connector import errorcode
import json

TABLE_NAME = "transacts"

TABLES = {}
TABLES[TABLE_NAME] = (
    "CREATE TABLE `"+TABLE_NAME+"` ("
    "  `transactionId` int(11) NOT NULL AUTO_INCREMENT,"
    "  `payerId` int(10) NOT NULL,"
    "  `merchantId` varchar(50) NOT NULL,"
    "  `callbackUrl` varchar(50) NOT NULL,"
    "  `amount` int(10) NOT NULL,"
    "  `currency` varchar(4) NOT NULL,"
    "  `description` varchar(50),"
    "  `merchantUrl` varchar(50) NOT NULL,"
    "  `merchantOrderId` int(10) NOT NULL,"
    "  `userAgent` varchar(50) NOT NULL,"
    "  `userIpAddress` varchar(16) NOT NULL,"
    "  `status` varchar(10) NOT NULL,"
    "  `merchantIdCode` int(10) NOT NULL,"
    "  `bankId` varchar(10) NOT NULL,"
    "  `transactionType` varchar(10) NOT NULL,"
    "  PRIMARY KEY (`transactionId`)"
    ") ")

DB_NAME = "test"

cnx = mysql.connector.connect(user='root', password='strong_password',
                              host='localhost', port='3307')
cursor = cnx.cursor()


def create_database():
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def initialize_database():
	for table_name in TABLES:
	    table_description = TABLES[table_name]
	    try:
	        print("Creating table {}: ".format(table_name), end='')
	        cursor.execute(table_description)
	    except mysql.connector.Error as err:
	        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
	            print("already exists.")
	        else:
	            print(err.msg)
	    else:
	        print("OK")


def get_sql(transaction):
	keylist = "("
	valuelist = "("
	firstPair = True
	for key, value in transaction.items():
		if not firstPair:
			keylist += ", "
			valuelist += ", "
		firstPair = False
		keylist += key
		if type(value) == str:
			valuelist += "'" + value + "'"
		else:
			valuelist += str(value)
	keylist += ")"
	valuelist += ")"
	sqlstatement = "INSERT INTO " + TABLE_NAME +" " + keylist + " VALUES " + valuelist + "\n"
	return sqlstatement


def insert_to_database(transaction):
	initialize_database()
	sql = get_sql(transaction)
	cursor.execute(sql)
	cnx.commit()


def close_db():
	cursor.close()
	cnx.close()

def test():
	insert_to_database(sample)

sample = {
  "payerId": "0220100894",
  "merchantId": "e53519b4-460f-4687-8133-4c9b95209331",
  "callbackUrl": "http://paymark.co.nz/hobsonTakeaway",
  "amount": 6750,
  "currency": "NZD",
  "description": "RIGHTO",
  "merchantUrl": "www.paymark.co.nz",
  "merchantOrderId": "111123",
  "userAgent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US)",
  "userIpAddress": "127.0.0.1",
  "status": "NEW",
  "merchantIdCode": 300000114,
  "bankId": "ASB",
  "transactionType": "REGULAR"
}

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

test()

close_db()