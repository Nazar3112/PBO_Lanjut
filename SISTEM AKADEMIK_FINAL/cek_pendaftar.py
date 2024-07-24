import mysql.connector

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="siakad"
)

cursor = conn.cursor()

# Ganti dengan nomor users yang Anda cari
id = "16"

# Debug: cek nilai id
print("ID:", id)

# Query ke database
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (id,))

# Ambil hasil query
results = cursor.fetchall()

# Debug: cek hasil query
print("Hasil Query:", results)

if results:
    for row in results:
        print("ID:", row[0])
        # Tambahkan pengolahan data sesuai kebutuhan
else:
    print("users tidak ditemukan.")

# Tutup koneksi
cursor.close()
conn.close()
