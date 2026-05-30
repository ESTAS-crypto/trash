# -*- coding: utf-8 -*-
"""
Scanner: Modul untuk scan folder-folder di laptop.
Mendeteksi folder yang berpotensi tidak berguna dan menghitung ukurannya.
"""

import os
import sys
import time
import ctypes
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class FolderResult:
    """Hasil scan satu folder."""
    path: str
    name: str
    size_bytes: int = 0
    file_count: int = 0
    folder_count: int = 0
    last_modified: float = 0
    description: str = ""
    risk_level: str = "caution"  # safe, caution, danger
    category: str = "Unknown"
    can_delete: Optional[bool] = None
    note: str = ""
    safety_score: int = 5   # 1-10 (10 = paling aman dihapus)
    impact: str = ""        # Apa dampak jika dihapus
    recovery: str = ""      # Cara memulihkan
    error: str = ""


def get_folder_size(path: str) -> Tuple[int, int, int]:
    """
    Menghitung ukuran total folder, jumlah file, dan jumlah subfolder.
    Returns: (size_bytes, file_count, folder_count)
    """
    total_size = 0
    file_count = 0
    folder_count = 0
    
    try:
        for dirpath, dirnames, filenames in os.walk(path):
            folder_count += len(dirnames)
            for filename in filenames:
                file_count += 1
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    
    return total_size, file_count, folder_count


