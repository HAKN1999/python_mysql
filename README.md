# Cara Menggunakan
Pastikan sudah terinstall python 3.x

<b>Jalankan perintah di cmd dengan lokasi yang sama</b>

download via zip / download degan git clone https://github.com/HAKN1999/python_mysql.git

cd python_mysql

python -m venv env

env\Scripts\activate

pip install -r requirements.txt


python db.py

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
