# -*- coding: utf-8 -*-
"""
🧹 LAPTOP FOLDER CLEANER - Pusat Kontrol
==========================================
Jalankan file ini saja! Dari sini Anda bisa mengakses semua fitur:
  1. Scan folder
  2. Lihat detail & penjelasan folder
  3. Hapus folder yang tidak berguna
  4. Lihat ringkasan
  5. dll.

Cara pakai:
  python run.py
"""

import os
import sys
import time
import ctypes
import datetime

# Pastikan path benar
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# ═══════════════════════════════════════════════════════════════
# SETUP TERMINAL
# ═══════════════════════════════════════════════════════════════
def setup_terminal():
    """Setup terminal agar mendukung warna dan emoji."""
    if sys.platform == "win32":
        try:
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════
# WARNA TERMINAL
# ═══════════════════════════════════════════════════════════════
R = "\033[0m"       # Reset
B = "\033[1m"       # Bold
D = "\033[2m"       # Dim
RED = "\033[91m"
GRN = "\033[92m"
YLW = "\033[93m"
BLU = "\033[94m"
MAG = "\033[95m"
CYN = "\033[96m"
WHT = "\033[97m"
GRY = "\033[90m"
BG_GRN = "\033[42m"
BG_YLW = "\033[43m"
BG_RED = "\033[41m"
BG_BLU = "\033[44m"
BG_CYN = "\033[46m"


def clear():
    os.system("cls" if sys.platform == "win32" else "clear")


def pause():
    print()
    input(f"  {D}Tekan Enter untuk kembali ke menu...{R}")


# ═══════════════════════════════════════════════════════════════
# STATE GLOBAL - menyimpan hasil scan agar tidak perlu scan ulang
# ═══════════════════════════════════════════════════════════════
scan_results = None      # Dict[str, List[FolderResult]]
scan_index_map = None    # Dict[int, FolderResult]
last_scan_time = None


# ═══════════════════════════════════════════════════════════════
# BANNER
# ═══════════════════════════════════════════════════════════════
def show_banner():
    clear()
    print(f"""
{CYN}{B}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🧹 LAPTOP FOLDER CLEANER                                   ║
    ║   ─────────────────────────────                              ║
    ║   Pusat Kontrol Pembersihan Laptop                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{R}""")
    print(f"  {D}📅 {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}{R}")
    print(f"  {D}👤 {os.environ.get('USERNAME', 'Unknown')}{R}")
    print(f"  {D}🏠 {os.path.expanduser('~')}{R}")

    # Status scan
    if scan_results is not None:
        total = sum(len(v) for v in scan_results.values())
        print(f"  {GRN}✅ Data scan tersedia ({total} folder ditemukan){R}")
        if last_scan_time:
            print(f"  {D}🕐 Scan terakhir: {last_scan_time}{R}")
    else:
        print(f"  {YLW}⚠️  Belum ada data scan. Pilih [1] untuk scan dulu.{R}")
    print()


# ═══════════════════════════════════════════════════════════════
# MENU UTAMA
# ═══════════════════════════════════════════════════════════════
def show_menu():
    has_data = scan_results is not None

    print(f"  {GRY}{'═' * 58}{R}")
    print(f"  {B}{WHT}  MENU UTAMA{R}")
    print(f"  {GRY}{'═' * 58}{R}")
    print()
    print(f"  {BG_BLU}{WHT}{B} 1 {R}  {B}🔍 Scan Folder{R}")
    print(f"      {D}Scan semua folder di laptop & hitung ukuran{R}")
    print()

    if has_data:
        color = ""
    else:
        color = D  # dim if no data

    print(f"  {BG_CYN}{WHT}{B} 2 {R}  {color}{B}📊 Lihat Ringkasan{R}")
    print(f"      {color}{D}Tampilkan ringkasan hasil scan{R}")
    print()
    print(f"  {BG_CYN}{WHT}{B} 3 {R}  {color}{B}📋 Lihat Semua Folder{R}")
    print(f"      {color}{D}Daftar lengkap folder dengan penjelasan detail{R}")
    print()
    print(f"  {BG_CYN}{WHT}{B} 4 {R}  {color}{B}🔎 Detail Folder{R}")
    print(f"      {color}{D}Lihat penjelasan detail satu folder tertentu{R}")
    print()
    print(f"  {BG_GRN}{WHT}{B} 5 {R}  {color}{B}🗑️  Hapus Folder{R}")
    print(f"      {color}{D}Pilih & hapus folder yang tidak berguna{R}")
    print()
    print(f"  {BG_GRN}{WHT}{B} 6 {R}  {color}{B}⚡ Hapus Semua yang Aman{R}")
    print(f"      {color}{D}Otomatis hapus semua folder berlabel ✅ AMAN{R}")
    print()
    print(f"  {BG_YLW}{WHT}{B} 7 {R}  {B}📖 Bantuan & Info{R}")
    print(f"      {D}Penjelasan cara kerja program ini{R}")
    print()
    print(f"  {BG_CYN}{WHT}{B} 8 {R}  {B}🤖 Kelola Logs & Riwayat{R}")
    print(f"      {D}Scan semua logs berat: AI, aplikasi, Windows{R}")
    print()
    print(f"  {BG_YLW}{WHT}{B} 9 {R}  {B}🧹 Bersihkan Logs Lama{R}")
    print(f"      {D}Hapus file log cleanup yang sudah tidak dibutuhkan{R}")
    print()
    print(f"  {BG_RED}{WHT}{B} 0 {R}  {B}🚪 Keluar{R}")
    print()
    print(f"  {GRY}{'─' * 58}{R}")


