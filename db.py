import mysql.connector
from mysql.connector import errorcode
from prettytable import PrettyTable
import os


class Database:
    def __init__(self, config, table=''):
        self.config = config
        self.nama_db = config['database'].lower()

        try:
            self.db = mysql.connector.Connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Ada yang salah dengan user name atau password!")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"Database {self.nama_db} tidak ditemukan!")

                user_input = input(
                    f'Mencoba membuat databse {self.nama_db} [yY/nN]: ')
                try:
                    if user_input in ['Y', 'y']:
                        host = config['host']
                        port = config['port']
                        user = config['user']
                        passwd = config['password']

                        self.db = mysql.connector.Connect(
                            host=host, port=port, user=user, passwd=passwd)
                        if self.db.is_connected():
                            self.show_id
                            try:
                                self.cursor = self.db.cursor()
                                self.membuat_db()
                            finally:
                                self.db.close()
                            self.membuat_table(table)
                    else:
                        print('Program berhenti!')
                        exit(1)
                except Exception as e:
                    print(e)
        else:
            if self.db.is_connected():
                self.show_id
                self.db.close()

    def membuat_db(self):
        """ membuat database """
        try:
            self.cursor.execute(f'CREATE DATABASE {self.nama_db}')
        except mysql.connector.Error as err:
            print('Databse telah dibuat!')
        else:
            print(f'\t|_Database {self.nama_db} sukses dibuat!')

    def membuat_table(self, table):
        """ membuat table """
        db = mysql.connector.Connect(**self.config)
        cursor = db.cursor()

        for nama_table in table:
            buat_table = table[nama_table]
            try:
                cursor.execute(f'USE {self.nama_db}')
                cursor.execute(buat_table)
                print(f'\t|_Membuat table {nama_table}')
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Table telah dibuat!')
                else:
                    print(err)
            else:
                print(f'\t|_Table {nama_table} sukses dibuat!')
            finally:
                db.close()

    def insert(self, table, msg, menu=0, file_name=''):
        db = mysql.connector.Connect(**self.config)
        cursor = db.cursor()

        user_input, table_desc = self.get_structur_table(table, msg)
        if menu == 0:
            if user_input:
                self.show_structur_table(table_desc)
                try:
                    columns, values = self.get_columns_values(
                        table, table_desc)
                    cursor.execute(
                        f'INSERT INTO {table}({columns}) VALUES ({values})')
                    print('Data berhasil di tambah')
                    db.commit()
                except Exception as e:
                    print(e)
                finally:
                    db.close()
            else:
                try:
                    columns, values = self.get_columns_values(
                        table, table_desc)
                    cursor.execute(
                        f'INSERT INTO {table}({columns}) VALUES ({values})')
                    print('Data berhasil di tambah')
                    db.commit()
                except Exception as e:
                    print(e)
                finally:
                    db.close()

    def get_columns_values(self, table, table_desc):
        columns = []
        values = []

        print(
            f"Masukan data yang akan dimasukan ke tabel {table}")
        for idx in range(len(table_desc)):
            column = table_desc[idx][0]
            value = input(f'Nilai untuk dimasukan ke kolom {column}: ')
            columns.append(str(column))

            if len(value) == 0:
                value = "''"
                print(value)
            values.append("'" + str(value) + "'")

        columns = ','.join(columns)
        values = ','.join(values)
        return columns, values

    @property
    def show_tables(self):
        db = mysql.connector.Connect(**self.config)
        cursor = db.cursor()

        table_list = []
        item_dict = {}

        print('\nDaftar tabel yang sudah terbuat: ')
        cursor.execute('SHOW TABLES')
        table_results = cursor.fetchall()
        for idx in range(len(table_results)):
            print(str(idx+1)+'.', table_results[idx][0])

        try:
            user_input = int(input('Masukan tabel yang akan digunakan: '))
        except Exception as e:
            print(e)
        finally:
            db.close()

        if user_input < 0 or user_input > len(table_results):
            print(
                f'Masukan tidak boleh <0 dan tidak boleh >{len(results)}!')
            db.close()
            self.show_tables
            return

        return table_results[user_input-1][0]
        db.close()

    def get_structur_table(self, table, msg=None):
        db = mysql.connector.Connect(**self.config)
        cursor = db.cursor()

        cursor.execute(f'DESCRIBE {table}')
        table_desc = cursor.fetchall()

        if msg != None:
            user_input = input(msg)
            if user_input in ['y', 'Y']:
                db.close()
                return True, table_desc
            else:
                db.close()
                return False, table_desc
        db.close()
        return table_desc

    def show_structur_table(self, table_desc):
        column = ["Field", "Type", "Null", "Key", "Default", "Extra"]
        obj_pretty = PrettyTable(field_names=column)

        for idx in range(len(table_desc)):
            obj_pretty.add_row([table_desc[idx][0], table_desc[idx][1], table_desc[idx]
                                [2], table_desc[idx][3], table_desc[idx][4], table_desc[idx][5]])
        print(obj_pretty)

    def show_all_records(self, table, table_desc):
        db = mysql.connector.Connect(**self.config)
        cursor = db.cursor()

        column = [table_desc[i][0] for i in range(len(table_desc))]
        obj_pretty = PrettyTable(field_names=column)
        cursor.execute(f'SELECT * FROM {table}')

        data_records = cursor.fetchall()
        [obj_pretty.add_row(i) for i in data_records]
        print(obj_pretty)

    @ property
    def show_id(self):
        print(f'Terhubung dengan MySQL koneksi ID: {self.db.connection_id}')


def main():
    TABLES = {}
    msg = 'Ingin melihat struktur database tabel [y/Y:n/N]: '
    config = {
        'host': 'localhost',
        'port': 3306,
        'database': 'kampus2',
        'user': 'root',
        'password': 'toor',
        'auth_plugin': 'mysql_native_password'
    }

    TABLES['mahasiswa'] = (
        "CREATE TABLE `mahasiswa` ("
        "  `nim` varchar(10),"
        "  `nama` varchar(100),"
        "  `alamat` varchar(100)"
        ")")

    db = Database(config, TABLES)
    table = db.show_tables
    table_desc = db.get_structur_table(table)
    db.insert(table, msg)
    db.show_all_records(table, table_desc)


if __name__ == '__main__':
    main()
