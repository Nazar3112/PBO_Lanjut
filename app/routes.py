from flask import Flask, request, redirect, url_for, render_template, flash, session, send_file
from functools import wraps
from app.config import db_config, UPLOAD_FOLDER
from app.models import insert_mahasiswa, check_login
from app import app
from app.utils import generate_pdf
import os
import mysql.connector

@app.route('/')
@app.route('/index.html')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'], role=session['role'])
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Anda harus login terlebih dahulu', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

@app.route('/cetak_formulir.html')
@login_required
def cetak_formulir():
    user_id = session.get('user_id')
    if not user_id:
        flash('User ID tidak ditemukan dalam sesi.', 'danger')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mahasiswa WHERE id = %s", (user_id,))
    pendaftar = cursor.fetchone()
    cursor.close()
    conn.close()

    if not pendaftar:
        flash('Pendaftar tidak ditemukan.', 'danger')
        return redirect(url_for('informasi_pendaftar'))

    pdf_buffer = generate_pdf(pendaftar)
    return send_file(pdf_buffer, as_attachment=True, download_name='formulir_pendaftar.pdf', mimetype='application/pdf')

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Trying to login with username: {username}, password: {password}")

        user = check_login(username, password)
        if user:
            session['user_id'] = user[0]  # Simpan user_id dalam sesi
            session['username'] = user[1]  # Simpan username dalam sesi
            session['role'] = user[2]  # Simpan role dalam sesi
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah')
            return redirect(url_for('login'))

    return render_template('login.html')



@app.route('/informasi_pendaftar.html')
@login_required
def informasi_pendaftar():
    user_id = session.get('user_id')  # Ambil user_id dari sesi
    if not user_id:
        flash('User ID tidak ditemukan dalam sesi.', 'danger')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mahasiswa WHERE id = %s", (user_id,))
    pendaftar = cursor.fetchone()
    cursor.close()
    conn.close()

    if not pendaftar:
        flash('Pendaftar tidak ditemukan.', 'danger')

    return render_template('informasi_pendaftar.html', pendaftar=pendaftar)

# @app.route('/cetak_formulir_kartu_ujian.html')
# @login_required
# def cetak_formulir_kartu_ujian():
#     return render_template('cetak_formulir_kartu_ujian.html')

@app.route('/informasi_kampus.html')
def informasi_kampus():
    return render_template('informasi_kampus.html')

@app.route('/countdown.html')
def countdown():
    return render_template('countdown.html')

@app.route('/sk.html')
def sk():
    return render_template('sk.html')

@app.route('/pengaturan_program_studi.html')
def pengaturan_program_studi():
    return render_template('pengaturan_program_studi.html')

@app.route('/tutorial_pembayaran.html')
def tutorial_pembayaran():
    return render_template('tutorial_pembayaran.html')

@app.route('/pendaftaran.html', methods=['GET', 'POST'])
@login_required
def pendaftaran():
    if request.method == 'POST':
        # Get form data
        nama = request.form['nama']
        tempat_lahir = request.form['tempat_lahir']
        tanggal_lahir = request.form['tanggal_lahir']
        jenis_kelamin = request.form['jenis_kelamin']
        alamat = request.form['alamat']
        telepon = request.form['telepon']
        email = request.form['email']
        nik = request.form['nik']
        sekolah_asal = request.form['sekolah_asal']
        tahun_lulus = request.form['tahun_lulus']
        jurusan = request.form['jurusan']
        nama_ayah = request.form['nama_ayah']
        pekerjaan_ayah = request.form['pekerjaan_ayah']
        nama_ibu = request.form['nama_ibu']
        pekerjaan_ibu = request.form['pekerjaan_ibu']
        nama_wali = request.form['nama_wali']
        pekerjaan_wali = request.form['pekerjaan_wali']
        alamat_orangtua = request.form['alamat_orangtua']
        telepon_orangtua = request.form['telepon_orangtua']
        pernyataan = 1 if 'pernyataan' in request.form else 0

        # Handle file uploads
        foto = request.files['foto']
        ktp = request.files['ktp']
        kk = request.files['kk']
        aktalahir = request.files['aktalahir']
        ijazah = request.files['ijazah']
        prestasi = request.files['prestasi']
        syarikat = request.files['syarikat']

        foto_filename = os.path.join(app.config['UPLOAD_FOLDER'], foto.filename)
        ktp_filename = os.path.join(app.config['UPLOAD_FOLDER'], ktp.filename)
        kk_filename = os.path.join(app.config['UPLOAD_FOLDER'], kk.filename)
        aktalahir_filename = os.path.join(app.config['UPLOAD_FOLDER'], aktalahir.filename)
        ijazah_filename = os.path.join(app.config['UPLOAD_FOLDER'], ijazah.filename)
        prestasi_filename = os.path.join(app.config['UPLOAD_FOLDER'], prestasi.filename)
        syarikat_filename = os.path.join(app.config['UPLOAD_FOLDER'], syarikat.filename)

        foto.save(foto_filename)
        ktp.save(ktp_filename)
        kk.save(kk_filename)
        aktalahir.save(aktalahir_filename)
        ijazah.save(ijazah_filename)
        prestasi.save(prestasi_filename)
        syarikat.save(syarikat_filename)

        # Prepare data for insertion
        data = (nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, telepon, email, nik, sekolah_asal, tahun_lulus, jurusan, nama_ayah, pekerjaan_ayah, nama_ibu, pekerjaan_ibu, nama_wali, pekerjaan_wali, alamat_orangtua, telepon_orangtua, foto.filename, ktp.filename, kk.filename, aktalahir.filename, ijazah.filename, prestasi.filename, syarikat.filename, pernyataan)

        # Insert data into the database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = """
        INSERT INTO mahasiswa (nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, telepon, email, nik, sekolah_asal, tahun_lulus, jurusan, nama_ayah, pekerjaan_ayah, nama_ibu, pekerjaan_ibu, nama_wali, pekerjaan_wali, alamat_orangtua, telepon_orangtua, foto, ktp, kk, aktalahir, ijazah, prestasi, syarikat, pernyataan) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        conn.commit()
        pendaftar_id = cursor.lastrowid
        cursor.close()
        conn.close()
       
        session['user_id'] = pendaftar_id  # Simpan pendaftar_id dalam sesi
        return redirect(url_for('informasi_pendaftar'))

    return render_template('pendaftaran.html')

