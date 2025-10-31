**#🛡️ PHP Secure Coding Checker**

Script ini digunakan untuk melakukan pemeriksaan keamanan kode PHP secara otomatis dengan mengintegrasikan beberapa tools keamanan seperti:

PHP_CodeSniffer (phpcs) – untuk memastikan kode mengikuti standar secure coding

Symfony Security Checker – untuk mendeteksi kerentanan pada dependensi PHP (Composer)

Trivy (opsional) – untuk memindai celah keamanan pada aplikasi dan dependensi sistem

Hasil pemeriksaan akan disimpan dalam bentuk file HTML report di /var/reports/security/.

```📂 Struktur Direktori
/var/reports/security/
├── security_report_2025-10-29.html
├── security_report_2025-10-30.html
└── ...
```
**⚙️ 1. Persyaratan Sistem**

Pastikan sistem telah memiliki dependensi berikut:

Tool	Fungsi	Instalasi
phpcs	Analisis secure coding	

```sudo apt install php-codesniffer -y```

symfony/security-checker	Cek kerentanan dependency PHP	

```wget https://get.symfony.com/cli/installer -O - | bash```
 
trivy (opsional)	Analisis keamanan container dan dependensi	

```sudo apt install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo gpg --dearmor -o /usr/share/keyrings/trivy.gpg
echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy -y
```

**🧩 2. Instalasi Script**

Simpan file script berikut ke lokasi yang kamu inginkan, misalnya di /usr/local/bin/php_security_check_html.py:

```sudo nano /usr/local/bin/php_security_check_html.py```


Tempelkan isi script Python (yang sudah kamu dapatkan dari ChatGPT sebelumnya).

Lalu berikan izin eksekusi:

```sudo chmod +x /usr/local/bin/php_security_check_html.py```

**🚀 3. Menjalankan Pemeriksaan**

Jalankan perintah berikut untuk memulai pemeriksaan:

```python3 /usr/local/bin/php_security_check_html.py```


Script akan:

Menjalankan phpcs di direktori project (misalnya /var/www/html/sinerghi)

Menjalankan Symfony Security Checker

Menjalankan Trivy (jika tersedia)

Menghasilkan laporan HTML di /var/reports/security/ dengan timestamp otomatis

**📊 4. Melihat Hasil Laporan**

🔹 Opsi 1: Server Memiliki GUI
```sudo apt install xdg-utils -y```
```xdg-open /var/reports/security/security_report_*.html```

🔹 Opsi 2: Salin ke Komputer Lokal
```scp satupmk@192.168.10.234:/var/reports/security/security_report_*.html .```


💡 Ganti IP sesuai alamat server kamu.

Buka file hasilnya di browser lokal.

🔹 Opsi 3: Lihat Langsung di Terminal
```cat /var/reports/security/security_report_*.html | less```

**🕒 5. Menjadwalkan Otomatis (Opsional)**

Untuk menjadwalkan pemeriksaan rutin (misalnya setiap hari pukul 02:00 dini hari):

```sudo crontab -e```

Tambahkan baris berikut:

```0 2 * * * /usr/bin/python3 /usr/local/bin/php_security_check_html.py```

**🧾 6. Output dan Logging**

File laporan akan disimpan dengan format:

```security_report_YYYYMMDD_HHMMSS.html```


Contoh:

security_report_20251030_143548.html


Jika salah satu tool tidak ditemukan (misalnya trivy belum diinstal), script akan tetap berjalan dan menampilkan pesan:

"trivy": "/bin/sh: 1: trivy: not found"

**🧠 7. Tips Tambahan**

Gunakan PSR12 sebagai standar kode:

```phpcs --standard=PSR12 /var/www/html/sinerghi```


Pastikan Composer dependencies selalu update:

composer update
symfony check:security

**📌 8. Catatan**

Script ini hanya melakukan pemeriksaan statis (static analysis) — tidak memperbaiki otomatis.

Untuk hardening lebih lanjut, gabungkan dengan OWASP Dependency-Check atau SonarQube.