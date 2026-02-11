#!/usr/bin/env python3
"""
Script untuk setup database PostgreSQL dan insert sample data
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
import sys

DB_CONFIG = {
    "host": "localhost",
    "database": "postgres",  # Koneksi ke database default dulu
    "user": "ruziq354",
    "password": "merdeka354",
    "port": 5432
}

DB_TARGET = "ruziq_db"

def create_database():
    """Buat database ruziq_db jika belum ada"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Cek apakah database sudah ada
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_TARGET,))
        if cursor.fetchone():
            print(f"✓ Database '{DB_TARGET}' sudah ada")
        else:
            cursor.execute(f"CREATE DATABASE {DB_TARGET}")
            print(f"✓ Database '{DB_TARGET}' berhasil dibuat")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error membuat database: {e}")
        return False

def create_tables():
    """Buat tabel-tabel yang diperlukan"""
    try:
        config = DB_CONFIG.copy()
        config["database"] = DB_TARGET
        conn = psycopg2.connect(**config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create master_barang table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_barang (
            id SERIAL PRIMARY KEY,
            kode VARCHAR(50),
            nama_barang VARCHAR(255) NOT NULL UNIQUE,
            satuan VARCHAR(50) NOT NULL,
            harga DECIMAL(12, 2) NOT NULL,
            modal DECIMAL(12, 2) DEFAULT 0,
            stok DECIMAL(12, 2) NOT NULL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✓ Tabel 'master_barang' dibuat")
        
        # Create transaksi table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id SERIAL PRIMARY KEY,
            kasir VARCHAR(255) NOT NULL,
            nama_barang VARCHAR(255) NOT NULL,
            jumlah DECIMAL(12, 2) NOT NULL,
            satuan VARCHAR(50) NOT NULL,
            harga DECIMAL(12, 2) NOT NULL,
            total_harga DECIMAL(12, 2) NOT NULL,
            tanggal_waktu TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (nama_barang) REFERENCES master_barang(nama_barang)
        )
        """)
        print("✓ Tabel 'transaksi' dibuat")
        
        # Create user_kasir table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_kasir (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL UNIQUE,
            password VARCHAR(100) NOT NULL,
            nama_kasir VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        print("✓ Tabel 'user_kasir' dibuat")
        
        # Create indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_master_barang_nama ON master_barang(nama_barang)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaksi_kasir ON transaksi(kasir)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaksi_tanggal ON transaksi(tanggal_waktu)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transaksi_barang ON transaksi(nama_barang)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_kasir_username ON user_kasir(username)")
        print("✓ Index berhasil dibuat")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error membuat tabel: {e}")
        return False

def insert_sample_data():
    """Insert sample data ke database"""
    try:
        config = DB_CONFIG.copy()
        config["database"] = DB_TARGET
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Cek apakah user sudah ada
        cursor.execute("SELECT COUNT(*) FROM user_kasir")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO user_kasir (username, password, nama_kasir) 
            VALUES (%s, %s, %s)
            """, ("ruziq354", "merdeka354", "Muhammad Ruziq"))
            print("✓ Sample user 'ruziq354' ditambahkan")
        else:
            print("✓ User sudah ada, skip insert")
        
        # Cek apakah produk sudah ada
        cursor.execute("SELECT COUNT(*) FROM master_barang")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
            INSERT INTO master_barang (kode, nama_barang, satuan, harga, modal, stok) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, ("P0001", "Semen 50kg", "sak", 75000, 65000, 10))
            
            cursor.execute("""
            INSERT INTO master_barang (kode, nama_barang, satuan, harga, modal, stok) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, ("P0002", "Pasir", "rit", 120000, 100000, 5))
            
            cursor.execute("""
            INSERT INTO master_barang (kode, nama_barang, satuan, harga, modal, stok) 
            VALUES (%s, %s, %s, %s, %s, %s)
            """, ("P0003", "Besi Beton 10mm", "batang", 85000, 70000, 20))
            
            print("✓ Sample produk ditambahkan (3 item)")
        else:
            print("✓ Produk sudah ada, skip insert")
        
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Error insert data: {e}")
        return False

def main():
    print("=" * 50)
    print("SETUP DATABASE KASIR OTOMATIS")
    print("=" * 50)
    
    print("\n1. Membuat database...")
    if not create_database():
        print("\n✗ GAGAL: Database tidak berhasil dibuat")
        return False
    
    print("\n2. Membuat tabel...")
    if not create_tables():
        print("\n✗ GAGAL: Tabel tidak berhasil dibuat")
        return False
    
    print("\n3. Insert sample data...")
    if not insert_sample_data():
        print("\n✗ GAGAL: Data tidak berhasil ditambahkan")
        return False
    
    print("\n" + "=" * 50)
    print("✓ SETUP DATABASE BERHASIL")
    print("=" * 50)
    print("\nAnda bisa menjalankan aplikasi dengan:")
    print("  streamlit run kasir.py")
    print("\nLogin credentials:")
    print("  Username: ruziq354")
    print("  Password: merdeka354")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
