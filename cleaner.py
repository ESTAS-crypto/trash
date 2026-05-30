# -*- coding: utf-8 -*-
"""
Cleaner: Modul untuk menghapus folder dengan aman.
Mendukung dry-run, logging, konfirmasi, dan progress callback.
Folder yang dilindungi (seperti .gemini/Antigravity) otomatis ditolak.
"""

import os
import sys
import stat
import shutil
import logging
import datetime
from pathlib import Path
from typing import List, Optional, Callable


# ═══════════════════════════════════════════════════════════════
# LONG PATH SUPPORT (Fix WinError 145 / path > 260 chars)
# ═══════════════════════════════════════════════════════════════
def _long_path(path: str) -> str:
    """Convert path ke format long path Windows (\\\\?\\) agar bisa hapus path > 260 karakter."""
    if sys.platform == "win32" and not path.startswith("\\\\?\\"):
        abs_path = os.path.abspath(path)
        return "\\\\?\\" + abs_path
    return path


def _force_remove_readonly(func, path, exc_info):
    """Error handler untuk shutil.rmtree: hapus readonly flag lalu coba lagi."""
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except (OSError, PermissionError):
        pass  # Skip jika masih gagal


def _rmtree_safe(path: str, logger: logging.Logger):
    """
    Hapus folder tree dengan dukungan long path Windows.
    Mencoba beberapa strategi jika gagal.
    """
    errors_count = 0
    
    # Strategi 1: Normal rmtree dengan error handler
    try:
        shutil.rmtree(path, onerror=_force_remove_readonly)
        return 0
    except Exception:
        pass
    
    # Strategi 2: Long path rmtree
    try:
        long_p = _long_path(path)
        shutil.rmtree(long_p, onerror=_force_remove_readonly)
        return 0
    except Exception:
        pass
    
    # Strategi 3: Manual recursive delete (paling aman)
    try:
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                try:
                    fpath = _long_path(os.path.join(root, name))
                    os.chmod(fpath, stat.S_IWRITE)
                    os.unlink(fpath)
                except (OSError, PermissionError):
                    errors_count += 1
            for name in dirs:
                try:
                    dpath = _long_path(os.path.join(root, name))
                    os.rmdir(dpath)
                except (OSError, PermissionError):
                    errors_count += 1
        # Try removing the root
        try:
            os.rmdir(_long_path(path))
        except (OSError, PermissionError):
            errors_count += 1
    except Exception as e:
        logger.debug(f"Manual delete fallback error: {e}")
        errors_count += 1
    
    return errors_count


# Setup logging
def setup_logger() -> logging.Logger:
    """Setup logger untuk mencatat semua operasi penghapusan."""
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"cleanup_{timestamp}.log")
    
    logger = logging.getLogger("FolderCleaner")
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers to prevent duplicate logs
    logger.handlers.clear()
    
    # File handler
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(fh)
    
    # Console handler (minimal - hanya error fatal)
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)
    ch.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(ch)
    
    logger.info(f"=== Sesi Pembersihan Dimulai: {timestamp} ===")
    logger.info(f"Log file: {log_file}")
    
    return logger


def _check_protected(path: str, logger: logging.Logger) -> bool:
    """Cek apakah folder dilindungi. Return True jika dilindungi."""
    try:
        from scanner import is_protected_path
        if is_protected_path(path):
            logger.warning(f"DILINDUNGI - Menolak menghapus: {path}")
            return True
    except ImportError:
        pass
    return False