def format_size(size_bytes: int) -> str:
    """Format ukuran bytes ke format yang mudah dibaca."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_last_modified(path: str) -> float:
    """Mendapatkan waktu terakhir folder dimodifikasi."""
    try:
        return os.path.getmtime(path)
    except (OSError, PermissionError):
        return 0


def days_since_modified(timestamp: float) -> int:
    """Menghitung berapa hari sejak terakhir dimodifikasi."""
    if timestamp == 0:
        return -1
    return int((time.time() - timestamp) / 86400)


def get_user_home() -> str:
    """Mendapatkan path home directory user."""
    return str(Path.home())


def get_temp_dirs() -> List[str]:
    """Mendapatkan daftar folder temp."""
    dirs = []
    
    # Windows TEMP
    temp = os.environ.get("TEMP", "")
    if temp and os.path.exists(temp):
        dirs.append(temp)
    
    tmp = os.environ.get("TMP", "")
    if tmp and os.path.exists(tmp) and tmp != temp:
        dirs.append(tmp)
    
    # Windows global temp
    win_temp = r"C:\Windows\Temp"
    if os.path.exists(win_temp):
        dirs.append(win_temp)
    
    return dirs


# Folder yang DILINDUNGI - TIDAK AKAN PERNAH disarankan untuk dihapus
PROTECTED_FOLDERS = {
    ".gemini",          # Antigravity IDE / Claude AI - histori obrolan & data penting
    ".vscode",          # VS Code settings & extensions
    ".ssh",             # SSH keys - sangat penting!
    ".gnupg",           # GPG encryption keys
    ".config",          # Konfigurasi aplikasi Linux-style
    ".android",         # Android SDK config (bukan cache)
    "AppData",          # Jangan hapus root AppData
}

# Path yang dilindungi (partial match)
PROTECTED_PATH_PARTS = {
    ".gemini",
    "antigravity-ide",
    "brain",            # Antigravity brain/conversation data
}


def is_protected_path(path: str) -> bool:
    """Cek apakah path ini dilindungi dan tidak boleh dihapus."""
    path_lower = path.lower()
    # Cek apakah path mengandung folder yang dilindungi
    for protected in PROTECTED_PATH_PARTS:
        if protected.lower() in path_lower:
            return True
    # Cek apakah nama folder adalah folder yang dilindungi
    basename = os.path.basename(path)
    if basename in PROTECTED_FOLDERS:
        return True
    return False


def get_scan_locations() -> Dict[str, List[str]]:
    """
    Mendapatkan semua lokasi yang akan di-scan.
    Returns: Dict dengan kategori -> list of paths
    Folder yang dilindungi (seperti .gemini/Antigravity) otomatis dikecualikan.
    """
    home = get_user_home()
    local_appdata = os.environ.get("LOCALAPPDATA", os.path.join(home, "AppData", "Local"))
    roaming_appdata = os.environ.get("APPDATA", os.path.join(home, "AppData", "Roaming"))
    
    locations = {
        "🗑️ Temporary Files": [],
        "💾 Cache & Performance": [],
        "🔧 Development (Build/Cache)": [],
        "📝 Logs & Crash Reports": [],
        "🌐 Browser Cache": [],
        "📦 Package Manager Cache": [],
        "🪟 Windows System Cache": [],
    }
    
    # --- Temporary Files ---
    for temp_dir in get_temp_dirs():
        locations["🗑️ Temporary Files"].append(temp_dir)
    
    # --- Cache & Performance ---
    cache_paths = [
        os.path.join(local_appdata, "D3DSCache"),
        os.path.join(local_appdata, "IconCache.db"),
        os.path.join(local_appdata, "CrashDumps"),
        os.path.join(local_appdata, "CrashReports"),
    ]
    for p in cache_paths:
        if os.path.exists(p):
            locations["💾 Cache & Performance"].append(p)
    
    # --- Windows System Cache ---
    win_cache = [
        r"C:\Windows\Prefetch",
        r"C:\Windows\SoftwareDistribution\Download",
        os.path.join(home, "AppData", "Local", "Temp"),
    ]
    for p in win_cache:
        if os.path.exists(p) and p not in locations["🗑️ Temporary Files"]:
            locations["🪟 Windows System Cache"].append(p)
    
    # Windows.old
    if os.path.exists(r"C:\Windows.old"):
        locations["🪟 Windows System Cache"].append(r"C:\Windows.old")
    
    # $WINDOWS.~BT
    if os.path.exists(r"C:\$WINDOWS.~BT"):
        locations["🪟 Windows System Cache"].append(r"C:\$WINDOWS.~BT")
    
    # --- Browser Cache ---
    browsers = {
        "Google Chrome": os.path.join(local_appdata, "Google", "Chrome", "User Data"),
        "Microsoft Edge": os.path.join(local_appdata, "Microsoft", "Edge", "User Data"),
        "Brave": os.path.join(local_appdata, "BraveSoftware", "Brave-Browser", "User Data"),
        "Opera": os.path.join(roaming_appdata, "Opera Software", "Opera Stable"),
        "Opera GX": os.path.join(roaming_appdata, "Opera Software", "Opera GX Stable"),
        "Vivaldi": os.path.join(local_appdata, "Vivaldi", "User Data"),
    }
    
    cache_subfolder_names = [
        "Cache", "Code Cache", "GPUCache", "ShaderCache", "DawnCache",
        "GrShaderCache", "GraphiteDawnCache", "Service Worker", "CacheStorage",
    ]
    
    for browser_name, browser_path in browsers.items():
        if os.path.exists(browser_path):
            # Scan Default profile and numbered profiles
            profiles = ["Default"]
            try:
                for item in os.listdir(browser_path):
                    if item.startswith("Profile "):
                        profiles.append(item)
            except (OSError, PermissionError):
                pass
            
            for profile in profiles:
                profile_path = os.path.join(browser_path, profile)
                if os.path.exists(profile_path):
                    for cache_name in cache_subfolder_names:
                        cache_path = os.path.join(profile_path, cache_name)
                        if os.path.exists(cache_path):
                            locations["🌐 Browser Cache"].append(cache_path)
            
            # Top-level browser cache
            for cache_name in ["ShaderCache", "GrShaderCache", "GraphiteDawnCache"]:
                cache_path = os.path.join(browser_path, cache_name)
                if os.path.exists(cache_path):
                    locations["🌐 Browser Cache"].append(cache_path)
    
    # Firefox cache
    firefox_path = os.path.join(local_appdata, "Mozilla", "Firefox", "Profiles")
    if os.path.exists(firefox_path):
        try:
            for profile_dir in os.listdir(firefox_path):
                cache_path = os.path.join(firefox_path, profile_dir, "cache2")
                if os.path.exists(cache_path):
                    locations["🌐 Browser Cache"].append(cache_path)
        except (OSError, PermissionError):
            pass
    
    # --- Package Manager Cache ---
    pkg_caches = {
        ".npm": os.path.join(home, ".npm"),
        ".yarn": os.path.join(home, ".yarn"),
        "pip": os.path.join(local_appdata, "pip", "cache"),
        ".nuget": os.path.join(home, ".nuget", "packages"),
        ".gradle": os.path.join(home, ".gradle", "caches"),
        ".m2": os.path.join(home, ".m2", "repository"),
        "pnpm": os.path.join(local_appdata, "pnpm-cache"),
    }
    for name, pkg_path in pkg_caches.items():
        if os.path.exists(pkg_path):
            locations["📦 Package Manager Cache"].append(pkg_path)
    
    # --- Logs & Crash Reports ---
    # Scan AppData for crash/log folders (kecuali folder yang dilindungi)
    for appdata_dir in [local_appdata, roaming_appdata]:
        if not os.path.exists(appdata_dir):
            continue
        try:
            for app_folder in os.listdir(appdata_dir):
                app_path = os.path.join(appdata_dir, app_folder)
                if not os.path.isdir(app_path):
                    continue
                # Skip folder yang dilindungi
                if app_folder in PROTECTED_FOLDERS or is_protected_path(app_path):
                    continue
                for subfolder in ["Logs", "logs", "CrashDumps", "CrashReports", "crash_reports"]:
                    log_path = os.path.join(app_path, subfolder)
                    if os.path.exists(log_path) and os.path.isdir(log_path):
                        if not is_protected_path(log_path):
                            locations["📝 Logs & Crash Reports"].append(log_path)
        except (OSError, PermissionError):
            pass
    
    # --- Development Build/Cache ---
    # Scan common project directories for node_modules, __pycache__, etc.
    dev_scan_roots = [
        os.path.join(home, "Documents"),
        os.path.join(home, "Desktop"),
        os.path.join(home, "OneDrive", "Documents"),
        os.path.join(home, "Projects"),
        os.path.join(home, "projects"),
        os.path.join(home, "dev"),
        os.path.join(home, "Dev"),
        os.path.join(home, "Code"),
        os.path.join(home, "code"),
        os.path.join(home, "workspace"),
        os.path.join(home, "Workspace"),
        os.path.join(home, "repos"),
        os.path.join(home, "source"),
        os.path.join(home, "src"),
    ]
    
    dev_folder_names = {
        "node_modules", "__pycache__", ".next", ".nuxt", ".output",
        "dist", "build", ".cache", ".parcel-cache", ".turbo",
        "coverage", ".venv", "venv",
    }
    
    for scan_root in dev_scan_roots:
        if not os.path.exists(scan_root):
            continue
        try:
            for root, dirs, files in os.walk(scan_root):
                # Don't go too deep
                depth = root.replace(scan_root, "").count(os.sep)
                if depth > 4:
                    dirs.clear()
                    continue
                
                # Skip certain directories (termasuk folder yang dilindungi)
                skip_dirs = {".git", "Windows", "System32", "$Recycle.Bin"}
                skip_dirs.update(PROTECTED_FOLDERS)
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                
                for d in list(dirs):
                    if d in dev_folder_names:
                        dev_path = os.path.join(root, d)
                        locations["🔧 Development (Build/Cache)"].append(dev_path)
                        # Don't recurse into these
                        dirs.remove(d)
        except (OSError, PermissionError):
            pass
    
    # Remove empty categories
    return {k: v for k, v in locations.items() if v}


def scan_folder(path: str) -> FolderResult:
    """Scan satu folder dan kumpulkan informasinya."""
    from folder_knowledge import get_folder_info
    
    name = os.path.basename(path)
    result = FolderResult(path=path, name=name)
    
    try:
        # Get folder info from knowledge base
        info = get_folder_info(name)
        result.description = info["description"]
        result.risk_level = info["risk_level"]
        result.category = info["category"]
        result.can_delete = info["can_delete"]
        result.note = info["note"]
        
        # Calculate size
        result.size_bytes, result.file_count, result.folder_count = get_folder_size(path)
        result.last_modified = get_last_modified(path)
        
        # Calculate safety score & impact
        result.safety_score = calculate_safety_score(result)
        result.impact, result.recovery = get_impact_recovery(result)
        
    except Exception as e:
        result.error = str(e)
    
    return result


def scan_all(progress_callback=None) -> Dict[str, List[FolderResult]]:
    """
    Scan semua lokasi dan kembalikan hasil terorganisir.
    progress_callback: fungsi yang dipanggil dengan (current, total, message)
    """
    locations = get_scan_locations()
    results = {}
    
    total_folders = sum(len(paths) for paths in locations.values())
    current = 0
    
    for category, paths in locations.items():
        category_results = []
        
        for path in paths:
            current += 1
            if progress_callback:
                progress_callback(current, total_folders, f"Scanning: {os.path.basename(path)}")
            
            result = scan_folder(path)
            if result.size_bytes > 0:  # Only include non-empty folders
                category_results.append(result)
        
        if category_results:
            # Sort by size (biggest first)
            category_results.sort(key=lambda x: x.size_bytes, reverse=True)
            results[category] = category_results
    
    return results


# ═══════════════════════════════════════════════════════════════
# ANALISIS DETAIL (dipanggil on-demand, bukan saat scan)
# ═══════════════════════════════════════════════════════════════

def analyze_folder_detail(path: str) -> dict:
    """
    Analisis mendalam isi folder. Dipanggil saat user minta detail.
    Returns dict berisi:
      - top_files: 10 file terbesar
      - file_types: breakdown jenis file
      - oldest_file: file paling tua
      - newest_file: file paling baru
      - total_depth: kedalaman folder
      - suspicious_files: file yang mungkin penting
    """
    analysis = {
        "top_files": [],
        "file_types": {},
        "oldest_file": None,
        "newest_file": None,
        "total_depth": 0,
        "suspicious_files": [],
    }
    
    all_files = []
    
    # Ekstensi file yang mungkin penting (user data)
    important_extensions = {
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3",
        ".zip", ".rar", ".7z", ".psd", ".ai", ".sketch",
        ".sqlite", ".db", ".mdb",
    }
    
    try:
        for root, dirs, files in os.walk(path):
            depth = root.replace(path, "").count(os.sep)
            analysis["total_depth"] = max(analysis["total_depth"], depth)
            
            # Limit depth untuk kecepatan
            if depth > 5:
                dirs.clear()
                continue
            
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    fsize = os.path.getsize(fpath)
                    fmtime = os.path.getmtime(fpath)
                    rel_path = os.path.relpath(fpath, path)
                    ext = os.path.splitext(fname)[1].lower() or "(tanpa ekstensi)"
                    
                    all_files.append((rel_path, fsize, fmtime, ext))
                    
                    # Count file types
                    if ext not in analysis["file_types"]:
                        analysis["file_types"][ext] = {"count": 0, "size": 0}
                    analysis["file_types"][ext]["count"] += 1
                    analysis["file_types"][ext]["size"] += fsize
                    
                    # Check for important/suspicious files
                    if ext in important_extensions and fsize > 1024:
                        analysis["suspicious_files"].append((rel_path, fsize, ext))
                    
                except (OSError, PermissionError):
                    pass
    except (OSError, PermissionError):
        pass
    
    # Top 10 file terbesar
    all_files.sort(key=lambda x: x[1], reverse=True)
    analysis["top_files"] = [(f[0], f[1], f[3]) for f in all_files[:10]]
    
    # File tertua dan terbaru
    if all_files:
        by_time = sorted(all_files, key=lambda x: x[2])
        analysis["oldest_file"] = (by_time[0][0], by_time[0][2])
        analysis["newest_file"] = (by_time[-1][0], by_time[-1][2])
    
    # Top 10 jenis file berdasarkan ukuran
    analysis["file_types"] = dict(
        sorted(analysis["file_types"].items(), 
               key=lambda x: x[1]["size"], reverse=True)[:10]
    )
    
    # Limit suspicious files
    analysis["suspicious_files"] = sorted(
        analysis["suspicious_files"], 
        key=lambda x: x[1], reverse=True
    )[:5]
    
    return analysis


def calculate_safety_score(result: FolderResult) -> int:
    """
    Hitung skor keamanan 1-10.
    10 = sangat aman dihapus (tidak ada risiko)
    1  = sangat berbahaya (bisa rusak sistem)
    """
    score = 5  # default
    
    # Base score dari risk level
    if result.risk_level == "safe":
        score = 8
    elif result.risk_level == "caution":
        score = 4
    elif result.risk_level == "danger":
        score = 1
    
    # Bonus untuk folder yang sudah lama tidak dipakai
    days = days_since_modified(result.last_modified)
    if days > 365:
        score = min(10, score + 2)
    elif days > 180:
        score = min(10, score + 2)
    elif days > 90:
        score = min(10, score + 1)
    elif days < 3 and result.risk_level != "safe":
        score = max(1, score - 1)  # baru dipakai, kurangi skor
    
    # Bonus untuk kategori yang bisa diregenerasi
    regen_categories = {
        "Cache", "Temporary Files", "Crash Reports", 
        "Logs", "Performance Cache"
    }
    if result.category in regen_categories:
        score = min(10, score + 1)
    
    # Khusus development: cek nama folder
    always_safe_names = {
        "node_modules", "__pycache__", ".next", ".nuxt", 
        "dist", "build", ".cache", ".parcel-cache", ".turbo",
        "coverage", "CachedData", "CachedExtensions",
        "CachedExtensionVSIXs", "GPUCache", "ShaderCache",
        "Code Cache", "DawnCache", "GrShaderCache",
        "GraphiteDawnCache", "D3DSCache", "CrashDumps",
        "CrashReports", "Thumbnails", "Prefetch",
    }
    if result.name in always_safe_names:
        score = max(score, 8)
    
    # Danger override: folder yang TIDAK BOLEH dihapus
    never_delete_names = {
        "Windows", "System32", "SysWOW64", "WinSxS",
        "Program Files", "Program Files (x86)", "ProgramData",
        "Documents", "OneDrive", "User Data", "Default",
    }
    if result.name in never_delete_names:
        score = min(score, 2)
    
    return max(1, min(10, score))


def get_impact_recovery(result: FolderResult) -> tuple:
    """
    Dapatkan penjelasan dampak dan cara pemulihan.
    Returns: (impact_text, recovery_text)
    """
    name = result.name
    cat = result.category
    
    # ── Khusus berdasarkan nama folder ──
    specific = {
        "node_modules": (
            "Proyek JavaScript/Node.js tidak bisa dijalankan sampai dependencies di-install ulang. "
            "Tidak ada data pribadi yang hilang.",
            "Buka terminal di folder proyek, jalankan: npm install"
        ),
        "__pycache__": (
            "TIDAK ADA DAMPAK. Ini hanya cache bytecode Python yang 100% otomatis.",
            "Dibuat ulang otomatis saat menjalankan script Python."
        ),
        ".venv": (
            "Virtual environment Python hilang. Script di proyek ini tidak bisa jalan "
            "sampai environment dibuat ulang.",
            "Jalankan: python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt"
        ),
        "venv": (
            "Virtual environment Python hilang. Sama seperti .venv.",
            "Jalankan: python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt"
        ),
        ".next": (
            "Build cache Next.js hilang. Website dev tidak bisa diakses sampai di-build ulang.",
            "Jalankan: npm run dev (development) atau npm run build (production)"
        ),
        ".nuxt": (
            "Build cache Nuxt.js hilang.",
            "Jalankan: npm run dev untuk regenerasi."
        ),
        "build": (
            "Output build proyek hilang (file hasil kompilasi). "
            "Source code TETAP AMAN, hanya hasil build yang hilang.",
            "Jalankan build command proyek: npm run build / gradle build / dotnet build"
        ),
        "dist": (
            "File distribusi/output build hilang. Source code TETAP AMAN.",
            "Jalankan: npm run build atau build command yang sesuai."
        ),
        "Temp": (
            "TIDAK ADA DAMPAK berarti. File sementara yang seharusnya sudah tidak dipakai. "
            "Beberapa aplikasi yang sedang berjalan mungkin error (tutup dulu).",
            "File dibuat ulang otomatis oleh Windows dan aplikasi."
        ),
        "CrashDumps": (
            "TIDAK ADA DAMPAK. Hanya kehilangan laporan crash lama untuk debugging.",
            "Tidak perlu recovery. Crash dump baru dibuat otomatis jika ada error."
        ),
        "CrashReports": (
            "TIDAK ADA DAMPAK. Sama seperti CrashDumps.",
            "Tidak perlu recovery."
        ),
        "D3DSCache": (
            "Game/aplikasi 3D mungkin sedikit lambat pertama kali (kompilasi shader ulang).",
            "Otomatis diregenerasi saat menjalankan game/aplikasi."
        ),
        "Cache": (
            "Browser/aplikasi perlu memuat ulang data dari internet. "
            "Browsing mungkin sedikit lambat sementara.",
            "Cache diregenerasi otomatis saat browsing. Tidak perlu aksi manual."
        ),
        "Code Cache": (
            "JavaScript yang sudah dikompilasi browser hilang. Web app mungkin sedikit lambat.",
            "Otomatis diregenerasi saat mengunjungi website."
        ),
        "GPUCache": (
            "Cache rendering GPU browser hilang. Minimal impact.",
            "Otomatis diregenerasi oleh browser."
        ),
        "ShaderCache": (
            "Cache shader grafis hilang. Game mungkin stutter sebentar saat kompilasi ulang.",
            "Otomatis diregenerasi saat menjalankan game/browser."
        ),
        "DawnCache": (
            "Cache WebGPU hilang. Tidak ada dampak terasa.",
            "Otomatis diregenerasi."
        ),
        "GrShaderCache": (
            "Cache rendering Skia hilang. Tidak ada dampak terasa.",
            "Otomatis diregenerasi."
        ),
        "GraphiteDawnCache": (
            "Cache rendering Graphite hilang. Tidak ada dampak terasa.",
            "Otomatis diregenerasi."
        ),
        "Logs": (
            "TIDAK ADA DAMPAK. Hanya kehilangan catatan log lama.",
            "Log baru dibuat otomatis oleh aplikasi."
        ),
        "logs": (
            "TIDAK ADA DAMPAK. Hanya kehilangan catatan log lama.",
            "Log baru dibuat otomatis oleh aplikasi."
        ),
        "Service Worker": (
            "Service worker cache dari website PWA hilang. "
            "Website offline mungkin tidak bisa diakses sementara.",
            "Otomatis diregenerasi saat mengunjungi website."
        ),
        "Prefetch": (
            "Windows perlu belajar ulang pola penggunaan aplikasi. "
            "Loading aplikasi mungkin sedikit lambat 1-2 hari.",
            "Windows otomatis membangun ulang data prefetch."
        ),
        "Download": (
            "File update Windows yang sudah ter-download akan hilang. "
            "Update akan di-download ulang jika diperlukan.",
            "Windows Update akan mendownload ulang file yang dibutuhkan."
        ),
        "Windows": (
            "⛔ SISTEM OPERASI RUSAK TOTAL! Laptop tidak bisa menyala!",
            "Perlu install ulang Windows dari USB/DVD. JANGAN HAPUS!"
        ),
        "System32": (
            "⛔ SISTEM OPERASI RUSAK TOTAL! Tidak bisa boot!",
            "Install ulang Windows. JANGAN PERNAH HAPUS!"
        ),
        "Documents": (
            "⛔ SEMUA DOKUMEN PRIBADI HILANG PERMANEN!",
            "Tidak bisa dipulihkan kecuali ada backup. JANGAN HAPUS!"
        ),
        "User Data": (
            "⛔ SEMUA data browser hilang: bookmark, password, history, extension.",
            "Jika ada sync (Google/Microsoft), sebagian bisa dipulihkan dengan login ulang."
        ),
    }
    
    if name in specific:
        return specific[name]
    
    # ── Fallback berdasarkan kategori ──
    category_impacts = {
        "Temporary Files": (
            "Tidak ada dampak berarti. File sementara dibuat ulang otomatis.",
            "Otomatis diregenerasi oleh sistem/aplikasi."
        ),
        "Cache": (
            "Aplikasi perlu memuat ulang data. Sedikit lebih lambat sementara.",
            "Cache diregenerasi otomatis saat aplikasi digunakan."
        ),
        "Development": (
            "Output build hilang, tapi source code TETAP AMAN. Perlu build ulang.",
            "Jalankan build/install command yang sesuai di folder proyek."
        ),
        "Crash Reports": (
            "Tidak ada dampak. Hanya laporan error lama.",
            "Tidak perlu recovery."
        ),
        "Logs": (
            "Tidak ada dampak. Hanya catatan log lama.",
            "Log baru dibuat otomatis."
        ),
        "Browser Data": (
            "⚠️ Bisa kehilangan data browsing (bookmark, password, history, cookie).",
            "Login ulang ke website. Data dari sync akan kembali."
        ),
        "System": (
            "⛔ BISA MERUSAK SISTEM! Windows mungkin tidak bisa boot.",
            "Perlu install ulang Windows. JANGAN HAPUS!"
        ),
        "Application Data": (
            "Aplikasi mungkin kehilangan pengaturan dan perlu setup ulang.",
            "Reinstall atau reconfigure aplikasi yang terpengaruh."
        ),
        "Windows Update": (
            "Tidak bisa rollback ke versi Windows sebelumnya.",
            "Windows Update akan download ulang jika dibutuhkan."
        ),
        "Performance Cache": (
            "Sistem mungkin sedikit lambat sementara.",
            "Cache diregenerasi otomatis."
        ),
        "Gaming": (
            "⚠️ Game dan save data bisa hilang!",
            "Download ulang game dari platform (Steam, Epic, dll)."
        ),
        "Cloud Storage": (
            "⛔ File cloud bisa hilang jika sinkronisasi rusak!",
            "File masih ada di cloud, tapi JANGAN hapus folder ini."
        ),
    }
    
    return category_impacts.get(cat, (
        "Dampak tidak diketahui. Periksa isi folder manual sebelum menghapus.",
        "Backup folder ini dulu jika tidak yakin."
    ))

