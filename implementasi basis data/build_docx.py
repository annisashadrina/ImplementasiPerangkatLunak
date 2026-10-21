import os
import docx
from docx import Document
from docx.shared import Pt, Inches, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def set_table_borders(table, color="CBD5E0", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_code_block(doc, code_text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Cm(16.0)

    cell = table.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Border khusus code block
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="2C7A7B"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    
    run = p.add_run(code_text.strip())
    run.font.name = 'Consolas'
    run.font.size = Pt(8.0)
    run.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_docx(output_path):
    doc = Document()

    # Page Margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Style defaults
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Arial'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)

    # ==================== HALAMAN SAMPUL ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(6)
    run_title = p_title.add_run("LAPORAN PERANCANGAN BASIS DATA")
    run_title.font.name = 'Arial'
    run_title.font.size = Pt(20)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1A, 0x20, 0x2C)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run("Sintaks SQL DDL (Create Table) & DML (Insert 5 Data)")
    run_sub.font.name = 'Arial'
    run_sub.font.size = Pt(12)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x2C, 0x7A, 0x7B)

    p_badge = doc.add_paragraph()
    p_badge.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_badge.paragraph_format.space_after = Pt(24)
    run_badge = p_badge.add_run("PROYEK TUBES: STREAMLY (TIKTOK LIVE AI CHAT ANALYZER)")
    run_badge.font.name = 'Arial'
    run_badge.font.size = Pt(9.5)
    run_badge.font.bold = True
    run_badge.font.color.rgb = RGBColor(0x23, 0x4E, 0x52)

    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc.paragraph_format.space_after = Pt(30)
    run_desc = p_desc.add_run(
        "Implementasi Skema Relasional Persisten 5 Tabel Sesuai Rancangan Asli:\n"
        "tubes/Streamly/skets/streamly_db_design/schema.sql\n"
        "Mencakup Sesi Streaming, Riwayat Komentar, Analisis AI, dan Keterlacakan Data (Provenance)."
    )
    run_desc.font.name = 'Arial'
    run_desc.font.size = Pt(9.5)
    run_desc.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    # Tabel Anggota
    p_group = doc.add_paragraph()
    p_group.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_group.paragraph_format.space_after = Pt(8)
    run_group = p_group.add_run("Disusun oleh Kelompok:")
    run_group.font.bold = True
    run_group.font.size = Pt(10)

    members = [
        ("No", "Nama Anggota", "NIM"),
        ("1", "Aryo Abdillah Ainnurrofiq", "103072400006"),
        ("2", "Annisa Nur Shadrina", "103072400134"),
        ("3", "Fadia Nabila Shifa", "10307200066"),
        ("4", "Refito Rahmat Firmansyah", "103072430002"),
        ("5", "Revaldi Ramadhan Nugraha", "103072400059")
    ]

    t_members = doc.add_table(rows=len(members), cols=3)
    t_members.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_members.autofit = False
    set_table_borders(t_members)

    col_widths = [Cm(1.5), Cm(9.5), Cm(5.0)]

    for row_idx, row_data in enumerate(members):
        for col_idx, text in enumerate(row_data):
            cell = t_members.cell(row_idx, col_idx)
            cell.width = col_widths[col_idx]
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(text)
            run.font.name = 'Arial'

            if row_idx == 0:
                set_cell_background(cell, "2C7A7B")
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                if row_idx % 2 == 0:
                    set_cell_background(cell, "F7FAFC")
                run.font.size = Pt(9)
                if col_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif col_idx == 1:
                    run.font.bold = True
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(50)

    p_footer = doc.add_paragraph()
    p_footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_footer = p_footer.add_run(
        "PROGRAM STUDI S1 INFORMATIKA\n"
        "FAKULTAS INFORMATIKA — UNIVERSITAS TELKOM\n"
        "Mata Kuliah: Implementasi Perangkat Lunak (IMPAL)\n"
        "Tahun 2026"
    )
    run_footer.font.name = 'Arial'
    run_footer.font.size = Pt(9.5)
    run_footer.font.bold = True
    run_footer.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)

    doc.add_page_break()

    # ==================== BAB 1 ====================
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Deskripsi Skema Basis Data 5 Tabel Streamly")
    r_h1.font.bold = True
    r_h1.font.size = Pt(14)
    r_h1.font.color.rgb = RGBColor(0x23, 0x4E, 0x52)

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_after = Pt(6)
    p1.paragraph_format.line_spacing = 1.2
    p1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p1.add_run(
        "Rancangan basis data relasional ini mengacu secara langsung pada dokumen sketsa asli di "
        "tubes/Streamly/skets/streamly_db_design/schema.sql dan ERD.md. Di dalam sistem Streamly, "
        "Redis bertugas mengelola antrean pesan waktu nyata (real-time queue) dan cache insight cepat, "
        "sedangkan MySQL bertindak sebagai penyimpan riwayat permanen (durable history)."
    )

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(8)
    p2.add_run("Skema terdiri dari 5 tabel utama yang saling terhubung melalui relasi kunci asing (Foreign Key):")

    table_info = [
        ("No", "Nama Tabel", "Peran & Kardinalitas", "Deskripsi Fungsi"),
        ("1", "live_sessions", "1 baris per siaran live", "Mencatat satu siklus monitoring scraper terhadap live streaming seorang kreator TikTok."),
        ("2", "messages", "N baris per session (1:N)", "Menyimpan rekaman obrolan mentah penonton TikTok yang ditangkap scraper."),
        ("3", "insights", "N baris per session (1:N)", "Menyimpan hasil analisis AI Gemini dalam 3 jendela waktu (5m, 20m, 45m)."),
        ("4", "insight_messages", "Many-to-Many (M:N)", "Tabel relasi pelacakan (provenance) komentar mentah mana saja yang dianalisis pada laporan 5m."),
        ("5", "insight_dependencies", "Many-to-Many (M:N)", "Tabel relasi turunan hierarkis (laporan 5m menjadi input laporan 20m, dan 20m menjadi input 45m).")
    ]

    t_info = doc.add_table(rows=len(table_info), cols=4)
    t_info.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_info.autofit = False
    set_table_borders(t_info)
    t_widths = [Cm(1.2), Cm(4.0), Cm(3.8), Cm(7.0)]

    for r_idx, r_data in enumerate(table_info):
        for c_idx, val in enumerate(r_data):
            cell = t_info.cell(r_idx, c_idx)
            cell.width = t_widths[c_idx]
            set_cell_margins(cell, top=70, bottom=70, left=90, right=90)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.15
            run = p.add_run(val)

            if r_idx == 0:
                set_cell_background(cell, "2C7A7B")
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                if r_idx % 2 == 0:
                    set_cell_background(cell, "F7FAFC")
                run.font.size = Pt(8.5)
                if c_idx == 0:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                elif c_idx == 1:
                    run.font.bold = True
                    run.font.name = 'Consolas'

    doc.add_page_break()

    # ==================== BAB 2 ====================
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Sintaks SQL DDL (Create 5 Tabel)")
    r_h2.font.bold = True
    r_h2.font.size = Pt(14)
    r_h2.font.color.rgb = RGBColor(0x23, 0x4E, 0x52)

    p_ddl_desc = doc.add_paragraph()
    p_ddl_desc.paragraph_format.space_after = Pt(8)
    p_ddl_desc.add_run(
        "Berikut adalah sintaks DDL (Data Definition Language) lengkap untuk membuat basis data streamly_db "
        "dan kelima tabel relasional persisten menggunakan MySQL 8.0+ sesuai berkas rancangan:"
    )

    sql_ddl_content = """-- =============================================================================
-- DDL PEMBUATAN DATABASE DAN 5 TABEL UTAMA STREAMLY
-- Rujukan: tubes/Streamly/skets/streamly_db_design/schema.sql
-- =============================================================================
CREATE DATABASE IF NOT EXISTS streamly_db
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE streamly_db;

-- 1. TABEL SESI SIARAN LANGSUNG (live_sessions)
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

-- 2. TABEL KOMENTAR CHAT AUDIENS (messages)
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

-- 3. TABEL LAPORAN ANALISIS AI (insights)
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

-- 4. TABEL PROVENANCE PESAN KE INSIGHT (insight_messages)
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

-- 5. TABEL RELASI DEPENDENSI INSIGHT HIERARKIS (insight_dependencies)
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
) ENGINE=InnoDB;"""

    add_code_block(doc, sql_ddl_content)

    doc.add_page_break()

    # ==================== BAB 3 ====================
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(12)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Sintaks SQL DML (Insert 5 Data Tiap Tabel)")
    r_h3.font.bold = True
    r_h3.font.size = Pt(14)
    r_h3.font.color.rgb = RGBColor(0x23, 0x4E, 0x52)

    p_dml_desc = doc.add_paragraph()
    p_dml_desc.paragraph_format.space_after = Pt(8)
    p_dml_desc.add_run(
        "Berikut adalah sintaks DML (Data Manipulation Language) yang memasukkan tepat 5 baris data contoh "
        "ke dalam masing-masing dari 5 tabel (total 25 baris data). Data disusun realistis sesuai skenario siaran langsung "
        "TikTok di Indonesia dan menjaga integritas referensial kunci asing:"
    )

    sql_dml_content = """-- =============================================================================
-- DML INSERT 5 DATA CONTOH UNTUK MASING-MASING DARI 5 TABEL
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

-- 4. INSERT 5 DATA insight_messages (PROVENANCE KOMENTAR KE INSIGHT 5m)
INSERT INTO insight_messages (insight_id, message_id) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5);

-- 5. INSERT 5 DATA insight_dependencies (SINTESIS HIERARKIS ANTAR-INSIGHT)
INSERT INTO insight_dependencies (insight_id, source_insight_id) VALUES
(4, 1),
(4, 2),
(4, 3),
(5, 4),
(5, 1);"""

    add_code_block(doc, sql_dml_content)

    doc.add_page_break()

    # ==================== BAB 4 ====================
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(12)
    h4.paragraph_format.space_after = Pt(6)
    r_h4 = h4.add_run("4. Pengujian Integritas Relasi Data")
    r_h4.font.bold = True
    r_h4.font.size = Pt(14)
    r_h4.font.color.rgb = RGBColor(0x23, 0x4E, 0x52)

    p_test_desc = doc.add_paragraph()
    p_test_desc.paragraph_format.space_after = Pt(8)
    p_test_desc.add_run("Kueri berikut digunakan untuk menguji keterhubungan data antar tabel dalam lingkungan sistem nyata:")

    # Kueri 1
    p_t1 = doc.add_paragraph()
    p_t1.paragraph_format.space_after = Pt(4)
    r_t1 = p_t1.add_run("A. Kueri Rekap Sesi Live Streaming dan Total Insight yang Dihasilkan:")
    r_t1.font.bold = True
    r_t1.font.size = Pt(10.5)
    r_t1.font.color.rgb = RGBColor(0x28, 0x5E, 0x61)

    q1 = """SELECT 
    ls.id AS session_id,
    ls.username,
    ls.room_id,
    ls.status,
    COUNT(DISTINCT m.id) AS total_messages,
    COUNT(DISTINCT i.id) AS total_insights
FROM live_sessions ls
LEFT JOIN messages m ON ls.id = m.session_id
LEFT JOIN insights i ON ls.id = i.session_id
WHERE ls.id = 1
GROUP BY ls.id, ls.username, ls.room_id, ls.status;"""
    add_code_block(doc, q1)

    # Kueri 2
    p_t2 = doc.add_paragraph()
    p_t2.paragraph_format.space_after = Pt(4)
    r_t2 = p_t2.add_run("B. Kueri Pelacakan Komentar Mentah yang Mendasari Saran AI (Provenance):")
    r_t2.font.bold = True
    r_t2.font.size = Pt(10.5)
    r_t2.font.color.rgb = RGBColor(0x28, 0x5E, 0x61)

    q2 = """SELECT 
    i.batch_type,
    i.sentiment_score,
    i.actionable_insight,
    msg.display_name,
    msg.message
FROM insights i
JOIN insight_messages im ON i.id = im.insight_id
JOIN messages msg ON im.message_id = msg.id
WHERE i.id = 1;"""
    add_code_block(doc, q2)

    # Kueri 3
    p_t3 = doc.add_paragraph()
    p_t3.paragraph_format.space_after = Pt(4)
    r_t3 = p_t3.add_run("C. Kueri Keterkaitan Sintesis Hierarkis (Insight 20m & 45m terhadap Sumbernya):")
    r_t3.font.bold = True
    r_t3.font.size = Pt(10.5)
    r_t3.font.color.rgb = RGBColor(0x28, 0x5E, 0x61)

    q3 = """SELECT 
    parent.id AS parent_insight_id,
    parent.batch_type AS parent_type,
    parent.summary AS parent_summary,
    source.id AS source_insight_id,
    source.batch_type AS source_type,
    source.summary AS source_summary
FROM insight_dependencies id_dep
JOIN insights parent ON id_dep.insight_id = parent.id
JOIN insights source ON id_dep.source_insight_id = source.id
ORDER BY parent.id, source.id;"""
    add_code_block(doc, q3)

    # Kesimpulan
    p_concl = doc.add_paragraph()
    p_concl.paragraph_format.space_before = Pt(8)
    p_concl.paragraph_format.space_after = Pt(6)
    p_concl.paragraph_format.line_spacing = 1.2
    p_concl.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    
    r_cb = p_concl.add_run("Kesimpulan Pengujian:\n")
    r_cb.font.bold = True
    p_concl.add_run(
        "Semua relasi kunci asing (Foreign Key) terhubung secara utuh tanpa anomali data. "
        "Skema 5 tabel ini memenuhi kebutuhan fungsional arsitektur Streamly secara presisi, "
        "memungkinkan pelacakan penuh dari sesi live, riwayat obrolan penonton, hingga hasil sintesis bertingkat AI."
    )

    doc.save(output_path)
    print(f"[SUCCESS] DOCX successfully created at: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(current_dir, "TUGAS_BASIS_DATA_STREAMLY.docx")
    build_docx(docx_path)
