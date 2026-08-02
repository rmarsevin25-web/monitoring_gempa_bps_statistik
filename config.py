import os

DB_HOST = os.getenv("MYSQLHOST", "localhost")
DB_PORT = os.getenv("MYSQLPORT", "3306")
DB_USER = os.getenv("MYSQLUSER", "root")
DB_PASSWORD = os.getenv("MYSQLPASSWORD", "")
DB_NAME = os.getenv("MYSQLDATABASE", "bps_lubuklinggau")