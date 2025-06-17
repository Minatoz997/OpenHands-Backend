# Changelog: Auto Deploy ke Hugging Face Space

## Perubahan yang Dibuat

### 1. File GitHub Actions Workflow (`.github/workflows/deploy.yaml`)

**Sebelum:**
- Workflow yang tidak lengkap dan bermasalah
- Hanya menyalin folder `/openhands` saja
- Menggunakan `rsync` ke direktori yang tidak ada (`./repo/`)
- Menggunakan action yang deprecated

**Sesudah:**
- Workflow yang lengkap dan robust
- Menyalin semua file yang diperlukan untuk HF Spaces:
  - Folder `openhands/` (kode backend)
  - `app_hf.py` → `app.py` (entry point)
  - `requirements.txt` (dependencies)
  - `Dockerfile_HF` → `Dockerfile` (container config)
  - `README_HF.md` → `README.md` (dengan metadata Space)
  - `.env.hf` → `.env` (environment template)
- Menggunakan `huggingface_hub` library untuk upload yang lebih reliable
- Fallback ke git push jika HF API gagal
- Proper error handling dan logging

### 2. File Konfigurasi Baru

**`space_config.yml`** - Konfigurasi metadata untuk HF Space:
```yaml
title: OpenHands Backend API
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
app_port: 7860
```

**`HUGGINGFACE_AUTO_DEPLOY.md`** - Dokumentasi lengkap setup dan troubleshooting

**`test_hf_deploy.py`** - Script untuk testing deployment secara lokal

### 3. Perbaikan Workflow

**Trigger:**
- Push ke branch `main`
- Manual trigger via GitHub Actions

**Steps:**
1. **Checkout** - Download kode dengan full history
2. **Setup Python** - Install Python 3.12 dan huggingface_hub
3. **Prepare Files** - Salin dan setup file untuk HF Space
4. **Upload** - Upload ke HF Space dengan proper error handling

**Features:**
- ✅ Automatic file preparation
- ✅ Proper README.md dengan metadata Space
- ✅ Environment variables template
- ✅ Robust error handling
- ✅ Fallback mechanism
- ✅ Detailed logging

## Setup yang Diperlukan

### 1. GitHub Secrets
Tambahkan `HF_TOKEN` di repository settings:
- Buat token di: https://huggingface.co/settings/tokens
- Role: `write`

### 2. Hugging Face Space
Pastikan Space `Minatoz997/Backend66` sudah dibuat

### 3. Environment Variables di HF Space
Set di Space settings:
```bash
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
```

## Testing

Jalankan script test untuk memverifikasi setup:
```bash
python test_hf_deploy.py
```

## Monitoring

Monitor deployment di:
- GitHub Actions tab → "Deploy to Hugging Face Space"
- Hugging Face Space logs

## Hasil

Sekarang setiap kali ada push ke branch `main`, file backend akan otomatis ter-sync ke Hugging Face Space dengan:
- ✅ Semua file yang diperlukan
- ✅ Konfigurasi yang benar
- ✅ Error handling yang robust
- ✅ Logging yang detail