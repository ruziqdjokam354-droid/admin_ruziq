Host: localhost
Database: ruziq_db
Username: ruziq354
Password: merdeka354
Port: 5432

# Setup Guide untuk Kasir Otomatis dengan PostgreSQL

## Prasyarat
- PostgreSQL terpasang dan berjalan (versi 12 atau lebih)
- Python 3.8 atau lebih
- pip (Python package manager)

## Langkah Setup

### 1. Install Dependencies Python
Buka terminal PowerShell/Command Prompt di folder project:
```bash
pip install -r requirements.txt
```

### 2. Setup Database (OTOMATIS)
Jalankan script setup database:
```bash
python setup_db.py
```

Script ini akan secara otomatis:
- Membuat database `ruziq_db` 
- Membuat semua tabel yang diperlukan
- Insert sample data (1 user, 3 produk)

**Jika terjadi error**, pastikan:
- PostgreSQL server sudah running
- Username `ruziq354` dan password `merdeka354` sudah dibuat di PostgreSQL
- Tidak ada firewall yang memblokir koneksi ke localhost:5432

Untuk membuat user PostgreSQL (jalankan sebagai admin):
```bash
psql -U postgres
CREATE USER ruziq354 WITH PASSWORD 'merdeka354';
ALTER ROLE ruziq354 CREATEDB;
\q
```

### 3. Jalankan Aplikasi Streamlit
```bash
streamlit run kasir.py
```

Aplikasi akan buka di browser: `http://localhost:8501`

## Konfigurasi Database

File `kasir.py` menggunakan konfigurasi:
- **Host**: localhost
- **Database**: ruziq_db
- **Username**: ruziq354
- **Password**: merdeka354
- **Port**: 5432

Untuk mengubah konfigurasi, edit bagian `DB_CONFIG` di awal file `kasir.py`:
```python
DB_CONFIG = {
    "host": "localhost",
    "database": "ruziq_db",
    "user": "ruziq354",
    "password": "merdeka354",
    "port": 5432
}
```

## Login Default

Setelah setup selesai, gunakan credentials ini:
- **Username**: `ruziq354`
- **Password**: `merdeka354`
- **Nama Kasir**: Muhammad Ruziq

Anda bisa menambah user baru langsung dari database atau dari menu aplikasi.

## Setup Manual (Alternatif)

Jika `setup_db.py` tidak bisa dijalankan, ikuti langkah ini:

### 1. Buat Database
```bash
createdb ruziq_db -U ruziq354
```

### 2. Buat Tabel dengan Script SQL
```bash
psql -U ruziq354 -d ruziq_db -f init_database.sql
```

### 3. Insert Sample Data
```sql
-- Insert sample user
INSERT INTO user_kasir (username, password, nama_kasir) 
VALUES ('ruziq354', 'merdeka354', 'Muhammad Ruziq');

-- Insert sample produk
INSERT INTO master_barang (kode, nama_barang, satuan, harga, modal, stok) 
VALUES 
('P0001', 'Semen 50kg', 'sak', 75000, 65000, 10),
('P0002', 'Pasir', 'rit', 120000, 100000, 5),
('P0003', 'Besi Beton 10mm', 'batang', 85000, 70000, 20);
```

## Troubleshooting

### "psycopg2" module not found
Jalankan:
```bash
pip install psycopg2-binary
```

### "could not connect to server"
- Pastikan PostgreSQL service sudah running: `net start postgresql-x64-15` (Windows)
- Cek apakah PostgreSQL listening di port 5432: `netstat -an | findstr 5432` (Windows)

### "FATAL: role 'ruziq354' does not exist"
Buat user PostgreSQL terlebih dahulu:
```bash
psql -U postgres
CREATE USER ruziq354 WITH PASSWORD 'merdeka354';
ALTER ROLE ruziq354 CREATEDB;
\q
```

### Error: "database 'ruziq_db' does not exist"
Jalankan `python setup_db.py` untuk membuat database secara otomatis, atau gunakan setup manual di atas.

### "relation 'transaksi' does not exist"
Jalankan `python setup_db.py` atau `psql -U ruziq354 -d ruziq_db -f init_database.sql`

## Fitur Aplikasi

1. **🔐 Login Kasir** - Multi user dengan username/password
2. **📝 Input Transaksi** - Catat penjualan dengan support desimal
3. **📊 Data Transaksi** - Lihat dan manage semua transaksi
4. **🛠️ Manajemen Stok** - Tambah/update stok & produk baru
5. **📈 Dashboard** - Analisis penjualan dan keuntungan

## File-file Penting

- `kasir.py` - Aplikasi utama Streamlit
- `setup_db.py` - Script setup database otomatis
- `requirements.txt` - Python dependencies
- `init_database.sql` - SQL schema (digunakan jika setup manual)
- `SETUP_GUIDE.md` - Panduan ini

---
**Created**: 2026-02-11  
**Database**: PostgreSQL  
**Framework**: Streamlit  
**Author**: Muhammad Ruziq
