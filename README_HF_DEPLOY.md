# 🚀 Cara Deploy OpenHands ke Hugging Face Spaces

## 📋 Langkah-langkah Deploy

### 1. Persiapan File
Pastikan file-file ini ada di repository Anda:

**File Utama:**
- `Dockerfile_HF_Fixed` → rename menjadi `Dockerfile`
- `app_hf_fixed.py` → rename menjadi `app.py` 
- `requirements_hf.txt` → rename menjadi `requirements.txt`
- `space_config.yml` (sudah diperbaiki)
- Folder `openhands/` (kode aplikasi)

### 2. Buat Hugging Face Space
1. Buka [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space name**: `openhands-backend` (atau nama lain)
3. **SDK**: Docker
4. **Visibility**: Public
5. **Hardware**: CPU basic (gratis)

### 3. Upload File ke Space
Upload semua file yang diperlukan ke Space Anda.

### 4. Set Environment Variables
Di Space Settings → Environment Variables, tambahkan:

```bash
# WAJIB - API Key OpenRouter
LLM_API_KEY=your_openrouter_api_key_here

# OPSIONAL - Model Configuration
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
```

### 5. Deploy!
Hugging Face akan otomatis build dan deploy aplikasi Anda.

## 🔧 Perbaikan yang Dilakukan

### Masalah yang Diperbaiki:
1. **Port Conflict**: Port diseragamkan ke 7860
2. **Dependencies**: Dihapus dependency yang bermasalah
3. **File Permissions**: Menggunakan memory storage
4. **Environment**: Konfigurasi yang lebih sederhana

### File yang Diperbaiki:
- `space_config.yml`: Port 8000 → 7860
- `requirements_hf.txt`: Dependencies yang lebih minimal
- `Dockerfile_HF_Fixed`: Optimized untuk HF Spaces
- `app_hf_fixed.py`: Konfigurasi yang lebih stabil

## 🧪 Testing Deployment

Setelah deploy berhasil, test endpoint ini:

```bash
# Health check
GET https://your-space-name.hf.space/health

# API documentation
GET https://your-space-name.hf.space/docs

# Configuration
GET https://your-space-name.hf.space/api/options/config
```

## 🔑 Mendapatkan OpenRouter API Key

1. Daftar di [openrouter.ai](https://openrouter.ai)
2. Buat API Key di dashboard
3. Masukkan ke Environment Variables HF Space

## 🐛 Troubleshooting

### Jika Build Gagal:
1. Cek logs di Space → Settings → Logs
2. Pastikan semua file sudah diupload
3. Pastikan `LLM_API_KEY` sudah diset

### Jika Runtime Error:
1. Cek `/health` endpoint
2. Lihat logs untuk error message
3. Pastikan dependencies tidak conflict

## 📞 Bantuan

Jika masih ada masalah, share:
1. Link ke HF Space Anda
2. Screenshot error logs
3. Environment variables yang diset (tanpa API key)

Semoga berhasil! 🎉