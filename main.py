# -*- coding: utf-8 -*-
"""
🧹 Laptop Folder Cleaner - Pembersih Folder Laptop
=====================================================
Sistem Python yang memindai folder-folder di laptop Anda,
menjelaskan fungsi setiap folder, dan membantu Anda
menghapus folder yang tidak berguna dengan aman.

Fitur:
  ✅ Scan otomatis folder temp, cache, browser, development
  ✅ Penjelasan detail fungsi setiap folder (Bahasa Indonesia)
  ✅ Kategori risiko (Aman / Hati-hati / Berbahaya)
  ✅ Perhitungan ukuran folder
  ✅ Konfirmasi sebelum menghapus
  ✅ Log semua operasi penghapusan

Penggunaan:
  python main.py              → Mode interaktif
  python main.py --scan-only  → Scan saja tanpa hapus
  python main.py --help       → Bantuan
"""

import os
import sys
import time
import ctypes
import argparse
import datetime
from typing import List, Dict, Optional

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scanner import scan_all, format_size, days_since_modified, FolderResult
from cleaner import setup_logger, delete_folder_contents, delete_entire_folder


# ═══════════════════════════════════════════════════════════════
# ANSI Colors & Styling
# ═══════════════════════════════════════════════════════════════
class Colors:
    """ANSI color codes untuk terminal."""
    # Basic
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    
    # Colors
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    GRAY = "\033[90m"
    
    # Backgrounds
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"


def enable_ansi_windows():
    """Enable ANSI escape codes di Windows terminal."""
    if sys.platform == "win32":
        try:
            # Enable ANSI
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass
        try:
            # Force UTF-8 output
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def clear_screen():
    """Bersihkan layar terminal."""
    os.system("cls" if sys.platform == "win32" else "clear")


# ═══════════════════════════════════════════════════════════════
# UI Components
# ═══════════════════════════════════════════════════════════════

def print_banner():
    """Tampilkan banner aplikasi."""
    banner = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║   🧹  LAPTOP FOLDER CLEANER                                  ║
    ║   ─────────────────────────────                              ║
    ║   Pembersih & Analis Folder Laptop Anda                      ║
    ║                                                              ║
    ║   • Scan folder yang tidak berguna                           ║
    ║   • Penjelasan detail fungsi setiap folder                   ║
    ║   • Hapus dengan aman & konfirmasi                           ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
    print(banner)


def print_divider(char="═", length=70, color=Colors.GRAY):
    """Print garis pembatas."""
    print(f"{color}{char * length}{Colors.RESET}")


def print_section(title: str, icon: str = ""):
    """Print judul section."""
    print()
    print_divider()
    print(f"{Colors.BOLD}{Colors.CYAN}{icon} {title}{Colors.RESET}")
    print_divider()


def risk_badge(level: str) -> str:
    """Buat badge risiko berwarna."""
    if level == "safe":
        return f"{Colors.BG_GREEN}{Colors.WHITE}{Colors.BOLD} ✅ AMAN DIHAPUS {Colors.RESET}"
    elif level == "caution":
        return f"{Colors.BG_YELLOW}{Colors.WHITE}{Colors.BOLD} ⚠️  HATI-HATI  {Colors.RESET}"
    elif level == "danger":
        return f"{Colors.BG_RED}{Colors.WHITE}{Colors.BOLD} ⛔ BERBAHAYA  {Colors.RESET}"
    return f"{Colors.DIM}❓ TIDAK DIKETAHUI{Colors.RESET}"


def size_colored(size_bytes: int) -> str:
    """Format ukuran dengan warna berdasarkan besarnya."""
    size_str = format_size(size_bytes)
    if size_bytes > 1024 * 1024 * 1024:  # > 1 GB
        return f"{Colors.RED}{Colors.BOLD}{size_str}{Colors.RESET}"
    elif size_bytes > 100 * 1024 * 1024:  # > 100 MB
        return f"{Colors.YELLOW}{Colors.BOLD}{size_str}{Colors.RESET}"
    elif size_bytes > 10 * 1024 * 1024:  # > 10 MB
        return f"{Colors.YELLOW}{size_str}{Colors.RESET}"
    else:
        return f"{Colors.GREEN}{size_str}{Colors.RESET}"


