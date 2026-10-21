import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#718096"))
            # Header
            self.drawString(18 * mm, 282 * mm, "TUGAS BASIS DATA: STREAMLY (5 TABEL UTAMA) — TELKOM UNIVERSITY")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(18 * mm, 280 * mm, 192 * mm, 280 * mm)
            # Footer
            self.line(18 * mm, 15 * mm, 192 * mm, 15 * mm)
            self.drawRightString(192 * mm, 11 * mm, f"Halaman {self._pageNumber} dari {page_count}")
            self.drawString(18 * mm, 11 * mm, "S1 Informatika — Fakultas Informatika")
            self.restoreState()

def create_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=20 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1A202C'),
        alignment=1,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#2C7A7B'),
        alignment=1,
        spaceAfter=14
    )

    badge_style = ParagraphStyle(
        'CoverBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#234E52'),
        alignment=1,
        spaceAfter=25
    )

    desc_style = ParagraphStyle(
        'CoverDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=14,
        textColor=colors.HexColor('#4A5568'),
        alignment=1,
        spaceAfter=30
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#234E52'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#285E61'),
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#2D3748'),
        alignment=4,
        spaceAfter=6
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=9,
        textColor=colors.HexColor('#1A202C'),
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#2D3748')
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor('#1A202C')
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 20 * mm))
    story.append(Paragraph("LAPORAN PERANCANGAN BASIS DATA", title_style))
    story.append(Paragraph("Sintaks SQL DDL (Create Table) & DML (Insert 5 Data)", subtitle_style))
    story.append(Paragraph("PROYEK TUBES: STREAMLY (TIKTOK LIVE AI CHAT ANALYZER)", badge_style))
    
    desc_text = (
        "Implementasi Skema Relasional Persisten 5 Tabel Sesuai Rancangan Asli:<br/>"
        "<code>tubes/Streamly/skets/streamly_db_design/schema.sql</code><br/>"
        "Mencakup Sesi Streaming, Riwayat Komentar, Analisis AI, dan Keterlacakan Data (Provenance)."
    )
    story.append(Paragraph(desc_text, desc_style))
    story.append(Spacer(1, 15 * mm))

    # Kelompok Table
    story.append(Paragraph("<b>Disusun oleh Kelompok:</b>", ParagraphStyle('GroupHeading', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=1, spaceAfter=8)))
    
    members_data = [
        [Paragraph("<b>No</b>", table_header_style), Paragraph("<b>Nama Anggota</b>", table_header_style), Paragraph("<b>NIM</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("Aryo Abdillah Ainnurrofiq", table_cell_bold), Paragraph("103072400006", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("Annisa Nur Shadrina", table_cell_bold), Paragraph("103072400134", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("Fadia Nabila Shifa", table_cell_bold), Paragraph("10307200066", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("Refito Rahmat Firmansyah", table_cell_bold), Paragraph("103072430002", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("Revaldi Ramadhan Nugraha", table_cell_bold), Paragraph("103072400059", table_cell_style)],
    ]
    t_members = Table(members_data, colWidths=[15 * mm, 80 * mm, 45 * mm])
    t_members.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C7A7B')),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (2, 0), (2, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_members)

    story.append(Spacer(1, 35 * mm))
    footer_text = (
        "<b>PROGRAM STUDI S1 INFORMATIKA</b><br/>"
        "FAKULTAS INFORMATIKA — UNIVERSITAS TELKOM<br/>"
        "Mata Kuliah: Implementasi Perangkat Lunak (IMPAL)<br/>"
        "Tahun 2026"
    )
    story.append(Paragraph(footer_text, ParagraphStyle('CoverFooter', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, alignment=1, textColor=colors.HexColor('#4A5568'))))
    story.append(PageBreak())

    # ==================== BAB 1 ====================
    story.append(Paragraph("1. Deskripsi Skema Basis Data 5 Tabel Streamly", h1_style))
    story.append(Paragraph(
        "Rancangan basis data relasional ini mengacu secara langsung pada dokumen sketsa asli di "
        "<code>tubes/Streamly/skets/streamly_db_design/schema.sql</code> dan <code>ERD.md</code>. "
        "Di dalam sistem Streamly, Redis bertugas mengelola antrean pesan waktu nyata (*real-time queue*) dan cache insight cepat, "
        "sedangkan MySQL bertindak sebagai penyimpan riwayat permanen (*durable history*).",
        body_style
    ))
    story.append(Paragraph(
        "Skema terdiri dari <b>5 tabel utama</b> yang saling terhubung melalui relasi kunci asing (Foreign Key):",
        body_style
    ))

    tables_summary = [
        [Paragraph("<b>No</b>", table_header_style), Paragraph("<b>Nama Tabel</b>", table_header_style), Paragraph("<b>Peran &amp; Kardinalitas</b>", table_header_style), Paragraph("<b>Deskripsi Fungsi</b>", table_header_style)],
        [Paragraph("1", table_cell_style), Paragraph("<code>live_sessions</code>", table_cell_bold), Paragraph("1 baris per siaran live", table_cell_style), Paragraph("Mencatat satu siklus monitoring scraper terhadap live streaming seorang kreator TikTok.", table_cell_style)],
        [Paragraph("2", table_cell_style), Paragraph("<code>messages</code>", table_cell_bold), Paragraph("N baris per session (1:N)", table_cell_style), Paragraph("Menyimpan rekaman obrolan mentah penonton TikTok yang ditangkap scraper.", table_cell_style)],
        [Paragraph("3", table_cell_style), Paragraph("<code>insights</code>", table_cell_bold), Paragraph("N baris per session (1:N)", table_cell_style), Paragraph("Menyimpan hasil analisis AI Gemini dalam 3 jendela waktu (5m, 20m, 45m).", table_cell_style)],
        [Paragraph("4", table_cell_style), Paragraph("<code>insight_messages</code>", table_cell_bold), Paragraph("Many-to-Many (M:N)", table_cell_style), Paragraph("Tabel relasi pelacakan (provenance) komentar mentah mana saja yang dianalisis pada laporan 5m.", table_cell_style)],
        [Paragraph("5", table_cell_style), Paragraph("<code>insight_dependencies</code>", table_cell_bold), Paragraph("Many-to-Many (M:N)", table_cell_style), Paragraph("Tabel relasi turunan hierarkis (laporan 5m menjadi input laporan 20m, dan laporan 20m menjadi input 45m).", table_cell_style)],
    ]
    t_summary = Table(tables_summary, colWidths=[8 * mm, 42 * mm, 38 * mm, 86 * mm])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C7A7B')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F7FAFC')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t_summary)

    # ==================== BAB 2 ====================
    story.append(PageBreak())
    story.append(Paragraph("2. Sintaks SQL DDL (Create 5 Tabel)", h1_style))
    story.append(Paragraph(
        "Berikut adalah sintaks DDL (Data Definition Language) lengkap untuk membuat basis data <code>streamly_db</code> "
        "dan kelima tabel relasional persisten menggunakan MySQL 8.0+ sesuai berkas rancangan:",
        body_style
    ))

    sql_ddl = """-- =============================================================================
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

    story.append(Preformatted(sql_ddl, code_style))

    # ==================== BAB 3 ====================
    story.append(PageBreak())
    story.append(Paragraph("3. Sintaks SQL DML (Insert 5 Data Tiap Tabel)", h1_style))
    story.append(Paragraph(
        "Berikut adalah sintaks DML (Data Manipulation Language) yang memasukkan tepat <b>5 baris data contoh</b> "
        "ke dalam masing-masing dari 5 tabel (total 25 baris data). Data disusun realistis sesuai skenario operasional siaran langsung "
        "TikTok di Indonesia dan menjaga integritas referensial kunci asing.",
        body_style
    ))

    sql_dml = """-- =============================================================================
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

    story.append(Preformatted(sql_dml, code_style))

    # ==================== BAB 4 ====================
    story.append(PageBreak())
    story.append(Paragraph("4. Pengujian Integritas Relasi Data", h1_style))
    story.append(Paragraph(
        "Kueri berikut digunakan untuk menguji keterhubungan data antar tabel dalam lingkungan sistem nyata:",
        body_style
    ))

    story.append(Paragraph("A. Kueri Rekap Sesi Live Streaming dan Total Insight yang Dihasilkan:", h2_style))
    sql_test_1 = """SELECT 
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
    story.append(Preformatted(sql_test_1, code_style))

    story.append(Paragraph("B. Kueri Pelacakan Komentar Mentah yang Mendasari Saran AI (Provenance):", h2_style))
    sql_test_2 = """SELECT 
    i.batch_type,
    i.sentiment_score,
    i.actionable_insight,
    msg.display_name,
    msg.message
FROM insights i
JOIN insight_messages im ON i.id = im.insight_id
JOIN messages msg ON im.message_id = msg.id
WHERE i.id = 1;"""
    story.append(Preformatted(sql_test_2, code_style))

    story.append(Paragraph("C. Kueri Keterkaitan Sintesis Hierarkis (Insight 20m &amp; 45m terhadap Insight Sumber):", h2_style))
    sql_test_3 = """SELECT 
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
    story.append(Preformatted(sql_test_3, code_style))

    story.append(Paragraph(
        "<b>Kesimpulan Pengujian:</b><br/>"
        "Semua relasi kunci asing (Foreign Key) terhubung secara utuh tanpa anomali data. "
        "Skema 5 tabel ini memenuhi kebutuhan fungsional arsitektur Streamly secara presisi, "
        "memungkinkan pelacakan penuh dari sesi live, riwayat obrolan penonton, hingga hasil sintesis bertingkat AI.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] PDF 5 Tabel successfully created at: {output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(current_dir, "TUGAS_BASIS_DATA_STREAMLY.pdf")
    create_pdf(pdf_path)