def delete_folder_contents(path: str, logger: logging.Logger,
                           on_progress: Optional[Callable] = None) -> dict:
    """
    Menghapus ISI folder (bukan folder itu sendiri).
    on_progress(deleted, total, current_file) dipanggil untuk setiap file.
    """
    stats = {
        "deleted_files": 0,
        "deleted_folders": 0,
        "failed_files": 0,
        "failed_folders": 0,
        "freed_bytes": 0,
        "errors": []
    }
    
    if not os.path.exists(path):
        logger.warning(f"Path tidak ditemukan: {path}")
        return stats
    
    if _check_protected(path, logger):
        stats["errors"].append(f"🛡️ DILINDUNGI: {path} tidak boleh dihapus!")
        return stats
    
    logger.info(f"Mulai menghapus isi: {path}")
    
    # Hitung total items dulu untuk progress
    total_items = 0
    try:
        total_items = len(os.listdir(path))
    except (OSError, PermissionError):
        pass

    access_denied_count = 0
    processed = 0
    
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            processed += 1
            
            if _check_protected(item_path, logger):
                continue
            
            if on_progress and total_items > 0:
                on_progress(processed, total_items, item)
            
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    size = os.path.getsize(item_path)
                    try:
                        os.unlink(_long_path(item_path))
                    except PermissionError:
                        os.chmod(_long_path(item_path), stat.S_IWRITE)
                        os.unlink(_long_path(item_path))
                    stats["deleted_files"] += 1
                    stats["freed_bytes"] += size
                    logger.debug(f"  Hapus file: {item_path}")
                elif os.path.isdir(item_path):
                    size = sum(
                        os.path.getsize(os.path.join(dp, f))
                        for dp, dn, fns in os.walk(item_path)
                        for f in fns
                        if os.path.exists(os.path.join(dp, f))
                    )
                    errs = _rmtree_safe(item_path, logger)
                    stats["deleted_folders"] += 1
                    stats["freed_bytes"] += size
                    if errs > 0:
                        access_denied_count += errs
                    logger.debug(f"  Hapus folder: {item_path}")
            except PermissionError:
                access_denied_count += 1
                if os.path.isfile(item_path):
                    stats["failed_files"] += 1
                else:
                    stats["failed_folders"] += 1
                logger.debug(f"  Akses ditolak (skip): {item_path}")
            except Exception as e:
                if os.path.isfile(item_path):
                    stats["failed_files"] += 1
                else:
                    stats["failed_folders"] += 1
                logger.error(f"  Error: {item_path} -> {str(e)}")
    except PermissionError:
        stats["errors"].append(f"⚠️ Tidak bisa mengakses folder: {path}")
    except Exception as e:
        stats["errors"].append(f"❌ Error: {path} -> {str(e)}")
    
    if access_denied_count > 0:
        summary = (f"  ⚠️ {access_denied_count} file/folder dilewati "
                   f"(akses ditolak - sedang dipakai)")
        stats["errors"].append(summary)
        logger.info(summary)
    
    logger.info(
        f"Selesai: {path} | "
        f"File: {stats['deleted_files']} | Folder: {stats['deleted_folders']} | "
        f"Gagal: {stats['failed_files'] + stats['failed_folders']} | "
        f"Freed: {stats['freed_bytes']} bytes"
    )
    
    return stats


def delete_entire_folder(path: str, logger: logging.Logger,
                         on_progress: Optional[Callable] = None) -> dict:
    """
    Menghapus folder beserta isinya. Menggunakan delete_folder_contents
    untuk progress real-time per-file, lalu hapus folder root.
    """
    stats = {
        "deleted_files": 0,
        "deleted_folders": 1,
        "failed_files": 0,
        "failed_folders": 0,
        "freed_bytes": 0,
        "errors": []
    }
    
    if not os.path.exists(path):
        logger.warning(f"Path tidak ditemukan: {path}")
        return stats
    
    if _check_protected(path, logger):
        stats["errors"].append(f"🛡️ DILINDUNGI: {path} tidak boleh dihapus!")
        stats["deleted_folders"] = 0
        return stats
    
    logger.info(f"Menghapus seluruh folder: {path}")
    
    # Gunakan delete_folder_contents agar progress real-time
    content_stats = delete_folder_contents(path, logger, on_progress)
    stats["deleted_files"] = content_stats["deleted_files"]
    stats["freed_bytes"] = content_stats["freed_bytes"]
    stats["failed_files"] = content_stats["failed_files"]
    stats["failed_folders"] = content_stats["failed_folders"]
    stats["errors"] = content_stats["errors"]
    
    # Coba hapus folder root (sekarang sudah kosong)
    try:
        os.rmdir(_long_path(path))
        logger.info(f"Folder root dihapus: {path}")
    except OSError:
        # Folder mungkin masih ada file yang gagal dihapus, itu OK
        logger.debug(f"Folder root tidak bisa dihapus (masih ada isi): {path}")
    
    return stats