# ═══════════════════════════════════════════════════════════════
# FITUR 1: SCAN
# ═══════════════════════════════════════════════════════════════
def do_scan():
    global scan_results, scan_index_map, last_scan_time
    from scanner import scan_all, format_size

    print()
    print(f"  {CYN}{B}🔍 SCAN FOLDER LAPTOP{R}")
    print(f"  {GRY}{'─' * 58}{R}")

    if scan_results is not None:
        print(f"  {YLW}Data scan sebelumnya sudah ada.{R}")
        print(f"  {WHT}Scan ulang? (y/n): {R}", end="")
        try:
            ans = input().strip().lower()
        except (KeyboardInterrupt, EOFError):
            return
        if ans not in ("y", "ya", "yes"):
            print(f"  {D}Menggunakan data scan yang sudah ada.{R}")
            pause()
            return

    print()
    print(f"  {CYN}Memulai scan... Ini mungkin butuh 1-2 menit.{R}")
    print(f"  {D}Scanning temp, cache, browser, development, logs...{R}")
    print()

    start = time.time()

    def on_progress(current, total, message):
        if total == 0:
            return
        pct = current / total
        filled = int(40 * pct)
        bar = "█" * filled + "░" * (40 - filled)
        msg = message[:35] + "..." if len(message) > 35 else message
        sys.stdout.write(
            f"\r  {CYN}[{bar}]{R} {B}{pct*100:5.1f}%{R} {D}{msg:<38}{R}"
        )
        sys.stdout.flush()
        if current >= total:
            print()

    scan_results = scan_all(progress_callback=on_progress)
    elapsed = time.time() - start
    last_scan_time = datetime.datetime.now().strftime("%H:%M:%S")

    # Build index map
    scan_index_map = {}
    idx = 1
    for category, folders in scan_results.items():
        for f in folders:
            scan_index_map[idx] = f
            idx += 1

    total_folders = sum(len(v) for v in scan_results.values())
    total_size = sum(f.size_bytes for v in scan_results.values() for f in v)
    safe_size = sum(
        f.size_bytes for v in scan_results.values() for f in v
        if f.risk_level == "safe" and f.can_delete
    )

    print()
    print(f"  {GRN}{B}✅ Scan selesai dalam {elapsed:.1f} detik!{R}")
    print()
    print(f"  {WHT}Total folder  : {B}{total_folders}{R}")
    print(f"  {WHT}Total ukuran  : {B}{format_size(total_size)}{R}")
    print(f"  {GRN}Bisa dihapus  : {B}{format_size(safe_size)}{R}")

    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 2: RINGKASAN
# ═══════════════════════════════════════════════════════════════
def do_summary():
    from scanner import format_size

    print()
    print(f"  {CYN}{B}📊 RINGKASAN HASIL SCAN{R}")
    print(f"  {GRY}{'─' * 58}{R}")
    print()

    total_size = 0
    total_safe = 0
    total_count = 0
    safe_count = 0

    for category, folders in scan_results.items():
        cat_size = sum(f.size_bytes for f in folders)
        cat_safe = sum(f.size_bytes for f in folders if f.risk_level == "safe" and f.can_delete)
        total_size += cat_size
        total_safe += cat_safe
        total_count += len(folders)
        safe_count += sum(1 for f in folders if f.risk_level == "safe" and f.can_delete)

        # Color based on size
        if cat_size > 1024**3:
            sc = RED
        elif cat_size > 100 * 1024**2:
            sc = YLW
        else:
            sc = GRN

        print(f"  {B}{category}{R}")
        print(f"    📁 {len(folders)} folder  │  💿 {sc}{B}{format_size(cat_size)}{R}")
        print()

    print(f"  {GRY}{'═' * 58}{R}")
    print(f"  {B}{WHT}TOTAL{R}")
    print(f"    📁 {total_count} folder")
    print(f"    💿 Total ukuran    : {RED}{B}{format_size(total_size)}{R}")
    print(f"    ✅ Aman dihapus    : {safe_count} folder ({GRN}{B}{format_size(total_safe)}{R})")
    print(f"  {GRY}{'═' * 58}{R}")

    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 3: LIHAT SEMUA FOLDER (GLOBAL SORT BY SIZE)
# ═══════════════════════════════════════════════════════════════
def safety_bar(score: int) -> str:
    """Buat visual bar skor keamanan."""
    filled = score
    empty = 10 - score
    if score >= 8:
        color = GRN
    elif score >= 5:
        color = YLW
    else:
        color = RED
    return f"{color}{'█' * filled}{'░' * empty}{R} {color}{B}{score}/10{R}"


def do_list_all():
    from scanner import format_size, days_since_modified

    print()
    print(f"  {CYN}{B}📋 DAFTAR SEMUA FOLDER (Urutan: Terbesar → Terkecil){R}")
    print(f"  {GRY}{'─' * 58}{R}")
    print()

    # Kumpulkan semua folder dari semua kategori
    all_folders = []
    for category, folders in scan_results.items():
        for f in folders:
            all_folders.append((f, category))

    # Sort global by size (terbesar dulu)
    all_folders.sort(key=lambda x: x[0].size_bytes, reverse=True)

    total_size = sum(f.size_bytes for f, _ in all_folders)
    safe_size = sum(f.size_bytes for f, _ in all_folders if f.risk_level == "safe" and f.can_delete)

    print(f"  {WHT}Total: {B}{len(all_folders)}{R} folder  │  "
          f"💿 {RED}{B}{format_size(total_size)}{R}  │  "
          f"✅ Bisa dibebaskan: {GRN}{B}{format_size(safe_size)}{R}")
    print()

    for rank, (f, category) in enumerate(all_folders, 1):
        # Cari nomor index di scan_index_map
        idx = None
        for k, v in scan_index_map.items():
            if v is f:
                idx = k
                break

        # Risk badge
        if f.risk_level == "safe":
            badge = f"{BG_GRN}{WHT}{B} AMAN {R}"
        elif f.risk_level == "caution":
            badge = f"{BG_YLW}{WHT}{B} HATI² {R}"
        else:
            badge = f"{BG_RED}{WHT}{B} BAHAYA {R}"

        # Size color
        if f.size_bytes > 1024**3:
            sc = f"{RED}{B}"
        elif f.size_bytes > 100 * 1024**2:
            sc = f"{YLW}{B}"
        elif f.size_bytes > 10 * 1024**2:
            sc = YLW
        else:
            sc = GRN

        # Age
        days = days_since_modified(f.last_modified)
        if days > 90:
            age = f"{RED}({days} hari){R}"
        elif days > 30:
            age = f"{YLW}({days} hari){R}"
        elif days >= 0:
            age = f"{D}({days} hari){R}"
        else:
            age = ""

        # Safety score bar (compact)
        ss = f.safety_score
        if ss >= 8:
            ss_color = GRN
        elif ss >= 5:
            ss_color = YLW
        else:
            ss_color = RED
        score_display = f"{ss_color}{'█' * ss}{'░' * (10-ss)} {ss}/10{R}"

        print(f"  {B}{WHT}[{idx:3d}]{R} {B}{f.name}{R}  {badge}")
        print(f"        {D}{f.path}{R}")
        print(f"        💿 {sc}{format_size(f.size_bytes):>10}{R}  │  "
              f"📄 {f.file_count:,} file  │  "
              f"🛡️ {score_display}  {age}")
        
        # Compact impact
        if f.impact:
            impact_short = f.impact[:70] + "..." if len(f.impact) > 70 else f.impact
            print(f"        {D}💬 {impact_short}{R}")
        print()
    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 4: DETAIL FOLDER (SUPER DETAIL)
