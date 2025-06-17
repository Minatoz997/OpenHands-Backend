# Auto Deploy ke Hugging Face Space

Dokumentasi ini menjelaskan cara setup auto-deploy dari GitHub repository ke Hugging Face Space.

## Setup yang Diperlukan

### 1. GitHub Secrets
Tambahkan secret berikut di GitHub repository settings:

- `HF_TOKEN`: Token akses Hugging Face Anda
  - Buat di: https://huggingface.co/settings/tokens
  - Pilih role: `write` untuk bisa upload ke Space

### 2. Hugging Face Space
Pastikan Space sudah dibuat dengan nama: `Minatoz997/Backend66`

Jika ingin mengubah nama Space, edit file `.github/workflows/deploy.yaml` pada line 85:
```yaml
repo_id = "USERNAME/SPACE_NAME"
```

### 3. File yang Akan Di-sync

Workflow akan menyalin file-file berikut ke Hugging Face Space:

- **Folder `openhands/`**: Seluruh kode backend
- **`app_hf.py`**: Entry point untuk HF Spaces (akan dicopy sebagai `app.py`)
- **`requirements.txt`**: Dependencies Python
- **`Dockerfile_HF`**: Dockerfile khusus HF Spaces (akan dicopy sebagai `Dockerfile`)
- **`README_HF.md`**: Dokumentasi (akan dicopy sebagai `README.md` dengan metadata Space)
- **`.env.hf`**: Template environment variables (opsional)

## Cara Kerja Auto Deploy

### Trigger
Auto deploy akan berjalan ketika:
1. Ada push ke branch `main`
2. Manual trigger melalui GitHub Actions tab

### Proses Deploy
1. **Checkout**: Download kode dari GitHub
2. **Setup Python**: Install Python 3.12 dan huggingface_hub
3. **Prepare Files**: Salin file-file yang diperlukan ke folder temporary
4. **Upload**: Upload semua file ke Hugging Face Space menggunakan HF API

### Fallback
Jika upload menggunakan HF API gagal, workflow akan menggunakan git push sebagai fallback.

## Environment Variables di Hugging Face Space

Setelah deploy, set environment variables berikut di HF Space settings:

```bash
# Required
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1

# Optional
SESSION_API_KEY=your_session_key
DEBUG=false
```

## Troubleshooting

### Error: Authentication failed
- Pastikan `HF_TOKEN` sudah diset dengan benar di GitHub Secrets
- Pastikan token memiliki permission `write`

### Error: Space not found
- Pastikan Space sudah dibuat di Hugging Face
- Pastikan nama Space sesuai dengan yang ada di workflow

### Error: File not found
- Pastikan semua file yang diperlukan ada di repository
- Cek log GitHub Actions untuk detail error

## Monitoring

Untuk memonitor status deploy:
1. Buka GitHub repository
2. Klik tab "Actions"
3. Lihat workflow "Deploy to Hugging Face Space"
4. Klik pada run terakhir untuk melihat detail log

## Manual Deploy

Untuk deploy manual:
1. Buka GitHub repository
2. Klik tab "Actions"
3. Pilih workflow "Deploy to Hugging Face Space"
4. Klik "Run workflow"
5. Pilih branch `main` dan klik "Run workflow"