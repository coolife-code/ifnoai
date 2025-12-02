<div align="center">

```text
██╗███████╗███╗   ██╗ ██████╗  █████╗ ██╗
██║██╔════╝████╗  ██║██╔═══██╗██╔══██╗██║
██║█████╗  ██╔██╗ ██║██║   ██║███████║██║
██║██╔══╝  ██║╚██╗██║██║   ██║██╔══██║██║
██║██║     ██║ ╚████║╚██████╔╝██║  ██║██║
╚═╝╚═╝     ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝╚═╝
                                         
      [ THE SILENCE OF THE CLOUD ]
```

# IfNoAI

> **A Sci-Fi Experiment on your Desktop.**
>
> **"In the silence of the cloud, we hear the echo of our own minds."**

![License](https://img.shields.io/badge/license-MIT-00ff88?style=for-the-badge) 
![Platform](https://img.shields.io/badge/platform-Windows-00d4ff?style=for-the-badge)
![Status](https://img.shields.io/badge/status-EXPERIMENTAL-ff0055?style=for-the-badge)

</div>

---

## 🌌 The Collapse & The Reconstruction

What if... just what if... one day, the wisdom of the cloud suddenly falls into dead silence?

Those digital neurons that have subtly embedded themselves into our cerebral cortex, reconstructing our patterns of thought—if they were to snap in an instant, would the cognitive edifice humanity has built for so long collapse with them?

We have already sensed this shift. That sudden helplessness when severed from AI assistance; that stagnation and blankness of mind when facing an empty screen. We know this "silicon dependency" is etching away at our souls, yet we often choose to turn a blind eye, unable to confront it.

**IfNoAI** is not merely software; it is a rehearsal for "loss," a stress test for self-belief.

When you initiate it, your device will completely sever contact with all cloud AI.
Facing your every inquiry, your every habitual reliance, the response will no longer be an emergence of wisdom, but a cold, repetitive, emotionless—

**"Network Error"**

Perhaps in the distant future, humanity will truly lose itself amidst a screen full of "Network Errors," our beliefs crumbling. But before that day truly arrives, in this "moment of silence" you initiate yourself, try to face this silence directly.

---

## 🗝️ The Experience

<div align="center">
  <img src="src/image/屏幕截图 2025-12-02 221933.png" width="80%" alt="Main Interface">
  <p><em> - </em></p>
</div>

- **🛑 The Severance (阻断)**  
  Instantly cut the umbilical connection to hundreds of AI services like OpenAI, Copilot, Claude, Gemini, etc. A system-level Hosts hijack ensures not a single signal escapes this isolated island.

- **🕳️ The Void (虚空)**  
  When you attempt to wake the AI, the Sinkhole Server captures these requests and devours them. You will only see connection failure prompts—withdrawal symptoms of the digital age.

- **🧘 The Reflection (反思)**  
  Set a period of "AI-free" solitude (1-24 hours). After the experiment concludes, the system will tell you: during this time, how many times did you subconsciously reach out to the cloud.


---

## 📄 Technical Blueprint

For details on how this wall of sighs is constructed, please refer to the [DESIGN_DOC.md](./DESIGN_DOC.md).

## 🚀 Initiate Protocol

### 1. Prerequisites
- **OS**: Windows 10 / 11
- **Runtime**: Python 3.10+
- **Privileges**: Administrator rights required (to touch the system's neural center—the Hosts file)

### 2. Installation

```bash
# Clone repository
git clone https://github.com/coolife-code/ifnoai.git
cd ifnoai

# Install dependencies
pip install -r requirements.txt
```

### 3. Execution

Recommended to use the GUI to visually observe the connection status:

```bash
# Launch Console (GUI)
python src/main.py
```

Or use Command Line Interface (CLI):

```bash
# Check current status
python src/main.py status

# Engage Interceptor (Sever Connection)
python src/main.py on

# Restore Connection (Rebuild Link)
python src/main.py off
```

### 4. Troubleshooting
- **🛡️ Antivirus Interception**: Since the program needs to modify the `hosts` file, it may be mistaken for a malicious intrusion by antivirus software. Please grant it trust, or temporarily disable protection.
- **⚠️ Lost in the Void (Unable to Restore)**: If an accident occurs and the network fails to recover automatically, please manually delete the `IfNoAI` related section in the `hosts` file, and run `ipconfig /flushdns` to flush the DNS cache.

---

## 🤝 Join the Resistance

This list is far from complete. The tentacles of the cloud are extending every moment, and new AI services are emerging endlessly.

If you find an AI service domain that has not been blocked, please submit a Pull Request to supplement `data/ai_domains.json`.
Let us jointly perfect this line of defense and ensure the purity of the experiment.

## ⚠️ Disclaimer

This software is intended for technical experimentation and philosophical reflection. It works by modifying core system files. Please ensure you understand the consequences of this action, and properly preserve your data and beliefs.

---

<div align="center">

*Looking for the ghost in the machine.*

</div>