def print_folder_detail(index: int, result: FolderResult, show_full: bool = True):
    """Print detail satu folder."""
    print()
    
    # Header
    print(f"  {Colors.BOLD}{Colors.WHITE}[{index}]{Colors.RESET} ", end="")
    print(f"{Colors.BOLD}{result.name}{Colors.RESET}")
    print(f"      {Colors.DIM}📂 {result.path}{Colors.RESET}")
    
    # Risk badge & size
    print(f"      {risk_badge(result.risk_level)}  │  ", end="")
    print(f"💿 Ukuran: {size_colored(result.size_bytes)}  │  ", end="")
    print(f"📄 {result.file_count} file, 📁 {result.folder_count} subfolder")
    
    # Last modified
    days = days_since_modified(result.last_modified)
    if days >= 0:
        if days > 90:
            age_color = Colors.RED
            age_text = f"⏰ {days} hari lalu (sudah lama!)"
        elif days > 30:
            age_color = Colors.YELLOW
            age_text = f"⏰ {days} hari lalu"
        else:
            age_color = Colors.GREEN
            age_text = f"⏰ {days} hari lalu"
        print(f"      {age_color}{age_text}{Colors.RESET}")
    
    if show_full:
        # Description
        print()
        for line in result.description.split("\n"):
            print(f"      {Colors.WHITE}{line}{Colors.RESET}")
        
        # Note
        if result.note:
            print(f"      {Colors.YELLOW}💡 Catatan: {result.note}{Colors.RESET}")
    
    print(f"      {Colors.DIM}{'─' * 58}{Colors.RESET}")


def print_summary(results: Dict[str, List[FolderResult]]):
    """Print ringkasan hasil scan."""
    total_size = 0
    total_safe_size = 0
    total_folders = 0
    safe_folders = 0
    
    for category, folders in results.items():
        for f in folders:
            total_size += f.size_bytes
            total_folders += 1
            if f.risk_level == "safe" and f.can_delete:
                total_safe_size += f.size_bytes
                safe_folders += 1
    
    print_section("📊 RINGKASAN SCAN", "")
    print()
    print(f"  {Colors.WHITE}Total folder ditemukan  : {Colors.BOLD}{total_folders}{Colors.RESET}")
    print(f"  {Colors.WHITE}Total ukuran            : {size_colored(total_size)}")
    print(f"  {Colors.GREEN}Folder aman dihapus     : {Colors.BOLD}{safe_folders}{Colors.RESET}")
    print(f"  {Colors.GREEN}Potensi ruang bebas     : {size_colored(total_safe_size)}")
    print()


def progress_bar(current: int, total: int, message: str = "", width: int = 40):
    """Tampilkan progress bar."""
    if total == 0:
        return
    
    percent = current / total
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    
    # Truncate message if too long
    max_msg_len = 35
    if len(message) > max_msg_len:
        message = message[:max_msg_len-3] + "..."
    
    sys.stdout.write(
        f"\r  {Colors.CYAN}[{bar}]{Colors.RESET} "
        f"{Colors.BOLD}{percent*100:5.1f}%{Colors.RESET} "
        f"{Colors.DIM}{message:<{max_msg_len}}{Colors.RESET}"
    )
    sys.stdout.flush()
    
    if current >= total:
        print()  # New line when done


# ═══════════════════════════════════════════════════════════════
# Main Logic
# ═══════════════════════════════════════════════════════════════

def run_scan() -> Dict[str, List[FolderResult]]:
    """Jalankan scan dan tampilkan progress."""
    print()
    print(f"  {Colors.CYAN}{Colors.BOLD}🔍 Memulai scan folder...{Colors.RESET}")
    print(f"  {Colors.DIM}Ini mungkin memakan waktu beberapa menit...{Colors.RESET}")
    print()
    
    start_time = time.time()
    
    def on_progress(current, total, message):
        progress_bar(current, total, message)
    
    results = scan_all(progress_callback=on_progress)
    
    elapsed = time.time() - start_time
    print()
    print(f"  {Colors.GREEN}✅ Scan selesai dalam {elapsed:.1f} detik!{Colors.RESET}")
    
    return results


