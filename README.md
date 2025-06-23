---
title: Human-Like Writing Assistant
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "4.36.0"
app_file: app.py
pinned: false
license: mit
app_port: 7860
---

# 🎭 Human-Like Writing Assistant

A premium AI writing assistant that creates content indistinguishable from human writing. Revolutionary technology that analyzes writing patterns and generates authentic content.

## 🚀 Features

- **Advanced Writing Style Analysis** - Analyze and learn from writing samples
- **Human-Like Content Generation** - Generate content that matches your style
- **AI Text Humanization** - Convert AI-generated text to appear human-written
- **AI Detection Risk Assessment** - Check and improve content to avoid AI detection
- **Anti-Detection Technology** - Advanced techniques to ensure authenticity

## 🔐 Authentication

Most endpoints require a Bearer token for security. Set a `PERSONAL_ACCESS_TOKEN` in your HF Spaces environment variables.

### 📋 Required Setup

Set these environment variables in your HF Spaces settings:

```bash
# Required - Your OpenRouter API key
LLM_API_KEY=your_openrouter_api_key

# Required - Your personal access token (choose any password you like!)
PERSONAL_ACCESS_TOKEN=your_chosen_password_here

# Optional - LLM configuration (defaults provided)
LLM_MODEL=openrouter/anthropic/claude-3-haiku-20240307
LLM_BASE_URL=https://openrouter.ai/api/v1
## 🌐 API Endpoints

### Public Endpoints (No Authentication)
```bash
# Health check
GET /health

# Root information
GET /
```

### Protected Endpoints (Require Bearer Token)
```bash
# Analyze writing style
POST /api/analyze-writing-style
Authorization: Bearer your_personal_token
Content-Type: application/json
{
  "text_samples": ["Sample text 1", "Sample text 2"]
}

# Generate human-like content
POST /api/generate-human-content
Authorization: Bearer your_personal_token
Content-Type: application/json
{
  "prompt": "Write about...",
  "style_profile": {...},
  "length": 500
}

# Humanize AI text
POST /api/humanize-text
Authorization: Bearer your_personal_token
Content-Type: application/json
{
  "ai_text": "AI generated text...",
  "style_profile": {...}
}

# Check AI detection risk
POST /api/check-ai-detection
Authorization: Bearer your_personal_token
Content-Type: application/json
{
  "text": "Text to analyze..."
}
```

### 💻 Example Usage

```javascript
// Analyze writing style
const API_TOKEN = 'your_chosen_password';

const response = await fetch('https://your-space.hf.space/api/analyze-writing-style', {
  method: 'POST',
  headers: { 
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${API_TOKEN}`
  },
  body: JSON.stringify({
    text_samples: [
      "This is my first writing sample. I tend to write in a casual, friendly tone.",
      "Here's another example of my writing style. I like to use simple words and short sentences."
    ]
  })
});

const analysis = await response.json();
console.log(analysis);
```

### 🧪 Test Your Setup

```bash
# Test health check (should work)
curl https://your-space.hf.space/health

# Test with token (should work)
curl -H "Authorization: Bearer your_chosen_password" \
     -H "Content-Type: application/json" \
     -d '{"text":"Test text for AI detection"}' \
     https://your-space.hf.space/api/check-ai-detection
```

## 🔧 Features

- 🎭 **Advanced Writing Analysis** - Deep analysis of writing patterns
- 🤖 **Human-Like Generation** - Content that passes AI detection
- 🔄 **Text Humanization** - Convert AI text to human-like
- 🔍 **Detection Risk Assessment** - Check and improve authenticity
- 🔐 **Secure Authentication** - Protected with personal tokens
- ✅ **OpenRouter Only** - No need for multiple API keys
- ✅ **Local Runtime** - Works without Docker in container
- ✅ **CORS Enabled** - Ready for frontend integration
- ✅ **No Google Cloud** - Zero Google dependencies
- ✅ **HF Spaces Optimized** - Perfect for Hugging Face deployment
- ✅ **Indonesian Novel Writing** - Special support for creative writing
- ✅ **All-in-One File** - Single app.py file, no confusion

## 🎯 Use Cases

- **AI Coding Assistant**: Help with programming tasks
- **Web Automation**: Browse and interact with websites  
- **Code Execution**: Run and test code snippets
- **Research Assistant**: Gather information from multiple sources
- **Educational Tools**: Interactive learning experiences
- **Novel Writing**: Indonesian creative writing support

## 🔒 Security & Privacy

- **Bearer Token Authentication**: Simple password protection
- **No Google Login**: No complex OAuth setup needed
- **Private Access**: Only you and your girlfriend can use it
- **API Key Protection**: Your OpenRouter key is protected
- **CORS Security**: Only allowed domains can access

## 📚 Documentation

- **OpenHands GitHub**: [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
- **LLM Provider**: [OpenRouter](https://openrouter.ai)
- **Frontend Examples**: Deploy your own UI on Vercel

## 🚨 Troubleshooting

### "Invalid personal access token" error:
1. Check if you set `PERSONAL_ACCESS_TOKEN` in HF Spaces environment variables
2. Make sure you're using the same token in your API calls
3. Restart your HF Space after setting the token

### "Missing LLM_API_KEY" error:
1. Get your API key from [OpenRouter](https://openrouter.ai)
2. Set `LLM_API_KEY` in HF Spaces environment variables
3. Restart your HF Space

### "Authentication failed" error:
1. Make sure you set `PERSONAL_ACCESS_TOKEN` in environment variables
2. Use the correct token in Authorization header: `Bearer your_token`
3. Check that the token matches exactly

## 📝 License

MIT License - Feel free to use in your projects!

---

**Ready to create human-like content?** 🎭

Start by setting up your environment variables and calling the API endpoints above!
# Updated Mon Jun 23 00:43:00 UTC 2025
