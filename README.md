# Cara Menggunakan
Pastikan sudah terinstall python 3.x

<b>Jalankan perintah di cmd dengan lokasi yang sama</b>

cd python_mysql

python -m venv env

env\Scripts\activate

pip install -r requirements.txt


python database.py

# Konfigurasi Ulang Sesuai Kebutuhan
<pre>
config = {
    'host': 'localhost',
    'port': 3306,
    'database': '<nama database>',
    'user': 'root',
    'password': '<password>',
    'auth_plugin': 'mysql_native_password'
}
</pre>
