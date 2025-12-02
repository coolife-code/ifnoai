# IfNoAI - Technical Blueprint

> **"Deconstruct the cloud. Reclaim the mind."**

This document details the system architecture and operational mechanism of **IfNoAI**. It is not just software, but a precision experimental apparatus designed to simulate a scenario of "AI Silence."

---

## 1. Core Philosophy

**Project IfNoAI** aims to create an isolated environment that uses technical means to temporarily sever the device's connection to cloud artificial intelligence services. This is not a denial of AI, but a reverse test of "dependency."

During the experiment, the system simulates a parallel world where "AI has suddenly disappeared," allowing users to intuitively experience the extent to which modern workflows rely on intelligent assistance, and observe their cognitive state when returning to a mode of "pure human wisdom."

---

## 2. System Modules

### 2.1 The Interceptor
The core engine of the system. It does not rely on high-level firewall rules but acts directly on the network resolution layer of the operating system.
- **Global Coverage**: Precision strikes against hundreds of known AI service endpoints (including OpenAI, Anthropic, Google, Microsoft, GitHub Copilot, etc.).
- **Dual-Stack Blocking**: Handles both IPv4 and IPv6 traffic simultaneously to prevent intelligence leaks in modern network environments.
- **Dynamic Updates**: Maintains a continuously evolving "silence list" via `ai_domains.json`.

### 2.2 The Sinkhole
When the Interceptor is active, requests sent to AI do not simply time out; they are redirected to the local **Sinkhole Server**.
- **Capture**: Listens on local ports `80` (HTTP) and `443` (HTTPS).
- **Devour**: For captured requests, the server logs the source domain and then returns a meaningless response or directly disconnects, simulating a "Network Error."
- **Statistics**: Every captured request represents a subconscious user call to AI; this data will generate a "Dependency Report" at the end of the experiment.

### 2.3 The Time Lock
The boundary of the experiment.
- **Forced Silence**: Users set the experiment duration (1-24 hours). Before the countdown ends, the system encourages users to persist in working within the AI-free environment.
- **Psychological Game**: This is a process of confronting one's own habits.

---

## 3. The Mechanism

The system employs **Hosts Hijacking** and **Local Loopback** technologies to achieve efficient and low-overhead blocking.

### 3.1 Initiation Sequence
1.  **Snapshot**: The system first creates a complete backup of the current `C:\Windows\System32\drivers\etc\hosts` file, generating `hosts.backup.ifnoai`.
2.  **Injection**: Reads `ai_domains.json` and points all AI-related domain resolution records to the local loopback address:
    - IPv4: `127.0.0.1`
    - IPv6: `::1`
3.  **Flush**: Calls `ipconfig /flushdns` to clear the operating system's DNS cache, ensuring the block takes effect immediately.
4.  **Activation**: Starts the Sinkhole Server to begin listening for redirected traffic.

### 3.2 Restoration Sequence
1.  **Deactivation**: Stops the Sinkhole Server.
2.  **Revert**: Restores the original `hosts` content from the backup file, or precisely removes the entries injected by IfNoAI.
3.  **Flush**: Flushes the DNS cache again to restore normal network connectivity.

---

## 4. Safety Protocols

To prevent users from getting "lost" during the experiment, the system has built-in multiple fail-safe mechanisms.

### 4.1 Auto-Rollback
Whether the experiment ends normally or terminates abnormally (e.g., program crash), the system is designed with atomic recovery logic. On the next startup, the program will detect and clean up residual blocking rules.

### 4.2 Emergency Eject
The system generates an independent `Emergency_Restore.bat` script. Even if the main program fails to run, users can run this script with administrator privileges to forcibly reset network settings.

### 4.3 Permission Control
Since it involves modifying core system files, the program must be run with **Administrator** privileges. All modifications are restricted to a specific marked area within the `hosts` file (`# === IfNoAI START ===`) and never touch the user's other configurations.

---

## 5. Visual Language

The interface design of IfNoAI is deeply influenced by **Cyberpunk** and **Retro Terminal** aesthetics.

- **Tone**: Deep space black background paired with neon green/warning red, creating an immersive sense of "entering the system underlayer."
- **Typography**: Uses monospaced fonts to simulate code editors and command-line interfaces.
- **Metaphor**: All status prompts and loading animations aim to mimic spaceship consoles or hacker tools, reinforcing the ritual sense of "severing the connection."

---

> **"The silence is not empty. It is full of answers."**
