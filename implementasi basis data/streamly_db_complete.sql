-- =============================================================================
-- SISTEM MANAJEMEN BASIS DATA (DBMS) STREAMLY
-- Proyek     : Streamly - Intelligent Omni-Channel Live Streaming Co-Pilot
-- Mata Kuliah: Implementasi Perangkat Lunak (IMPAL) - Telkom University
-- Target DBMS: MySQL 8.0+
-- Deskripsi  : Skema Terintegrasi Social Commerce (Toko, Kasir, Live Session, AI Insights)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS streamly_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE streamly_db;

-- -----------------------------------------------------------------------------
-- 1. TABEL PENGGUNA (users)
-- Menyimpan akun pengguna sistem (Streamer, Host, Admin Toko, dan Analis)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  role ENUM('streamer', 'store_admin', 'analyst') NOT NULL DEFAULT 'streamer',
  phone_number VARCHAR(20) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_users_username (username),
  UNIQUE KEY uk_users_email (email)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 2. TABEL TOKO / MERCHANT (merchants)
-- Menyimpan entitas Toko/UMKM yang menyelenggarakan siaran live shopping
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS merchants (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  owner_id BIGINT UNSIGNED NOT NULL,
  store_name VARCHAR(100) NOT NULL,
  tiktok_shop_id VARCHAR(100) NULL,
  category VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_merchants_tiktok_shop (tiktok_shop_id),
  KEY idx_merchants_owner (owner_id),
  CONSTRAINT fk_merchants_owner FOREIGN KEY (owner_id)
    REFERENCES users(id) ON DELETE RESTRICT
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 3. TABEL KATALOG PRODUK (products)
-- Menyimpan katalog barang yang dijual tokomart di TikTok Shop
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  merchant_id BIGINT UNSIGNED NOT NULL,
  sku VARCHAR(50) NOT NULL,
  name VARCHAR(150) NOT NULL,
  description TEXT NULL,
  price DECIMAL(12,2) NOT NULL,
  stock INT UNSIGNED NOT NULL DEFAULT 0,
  category VARCHAR(50) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_products_sku (sku),
  KEY idx_products_merchant (merchant_id),
  CONSTRAINT fk_products_merchant FOREIGN KEY (merchant_id)
    REFERENCES merchants(id) ON DELETE CASCADE,
  CONSTRAINT chk_products_price CHECK (price >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 4. TABEL SESI SIARAN LANGSUNG (live_sessions)
-- Menyimpan riwayat jalannya live streaming yang dibawakan streamer untuk toko
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS live_sessions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  merchant_id BIGINT UNSIGNED NOT NULL,
  host_user_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(200) NOT NULL,
  tiktok_username VARCHAR(100) NOT NULL COMMENT 'Akun TikTok yang dipantau scraper',
  room_id VARCHAR(100) NULL COMMENT 'TikTok Room ID dari event connector',
  status ENUM('starting', 'active', 'ended', 'failed') NOT NULL DEFAULT 'starting',
  started_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  ended_at DATETIME(3) NULL,
  total_views INT UNSIGNED NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_sessions_merchant (merchant_id),
  KEY idx_sessions_host (host_user_id),
  KEY idx_sessions_user_time (tiktok_username, started_at),
  KEY idx_sessions_status (status),
  CONSTRAINT fk_sessions_merchant FOREIGN KEY (merchant_id)
    REFERENCES merchants(id) ON DELETE RESTRICT,
  CONSTRAINT fk_sessions_host FOREIGN KEY (host_user_id)
    REFERENCES users(id) ON DELETE RESTRICT,
  CONSTRAINT chk_session_times CHECK (ended_at IS NULL OR ended_at >= started_at)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 5. TABEL ETALASE / PRODUK PIN LIVE (session_pinned_products)
-- Menghubungkan produk yang di-pin/dipromosikan selama sesi live tertentu
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS session_pinned_products (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  pin_order INT UNSIGNED NOT NULL DEFAULT 1 COMMENT 'Nomor urut etalase keranjang kuning',
  discount_price DECIMAL(12,2) NULL COMMENT 'Harga spesial flash sale saat live',
  is_currently_pinned BOOLEAN NOT NULL DEFAULT FALSE,
  pinned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_session_product (session_id, product_id),
  KEY idx_spp_product (product_id),
  CONSTRAINT fk_spp_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE CASCADE,
  CONSTRAINT fk_spp_product FOREIGN KEY (product_id)
    REFERENCES products(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 6. TABEL KOMENTAR CHAT AUDIENS (messages)
-- Menyimpan rekaman pesan chat penonton yang ditangkap oleh TikTokScraper
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  message_time DATETIME(3) NOT NULL,
  tiktok_user_id VARCHAR(100) NULL,
  display_name VARCHAR(100) NULL,
  message TEXT NOT NULL,
  sentiment_label ENUM('positive', 'negative', 'neutral') NULL,
  is_potential_buyer BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_messages_session_time (session_id, message_time),
  CONSTRAINT fk_messages_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 7. TABEL TRANSAKSI KASIR LIVE (orders)
-- Mencatat pesanan dan transaksi yang terjadi langsung selama sesi siaran
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  merchant_id BIGINT UNSIGNED NOT NULL,
  order_number VARCHAR(50) NOT NULL,
  buyer_name VARCHAR(100) NOT NULL,
  buyer_phone VARCHAR(20) NOT NULL,
  payment_method ENUM('cash_on_delivery', 'qris', 'bank_transfer', 'e_wallet') NOT NULL,
  payment_status ENUM('unpaid', 'paid', 'refunded', 'cancelled') NOT NULL DEFAULT 'paid',
  total_amount DECIMAL(12,2) NOT NULL,
  order_time DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  UNIQUE KEY uk_orders_number (order_number),
  KEY idx_orders_session (session_id),
  KEY idx_orders_merchant (merchant_id),
  CONSTRAINT fk_orders_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE RESTRICT,
  CONSTRAINT fk_orders_merchant FOREIGN KEY (merchant_id)
    REFERENCES merchants(id) ON DELETE RESTRICT,
  CONSTRAINT chk_orders_total CHECK (total_amount >= 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 8. TABEL DETAIL ITEM TRANSAKSI KASIR (order_items)
-- Menyimpan rincian produk yang dibeli per transaksi kasir
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  order_id BIGINT UNSIGNED NOT NULL,
  product_id BIGINT UNSIGNED NOT NULL,
  quantity INT UNSIGNED NOT NULL DEFAULT 1,
  unit_price DECIMAL(12,2) NOT NULL,
  subtotal DECIMAL(12,2) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_items_order (order_id),
  KEY idx_items_product (product_id),
  CONSTRAINT fk_items_order FOREIGN KEY (order_id)
    REFERENCES orders(id) ON DELETE CASCADE,
  CONSTRAINT fk_items_product FOREIGN KEY (product_id)
    REFERENCES products(id) ON DELETE RESTRICT,
  CONSTRAINT chk_items_quantity CHECK (quantity > 0)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 9. TABEL LAPORAN AI INSIGHT (insights)
-- Menyimpan hasil inferensi AI Gemini dalam jendela 5m, 20m, dan 45m
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insights (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  batch_type ENUM('5m', '20m', '45m') NOT NULL,
  sentiment_score DECIMAL(5,4) NULL COMMENT 'Nilai -1.0000 sampai 1.0000',
  sentiment_trend ENUM('rising', 'falling', 'stable') NULL,
  emerging_topics JSON NULL,
  summary TEXT NOT NULL,
  actionable_insight TEXT NOT NULL,
  message_count INT UNSIGNED NOT NULL DEFAULT 0,
  model_name VARCHAR(100) NOT NULL DEFAULT 'gemini-2.5-flash',
  generated_at DATETIME(3) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_insights_session_type_time (session_id, batch_type, generated_at),
  CONSTRAINT fk_insights_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE CASCADE,
  CONSTRAINT chk_insights_sentiment CHECK (sentiment_score IS NULL OR (sentiment_score >= -1 AND sentiment_score <= 1))
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 10. TABEL PROVENANCE PESAN KE INSIGHT (insight_messages)
-- Menghubungkan komentar obrolan mana saja yang dianalisis dalam laporan 5m
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insight_messages (
  insight_id BIGINT UNSIGNED NOT NULL,
  message_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (insight_id, message_id),
  KEY idx_im_message (message_id),
  CONSTRAINT fk_im_insight FOREIGN KEY (insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT fk_im_message FOREIGN KEY (message_id)
    REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 11. TABEL RELASI DEPENDENSI INSIGHT HIERARKIS (insight_dependencies)
-- Menghubungkan laporan 20m/45m dengan input laporan 5m/20m sebelumnya
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insight_dependencies (
  insight_id BIGINT UNSIGNED NOT NULL,
  source_insight_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (insight_id, source_insight_id),
  KEY idx_id_source (source_insight_id),
  CONSTRAINT fk_id_insight FOREIGN KEY (insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT fk_id_source_insight FOREIGN KEY (source_insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT chk_not_self_dependency CHECK (insight_id <> source_insight_id)
) ENGINE=InnoDB;

-- =============================================================================
-- INSERT 5 DATA CONTOH UNTUK SETIAP TABEL
-- Memenuhi syarat integritas referensial antar tabel
-- =============================================================================

-- 1. Insert 5 Data Users
INSERT INTO users (id, username, email, password_hash, full_name, role, phone_number) VALUES
(1, 'aryo_streamer', 'aryo@streamly.id', '$2y$10$abcdef1234567890QWERTYuiopasdfghjklzxcvbnm12345678901', 'Aryo Abdillah A.', 'streamer', '081234567891'),
(2, 'annisa_admin', 'annisa@glowupbeauty.com', '$2y$10$abcdef1234567890QWERTYuiopasdfghjklzxcvbnm12345678902', 'Annisa Nur Shadrina', 'store_admin', '081234567892'),
(3, 'fadia_host', 'fadia@urbanstreet.co.id', '$2y$10$abcdef1234567890QWERTYuiopasdfghjklzxcvbnm12345678903', 'Fadia Nabila Shifa', 'streamer', '081234567893'),
(4, 'refito_analyst', 'refito@agencygrowth.com', '$2y$10$abcdef1234567890QWERTYuiopasdfghjklzxcvbnm12345678904', 'Refito Rahmat F.', 'analyst', '081234567894'),
(5, 'revaldi_host', 'revaldi@gadgetkita.com', '$2y$10$abcdef1234567890QWERTYuiopasdfghjklzxcvbnm12345678905', 'Revaldi Ramadhan N.', 'streamer', '081234567895');

-- 2. Insert 5 Data Merchants
INSERT INTO merchants (id, owner_id, store_name, tiktok_shop_id, category, city) VALUES
(1, 2, 'GlowUp Beauty Official', 'TTSHOP_GLOWUP_001', 'Beauty & Personal Care', 'Jakarta Selatan'),
(2, 3, 'UrbanStreet Apparel', 'TTSHOP_URBAN_002', 'Fashion Pria & Wanita', 'Bandung'),
(3, 2, 'DapurBunda Snack & Cookies', 'TTSHOP_DAPUR_003', 'Food & Beverage', 'Surabaya'),
(4, 5, 'GadgetKita Store', 'TTSHOP_GADGET_004', 'Elektronik & Aksesoris', 'Semarang'),
(5, 1, 'Batik Heritage Modern', 'TTSHOP_BATIK_005', 'Fashion Tradisional', 'Solo');

-- 3. Insert 5 Data Products
INSERT INTO products (id, merchant_id, sku, name, description, price, stock, category) VALUES
(1, 1, 'GLW-SRM-01', 'GlowUp Niacinamide 10% Brightening Serum 30ml', 'Serum pencerah wajah dengan ekstrak licorice dan zinc PCA.', 89000.00, 250, 'Skincare'),
(2, 2, 'URB-HD-02', 'UrbanStreet Oversized Heavyweight Hoodie Black', 'Hoodie katun fleece tebal 330gsm nyaman dipakai harian.', 219000.00, 80, 'Pakaian'),
(3, 3, 'DPB-KRP-03', 'Keripik Kentang Balado Spesial Daun Jeruk 200g', 'Keripik kentang renyah bumbu cabai asli tanpa pengawet.', 35000.00, 500, 'Makanan Ringan'),
(4, 4, 'GDT-TWS-04', 'GadgetKita True Wireless Earphones Pro Noise Cancelling', 'Bluetooth 5.3 dengan latensi rendah 45ms dan baterai 24 jam.', 179000.00, 120, 'Aksesoris HP'),
(5, 5, 'BTK-SLM-05', 'Kemeja Batik Katun Slimfit Motif Parang Modern', 'Batik katun primis halus dengan jahitan furing furing trikot.', 145000.00, 95, 'Kemeja');

-- 4. Insert 5 Data Live Sessions
INSERT INTO live_sessions (id, merchant_id, host_user_id, title, tiktok_username, room_id, status, started_at, ended_at, total_views) VALUES
(1, 1, 1, 'Gajian Cantik! Diskon Skincare Up to 50% + Free Gift', 'glowup_official', 'ROOM_7382910481920', 'ended', '2026-10-19 19:00:00.000', '2026-10-19 21:00:00.000', 8540),
(2, 2, 3, 'Midnight Drop! Koleksi Hoodie Streetwear Terbaru', 'urbanstreet.id', 'ROOM_7382910481921', 'active', '2026-10-19 20:30:00.000', NULL, 4320),
(3, 3, 1, 'Mukbang & Review Keripik Daun Jeruk Pedas Nampol', 'dapurbunda_live', 'ROOM_7382910481922', 'ended', '2026-10-18 14:00:00.000', '2026-10-18 15:45:00.000', 2890),
(4, 4, 5, 'Spill Audio TWS Murah! Bass Nendang Test Mic', 'gadgetkita_shop', 'ROOM_7382910481923', 'ended', '2026-10-18 19:30:00.000', '2026-10-18 20:30:00.000', 6120),
(5, 5, 5, 'Kemeja Batik Elegan Buat Wisuda & Ngantor Hemat', 'batikheritagemodern', 'ROOM_7382910481924', 'active', '2026-10-19 21:00:00.000', NULL, 1850);

-- 5. Insert 5 Data Session Pinned Products
INSERT INTO session_pinned_products (id, session_id, product_id, pin_order, discount_price, is_currently_pinned, pinned_at) VALUES
(1, 1, 1, 1, 75000.00, TRUE, '2026-10-19 19:05:00'),
(2, 2, 2, 1, 189000.00, TRUE, '2026-10-19 20:35:00'),
(3, 3, 3, 1, 29000.00, FALSE, '2026-10-18 14:05:00'),
(4, 4, 4, 1, 149000.00, FALSE, '2026-10-18 19:35:00'),
(5, 5, 5, 1, 125000.00, TRUE, '2026-10-19 21:05:00');

-- 6. Insert 5 Data Messages
INSERT INTO messages (id, session_id, message_time, tiktok_user_id, display_name, message, sentiment_label, is_potential_buyer) VALUES
(1, 1, '2026-10-19 19:07:12.150', 'tt_user_8819', 'Rina Pratiwi', 'Kak, serum etalase 1 aman buat kulit sensitif bruntusan gak?', 'positive', TRUE),
(2, 1, '2026-10-19 19:08:45.300', 'tt_user_2234', 'Budi Santoso', 'Spill diskonnya dong kak, kalau beli 2 dapet gratis ongkir kan?', 'positive', TRUE),
(3, 1, '2026-10-19 19:09:10.820', 'tt_user_9941', 'Dewi Lestari', 'Udah checkout etalase 1 kak! Tolong kirim malam ini juga yaa', 'positive', TRUE),
(4, 1, '2026-10-19 19:10:02.410', 'tt_user_5512', 'Agus Setiawan', 'Kak suaranya kok agak kresek-kresek ya di live barusan?', 'negative', FALSE),
(5, 1, '2026-10-19 19:11:15.600', 'tt_user_7733', 'Maya Sari', 'Serumnya ada sertifikat BPOM dan Halal gak kak?', 'neutral', TRUE);

-- 7. Insert 5 Data Orders (Kasir / Transaksi Live)
INSERT INTO orders (id, session_id, merchant_id, order_number, buyer_name, buyer_phone, payment_method, payment_status, total_amount, order_time) VALUES
(1, 1, 1, 'ORD-LIVE-20261019-001', 'Dewi Lestari', '082199887711', 'qris', 'paid', 75000.00, '2026-10-19 19:12:00.000'),
(2, 1, 1, 'ORD-LIVE-20261019-002', 'Budi Santoso', '081344556677', 'e_wallet', 'paid', 150000.00, '2026-10-19 19:15:20.000'),
(3, 2, 2, 'ORD-LIVE-20261019-003', 'Fikri Haikal', '085711223344', 'bank_transfer', 'paid', 189000.00, '2026-10-19 20:45:10.000'),
(4, 3, 3, 'ORD-LIVE-20261018-004', 'Siti Rahmawati', '087822334455', 'cash_on_delivery', 'paid', 58000.00, '2026-10-18 14:30:00.000'),
(5, 4, 4, 'ORD-LIVE-20261018-005', 'Kevin Pratama', '089633445566', 'qris', 'paid', 149000.00, '2026-10-18 19:42:30.000');

-- 8. Insert 5 Data Order Items
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price, subtotal) VALUES
(1, 1, 1, 1, 75000.00, 75000.00),
(2, 2, 1, 2, 75000.00, 150000.00),
(3, 3, 2, 1, 189000.00, 189000.00),
(4, 4, 3, 2, 29000.00, 58000.00),
(5, 5, 4, 1, 149000.00, 149000.00);

-- 9. Insert 5 Data Insights (AI Model Output)
INSERT INTO insights (id, session_id, batch_type, sentiment_score, sentiment_trend, emerging_topics, summary, actionable_insight, message_count, model_name, generated_at) VALUES
(1, 1, '5m', 0.8200, 'stable', '["kulit sensitif", "diskon beli 2", "bpom"]', 'Penonton antusias menanyakan kecocokan serum untuk kulit berjerawat dan syarat promo diskon gajian.', 'Segera sematkan pin etalase 1 dan jelaskan izin resmi BPOM serum agar konversi checkout meningkat.', 48, 'gemini-2.5-flash', '2026-10-19 19:10:00.000'),
(2, 1, '5m', 0.7500, 'falling', '["audio kresek", "packing aman", "spill tekstur"]', 'Terdapat keluhan minor mengenai kejelasan audio mic host, namun minat beli terhadap tekstur serum tetap stabil.', 'Periksa koneksi clip-on mic host lalu lakukan demonstrasi oles tekstur serum di punggung tangan.', 62, 'gemini-2.5-flash', '2026-10-19 19:15:00.000'),
(3, 1, '5m', 0.8900, 'rising', '["promo bundle", "free gift", "checkout sukses"]', 'Lonjakan sentimen positif terjadi berkat pengumuman bonus spatula dan pouch bagi 10 pembeli tercepat.', 'Umumkan sisa kuota bonus flash sale secara berkala untuk menciptakan urgensi pembelian bagi penonton baru.', 85, 'gemini-2.5-flash', '2026-10-19 19:20:00.000'),
(4, 1, '20m', 0.8200, 'rising', '["rekomendasi skincare", "flash sale gajian", "kecepatan kirim"]', 'Evolusi obrolan menunjukkan transisi cepat dari tahap tanya jawab komposisi bahan menuju keputusan checkout massal.', 'Pertahankan momentum interaksi dengan memberikan apresiasi nama-nama akun penonton yang baru saja checkout.', 240, 'gemini-2.5-flash', '2026-10-19 19:25:00.000'),
(5, 1, '45m', 0.8450, 'stable', '["brand trust", "retensi tinggi", "sold out etalase 1"]', 'Secara keseluruhan paruh pertama sesi live berlangsung efektif dengan tingkat retensi penonton tinggi dan stok menipis.', 'Siapkan produk etalase cadangan (toner atau moisturizer) sebelum stok serum etalase 1 habis total.', 520, 'gemini-2.5-flash', '2026-10-19 19:50:00.000');

-- 10. Insert 5 Data Insight Messages (Traceability 5m Insight -> Messages)
INSERT INTO insight_messages (insight_id, message_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5);

-- 11. Insert 5 Data Insight Dependencies (Hierarchical Insight Synthesis)
INSERT INTO insight_dependencies (insight_id, source_insight_id) VALUES
(4, 1),
(4, 2),
(4, 3),
(5, 4),
(5, 1);