# ═══════════════════════════════════════════════════════════════
def do_detail():
    from scanner import format_size, days_since_modified, analyze_folder_detail
    import datetime as dt

    # Tampilkan daftar ringkas dulu agar user tahu nomor-nomornya
    print()
    print(f"  {CYN}{B}🔎 DETAIL FOLDER (Super Detail){R}")
    print(f"  {GRY}{'─' * 62}{R}")
    print()
    print(f"  {B}Daftar folder yang ditemukan:{R}")
    print()

    # Sort by size for display
    sorted_items = sorted(scan_index_map.items(), key=lambda x: x[1].size_bytes, reverse=True)

    for idx, f in sorted_items:
        # Compact badge
        if f.risk_level == "safe":
            badge = f"{GRN}✅{R}"
        elif f.risk_level == "caution":
            badge = f"{YLW}⚠️{R}"
        else:
            badge = f"{RED}⛔{R}"

        # Size color
        if f.size_bytes > 1024**3:
            sc = f"{RED}{B}"
        elif f.size_bytes > 100 * 1024**2:
            sc = f"{YLW}{B}"
        else:
            sc = GRN

        # Safety score mini
        ss = f.safety_score
        if ss >= 8:
            ss_c = GRN
        elif ss >= 5:
            ss_c = YLW
        else:
            ss_c = RED

        name_display = f.name if len(f.name) <= 25 else f.name[:22] + "..."
        print(f"    {badge} {B}[{idx:3d}]{R} {name_display:<26} "
              f"{sc}{format_size(f.size_bytes):>10}{R}  "
              f"{ss_c}🛡️{ss}/10{R}  "
              f"{D}{f.category}{R}")

    print()
    print(f"  {GRY}{'─' * 62}{R}")
    print(f"  {D}Pilih nomor di atas untuk melihat detail lengkap.{R}")

    while True:
        print()

        try:
            inp = input(f"  {CYN}❯ Nomor folder (atau 'q' untuk kembali): {R}").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if inp.lower() in ("q", "quit", "back", "kembali"):
            break

        if not inp.isdigit() or int(inp) not in scan_index_map:
            print(f"  {RED}❌ Nomor tidak valid.{R}")
            continue

        f = scan_index_map[int(inp)]

        # ── HEADER ──
        if f.risk_level == "safe":
            badge = f"{BG_GRN}{WHT}{B} ✅ AMAN DIHAPUS {R}"
        elif f.risk_level == "caution":
            badge = f"{BG_YLW}{WHT}{B} ⚠️  HATI-HATI {R}"
        else:
            badge = f"{BG_RED}{WHT}{B} ⛔ BERBAHAYA {R}"

        # Size color
        if f.size_bytes > 1024**3:
            sc = f"{RED}{B}"
        elif f.size_bytes > 100 * 1024**2:
            sc = f"{YLW}{B}"
        else:
            sc = GRN

        days = days_since_modified(f.last_modified)

        print()
        print(f"  {GRY}{'═' * 62}{R}")
        print(f"  {B}{WHT}📁 {f.name}{R}    {badge}")
        print(f"  {GRY}{'═' * 62}{R}")

        # ── INFO DASAR ──
        print()
        print(f"  {B}📌 INFORMASI DASAR{R}")
        print(f"  {GRY}{'─' * 62}{R}")
        print(f"  📂 Path      : {D}{f.path}{R}")
        print(f"  💿 Ukuran    : {sc}{format_size(f.size_bytes)}{R}")
        print(f"  📄 File      : {f.file_count:,} file")
        print(f"  📁 Subfolder : {f.folder_count:,} subfolder")
        if days >= 0:
            if days > 180:
                age_text = f"{RED}{days} hari lalu (sudah sangat lama!){R}"
            elif days > 90:
                age_text = f"{YLW}{days} hari lalu (sudah lama){R}"
            elif days > 30:
                age_text = f"{YLW}{days} hari lalu{R}"
            else:
                age_text = f"{GRN}{days} hari lalu (baru dipakai){R}"
            print(f"  ⏰ Terakhir  : {age_text}")
        print(f"  🏷️  Kategori  : {f.category}")

        # ── SKOR KEAMANAN ──
        print()
        print(f"  {B}🛡️  SKOR KEAMANAN{R}")
        print(f"  {GRY}{'─' * 62}{R}")
        ss = f.safety_score
        print(f"  {safety_bar(ss)}")
        print()
        if ss >= 9:
            print(f"  {GRN}{B}SANGAT AMAN{R} — Folder ini 100% aman dihapus.")
            print(f"  {GRN}Tidak ada risiko sama sekali. Data bisa diregenerasi otomatis.{R}")
        elif ss >= 7:
            print(f"  {GRN}{B}AMAN{R} — Folder ini aman dihapus.")
            print(f"  {GRN}Risiko sangat rendah. Data bisa dipulihkan/dibuat ulang.{R}")
        elif ss >= 5:
            print(f"  {YLW}{B}CUKUP AMAN{R} — Bisa dihapus dengan sedikit kehati-hatian.")
            print(f"  {YLW}Ada dampak kecil, tapi bisa dipulihkan.{R}")
        elif ss >= 3:
            print(f"  {YLW}{B}HATI-HATI{R} — Periksa isi folder sebelum menghapus.")
            print(f"  {YLW}Ada risiko kehilangan data atau pengaturan.{R}")
        else:
            print(f"  {RED}{B}BERBAHAYA{R} — JANGAN HAPUS kecuali sangat yakin!")
            print(f"  {RED}Bisa merusak sistem atau kehilangan data penting.{R}")

        # ── PENJELASAN ──
        print()
        print(f"  {B}📝 APA ITU FOLDER INI?{R}")
        print(f"  {GRY}{'─' * 62}{R}")
        for line in f.description.split("\n"):
            print(f"  {WHT}{line}{R}")
        if f.note:
            print(f"  {YLW}💡 {f.note}{R}")

        # ── DAMPAK & RECOVERY ──
        print()
        print(f"  {B}⚡ APA YANG TERJADI KALAU DIHAPUS?{R}")
        print(f"  {GRY}{'─' * 62}{R}")
        if f.impact:
            print(f"  {WHT}{f.impact}{R}")
        print()
        print(f"  {B}🔄 CARA MEMULIHKAN:{R}")
        if f.recovery:
            print(f"  {GRN}{f.recovery}{R}")

        # ── ANALISIS ISI FOLDER (on-demand) ──
        print()
        print(f"  {B}🔬 ANALISIS ISI FOLDER{R}")
        print(f"  {GRY}{'─' * 62}{R}")
        print(f"  {D}Menganalisis isi folder...{R}", end=" ")

        analysis = analyze_folder_detail(f.path)
        print(f"{GRN}Selesai!{R}")
        print()

        # Top 10 file terbesar
        if analysis["top_files"]:
            print(f"  {B}📦 10 File Terbesar di Dalam:{R}")
            for i, (fname, fsize, fext) in enumerate(analysis["top_files"], 1):
                # Truncate filename
                display_name = fname if len(fname) <= 45 else "..." + fname[-42:]
                print(f"    {D}{i:2d}.{R} {display_name}")
                print(f"        {GRY}Ukuran: {format_size(fsize)} │ Tipe: {fext}{R}")
            print()

        # File type breakdown
        if analysis["file_types"]:
            total_type_size = sum(v["size"] for v in analysis["file_types"].values())
            print(f"  {B}📊 Breakdown Jenis File:{R}")
            for ext, info in analysis["file_types"].items():
                pct = (info["size"] / total_type_size * 100) if total_type_size > 0 else 0
                bar_len = int(pct / 5)
                bar = "▓" * bar_len + "░" * (20 - bar_len)
                print(f"    {CYN}{ext:<20}{R} {bar} {pct:5.1f}%  "
                      f"({info['count']:,} file, {format_size(info['size'])})")
            print()

        # Suspicious files (file penting yang mungkin ada di dalam)
        if analysis["suspicious_files"]:
            print(f"  {RED}{B}⚠️  FILE PENTING TERDETEKSI DI DALAM:{R}")
            print(f"  {RED}Folder ini mengandung file yang mungkin penting!{R}")
            for fname, fsize, fext in analysis["suspicious_files"]:
                display_name = fname if len(fname) <= 50 else "..." + fname[-47:]
                print(f"    {YLW}⚠️  {display_name} ({format_size(fsize)}, {fext}){R}")
            print()
        else:
            print(f"  {GRN}✅ Tidak ada file penting terdeteksi di dalam folder ini.{R}")
            print()

        # File tertua & terbaru
        if analysis["oldest_file"]:
            old_name, old_time = analysis["oldest_file"]
            old_date = dt.datetime.fromtimestamp(old_time).strftime("%d %b %Y")
            old_name = old_name if len(old_name) <= 40 else "..." + old_name[-37:]
            print(f"  {D}📅 File tertua  : {old_name} ({old_date}){R}")
        if analysis["newest_file"]:
            new_name, new_time = analysis["newest_file"]
            new_date = dt.datetime.fromtimestamp(new_time).strftime("%d %b %Y")
            new_name = new_name if len(new_name) <= 40 else "..." + new_name[-37:]
            print(f"  {D}📅 File terbaru : {new_name} ({new_date}){R}")

        # Kedalaman folder
        print(f"  {D}📐 Kedalaman   : {analysis['total_depth']} level{R}")

        # ── KESIMPULAN ──
        print()
        print(f"  {GRY}{'═' * 62}{R}")
        if f.safety_score >= 7:
            print(f"  {GRN}{B}✅ KESIMPULAN: Folder ini AMAN untuk dihapus.{R}")
            print(f"  {GRN}   Anda bisa menghemat {sc}{format_size(f.size_bytes)}{R}{GRN} ruang disk.{R}")
        elif f.safety_score >= 4:
            print(f"  {YLW}{B}⚠️  KESIMPULAN: Bisa dihapus, tapi PERIKSA DULU isinya.{R}")
            print(f"  {YLW}   Pastikan tidak ada file penting di dalam.{R}")
        else:
            print(f"  {RED}{B}⛔ KESIMPULAN: JANGAN HAPUS folder ini.{R}")
            print(f"  {RED}   Risiko kerusakan sistem atau kehilangan data!{R}")
        print(f"  {GRY}{'═' * 62}{R}")


