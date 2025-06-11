# 🛡️ TinyAI - AI-Powered Cybersecurity Assistant

**TinyAI** is a lightweight cybersecurity AI assistant. It leverages LLM-based intelligence to assist with **SIEM automation**, **log pattern detection**, **incident triage**, and **cybersecurity learning** in both offline and online modes. The chatbot is ideal for local use in SOC environments, academic research, or personal upskilling.

---

## 🔍 Overview

TinyAI is optimized for:
- Real-time log event analysis
- Context-aware threat identification
- Local or hybrid (internet-aware) intelligence
- Custom cybersecurity learning assistant
- Wazuh and SIEM integration preparation

It supports:
- ✅ **Streaming LLM responses with context memory**
- ✅ **Cyber-specific intent recognition**
- ✅ **Built-in 50+ annotated log patterns**
- ✅ **Works offline or uses DuckDuckGo online**

---

## ⚙️ Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/jagdishtripathy/tinyai-cyberbot.git
cd tinyai-cyberbot
```

### 2. Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Download & Place Model
- Download `openhermes-2.5-mistral-7b.Q4_K_M.gguf` from [TheBloke on HuggingFace](https://huggingface.co/TheBloke/OpenHermes-2.5-Mistral-7B-GGUF)
- Place it in your root directory or update the path in `config.py`

> Recommended format: `Q4_K_M` (balanced for speed and size)

---

## 🚀 Launch Chatbot
Run the chatbot with:
```bash
python run.py
```
Then visit: [http://127.0.0.1:7860](http://127.0.0.1:7860)

Try sample queries like:
- "What is SIEM?"
- "Detect SQL injection from logs"
- "Remember: I use Wireshark for analysis"

---

## 🔐 Security & SIEM Use
TinyAI can serve as a log investigation and learning assistant in a security operations center. By feeding it structured logs (from Wazuh, Elastic, Graylog, etc.), you can:
- Identify suspicious access patterns
- Cross-check known CVE behaviors
- Tag brute-force, port scans, or phishing attempts
- Use it alongside your Wazuh alerts for live triage

While TinyAI doesn’t replace your SIEM, it enhances your incident response and analyst workflow.

---

## 🧠 Extend or Customize
- Modify `mydata.csv` to reflect your role/profile
- Extend `log_patterns.csv` with new use cases
- Integrate with alert sources for real-time interaction

---

## 🔭 Roadmap
- 🔄 Live Wazuh alert-to-AI pipeline
- 📊 ElasticSearch support
- 🧩 Plugin system for tool integration
- 🌐 Web-hosted mode with user login

---

## 👨‍💻 Author
Built with ❤️ by [Jagadish Tripathy](https://www.linkedin.com/in/jagadishtripathy)

If you find this helpful, ⭐ star it and share it with your peers.

---

## 📄 License
MIT License - free to use, modify, and share.
