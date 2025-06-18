# 🚀 Setup Auto Deploy ke Hugging Face Spaces

## 📱 Solusi untuk Masalah Mobile

Karena susah klik tombol restart di Hugging Face dari HP, sekarang Anda bisa auto-deploy dari GitHub!

## 🔧 Setup Sekali Saja

### 1. Dapatkan Hugging Face Token
1. Buka [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Klik "New token"
3. **Name**: `GitHub Auto Deploy`
4. **Type**: Write
5. Copy token yang dihasilkan

### 2. Setup GitHub Secrets
Di repository GitHub Anda (`Minatoz997/OpenHands-Backend`):

1. Buka **Settings** → **Secrets and variables** → **Actions**
2. Klik **New repository secret**
3. Tambahkan 3 secrets ini:

```
HF_TOKEN = your_huggingface_token_here
HF_USERNAME = Minatoz997
HF_SPACE_NAME = openhands-backend
```

### 3. Buat Hugging Face Space (Sekali Saja)
1. Buka [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Owner**: Minatoz997
3. **Space name**: openhands-backend
4. **SDK**: Docker
5. **Visibility**: Public
6. **Hardware**: CPU basic (gratis)
7. Klik **Create Space**

### 4. Set Environment Variables di HF Space
Di Space Settings → Environment Variables:

```bash
LLM_API_KEY=your_openrouter_api_key
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
```

## 🎯 Cara Menggunakan

### Auto Deploy (Otomatis)
- Setiap kali push ke branch `main`, otomatis deploy ke HF Spaces
- Tidak perlu klik restart manual lagi!

### Manual Deploy (Jika Diperlukan)
1. Buka repository di GitHub
2. Klik tab **Actions**
3. Pilih **Deploy to Hugging Face Spaces**
4. Klik **Run workflow**
5. Tunggu selesai (sekitar 5-10 menit)

## 📱 Keuntungan untuk Mobile

✅ **Tidak perlu restart manual** - Auto deploy dari GitHub
✅ **Mobile-friendly** - Bisa trigger dari HP via GitHub app
✅ **Real-time logs** - Lihat progress deploy di GitHub Actions
✅ **Rollback mudah** - Revert commit jika ada masalah

## 🔍 Monitoring

### Cek Status Deploy:
1. **GitHub Actions**: Lihat progress di tab Actions
2. **HF Space Logs**: Cek logs di Space Settings
3. **Health Check**: Test `https://your-space.hf.space/health`

### Troubleshooting:
- **Deploy gagal**: Cek logs di GitHub Actions
- **Space error**: Cek logs di HF Space Settings
- **API tidak jalan**: Pastikan `LLM_API_KEY` sudah diset

## 🎉 Hasil Akhir

Setelah setup:
- **Space URL**: `https://huggingface.co/spaces/Minatoz997/openhands-backend`
- **API URL**: `https://Minatoz997-openhands-backend.hf.space`
- **Docs**: `https://Minatoz997-openhands-backend.hf.space/docs`

## 📞 Support

Jika ada masalah:
1. Cek GitHub Actions logs
2. Cek HF Space logs  
3. Test health endpoint
4. Pastikan semua secrets sudah diset

Sekarang Anda bisa deploy dari HP dengan mudah! 🎯