def display_results(results: Dict[str, List[FolderResult]], show_details: bool = True):
    """Tampilkan hasil scan per kategori."""
    
    global_index = 1
    index_map = {}  # global_index -> FolderResult
    
    for category, folders in results.items():
        category_size = sum(f.size_bytes for f in folders)
        
        print_section(f"{category} ({len(folders)} folder, {format_size(category_size)})")
        
        for folder in folders:
            print_folder_detail(global_index, folder, show_full=show_details)
            index_map[global_index] = folder
            global_index += 1
    
    return index_map


def interactive_delete(results: Dict[str, List[FolderResult]], index_map: Dict[int, FolderResult]):
    """Mode interaktif untuk memilih dan menghapus folder."""
    
    logger = setup_logger()
    
    while True:
        print()
        print_divider("─", 70, Colors.CYAN)
        print(f"""
  {Colors.BOLD}{Colors.WHITE}Pilihan Aksi:{Colors.RESET}
  
  {Colors.GREEN}[nomor]{Colors.RESET}          → Lihat detail & hapus folder tertentu (contoh: 1)
  {Colors.GREEN}[nomor,nomor]{Colors.RESET}    → Hapus beberapa folder sekaligus (contoh: 1,3,5)
  {Colors.GREEN}safe{Colors.RESET}             → Hapus SEMUA folder dengan label ✅ AMAN
  {Colors.GREEN}detail [nomor]{Colors.RESET}   → Lihat detail folder tertentu
  {Colors.GREEN}rescan{Colors.RESET}           → Scan ulang
  {Colors.YELLOW}q / quit{Colors.RESET}         → Keluar
""")
        
        try:
            choice = input(f"  {Colors.CYAN}❯ Pilihan Anda: {Colors.RESET}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print()
            break
        
        if choice in ("q", "quit", "exit", "keluar"):
            break
        
        elif choice == "rescan":
            clear_screen()
            print_banner()
            results = run_scan()
            print_summary(results)
            index_map = display_results(results)
            continue
        
        elif choice.startswith("detail"):
            parts = choice.split()
            if len(parts) == 2 and parts[1].isdigit():
                idx = int(parts[1])
                if idx in index_map:
                    print_folder_detail(idx, index_map[idx], show_full=True)
                else:
                    print(f"  {Colors.RED}❌ Nomor {idx} tidak valid.{Colors.RESET}")
            else:
                print(f"  {Colors.DIM}Gunakan: detail [nomor]  (contoh: detail 3){Colors.RESET}")
            continue
        
        elif choice == "safe":
            # Hapus semua folder safe
            safe_folders = [
                (idx, f) for idx, f in index_map.items()
                if f.risk_level == "safe" and f.can_delete
            ]
            
            if not safe_folders:
                print(f"  {Colors.YELLOW}Tidak ada folder aman untuk dihapus.{Colors.RESET}")
                continue
            
            total_size = sum(f.size_bytes for _, f in safe_folders)
            
            print()
            print(f"  {Colors.BOLD}{Colors.YELLOW}╔══════════════════════════════════════════════╗{Colors.RESET}")
            print(f"  {Colors.BOLD}{Colors.YELLOW}║  ⚠️  KONFIRMASI HAPUS SEMUA FOLDER AMAN     ║{Colors.RESET}")
            print(f"  {Colors.BOLD}{Colors.YELLOW}╚══════════════════════════════════════════════╝{Colors.RESET}")
            print()
            print(f"  Akan menghapus {Colors.BOLD}{len(safe_folders)}{Colors.RESET} folder")
            print(f"  Estimasi ruang bebas: {size_colored(total_size)}")
            print()
            
            for idx, f in safe_folders:
                print(f"    [{idx}] {f.name} ({format_size(f.size_bytes)})")
                print(f"        {Colors.DIM}{f.path}{Colors.RESET}")
            
            print()
            try:
                confirm = input(f"  {Colors.RED}{Colors.BOLD}Ketik 'HAPUS' untuk konfirmasi: {Colors.RESET}").strip()
            except (KeyboardInterrupt, EOFError):
                print()
                continue
            
            if confirm == "HAPUS":
                print()
                total_freed = 0
                for idx, f in safe_folders:
                    print(f"  🗑️  Menghapus [{idx}] {f.name}...", end=" ")
                    stats = delete_folder_contents(f.path, logger)
                    total_freed += stats["freed_bytes"]
                    
                    if stats["errors"]:
                        print(f"{Colors.YELLOW}⚠️ Sebagian gagal{Colors.RESET}")
                        for err in stats["errors"][:3]:
                            print(f"      {Colors.DIM}{err}{Colors.RESET}")
                    else:
                        print(f"{Colors.GREEN}✅ Berhasil!{Colors.RESET}")
                
                print()
                print(f"  {Colors.GREEN}{Colors.BOLD}✅ Selesai! Ruang dibebaskan: {format_size(total_freed)}{Colors.RESET}")
                logger.info(f"Total ruang dibebaskan: {format_size(total_freed)}")
            else:
                print(f"  {Colors.DIM}Dibatalkan.{Colors.RESET}")
            continue
        
        else:
            # Parse numbers (single or comma-separated)
            try:
                indices = [int(x.strip()) for x in choice.split(",") if x.strip().isdigit()]
            except ValueError:
                print(f"  {Colors.RED}❌ Input tidak valid. Coba lagi.{Colors.RESET}")
                continue
            
            if not indices:
                print(f"  {Colors.RED}❌ Input tidak valid. Coba lagi.{Colors.RESET}")
                continue
            
            # Validate all indices
            invalid = [i for i in indices if i not in index_map]
            if invalid:
                print(f"  {Colors.RED}❌ Nomor tidak valid: {invalid}{Colors.RESET}")
                continue
            
            folders_to_delete = [(idx, index_map[idx]) for idx in indices]
            total_size = sum(f.size_bytes for _, f in folders_to_delete)
            
            print()
            for idx, f in folders_to_delete:
                print_folder_detail(idx, f, show_full=True)
            
            print()
            print(f"  {Colors.BOLD}Total ukuran: {size_colored(total_size)}{Colors.RESET}")
            
            # Check for dangerous folders
            dangerous = [f for _, f in folders_to_delete if f.risk_level == "danger"]
            if dangerous:
                print()
                print(f"  {Colors.RED}{Colors.BOLD}⛔ PERINGATAN: Anda memilih folder BERBAHAYA!{Colors.RESET}")
                for f in dangerous:
                    print(f"     ⛔ {f.name}: {f.note}")
                print()
                print(f"  {Colors.RED}Menghapus folder berbahaya dapat merusak sistem!{Colors.RESET}")
                try:
                    confirm = input(f"  {Colors.RED}{Colors.BOLD}Ketik 'SAYA YAKIN' untuk melanjutkan: {Colors.RESET}").strip()
                except (KeyboardInterrupt, EOFError):
                    print()
                    continue
                if confirm != "SAYA YAKIN":
                    print(f"  {Colors.DIM}Dibatalkan.{Colors.RESET}")
                    continue
            else:
                # Warn for caution folders
                caution = [f for _, f in folders_to_delete if f.risk_level == "caution"]
                if caution:
                    print()
                    print(f"  {Colors.YELLOW}⚠️ Beberapa folder memerlukan kehati-hatian:{Colors.RESET}")
                    for f in caution:
                        print(f"     ⚠️ {f.name}: {f.note}")
                
                print()
                try:
                    confirm = input(
                        f"  {Colors.YELLOW}{Colors.BOLD}Hapus {len(folders_to_delete)} folder? "
                        f"(ketik 'y' atau 'HAPUS'): {Colors.RESET}"
                    ).strip().lower()
                except (KeyboardInterrupt, EOFError):
                    print()
                    continue
                
                if confirm not in ("y", "yes", "ya", "hapus"):
                    print(f"  {Colors.DIM}Dibatalkan.{Colors.RESET}")
                    continue
            
            # Execute deletion
            print()
            total_freed = 0
            for idx, f in folders_to_delete:
                print(f"  🗑️  Menghapus [{idx}] {f.name}...", end=" ")
                
                # For dev folders like node_modules, delete the whole folder
                dev_deletable = {"node_modules", "__pycache__", ".next", ".nuxt", 
                                ".output", "dist", "build", ".cache", ".parcel-cache",
                                ".turbo", "coverage", ".venv", "venv"}
                
                if f.name in dev_deletable:
                    stats = delete_entire_folder(f.path, logger)
                else:
                    stats = delete_folder_contents(f.path, logger)
                
                total_freed += stats["freed_bytes"]
                
                if stats["errors"]:
                    print(f"{Colors.YELLOW}⚠️ Sebagian gagal ({len(stats['errors'])} error){Colors.RESET}")
                    for err in stats["errors"][:2]:
                        print(f"      {Colors.DIM}{err}{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}✅ Berhasil! ({format_size(stats['freed_bytes'])}){Colors.RESET}")
            
            print()
            print(f"  {Colors.GREEN}{Colors.BOLD}✅ Total ruang dibebaskan: {format_size(total_freed)}{Colors.RESET}")
            logger.info(f"Batch delete total freed: {format_size(total_freed)}")


def main():
    """Entry point utama."""
    parser = argparse.ArgumentParser(
        description="🧹 Laptop Folder Cleaner - Pembersih Folder Laptop",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python main.py              # Mode interaktif (scan + pilih + hapus)
  python main.py --scan-only  # Hanya scan & tampilkan info
  python main.py --compact    # Tampilan ringkas tanpa detail penuh
        """
    )
    parser.add_argument(
        "--scan-only", action="store_true",
        help="Hanya scan dan tampilkan informasi, tanpa opsi hapus"
    )
    parser.add_argument(
        "--compact", action="store_true",
        help="Tampilan ringkas (tanpa penjelasan detail)"
    )
    
    args = parser.parse_args()
    
    # Setup
    enable_ansi_windows()
    clear_screen()
    print_banner()
    
    # Info sistem
    print(f"  {Colors.DIM}📅 Tanggal  : {datetime.datetime.now().strftime('%d %B %Y, %H:%M:%S')}{Colors.RESET}")
    print(f"  {Colors.DIM}👤 User     : {os.environ.get('USERNAME', 'Unknown')}{Colors.RESET}")
    print(f"  {Colors.DIM}🏠 Home     : {os.path.expanduser('~')}{Colors.RESET}")
    print(f"  {Colors.DIM}💻 Platform : {sys.platform}{Colors.RESET}")
    
    # Scan
    results = run_scan()
    
    if not results:
        print()
        print(f"  {Colors.GREEN}🎉 Laptop Anda sudah bersih! Tidak ada folder yang perlu dibersihkan.{Colors.RESET}")
        return
    
    # Summary
    print_summary(results)
    
    # Display results
    show_details = not args.compact
    index_map = display_results(results, show_details=show_details)
    
    if args.scan_only:
        print()
        print(f"  {Colors.DIM}(Mode scan-only: tidak ada opsi hapus){Colors.RESET}")
        print()
        return
    
    # Interactive delete
    interactive_delete(results, index_map)
    
    # Farewell
    print()
    print(f"  {Colors.CYAN}{Colors.BOLD}👋 Terima kasih telah menggunakan Laptop Folder Cleaner!{Colors.RESET}")
    print(f"  {Colors.DIM}Log operasi tersimpan di folder 'logs/' untuk referensi.{Colors.RESET}")
    print()


if __name__ == "__main__":
    main()