# ═══════════════════════════════════════════════════════════════
# FITUR 5: HAPUS FOLDER (PILIH)
# ═══════════════════════════════════════════════════════════════
def do_delete():
    from scanner import format_size
    from cleaner import setup_logger, delete_folder_contents, delete_entire_folder

    print()
    print(f"  {CYN}{B}🗑️  HAPUS FOLDER{R}")
    print(f"  {GRY}{'─' * 58}{R}")
    print()
    print(f"  {WHT}Masukkan nomor folder yang ingin dihapus.{R}")
    print(f"  {D}Bisa satu nomor (misal: 5) atau beberapa (misal: 1,3,5,7){R}")
    print(f"  {D}Ketik 'q' untuk kembali ke menu.{R}")
    print()

    try:
        inp = input(f"  {CYN}❯ Nomor folder: {R}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if inp.lower() in ("q", "quit", "back", "kembali"):
        return

    # Parse nomor
    try:
        indices = [int(x.strip()) for x in inp.split(",") if x.strip().isdigit()]
    except ValueError:
        print(f"  {RED}❌ Input tidak valid.{R}")
        pause()
        return

    invalid = [i for i in indices if i not in scan_index_map]
    if invalid:
        print(f"  {RED}❌ Nomor tidak valid: {invalid}{R}")
        pause()
        return

    if not indices:
        print(f"  {RED}❌ Tidak ada nomor yang valid.{R}")
        pause()
        return

    folders = [(idx, scan_index_map[idx]) for idx in indices]
    total_size = sum(f.size_bytes for _, f in folders)

    # Tampilkan yang akan dihapus
    print()
    print(f"  {YLW}{B}Folder yang akan dihapus:{R}")
    print()
    for idx, f in folders:
        if f.risk_level == "safe":
            badge = f"{GRN}✅ AMAN{R}"
        elif f.risk_level == "caution":
            badge = f"{YLW}⚠️ HATI²{R}"
        else:
            badge = f"{RED}⛔ BAHAYA{R}"
        print(f"    [{idx}] {B}{f.name}{R} ({format_size(f.size_bytes)}) {badge}")
        print(f"        {D}{f.path}{R}")
    print()
    print(f"  {B}Total: {format_size(total_size)}{R}")

    # Cek folder berbahaya
    dangerous = [(idx, f) for idx, f in folders if f.risk_level == "danger"]
    if dangerous:
        print()
        print(f"  {RED}{B}⛔ PERINGATAN! Anda memilih folder BERBAHAYA:{R}")
        for idx, f in dangerous:
            print(f"     ⛔ [{idx}] {f.name}: {f.note}")
        print()
        try:
            confirm = input(f"  {RED}{B}Ketik 'SAYA YAKIN' untuk lanjut: {R}").strip()
        except (KeyboardInterrupt, EOFError):
            return
        if confirm != "SAYA YAKIN":
            print(f"  {D}Dibatalkan.{R}")
            pause()
            return
    else:
        # Peringatan folder caution
        caution = [(idx, f) for idx, f in folders if f.risk_level == "caution"]
        if caution:
            print()
            print(f"  {YLW}⚠️  Beberapa folder perlu kehati-hatian:{R}")
            for idx, f in caution:
                print(f"     ⚠️ [{idx}] {f.name}: {f.note}")

        print()
        try:
            confirm = input(f"  {YLW}{B}Hapus {len(folders)} folder? (y/n): {R}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            return
        if confirm not in ("y", "ya", "yes"):
            print(f"  {D}Dibatalkan.{R}")
            pause()
            return

    # EKSEKUSI HAPUS (dengan progress bar real-time)
    logger = setup_logger()
    print()

    dev_deletable = {
        "node_modules", "__pycache__", ".next", ".nuxt", ".output",
        "dist", "build", ".cache", ".parcel-cache", ".turbo",
        "coverage", ".venv", "venv"
    }

    total_freed = 0
    total_count = len(folders)
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    spin_idx = [0]

    try:
        for fi, (idx, f) in enumerate(folders, 1):
            # Progress callback: update bar in real-time per file di dalam folder
            def make_progress(folder_name, folder_idx, folder_num, folder_total):
                def on_progress(done, total, current_file):
                    spin_idx[0] = (spin_idx[0] + 1) % len(spinner)
                    s = spinner[spin_idx[0]]
                    pct = done / max(total, 1) * 100
                    bar_len = 25
                    filled = int(bar_len * done / max(total, 1))
                    bar = f"{GRN}{'█' * filled}{GRY}{'░' * (bar_len - filled)}{R}"

                    # Truncate file name
                    short_file = current_file[:20] + "..." if len(current_file) > 23 else current_file

                    line = (f"\r  {s} [{bar}] {pct:5.1f}%  "
                            f"🗑️ [{folder_idx}] {folder_name}  "
                            f"{D}({done}/{total}) {short_file}{R}")
                    # Pad to overwrite previous line
                    print(f"{line:<100}", end="", flush=True)
                return on_progress

            # Tampilkan header awal
            print(f"\r  ⏳ [{'░' * 25}]   0.0%  🗑️ [{idx}] {f.name} ({format_size(f.size_bytes)})...",
                  end="", flush=True)

            progress_fn = make_progress(f.name, idx, fi, total_count)

            if f.name in dev_deletable:
                stats = delete_entire_folder(f.path, logger, on_progress=progress_fn)
            else:
                stats = delete_folder_contents(f.path, logger, on_progress=progress_fn)
            total_freed += stats["freed_bytes"]

            # Clear line and print result
            if stats["errors"]:
                warn_count = len(stats["errors"])
                full_bar = f"{YLW}{'█' * 25}{R}"
                print(f"\r  ✅ [{full_bar}] 100%   "
                      f"🗑️ [{idx}] {f.name} "
                      f"{YLW}⚠️ {warn_count} peringatan, {format_size(stats['freed_bytes'])} freed{R}"
                      + " " * 20)
            else:
                full_bar = f"{GRN}{'█' * 25}{R}"
                print(f"\r  ✅ [{full_bar}] 100%   "
                      f"🗑️ [{idx}] {f.name} "
                      f"{GRN}✅ {format_size(stats['freed_bytes'])} freed{R}"
                      + " " * 20)

    except KeyboardInterrupt:
        print()
        print(f"\n  {YLW}{B}⏹️ Dihentikan oleh user (Ctrl+C){R}")
        if total_freed > 0:
            print(f"  {WHT}Ruang yang sudah dibebaskan: {GRN}{format_size(total_freed)}{R}")
        print(f"  {D}Sisa folder tidak dihapus.{R}")
        pause()
        return

    # Final summary
    print()
    print(f"  {GRY}{'═' * 58}{R}")
    full_bar = f"{GRN}{'█' * 25}{R}"
    print(f"  [{full_bar}] {B}SELESAI!{R}")
    print(f"  {GRN}{B}✅ Ruang dibebaskan: {format_size(total_freed)}{R}")
    logger.info(f"Total freed: {format_size(total_freed)}")

    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 6: HAPUS SEMUA YANG AMAN
# ═══════════════════════════════════════════════════════════════
def do_delete_all_safe():
    from scanner import format_size
    from cleaner import setup_logger, delete_folder_contents, delete_entire_folder

    print()
    print(f"  {CYN}{B}⚡ HAPUS SEMUA FOLDER AMAN{R}")
    print(f"  {GRY}{'─' * 58}{R}")

    safe_folders = [
        (idx, f) for idx, f in scan_index_map.items()
        if f.risk_level == "safe" and f.can_delete
    ]

    if not safe_folders:
        print(f"  {GRN}🎉 Tidak ada folder aman untuk dihapus!{R}")
        pause()
        return

    total_size = sum(f.size_bytes for _, f in safe_folders)

    print()
    print(f"  {WHT}Akan menghapus {B}{len(safe_folders)}{R}{WHT} folder berlabel ✅ AMAN{R}")
    print(f"  {WHT}Estimasi ruang bebas: {GRN}{B}{format_size(total_size)}{R}")
    print()

    # Tampilkan top 10 terbesar
    sorted_safe = sorted(safe_folders, key=lambda x: x[1].size_bytes, reverse=True)
    show = sorted_safe[:10]
    print(f"  {B}Top {len(show)} terbesar:{R}")
    for idx, f in show:
        print(f"    [{idx:3d}] {f.name:<25} {format_size(f.size_bytes):>10}  {D}{f.path}{R}")
    if len(safe_folders) > 10:
        print(f"    {D}... dan {len(safe_folders) - 10} folder lainnya{R}")

    print()
    try:
        confirm = input(f"  {RED}{B}Ketik 'HAPUS' untuk konfirmasi: {R}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if confirm != "HAPUS":
        print(f"  {D}Dibatalkan.{R}")
        pause()
        return

    # EKSEKUSI
    logger = setup_logger()
    print()

    dev_deletable = {
        "node_modules", "__pycache__", ".next", ".nuxt", ".output",
        "dist", "build", ".cache", ".parcel-cache", ".turbo",
        "coverage", ".venv", "venv"
    }

    total_freed = 0
    success = 0
    failed = 0
    total_count = len(safe_folders)
    spinner = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    spin_idx = [0]

    for i, (idx, f) in enumerate(safe_folders, 1):
        def make_progress(fname, fi, total):
            def on_progress(done, tot, current_file):
                spin_idx[0] = (spin_idx[0] + 1) % len(spinner)
                s = spinner[spin_idx[0]]
                pct_inner = done / max(tot, 1) * 100
                pct_outer = (fi - 1 + done / max(tot, 1)) / total * 100
                bar_len = 25
                filled = int(bar_len * pct_outer / 100)
                bar = f"{GRN}{'█' * filled}{GRY}{'░' * (bar_len - filled)}{R}"
                short = current_file[:18] + "..." if len(current_file) > 21 else current_file
                line = (f"\r  {s} [{bar}] {pct_outer:5.1f}%  "
                        f"🗑️ {fname}  {D}({done}/{tot}) {short}{R}")
                print(f"{line:<100}", end="", flush=True)
            return on_progress

        pct = i / total_count * 100
        print(f"\r  ⏳ [{'░' * 25}] {pct:5.1f}%  🗑️ {f.name}...", end="", flush=True)

        progress_fn = make_progress(f.name, i, total_count)

        if f.name in dev_deletable:
            stats = delete_entire_folder(f.path, logger, on_progress=progress_fn)
        else:
            stats = delete_folder_contents(f.path, logger, on_progress=progress_fn)
        total_freed += stats["freed_bytes"]
        if stats["errors"]:
            bar = f"{YLW}{'█' * 25}{R}"
            print(f"\r  ✅ [{bar}] {pct:5.1f}%  🗑️ {f.name} {YLW}⚠️{R}" + " " * 30)
            failed += 1
        else:
            bar = f"{GRN}{'█' * 25}{R}"
            print(f"\r  ✅ [{bar}] {pct:5.1f}%  🗑️ {f.name} {GRN}✅{R}" + " " * 30)
            success += 1

    print()
    print(f"  {GRY}{'═' * 58}{R}")
    print(f"  {GRN}{B}✅ SELESAI!{R}")
    print(f"  {WHT}Berhasil  : {GRN}{success}{R}")
    if failed:
        print(f"  {WHT}Gagal     : {YLW}{failed}{R}")
    print(f"  {WHT}Ruang bebas: {GRN}{B}{format_size(total_freed)}{R}")
    print(f"  {GRY}{'═' * 58}{R}")
    logger.info(f"Batch safe delete: {success} OK, {failed} failed, freed {format_size(total_freed)}")

    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 7: BANTUAN
# ═══════════════════════════════════════════════════════════════
def do_help():
    print()
    print(f"""
  {CYN}{B}📖 BANTUAN & INFORMASI{R}
  {GRY}{'═' * 58}{R}

  {B}Apa itu Laptop Folder Cleaner?{R}
  {WHT}Program ini membantu Anda menemukan dan menghapus folder-folder
  di laptop yang sudah tidak berguna, seperti cache, file sementara,
  build output, dan lain-lain.{R}

  {B}Cara Pakai:{R}
  {WHT}1. {GRN}Scan dulu{R}{WHT} (menu 1) — program akan memindai semua folder{R}
  {WHT}2. {CYN}Lihat hasilnya{R}{WHT} (menu 2 atau 3) — pahami folder mana yang aman{R}
  {WHT}3. {CYN}Lihat detail{R}{WHT} (menu 4) — baca penjelasan per folder{R}
  {WHT}4. {YLW}Hapus{R}{WHT} (menu 5 atau 6) — hapus yang tidak dibutuhkan{R}

  {B}Label Risiko:{R}
  {BG_GRN}{WHT}{B} ✅ AMAN {R}    = Bisa dihapus tanpa masalah
  {BG_YLW}{WHT}{B} ⚠️ HATI² {R}  = Periksa dulu sebelum hapus
  {BG_RED}{WHT}{B} ⛔ BAHAYA {R}  = Jangan hapus (file penting sistem)

  {B}Apa yang di-scan?{R}
  {WHT}• Folder Temp & file sementara Windows
  • Cache browser (Chrome, Edge, Firefox, Opera, Brave)
  • Cache development (node_modules, __pycache__, build, .venv)
  • Cache package manager (npm, pip, gradle, maven)
  • Log & crash report dari aplikasi
  • File update Windows yang sudah tidak dibutuhkan{R}

  {B}Apakah aman?{R}
  {WHT}• Program SELALU minta konfirmasi sebelum menghapus
  • Folder sistem penting ditandai ⛔ BERBAHAYA
  • Semua operasi di-log ke folder 'logs/' untuk audit
  • Folder development bisa dibuat ulang (npm install, dll){R}

  {D}Log tersimpan di: {os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')}{R}
""")
    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 8: KELOLA LOGS & RIWAYAT BERAT
# ═══════════════════════════════════════════════════════════════
def do_ai_history():
    from scanner import format_size
    import datetime as dt
    import shutil

    home = os.path.expanduser("~")
    local_appdata = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    roaming_appdata = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))

    print()
    print(f"  {CYN}{B}🤖 KELOLA LOGS & RIWAYAT BERAT{R}")
    print(f"  {GRY}{'─' * 62}{R}")
    print(f"  {D}Scanning semua logs & riwayat di laptop...{R}")
    print()

    all_items = []
    current_conv = os.environ.get("CONVERSATION_ID", "")

    # ── Helper: hitung ukuran folder ──
    def folder_stats(path):
        total_size = 0
        file_count = 0
        try:
            for dp, dn, fns in os.walk(path):
                for f in fns:
                    try:
                        total_size += os.path.getsize(os.path.join(dp, f))
                        file_count += 1
                    except (OSError, PermissionError):
                        pass
        except (OSError, PermissionError):
            pass
        return total_size, file_count

    # ── 1. Antigravity/Claude AI History ──
    gemini_brain = os.path.join(home, ".gemini", "antigravity-ide", "brain")
    if os.path.exists(gemini_brain):
        for item in os.listdir(gemini_brain):
            conv_path = os.path.join(gemini_brain, item)
            if not os.path.isdir(conv_path):
                continue
            total_size, file_count = folder_stats(conv_path)
            try:
                mtime = os.path.getmtime(conv_path)
            except (OSError, PermissionError):
                mtime = 0
            all_items.append({
                "name": item[:12] + "..." if len(item) > 15 else item,
                "path": conv_path,
                "size": total_size,
                "files": file_count,
                "mtime": mtime,
                "source": "🤖 AI Riwayat",
                "is_protected": (item == current_conv),
                "is_dir": True,
            })

    # ── 2. Gemini MCP & Logs ──
    for gdir in [os.path.join(home, ".gemini", "antigravity-ide", "mcp"),
                 os.path.join(home, ".gemini", "antigravity-ide", "logs")]:
        if os.path.exists(gdir) and os.path.isdir(gdir):
            total_size, file_count = folder_stats(gdir)
            if total_size > 0:
                all_items.append({
                    "name": os.path.basename(gdir),
                    "path": gdir, "size": total_size, "files": file_count,
                    "mtime": os.path.getmtime(gdir), "source": "🤖 AI Config",
                    "is_protected": False, "is_dir": True,
                })

    # ── 3. Application Logs (AppData) ──
    for appdata_dir in [local_appdata, roaming_appdata]:
        if not os.path.exists(appdata_dir):
            continue
        try:
            for app_folder in os.listdir(appdata_dir):
                app_path = os.path.join(appdata_dir, app_folder)
                if not os.path.isdir(app_path):
                    continue
                for subfolder in ["Logs", "logs", "Log", "log", "CrashDumps",
                                  "CrashReports", "crash_reports", "Crash Reports"]:
                    log_path = os.path.join(app_path, subfolder)
                    if os.path.exists(log_path) and os.path.isdir(log_path):
                        total_size, file_count = folder_stats(log_path)
                        if total_size > 100 * 1024:
                            all_items.append({
                                "name": f"{app_folder}/{subfolder}",
                                "path": log_path, "size": total_size,
                                "files": file_count,
                                "mtime": os.path.getmtime(log_path),
                                "source": "📝 App Log",
                                "is_protected": False, "is_dir": True,
                            })
        except (OSError, PermissionError):
            pass

    # ── 4. Windows Logs ──
    for wpath, wsource in [
        (r"C:\Windows\Logs", "🪟 Win Logs"),
        (r"C:\Windows\Panther", "🪟 Win Setup"),
        (r"C:\Windows\debug", "🪟 Win Debug"),
        (r"C:\Windows\LiveKernelReports", "🪟 Kernel"),
        (r"C:\Windows\Minidump", "🪟 Minidump"),
    ]:
        if os.path.exists(wpath):
            total_size, file_count = folder_stats(wpath)
            if total_size > 100 * 1024:
                all_items.append({
                    "name": os.path.basename(wpath),
                    "path": wpath, "size": total_size, "files": file_count,
                    "mtime": os.path.getmtime(wpath), "source": wsource,
                    "is_protected": False, "is_dir": True,
                })

    # ── 5. Tool's own cleanup logs ──
    own_logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    if os.path.exists(own_logs):
        total_size, file_count = folder_stats(own_logs)
        if total_size > 0:
            all_items.append({
                "name": "cleanup logs (tool ini)",
                "path": own_logs, "size": total_size, "files": file_count,
                "mtime": os.path.getmtime(own_logs), "source": "🧹 Tool",
                "is_protected": False, "is_dir": True,
            })

    # Sort by size
    all_items.sort(key=lambda x: x["size"], reverse=True)

    total_size = sum(item["size"] for item in all_items)
    print(f"  {WHT}Ditemukan: {B}{len(all_items)}{R} sumber logs/riwayat")
    print(f"  {WHT}Total ukuran: {RED}{B}{format_size(total_size)}{R}")
    print()

    for i, item in enumerate(all_items, 1):
        date_str = dt.datetime.fromtimestamp(item["mtime"]).strftime("%d %b %Y") if item["mtime"] else "?"
        if item["size"] > 100 * 1024 * 1024:
            sc = f"{RED}{B}"
        elif item["size"] > 10 * 1024 * 1024:
            sc = f"{YLW}{B}"
        elif item["size"] > 1024 * 1024:
            sc = YLW
        else:
            sc = GRN

        badge = f" {BG_GRN}{WHT}{B} AKTIF {R}" if item["is_protected"] else ""
        name_display = item["name"][:30] if len(item["name"]) > 30 else item["name"]

        print(f"  {B}[{i:3d}]{R} {name_display:<32} "
              f"{sc}{format_size(item['size']):>10}{R}  "
              f"{D}{item['files']:>5} file  │  {date_str}{R}")
        print(f"        {D}{item['source']}  │  {item['path']}{R}{badge}")
        if item["size"] > 50 * 1024 * 1024:
            print(f"        {RED}⚠️ Sangat besar!{R}")
        print()

    print(f"  {GRY}{'─' * 62}{R}")
    print(f"  {YLW}⚠️  Item AKTIF/DILINDUNGI tidak bisa dihapus.{R}")
    print(f"  {D}Masukkan nomor (misal: 1,3,5) atau 'q' untuk kembali.{R}")
    print(f"  {D}Ketik 'heavy' untuk hapus semua > 50 MB yang tidak dilindungi.{R}")
    print()

    try:
        inp = input(f"  {CYN}❯ Pilihan: {R}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if inp.lower() in ("q", "quit", "back", "kembali"):
        return

    to_delete = []
    if inp.lower() == "heavy":
        for item in all_items:
            if item["size"] > 50 * 1024 * 1024 and not item["is_protected"]:
                to_delete.append(item)
    else:
        try:
            nums = [int(x.strip()) for x in inp.split(",") if x.strip().isdigit()]
        except ValueError:
            print(f"  {RED}❌ Input tidak valid.{R}")
            pause()
            return
        for num in nums:
            if 1 <= num <= len(all_items):
                item = all_items[num - 1]
                if item["is_protected"]:
                    print(f"  {RED}⛔ Item #{num} DILINDUNGI, dilewati.{R}")
                else:
                    to_delete.append(item)

    if not to_delete:
        print(f"  {YLW}Tidak ada yang dipilih.{R}")
        pause()
        return

    total_del = sum(item["size"] for item in to_delete)
    print()
    print(f"  {YLW}{B}Akan menghapus ISI dari {len(to_delete)} folder ({format_size(total_del)}){R}")
    for item in to_delete:
        print(f"    {D}• {item['name']} ({format_size(item['size'])}){R}")
    print(f"  {RED}TIDAK BISA DIBATALKAN!{R}")
    try:
        confirm = input(f"  {RED}Ketik 'HAPUS' untuk konfirmasi: {R}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if confirm != "HAPUS":
        print(f"  {D}Dibatalkan.{R}")
        pause()
        return

    deleted_count = 0
    freed = 0
    for item in to_delete:
        try:
            for sub in os.listdir(item["path"]):
                sub_path = os.path.join(item["path"], sub)
                try:
                    if os.path.isfile(sub_path) or os.path.islink(sub_path):
                        freed += os.path.getsize(sub_path)
                        os.unlink(sub_path)
                        deleted_count += 1
                    elif os.path.isdir(sub_path):
                        for dp, dn, fns in os.walk(sub_path):
                            for f in fns:
                                try:
                                    freed += os.path.getsize(os.path.join(dp, f))
                                except (OSError, PermissionError):
                                    pass
                        shutil.rmtree(sub_path, ignore_errors=True)
                        deleted_count += 1
                except (PermissionError, OSError):
                    pass
            print(f"  {GRN}✅ Dibersihkan: {item['name']}{R}")
        except Exception as e:
            print(f"  {RED}❌ Gagal: {item['name']} ({e}){R}")

    print()
    print(f"  {GRN}{B}Selesai! {deleted_count} item dihapus, ~{format_size(freed)} dibebaskan.{R}")
    pause()


# ═══════════════════════════════════════════════════════════════
# FITUR 9: BERSIHKAN LOGS LAMA
# ═══════════════════════════════════════════════════════════════
def do_clean_logs():
    from scanner import format_size
    import datetime as dt

    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")

    if not os.path.exists(log_dir):
        print(f"\n  {D}Belum ada folder logs.{R}")
        pause()
        return

    print()
    print(f"  {CYN}{B}🧹 BERSIHKAN LOGS LAMA{R}")
    print(f"  {GRY}{'─' * 62}{R}")
    print(f"  {D}Folder: {log_dir}{R}")
    print()

    logs = []
    for f in os.listdir(log_dir):
        fpath = os.path.join(log_dir, f)
        if os.path.isfile(fpath):
            try:
                size = os.path.getsize(fpath)
                mtime = os.path.getmtime(fpath)
                logs.append((f, fpath, size, mtime))
            except (OSError, PermissionError):
                pass

    if not logs:
        print(f"  {D}Tidak ada file log.{R}")
        pause()
        return

    logs.sort(key=lambda x: x[3], reverse=True)  # Terbaru dulu
    total_size = sum(l[2] for l in logs)

    print(f"  {WHT}Ditemukan: {B}{len(logs)}{R} file log ({format_size(total_size)})")
    print()

    for i, (name, path, size, mtime) in enumerate(logs, 1):
        date_str = dt.datetime.fromtimestamp(mtime).strftime("%d %b %Y %H:%M")
        print(f"  {B}[{i:2d}]{R} {name:<35} {format_size(size):>10}  {D}{date_str}{R}")

    print()
    print(f"  {D}Ketik 'all' untuk hapus semua, atau nomor (misal: 2,3) atau 'q' untuk kembali.{R}")
    print()

    try:
        inp = input(f"  {CYN}❯ Pilihan: {R}").strip()
    except (KeyboardInterrupt, EOFError):
        return

    if inp.lower() in ("q", "quit", "back"):
        return

    to_delete = []
    if inp.lower() == "all":
        to_delete = logs
    else:
        try:
            nums = [int(x.strip()) for x in inp.split(",") if x.strip().isdigit()]
            for num in nums:
                if 1 <= num <= len(logs):
                    to_delete.append(logs[num - 1])
        except ValueError:
            print(f"  {RED}❌ Input tidak valid.{R}")
            pause()
            return

    if not to_delete:
        print(f"  {D}Tidak ada yang dipilih.{R}")
        pause()
        return

    deleted = 0
    freed = 0
    for name, path, size, mtime in to_delete:
        try:
            os.unlink(path)
            deleted += 1
            freed += size
        except Exception as e:
            print(f"  {RED}❌ Gagal hapus {name}: {e}{R}")

    print(f"  {GRN}{B}✅ {deleted} file log dihapus ({format_size(freed)} dibebaskan){R}")
    pause()



# MAIN LOOP
# ═══════════════════════════════════════════════════════════════
def main():
    setup_terminal()

    while True:
        show_banner()
        show_menu()

        try:
            choice = input(f"  {CYN}{B}❯ Pilih menu (0-9): {R}").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if choice == "0":
            clear()
            print()
            print(f"  {CYN}{B}👋 Terima kasih telah menggunakan Laptop Folder Cleaner!{R}")
            print(f"  {D}Semoga laptop Anda makin ringan dan cepat! 🚀{R}")
            print()
            break

        elif choice == "1":
            do_scan()

        elif choice == "2":
            if scan_results is None:
                print(f"\n  {RED}❌ Belum ada data. Scan dulu (pilih 1)!{R}")
                pause()
            else:
                do_summary()

        elif choice == "3":
            if scan_results is None:
                print(f"\n  {RED}❌ Belum ada data. Scan dulu (pilih 1)!{R}")
                pause()
            else:
                do_list_all()

        elif choice == "4":
            if scan_results is None:
                print(f"\n  {RED}❌ Belum ada data. Scan dulu (pilih 1)!{R}")
                pause()
            else:
                do_detail()

        elif choice == "5":
            if scan_results is None:
                print(f"\n  {RED}❌ Belum ada data. Scan dulu (pilih 1)!{R}")
                pause()
            else:
                do_delete()

        elif choice == "6":
            if scan_results is None:
                print(f"\n  {RED}❌ Belum ada data. Scan dulu (pilih 1)!{R}")
                pause()
            else:
                do_delete_all_safe()

        elif choice == "7":
            do_help()

        elif choice == "8":
            do_ai_history()

        elif choice == "9":
            do_clean_logs()

        else:
            print(f"\n  {RED}❌ Pilihan tidak valid. Masukkan angka 0-9.{R}")
            pause()


if __name__ == "__main__":
    main()
