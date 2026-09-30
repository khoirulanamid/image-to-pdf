# 🖼️ Image to PDF Studio (Lossless & Client-Side)

> **High-precision client-side image editor & lossless PDF compiler.**  
> 100% diproses di browser pengunjung via CPU/RAM lokal — **Zero server uploads & Zero data tracking.**

🔗 **Live Web App:** [**https://khoirulanamid.github.io/image-to-pdf/**](https://khoirulanamid.github.io/image-to-pdf/)  
*(Bisa langsung digunakan di browser laptop, HP, atau tablet tanpa install apapun)*

---

## ⚡ Fitur Utama

- **100% Client-Side Privacy**: Seluruh parsing gambar, rendering canvas, dan kompilasi PDF berjalan langsung di browser pengguna menggunakan `pdf-lib` dan HTML5 Canvas API. File gambar tidak pernah dikirim ke server manapun.
- **Lossless Quality Passthrough**: Menggunakan direct stream passthrough untuk JPEG/PNG tanpa re-encoding destruktif yang merusak DPI gambar asli.
- **Interactive In-Browser Image Editor**:
  - ✂️ **Crop**: Pemotongan rasio fleksibel (Cropper.js engine).
  - 💧 **Pixelate Blur**: Sensor teks atau wajah secara instan.
  - ⬛ **Redact Box**: Blok hitam permanen untuk data rahasia/identitas.
  - 🔄 **Rotate 90° & Undo**: Putar dan batalkan aksi dengan riwayat state.
- **Batch Rotate All**: Putar seluruh gambar yang di-upload sekaligus dengan 1 klik.
- **Clipboard Paste Support (`Ctrl + V`)**: Screenshot langsung dari OS (`Win + Shift + S` / `Cmd + Shift + 4`) dan tekan `Ctrl + V` di browser tanpa perlu simpan file.
- **Multiple Compression Presets**:
  - `Lossless`: 100% Original (arsip/cetak).
  - `Web High (85%)`: Kualitas tajam ukuran efisien.
  - `Compact Doc (70%)`: Target portal dokumen (CPNS, beasiswa, lamaran kerja).
  - `Maximum Compress (50%)`: File PDF super ringkas.
- **Linear-Grade Dark UI**: Didesain dengan standar *Operate Surface*, font Inter (fitur OpenType `cv01`, `ss03`), micro-contrast tinggi, dan bebas elemen AI-slop.
- **Touch & Mobile Friendly**: Dilengkapi tombol geser urutan `‹` dan `›` di samping native drag-and-drop.
- **Standalone CLI Tool**: Disertakan script Python standalone (`cli.py`) untuk penggunaan terminal atau integrasi pipeline headless.

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Context | Aksi |
|---|---|---|
| `Ctrl + V` | Workspace | Paste gambar dari clipboard |
| `Ctrl + Enter` | Workspace | Langsung compile ke PDF |
| `C` | Modal Editor | Aktifkan Mode Crop |
| `B` | Modal Editor | Aktifkan Mode Blur / Sensor Teks |
| `R` | Modal Editor | Putar Gambar 90° |
| `Ctrl + Z` | Modal Editor | Undo aksi |
| `Enter` | Modal Editor | Simpan perubahan (Commit) |
| `Esc` | Modal Editor | Tutup / Batal |

---

## 🚀 Penggunaan Web App

Cukup buka `index.html` langsung di browser apapun (Chrome, Firefox, Safari, Edge) tanpa perlu build tools atau setup server:

```bash
# Atau jalankan local static server
python3 -m http.server 8080
```

Buka `http://localhost:8080`.

---

## 🛠️ Penggunaan Python CLI

```bash
# Install dependency
pip install img2pdf pillow

# Konversi gambar ke PDF tanpa loss kualitas
python3 cli.py input1.jpg input2.png -o output.pdf --page a4 --margin 20
```

---

## 📄 Lisensi

Non-Commercial (CC BY-NC 4.0). Bebas digunakan, dimodifikasi, dan disebarkan untuk keperluan pribadi, riset, dan edukasi non-komersial. Dilarang diperjualbelikan.
