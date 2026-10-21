-- =============================================================================
-- SISTEM MANAJEMEN BASIS DATA (DBMS) STREAMLY (5 TABEL UTAMA)
-- Rujukan     : d:\KULIAH\SEMESTER 5\IMPAL\tubes\Streamly\skets\streamly_db_design\schema.sql
-- Mata Kuliah : Implementasi Perangkat Lunak (IMPAL) - Telkom University
-- Target DBMS : MySQL 8.0+
-- Deskripsi   : Skema Relasional Persisten Streamly (5 Tabel Sesuai Rancangan Asli)
-- =============================================================================

CREATE DATABASE IF NOT EXISTS streamly_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE streamly_db;

-- -----------------------------------------------------------------------------
-- 1. TABEL SESI SIARAN LANGSUNG (live_sessions)
-- Menyimpan sesi live streaming TikTok yang sedang atau telah dipantau
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS live_sessions (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  username VARCHAR(100) NOT NULL COMMENT 'TikTok creator username being monitored',
  room_id VARCHAR(100) NULL COMMENT 'TikTok room ID when provided by connector',
  status ENUM('starting','active','ended','failed') NOT NULL DEFAULT 'starting',
  started_at DATETIME(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  ended_at DATETIME(3) NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_sessions_username_started (username, started_at),
  KEY idx_sessions_status (status),
  CONSTRAINT chk_session_times CHECK (ended_at IS NULL OR ended_at >= started_at)
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 2. TABEL KOMENTAR CHAT AUDIENS (messages)
-- Menyimpan pesan chat mentah dari penonton TikTok Live per sesi siaran
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS messages (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  message_time DATETIME(3) NOT NULL,
  tiktok_user_id VARCHAR(100) NULL COMMENT 'TikTok commenter unique ID if available',
  display_name VARCHAR(100) NULL,
  message TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_messages_session_time (session_id, message_time),
  CONSTRAINT fk_messages_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 3. TABEL LAPORAN ANALISIS AI (insights)
-- Menyimpan laporan inferensi AI Gemini (5m, 20m, 45m)
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insights (
  id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
  session_id BIGINT UNSIGNED NOT NULL,
  batch_type ENUM('5m','20m','45m') NOT NULL,
  sentiment_score DECIMAL(5,4) NULL COMMENT 'Expected range -1.0000 to 1.0000',
  sentiment_trend ENUM('rising','falling','stable') NULL,
  emerging_topics JSON NULL,
  summary TEXT NOT NULL,
  actionable_insight TEXT NOT NULL,
  message_count INT UNSIGNED NOT NULL DEFAULT 0,
  model_name VARCHAR(100) NULL,
  generated_at DATETIME(3) NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (id),
  KEY idx_insights_session_type_time (session_id, batch_type, generated_at),
  CONSTRAINT fk_insights_session FOREIGN KEY (session_id)
    REFERENCES live_sessions(id) ON DELETE CASCADE,
  CONSTRAINT chk_sentiment_score CHECK (sentiment_score IS NULL OR (sentiment_score >= -1 AND sentiment_score <= 1))
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 4. TABEL PROVENANCE PESAN KE INSIGHT (insight_messages)
-- Menghubungkan komentar obrolan mana saja yang dianalisis dalam laporan 5m
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insight_messages (
  insight_id BIGINT UNSIGNED NOT NULL,
  message_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (insight_id, message_id),
  KEY idx_insight_messages_message (message_id),
  CONSTRAINT fk_im_insight FOREIGN KEY (insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT fk_im_message FOREIGN KEY (message_id)
    REFERENCES messages(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- -----------------------------------------------------------------------------
-- 5. TABEL RELASI DEPENDENSI INSIGHT HIERARKIS (insight_dependencies)
-- Menghubungkan laporan 20m/45m dengan input laporan 5m/20m sebelumnya
-- -----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS insight_dependencies (
  insight_id BIGINT UNSIGNED NOT NULL,
  source_insight_id BIGINT UNSIGNED NOT NULL,
  PRIMARY KEY (insight_id, source_insight_id),
  KEY idx_insight_dependencies_source (source_insight_id),
  CONSTRAINT fk_id_insight FOREIGN KEY (insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT fk_id_source_insight FOREIGN KEY (source_insight_id)
    REFERENCES insights(id) ON DELETE CASCADE,
  CONSTRAINT chk_insight_not_self CHECK (insight_id <> source_insight_id)
) ENGINE=InnoDB;

-- =============================================================================
-- INSERT 5 DATA CONTOH UNTUK MASING-MASING DARI 5 TABEL
-- =============================================================================

-- 1. INSERT 5 DATA live_sessions
INSERT INTO live_sessions (id, username, room_id, status, started_at, ended_at) VALUES
(1, 'glowup_official', 'ROOM_7382910481920', 'ended', '2026-10-19 19:00:00.000', '2026-10-19 21:00:00.000'),
(2, 'urbanstreet.id', 'ROOM_7382910481921', 'active', '2026-10-19 20:30:00.000', NULL),
(3, 'dapurbunda_live', 'ROOM_7382910481922', 'ended', '2026-10-18 14:00:00.000', '2026-10-18 15:45:00.000'),
(4, 'gadgetkita_shop', 'ROOM_7382910481923', 'ended', '2026-10-18 19:30:00.000', '2026-10-18 20:30:00.000'),
(5, 'batikheritagemodern', 'ROOM_7382910481924', 'active', '2026-10-19 21:00:00.000', NULL);

-- 2. INSERT 5 DATA messages
INSERT INTO messages (id, session_id, message_time, tiktok_user_id, display_name, message) VALUES
(1, 1, '2026-10-19 19:07:12.150', 'tt_user_8819', 'Rina Pratiwi', 'Kak, serum etalase 1 aman buat kulit sensitif bruntusan gak?'),
(2, 1, '2026-10-19 19:08:45.300', 'tt_user_2234', 'Budi Santoso', 'Spill diskonnya dong kak, kalau beli 2 dapet gratis ongkir kan?'),
(3, 1, '2026-10-19 19:09:10.820', 'tt_user_9941', 'Dewi Lestari', 'Udah checkout etalase 1 kak! Tolong kirim malam ini juga yaa'),
(4, 1, '2026-10-19 19:10:02.410', 'tt_user_5512', 'Agus Setiawan', 'Kak suaranya kok agak kresek-kresek ya di live barusan?'),
(5, 1, '2026-10-19 19:11:15.600', 'tt_user_7733', 'Maya Sari', 'Serumnya ada sertifikat BPOM dan Halal gak kak?');

-- 3. INSERT 5 DATA insights
INSERT INTO insights (id, session_id, batch_type, sentiment_score, sentiment_trend, emerging_topics, summary, actionable_insight, message_count, model_name, generated_at) VALUES
(1, 1, '5m', 0.8200, 'stable', '["kulit sensitif", "diskon beli 2", "bpom"]', 'Penonton antusias menanyakan kecocokan serum dan syarat promo diskon gajian.', 'Segera sematkan pin etalase 1 dan jelaskan izin resmi BPOM serum agar konversi checkout meningkat.', 48, 'gemini-2.5-flash', '2026-10-19 19:10:00.000'),
(2, 1, '5m', 0.7500, 'falling', '["audio kresek", "packing aman", "spill tekstur"]', 'Terdapat keluhan minor mengenai kejelasan audio mic host, namun minat beli tetap stabil.', 'Periksa koneksi clip-on mic host lalu lakukan demonstrasi oles tekstur serum di punggung tangan.', 62, 'gemini-2.5-flash', '2026-10-19 19:15:00.000'),
(3, 1, '5m', 0.8900, 'rising', '["promo bundle", "free gift", "checkout sukses"]', 'Lonjakan sentimen positif terjadi berkat bonus pouch bagi 10 pembeli tercepat.', 'Umumkan sisa kuota bonus flash sale secara berkala untuk menciptakan urgensi audiens.', 85, 'gemini-2.5-flash', '2026-10-19 19:20:00.000'),
(4, 1, '20m', 0.8200, 'rising', '["rekomendasi skincare", "flash sale gajian", "kecepatan kirim"]', 'Evolusi obrolan menunjukkan pergeseran dari tanya jawab bahan menuju keputusan checkout massal.', 'Pertahankan momentum interaksi dengan memberikan apresiasi nama akun penonton yang baru checkout.', 240, 'gemini-2.5-flash', '2026-10-19 19:25:00.000'),
(5, 1, '45m', 0.8450, 'stable', '["brand trust", "retensi tinggi", "sold out etalase 1"]', 'Secara umum sesi live berjalan efektif dengan tingkat retensi penonton tinggi dan stok menipis.', 'Siapkan produk etalase cadangan (toner atau moisturizer) sebelum stok serum etalase 1 habis total.', 520, 'gemini-2.5-flash', '2026-10-19 19:50:00.000');

-- 4. INSERT 5 DATA insight_messages
INSERT INTO insight_messages (insight_id, message_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5);

-- 5. INSERT 5 DATA insight_dependencies
INSERT INTO insight_dependencies (insight_id, source_insight_id) VALUES
(4, 1),
(4, 2),
(4, 3),
(5, 4),
(5, 1);
