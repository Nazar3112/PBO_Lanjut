from functools import wraps
from flask import redirect, url_for, flash, session
import mysql.connector
from app.config import db_config

def insert_mahasiswa(data):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    query = """
    INSERT INTO mahasiswa (nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, telepon, email, nik, sekolah_asal, tahun_lulus, jurusan, nama_ayah, pekerjaan_ayah, nama_ibu, pekerjaan_ibu, nama_wali, pekerjaan_wali, alamat_orangtua, telepon_orangtua, foto, ktp, kk, aktalahir, ijazah, prestasi, syarikat, pernyataan) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Anda harus login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def check_login(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user:
            return user
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    return None
