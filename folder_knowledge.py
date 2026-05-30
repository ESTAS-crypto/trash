# -*- coding: utf-8 -*-
"""
Knowledge Base: Database penjelasan folder-folder di Windows.
Setiap entry berisi:
  - description (ID): Penjelasan detail dalam Bahasa Indonesia
  - risk_level: "safe" | "caution" | "danger"
  - category: Kategori folder
  - can_delete: True/False apakah aman dihapus
  - note: Catatan tambahan
"""

# Risk levels:
# "safe"    = Aman dihapus, tidak ada dampak berarti
# "caution" = Bisa dihapus tapi ada konsekuensi kecil (login ulang, download ulang, dll)
# "danger"  = Jangan hapus kecuali benar-benar yakin

FOLDER_KNOWLEDGE = {
    # ═══════════════════════════════════════════════════════════
    # TEMP & CACHE (Umumnya aman dihapus)
    # ═══════════════════════════════════════════════════════════
    "Temp": {
        "description": (
            "📁 Folder TEMP (Temporary Files)\n"
            "   Folder ini menyimpan file-file sementara yang dibuat oleh Windows dan aplikasi.\n"
            "   Contoh: file installer sementara, file download yang belum selesai,\n"
            "   cache kompilasi, log sementara, dsb.\n"
            "   File di sini seharusnya sudah tidak dibutuhkan setelah proses selesai."
        ),
        "risk_level": "safe",
        "category": "Temporary Files",
        "can_delete": True,
        "note": "Tutup semua aplikasi dulu sebelum menghapus agar tidak ada file yang sedang dipakai."
    },
    "tmp": {
        "description": (
            "📁 Folder TMP\n"
            "   Sama seperti Temp, ini adalah folder file sementara alternatif.\n"
            "   Beberapa aplikasi menggunakan 'tmp' sebagai lokasi penyimpanan sementara."
        ),
        "risk_level": "safe",
        "category": "Temporary Files",
        "can_delete": True,
        "note": "Aman dihapus, file sementara akan dibuat ulang jika dibutuhkan."
    },

    # ═══════════════════════════════════════════════════════════
    # BROWSER CACHE
    # ═══════════════════════════════════════════════════════════
    "Cache": {
        "description": (
            "📁 Folder CACHE\n"
            "   Menyimpan data cache (data tersimpan sementara) dari aplikasi atau browser.\n"
            "   Cache mempercepat loading karena tidak perlu download ulang dari internet.\n"
            "   Tapi cache bisa membesar seiring waktu dan memakan ruang disk."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Website/aplikasi mungkin sedikit lebih lambat pertama kali setelah cache dihapus."
    },
    "CachedData": {
        "description": (
            "📁 Folder CachedData\n"
            "   Data cache dari aplikasi Electron (VS Code, Discord, Slack, dll).\n"
            "   Menyimpan file JavaScript & resource yang sudah dikompilasi untuk loading cepat."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Aplikasi akan membuat ulang cache ini saat dibuka."
    },
    "CachedExtensions": {
        "description": (
            "📁 Folder CachedExtensions\n"
            "   Cache dari extension/plugin aplikasi (biasanya VS Code).\n"
            "   Menyimpan versi extension yang sudah di-download."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Extension akan di-download ulang jika diperlukan."
    },
    "CachedExtensionVSIXs": {
        "description": (
            "📁 Folder CachedExtensionVSIXs\n"
            "   File instalasi extension VS Code (.vsix) yang sudah di-cache.\n"
            "   Setelah extension terinstall, file VSIX ini tidak lagi dibutuhkan."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Aman dihapus, extension sudah terinstall."
    },
    "GPUCache": {
        "description": (
            "📁 Folder GPUCache\n"
            "   Cache untuk rendering GPU dari browser Chromium (Chrome, Edge, Brave).\n"
            "   Menyimpan shader yang sudah dikompilasi untuk mempercepat rendering halaman web."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Akan dibuat ulang otomatis oleh browser."
    },
    "ShaderCache": {
        "description": (
            "📁 Folder ShaderCache\n"
            "   Cache shader grafis untuk game atau aplikasi GPU.\n"
            "   Mempercepat loading game karena shader tidak perlu dikompilasi ulang."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Game mungkin agak lambat pertama kali setelah dihapus (kompilasi shader ulang)."
    },
    "Code Cache": {
        "description": (
            "📁 Folder Code Cache\n"
            "   Cache kode JavaScript yang sudah dikompilasi oleh browser.\n"
            "   Mempercepat eksekusi website yang sering dikunjungi."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Browser akan membuat ulang cache ini."
    },
    "DawnCache": {
        "description": (
            "📁 Folder DawnCache\n"
            "   Cache dari Dawn WebGPU implementation di Chrome/Edge.\n"
            "   Terkait dengan rendering grafis berbasis WebGPU."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Akan diregenerasi otomatis."
    },
    "GrShaderCache": {
        "description": (
            "📁 Folder GrShaderCache\n"
            "   Cache shader Skia graphics library yang digunakan browser Chromium.\n"
            "   Untuk akselerasi rendering 2D."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Aman dihapus, akan dibuat ulang."
    },
    "GraphiteDawnCache": {
        "description": (
            "📁 Folder GraphiteDawnCache\n"
            "   Cache baru dari rendering engine Graphite + Dawn di Chrome terbaru.\n"
            "   Pengganti Skia untuk rendering yang lebih efisien."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Aman dihapus."
    },

    # ═══════════════════════════════════════════════════════════
    # BROWSER DATA
    # ═══════════════════════════════════════════════════════════
    "User Data": {
        "description": (
            "📁 Folder User Data (Browser)\n"
            "   Folder utama data browser (Chrome/Edge). Berisi:\n"
            "   - Bookmark, history, password tersimpan\n"
            "   - Cookie, session login\n"
            "   - Extension & pengaturan browser\n"
            "   ⚠️ JANGAN HAPUS folder ini secara keseluruhan!"
        ),
        "risk_level": "danger",
        "category": "Browser Data",
        "can_delete": False,
        "note": "Menghapus ini = kehilangan semua data browser (bookmark, password, dll)."
    },
    "Default": {
        "description": (
            "📁 Folder Default (Browser Profile)\n"
            "   Profile default browser Chromium. Berisi semua data browsing Anda:\n"
            "   bookmark, history, cookie, password, extension, dll."
        ),
        "risk_level": "danger",
        "category": "Browser Data",
        "can_delete": False,
        "note": "JANGAN hapus! Ini profil utama browser Anda."
    },
    "Cookies": {
        "description": (
            "📁 File/Folder Cookies\n"
            "   Menyimpan cookie dari website. Cookie digunakan untuk:\n"
            "   - Menyimpan status login\n"
            "   - Preferensi website\n"
            "   - Tracking & analytics"
        ),
        "risk_level": "caution",
        "category": "Browser Data",
        "can_delete": True,
        "note": "Jika dihapus, Anda harus login ulang ke semua website."
    },
    "Session Storage": {
        "description": (
            "📁 Folder Session Storage\n"
            "   Data sesi sementara dari website. Biasanya berisi data form,\n"
            "   status UI, dan state aplikasi web yang sedang dibuka."
        ),
        "risk_level": "safe",
        "category": "Browser Data",
        "can_delete": True,
        "note": "Data sesi akan hilang, website kembali ke state awal."
    },
    "Local Storage": {
        "description": (
            "📁 Folder Local Storage\n"
            "   Data yang disimpan website secara permanen di browser.\n"
            "   Contoh: preferensi tema gelap/terang, pengaturan website, dll."
        ),
        "risk_level": "caution",
        "category": "Browser Data",
        "can_delete": True,
        "note": "Pengaturan website akan reset ke default."
    },

    # ═══════════════════════════════════════════════════════════
    # WINDOWS SYSTEM
    # ═══════════════════════════════════════════════════════════
    "Windows": {
        "description": (
            "📁 Folder WINDOWS\n"
            "   ⛔ Folder sistem operasi Windows utama.\n"
            "   Berisi semua file inti Windows: kernel, driver, DLL sistem,\n"
            "   registry, font, dan komponen vital lainnya."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "JANGAN PERNAH HAPUS! Laptop tidak akan bisa menyala."
    },
    "System32": {
        "description": (
            "📁 Folder System32\n"
            "   ⛔ Folder paling penting di Windows.\n"
            "   Berisi semua executable, library (DLL), dan driver inti Windows.\n"
            "   Tanpa folder ini, Windows tidak bisa berjalan sama sekali."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "JANGAN PERNAH HAPUS! Ini jantung dari Windows."
    },
    "SysWOW64": {
        "description": (
            "📁 Folder SysWOW64\n"
            "   ⛔ Folder sistem untuk menjalankan aplikasi 32-bit di Windows 64-bit.\n"
            "   'WOW64' = 'Windows on Windows 64-bit'."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "JANGAN HAPUS! Banyak aplikasi masih butuh ini."
    },
    "WinSxS": {
        "description": (
            "📁 Folder WinSxS (Windows Side-by-Side)\n"
            "   Folder besar yang menyimpan berbagai versi komponen Windows.\n"
            "   Dibutuhkan untuk Windows Update dan kompatibilitas.\n"
            "   ⚠️ Sering terlihat sangat besar (5-15GB) tapi JANGAN hapus manual."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "Gunakan Disk Cleanup bawaan Windows jika ingin membersihkan."
    },
    "Program Files": {
        "description": (
            "📁 Folder Program Files\n"
            "   Lokasi instalasi default untuk aplikasi 64-bit.\n"
            "   Setiap subfolder = satu aplikasi yang terinstall."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "Uninstall aplikasi lewat Settings, jangan hapus folder manual."
    },
    "Program Files (x86)": {
        "description": (
            "📁 Folder Program Files (x86)\n"
            "   Lokasi instalasi default untuk aplikasi 32-bit.\n"
            "   Sama seperti Program Files tapi untuk app versi lama/32-bit."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "Uninstall aplikasi lewat Settings, jangan hapus folder manual."
    },
    "ProgramData": {
        "description": (
            "📁 Folder ProgramData\n"
            "   Data bersama untuk semua user di komputer.\n"
            "   Berisi konfigurasi aplikasi, database lokal, license info, dll."
        ),
        "risk_level": "danger",
        "category": "System",
        "can_delete": False,
        "note": "Menghapus = banyak aplikasi kehilangan pengaturan/lisensi."
    },
    "Windows.old": {
        "description": (
            "📁 Folder Windows.old\n"
            "   Backup otomatis dari instalasi Windows sebelumnya.\n"
            "   Dibuat saat upgrade Windows (misal dari Win 10 ke Win 11).\n"
            "   Bisa sangat besar (10-30 GB).\n"
            "   Setelah yakin Windows baru berjalan baik, ini bisa dihapus."
        ),
        "risk_level": "caution",
        "category": "System Backup",
        "can_delete": True,
        "note": "Jika dihapus, tidak bisa rollback ke Windows versi sebelumnya. Gunakan Disk Cleanup."
    },
    "$Recycle.Bin": {
        "description": (
            "📁 Folder $Recycle.Bin\n"
            "   Folder Recycle Bin (Tong Sampah) Windows.\n"
            "   Menyimpan file yang sudah dihapus tapi belum permanen."
        ),
        "risk_level": "safe",
        "category": "System",
        "can_delete": True,
        "note": "Sama dengan mengosongkan Recycle Bin dari desktop."
    },
    "$WINDOWS.~BT": {
        "description": (
            "📁 Folder $WINDOWS.~BT\n"
            "   File download Windows Update/Upgrade.\n"
            "   Biasanya tersisa setelah update Windows selesai."
        ),
        "risk_level": "safe",
        "category": "Windows Update",
        "can_delete": True,
        "note": "Aman dihapus jika update sudah berhasil terinstall."
    },
    "SoftwareDistribution": {
        "description": (
            "📁 Folder SoftwareDistribution\n"
            "   File download Windows Update.\n"
            "   Menyimpan file update yang sudah didownload dan log update."
        ),
        "risk_level": "caution",
        "category": "Windows Update",
        "can_delete": True,
        "note": "Stop Windows Update service dulu sebelum menghapus. File akan didownload ulang."
    },
    "Prefetch": {
        "description": (
            "📁 Folder Prefetch\n"
            "   Data prefetch Windows untuk mempercepat loading aplikasi.\n"
            "   Windows mempelajari pola penggunaan dan menyiapkan file yang sering dibuka."
        ),
        "risk_level": "safe",
        "category": "Performance Cache",
        "can_delete": True,
        "note": "Aplikasi mungkin sedikit lambat pertama kali setelah dihapus. Windows akan belajar ulang."
    },

    # ═══════════════════════════════════════════════════════════
    # USER FOLDERS
    # ═══════════════════════════════════════════════════════════
    "Downloads": {
        "description": (
            "📁 Folder Downloads\n"
            "   Folder default untuk file yang didownload dari internet.\n"
            "   Sering menumpuk dengan installer, PDF, gambar, dll yang sudah tidak dibutuhkan."
        ),
        "risk_level": "caution",
        "category": "User Data",
        "can_delete": False,
        "note": "Periksa isinya satu per satu. Mungkin ada file penting di sini."
    },
    "Desktop": {
        "description": (
            "📁 Folder Desktop\n"
            "   File dan shortcut yang ada di desktop Anda.\n"
            "   Bersihkan file yang tidak dibutuhkan untuk desktop yang rapi."
        ),
        "risk_level": "caution",
        "category": "User Data",
        "can_delete": False,
        "note": "Periksa isinya, jangan hapus folder ini secara keseluruhan."
    },
    "Documents": {
        "description": (
            "📁 Folder Documents\n"
            "   Folder dokumen pribadi Anda.\n"
            "   Berisi file Word, Excel, PDF, dan dokumen lainnya."
        ),
        "risk_level": "danger",
        "category": "User Data",
        "can_delete": False,
        "note": "JANGAN hapus! Ini berisi dokumen penting Anda."
    },

    # ═══════════════════════════════════════════════════════════
    # APPDATA - LOCAL
    # ═══════════════════════════════════════════════════════════
    "CrashDumps": {
        "description": (
            "📁 Folder CrashDumps\n"
            "   Menyimpan file crash dump ketika aplikasi crash/error.\n"
            "   File ini untuk debugging/diagnosis tapi biasanya tidak dibutuhkan user biasa."
        ),
        "risk_level": "safe",
        "category": "Crash Reports",
        "can_delete": True,
        "note": "Aman dihapus. Hanya berguna jika Anda perlu mengirim laporan bug."
    },
    "CrashReports": {
        "description": (
            "📁 Folder CrashReports\n"
            "   Laporan crash dari aplikasi. Mirip CrashDumps tapi format berbeda."
        ),
        "risk_level": "safe",
        "category": "Crash Reports",
        "can_delete": True,
        "note": "Aman dihapus."
    },
    "D3DSCache": {
        "description": (
            "📁 Folder D3DSCache\n"
            "   Cache Direct3D Shader dari Windows.\n"
            "   Mempercepat rendering grafis game dan aplikasi 3D."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Akan diregenerasi otomatis. Game mungkin sedikit lambat pertama kali."
    },
    "IconCache": {
        "description": (
            "📁 Folder/File IconCache\n"
            "   Cache ikon dari Windows Explorer.\n"
            "   Mempercepat tampilan ikon file dan folder."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Ikon mungkin terlihat aneh sementara setelah dihapus, akan normal setelah restart."
    },

    # ═══════════════════════════════════════════════════════════
    # APLIKASI POPULER
    # ═══════════════════════════════════════════════════════════
    "node_modules": {
        "description": (
            "📁 Folder node_modules\n"
            "   Folder dependensi Node.js/npm untuk proyek JavaScript.\n"
            "   Bisa SANGAT BESAR (ratusan MB bahkan GB) untuk satu proyek.\n"
            "   Bisa di-regenerate kapan saja dengan 'npm install'."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Aman dihapus! Jalankan 'npm install' di folder proyek untuk membuat ulang."
    },
    "__pycache__": {
        "description": (
            "📁 Folder __pycache__\n"
            "   Cache bytecode Python (.pyc files).\n"
            "   Python mengkompilasi source code ke bytecode untuk eksekusi lebih cepat."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Akan dibuat ulang otomatis saat Python dijalankan."
    },
    ".venv": {
        "description": (
            "📁 Folder .venv\n"
            "   Virtual environment Python.\n"
            "   Berisi instalasi Python terisolasi untuk proyek tertentu.\n"
            "   Bisa 200MB-1GB per environment."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Buat ulang dengan 'python -m venv .venv' + install requirements."
    },
    "venv": {
        "description": (
            "📁 Folder venv\n"
            "   Virtual environment Python (nama alternatif dari .venv)."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Buat ulang dengan 'python -m venv venv' + install requirements."
    },
    ".git": {
        "description": (
            "📁 Folder .git\n"
            "   Repository Git untuk version control.\n"
            "   Berisi seluruh history perubahan kode proyek."
        ),
        "risk_level": "danger",
        "category": "Development",
        "can_delete": False,
        "note": "JANGAN hapus kecuali sudah di-push ke remote (GitHub, dll)."
    },
    "dist": {
        "description": (
            "📁 Folder dist\n"
            "   Output build dari proyek (JavaScript, Python, dll).\n"
            "   Berisi file yang sudah dikompilasi/dibundel untuk distribusi."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Bisa dibuat ulang dengan menjalankan build command proyek."
    },
    "build": {
        "description": (
            "📁 Folder build\n"
            "   Output build dari proyek. Mirip dengan 'dist'.\n"
            "   Berisi hasil kompilasi yang bisa di-regenerate."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Bisa dibuat ulang dengan menjalankan build command."
    },
    ".next": {
        "description": (
            "📁 Folder .next\n"
            "   Build cache dari Next.js framework.\n"
            "   Menyimpan hasil build untuk development dan production."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Akan dibuat ulang saat menjalankan 'npm run dev' atau 'npm run build'."
    },
    ".cache": {
        "description": (
            "📁 Folder .cache\n"
            "   Cache generik dari berbagai tools development (Babel, Webpack, dll)."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Akan diregenerasi saat tool dijalankan."
    },
    "coverage": {
        "description": (
            "📁 Folder coverage\n"
            "   Hasil laporan code coverage dari unit testing.\n"
            "   Berisi report HTML dan data coverage."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Dibuat ulang saat menjalankan test dengan coverage."
    },

    # ═══════════════════════════════════════════════════════════
    # APLIKASI SPESIFIK
    # ═══════════════════════════════════════════════════════════
    "Discord": {
        "description": (
            "📁 Folder Discord\n"
            "   Data aplikasi Discord (chat & voice app).\n"
            "   Berisi cache, log, dan data aplikasi Discord."
        ),
        "risk_level": "caution",
        "category": "Application Data",
        "can_delete": False,
        "note": "Sub-folder Cache di dalamnya bisa dihapus untuk menghemat ruang."
    },
    "Spotify": {
        "description": (
            "📁 Folder Spotify\n"
            "   Data aplikasi Spotify.\n"
            "   Termasuk cache musik yang di-download untuk offline listening."
        ),
        "risk_level": "caution",
        "category": "Application Data",
        "can_delete": False,
        "note": "Sub-folder 'Storage' bisa sangat besar jika ada download offline."
    },
    "Steam": {
        "description": (
            "📁 Folder Steam\n"
            "   Data platform gaming Steam.\n"
            "   Berisi game yang terinstall, save game, dan data Steam."
        ),
        "risk_level": "danger",
        "category": "Gaming",
        "can_delete": False,
        "note": "Berisi game dan save data. Jangan hapus kecuali ingin uninstall Steam."
    },
    "EpicGamesLauncher": {
        "description": (
            "📁 Folder EpicGamesLauncher\n"
            "   Data Epic Games Launcher.\n"
            "   Cache dan data game Epic Games."
        ),
        "risk_level": "caution",
        "category": "Gaming",
        "can_delete": False,
        "note": "Sub-folder 'Saved' berisi cache yang bisa dihapus."
    },

    # ═══════════════════════════════════════════════════════════
    # LOG FILES
    # ═══════════════════════════════════════════════════════════
    "Logs": {
        "description": (
            "📁 Folder Logs\n"
            "   File log (catatan aktivitas) dari aplikasi.\n"
            "   Berguna untuk debugging tapi biasanya tidak dibutuhkan user biasa."
        ),
        "risk_level": "safe",
        "category": "Logs",
        "can_delete": True,
        "note": "Aman dihapus. Aplikasi akan membuat file log baru."
    },
    "logs": {
        "description": (
            "📁 Folder logs\n"
            "   File log aplikasi (versi huruf kecil).\n"
            "   Sama fungsinya dengan folder 'Logs'."
        ),
        "risk_level": "safe",
        "category": "Logs",
        "can_delete": True,
        "note": "Aman dihapus."
    },

    # ═══════════════════════════════════════════════════════════
    # MICROSOFT / OFFICE
    # ═══════════════════════════════════════════════════════════
    "Microsoft": {
        "description": (
            "📁 Folder Microsoft\n"
            "   Data dari produk-produk Microsoft (Office, Edge, Teams, dll).\n"
            "   Berisi pengaturan, cache, dan data aplikasi Microsoft."
        ),
        "risk_level": "danger",
        "category": "Application Data",
        "can_delete": False,
        "note": "JANGAN hapus keseluruhan. Lihat sub-folder untuk cache yang bisa dibersihkan."
    },
    "OneDrive": {
        "description": (
            "📁 Folder OneDrive\n"
            "   Folder sinkronisasi cloud Microsoft OneDrive.\n"
            "   File di sini tersinkron dengan cloud OneDrive Anda."
        ),
        "risk_level": "danger",
        "category": "Cloud Storage",
        "can_delete": False,
        "note": "JANGAN hapus! Ini berisi file cloud Anda."
    },

    # ═══════════════════════════════════════════════════════════
    # PACKAGE MANAGERS
    # ═══════════════════════════════════════════════════════════
    ".npm": {
        "description": (
            "📁 Folder .npm\n"
            "   Cache global npm (Node Package Manager).\n"
            "   Menyimpan package yang sudah di-download agar tidak perlu download ulang."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Jalankan 'npm cache clean --force' untuk membersihkan secara resmi."
    },
    ".yarn": {
        "description": (
            "📁 Folder .yarn\n"
            "   Cache global Yarn package manager.\n"
            "   Sama seperti .npm tapi untuk Yarn."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Jalankan 'yarn cache clean' untuk membersihkan."
    },
    "pip": {
        "description": (
            "📁 Folder pip\n"
            "   Cache pip (Python package manager).\n"
            "   Menyimpan package Python yang sudah di-download."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Jalankan 'pip cache purge' untuk membersihkan secara resmi."
    },
    ".nuget": {
        "description": (
            "📁 Folder .nuget\n"
            "   Cache NuGet (.NET package manager).\n"
            "   Menyimpan package .NET yang sudah di-download."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Package akan di-download ulang saat build proyek .NET."
    },
    ".gradle": {
        "description": (
            "📁 Folder .gradle\n"
            "   Cache Gradle (build tool Java/Android).\n"
            "   Menyimpan dependensi dan build cache Android/Java."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Bisa sangat besar! Akan dibuat ulang saat build proyek."
    },
    ".m2": {
        "description": (
            "📁 Folder .m2\n"
            "   Cache Maven (Java dependency manager).\n"
            "   Menyimpan library Java yang sudah di-download."
        ),
        "risk_level": "safe",
        "category": "Development",
        "can_delete": True,
        "note": "Library akan di-download ulang saat build proyek Java."
    },

    # ═══════════════════════════════════════════════════════════
    # THUMBNAILS & MEDIA
    # ═══════════════════════════════════════════════════════════
    "Thumbnails": {
        "description": (
            "📁 Folder Thumbnails\n"
            "   Cache gambar thumbnail (gambar kecil preview) dari foto dan video.\n"
            "   Mempercepat tampilan preview di File Explorer."
        ),
        "risk_level": "safe",
        "category": "Cache",
        "can_delete": True,
        "note": "Aman dihapus. Windows akan membuat thumbnail baru saat dibutuhkan."
    },

    # ═══════════════════════════════════════════════════════════
    # RECENTS & HISTORY
    # ═══════════════════════════════════════════════════════════
    "Recent": {
        "description": (
            "📁 Folder Recent\n"
            "   Shortcut ke file yang baru-baru ini dibuka.\n"
            "   Ini hanya shortcut (.lnk), bukan file aslinya."
        ),
        "risk_level": "safe",
        "category": "History",
        "can_delete": True,
        "note": "Hanya menghapus daftar 'Recent Files', file asli tetap aman."
    },
}

# Patterns untuk deteksi otomatis
AUTO_DETECT_PATTERNS = {
    # Pattern name -> folder names to match (case-insensitive)
    "temp_folders": ["temp", "tmp", ".tmp", "~temp"],
    "cache_folders": ["cache", "caches", "cached", "cacheddata", "gpucache", 
                      "shadercache", "d3dscache", "code cache", "dawncache",
                      "grshadercache", "graphitedawncache", "cachedextensions",
                      "cachedextensionvsixs"],
    "log_folders": ["logs", "log", "logging"],
    "crash_folders": ["crashdumps", "crashreports", "crash reports", "crash_reports"],
    "build_folders": ["node_modules", "__pycache__", "dist", "build", ".next", 
                      ".cache", "coverage", ".output", ".nuxt", ".turbo",
                      ".parcel-cache", "out"],
    "venv_folders": [".venv", "venv", "env", ".env", "virtualenv"],
    "thumbnail_folders": ["thumbnails", "thumb", "thumbs"],
}


def get_folder_info(folder_name: str) -> dict:
    """
    Mendapatkan informasi tentang folder berdasarkan namanya.
    Mengembalikan info dari knowledge base atau generic info jika tidak dikenal.
    """
    # Exact match
    if folder_name in FOLDER_KNOWLEDGE:
        return FOLDER_KNOWLEDGE[folder_name]
    
    # Case-insensitive match
    for key, value in FOLDER_KNOWLEDGE.items():
        if key.lower() == folder_name.lower():
            return value
    
    # Pattern matching
    folder_lower = folder_name.lower()
    for pattern_category, patterns in AUTO_DETECT_PATTERNS.items():
        if folder_lower in [p.lower() for p in patterns]:
            if pattern_category == "temp_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   File sementara (temporary). Aman dihapus.",
                    "risk_level": "safe",
                    "category": "Temporary Files",
                    "can_delete": True,
                    "note": "File sementara, aman dihapus."
                }
            elif pattern_category == "cache_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   Cache data. Mempercepat loading tapi bisa dihapus.",
                    "risk_level": "safe",
                    "category": "Cache",
                    "can_delete": True,
                    "note": "Cache akan diregenerasi otomatis."
                }
            elif pattern_category == "log_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   File log/catatan aktivitas aplikasi.",
                    "risk_level": "safe",
                    "category": "Logs",
                    "can_delete": True,
                    "note": "Aman dihapus, log baru akan dibuat."
                }
            elif pattern_category == "crash_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   Laporan crash/error dari aplikasi.",
                    "risk_level": "safe",
                    "category": "Crash Reports",
                    "can_delete": True,
                    "note": "Aman dihapus kecuali Anda perlu mengirim bug report."
                }
            elif pattern_category == "build_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   Output build/cache development. Bisa di-regenerate.",
                    "risk_level": "safe",
                    "category": "Development",
                    "can_delete": True,
                    "note": "Jalankan build command untuk membuat ulang."
                }
            elif pattern_category == "venv_folders":
                return {
                    "description": f"📁 Folder {folder_name}\n   Virtual environment Python.",
                    "risk_level": "safe",
                    "category": "Development",
                    "can_delete": True,
                    "note": "Buat ulang dengan 'python -m venv' + install requirements."
                }
    
    # Unknown folder
    return {
        "description": f"📁 Folder {folder_name}\n   ❓ Folder tidak dikenal dalam database.",
        "risk_level": "caution",
        "category": "Unknown",
        "can_delete": None,  # Unknown
        "note": "Periksa isi folder ini secara manual sebelum menghapus."
    }