@app.route('/update_pendaftar.html', methods=['POST'])
@login_required
def update_pendaftar():
    # Ambil data dari form
    user_id = session.get('user_id')
    nama = request.form['nama']
    tempat_lahir = request.form['tempat_lahir']
    tanggal_lahir = request.form['tanggal_lahir']
    jenis_kelamin = request.form['jenis_kelamin']
    alamat = request.form['alamat']
    telepon = request.form['telepon']
    email = request.form['email']
    nik = request.form['nik']
    sekolah_asal = request.form['sekolah_asal']
    tahun_lulus = request.form['tahun_lulus']
    jurusan = request.form['jurusan']
    nama_ayah = request.form['nama_ayah']
    pekerjaan_ayah = request.form['pekerjaan_ayah']
    nama_ibu = request.form['nama_ibu']
    pekerjaan_ibu = request.form['pekerjaan_ibu']
    nama_wali = request.form['nama_wali']
    pekerjaan_wali = request.form['pekerjaan_wali']
    alamat_orangtua = request.form['alamat_orangtua']
    telepon_orangtua = request.form['telepon_orangtua']
    pernyataan = 1 if 'pernyataan' in request.form else 0

    # Buat koneksi ke database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query untuk update data pendaftar
    query = """
    UPDATE mahasiswa SET nama=%s, tempat_lahir=%s, tanggal_lahir=%s, jenis_kelamin=%s, alamat=%s, telepon=%s, email=%s, nik=%s, sekolah_asal=%s, tahun_lulus=%s, jurusan=%s, nama_ayah=%s, pekerjaan_ayah=%s, nama_ibu=%s, pekerjaan_ibu=%s, nama_wali=%s, pekerjaan_wali=%s, alamat_orangtua=%s, telepon_orangtua=%s, pernyataan=%s
    WHERE id=%s
    """
    cursor.execute(query, (nama, tempat_lahir, tanggal_lahir, jenis_kelamin, alamat, telepon, email, nik, sekolah_asal, tahun_lulus, jurusan, nama_ayah, pekerjaan_ayah, nama_ibu, pekerjaan_ibu, nama_wali, pekerjaan_wali, alamat_orangtua, telepon_orangtua, pernyataan, user_id))

    # Commit perubahan dan tutup koneksi
    conn.commit()
    cursor.close()
    conn.close()

    flash('Data pendaftar berhasil diperbarui', 'success')
    return redirect(url_for('informasi_pendaftar'))


@app.route('/profile.html')
@login_required
def profile():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT username, role FROM users WHERE username = %s', (session['username'],))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    if 'new_password' in request.form:
        new_password = request.form['new_password']
        print(f"New password received: {new_password}")
    else:
        print("No new_password key found in request.form")
        flash('Error: new_password key not found.')
        return redirect(url_for('profile'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET password = %s WHERE username = %s', (new_password, session['username']))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Profil berhasil diperbarui.')
    return redirect(url_for('profile'))



@app.route('/preview_formulir.html')
@login_required
def preview_formulir():
    user_id = session.get('user_id')
    if not user_id:
        flash('User ID tidak ditemukan dalam sesi.', 'danger')
        return redirect(url_for('login'))

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM mahasiswa WHERE id = %s", (user_id,))
    pendaftar = cursor.fetchone()
    cursor.close()
    conn.close()

    if not pendaftar:
        flash('Pendaftar tidak ditemukan.', 'danger')
        return redirect(url_for('informasi_pendaftar'))

    return render_template('preview_formulir.html', pendaftar=pendaftar)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('login'))

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('Username sudah ada, silakan pilih username lain.')
                return redirect(url_for('register'))

            cursor.execute('INSERT INTO users (username, password, role) VALUES (%s, %s, %s)', (username, password, 'user'))
            conn.commit()
            return redirect(url_for('register', success=True))
        except mysql.connector.Error as err:
            flash(f'Error: {err}')
        finally:
            cursor.close()
            conn.close()

    success = request.args.get('success')
    return render_template('register.html', success=success)