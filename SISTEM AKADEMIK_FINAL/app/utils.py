import io
from flask import Flask
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(data):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.drawString(100, 750, f"Nama: {data['nama']}")
    p.drawString(100, 735, f"Tempat Lahir: {data['tempat_lahir']}")
    p.drawString(100, 720, f"Tanggal Lahir: {data['tanggal_lahir']}")
    p.drawString(100, 705, f"Jenis Kelamin: {data['jenis_kelamin']}")
    p.drawString(100, 690, f"Alamat: {data['alamat']}")
    p.drawString(100, 675, f"Telepon: {data['telepon']}")
    p.drawString(100, 660, f"Email: {data['email']}")
    p.drawString(100, 645, f"NIK: {data['nik']}")
    p.drawString(100, 630, f"Sekolah Asal: {data['sekolah_asal']}")
    p.drawString(100, 615, f"Tahun Lulus: {data['tahun_lulus']}")
    p.drawString(100, 600, f"Jurusan: {data['jurusan']}")
    p.drawString(100, 585, f"Nama Ayah: {data['nama_ayah']}")
    p.drawString(100, 570, f"Pekerjaan Ayah: {data['pekerjaan_ayah']}")
    p.drawString(100, 555, f"Nama Ibu: {data['nama_ibu']}")
    p.drawString(100, 540, f"Pekerjaan Ibu: {data['pekerjaan_ibu']}")
    p.drawString(100, 525, f"Nama Wali: {data['nama_wali']}")
    p.drawString(100, 510, f"Pekerjaan Wali: {data['pekerjaan_wali']}")
    p.drawString(100, 495, f"Alamat Orang Tua: {data['alamat_orangtua']}")
    p.drawString(100, 480, f"Telepon Orang Tua: {data['telepon_orangtua']}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer
