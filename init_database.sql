-- Create master_barang table
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
);

-- Create transaksi table
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
);

-- Create user_kasir table
CREATE TABLE IF NOT EXISTS user_kasir (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    nama_kasir VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_master_barang_nama ON master_barang(nama_barang);
CREATE INDEX IF NOT EXISTS idx_transaksi_kasir ON transaksi(kasir);
CREATE INDEX IF NOT EXISTS idx_transaksi_tanggal ON transaksi(tanggal_waktu);
CREATE INDEX IF NOT EXISTS idx_transaksi_barang ON transaksi(nama_barang);
CREATE INDEX IF NOT EXISTS idx_user_kasir_username ON user_kasir(username);
