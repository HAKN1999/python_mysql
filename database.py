import mysql.connector
from mysql.connector import errorcode


class Database:
    def __init__(self, config, tbl):
        self.DB_NAME = config['database'].lower()
        try:  # mencoba terhubung dengan db server
            self.db = mysql.connector.Connect(**config)

        except mysql.connector.Error as err:
            # jika user salah memasuakan passwd atau username
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Ada yang salah dengan user name atau password!")

            # jika db tidak ditemukan
            # buat db
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database tidak ditemukan!")
                user_pilih = input(
                    f'Ingin memubat database dengan nama {self.DB_NAME} [yY/nN]: ')

                # penentuan user ingin membuat database baru atau tidak
                if user_pilih in ['y', 'Y']:
                    host = config['host']
                    port = config['port']
                    user = config['user']
                    passwd = config['password']

                    # membuat koneksi baru
                    self.db = mysql.connector.Connect(
                        host=host, port=port, user=user, passwd=passwd)

                    # cek apakah sudah terhubung dengan db server
                    if self.db.is_connected():
                        self.show_id()
                        self.cursor = self.db.cursor()
                        self.create_db(tbl)
        else:
            if self.db.is_connected():
                self.show_id()
                self.cursor = self.db.cursor()

    def create_db(self, tbl):
        """bagian membuat db"""

        try:
            self.cursor.execute(f'CREATE DATABASE {self.DB_NAME}')
            print(f'Database {self.DB_NAME} sukses dibuat!')

        except mysql.connector.Error as err:
            print('Databse telah dibuat ')

        else:
            self.create_tbl(tbl)

    def create_tbl(self, tbl):
        """bagian membuat tabel"""

        for tbl_name in tbl:
            write_tbl = tbl[tbl_name]

            try:
                self.cursor.execute(f'USE {self.DB_NAME}')
                self.cursor.execute(write_tbl)
                print(f'Membuat table {tbl_name}')

            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Tabel telah dibuat')

                else:
                    print(err)

            else:
                print('OK')

    def show_info(self):
        """hanya untuk pengecekan"""

        self.cursor.execute('SHOW TABLES')
        for tables in self.cursor:
            for table in tables:
                print(f'Aktif di db {self.DB_NAME} dengan table {table}')

    def show_id(self):
        """digunakan untuk menampilkan ID koneksi"""

        print(f'Terhubung dengan MySQL koneksi ID: {self.db.connection_id}')


TABLES = {}
config = {
    'host': 'localhost',
    'port': 1999,
    'database': 'kampus',
    'user': 'root',
    'password': 'admin',
    'auth_plugin': 'mysql_native_password'
}
TABLES['mahasiswa'] = (
    "CREATE TABLE `mahasiswa` ("
    "  `nim` varchar(10),"
    "  `nama` varchar(100),"
    "  `alamat` varchar(100)"
    ")")

db = Database(config, TABLES)
db.show_info()
