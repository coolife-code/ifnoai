# Project IfNoAI - Design Document

## 1. 项目愿景 (Vision)

**项目名称**: IfNoAI
**Concept**: "Simulating the silence of the cloud." (模拟云端的静默)

**核心目标**: 
创建一个 Windows 应用程序，用于模拟“AI 消失”的假设场景。通过在有限时间内切断设备与云端 AI 的所有连接，让用户直观地体验到 AI 对当前操作系统的渗透程度，以及在没有 AI 辅助下的真实工作状态。这是一个关于“依赖性”的社会实验工具。

---

## 2. 核心功能 (Core Features)

### 2.1 智能阻断 (The Blackout)
- **全局静默**: 基于系统底层网络配置，尽可能阻断设备上所有指向 AI 服务的网络流量。
- **深度覆盖**: 不仅针对浏览器，更着重于 IDE (VS Code, JetBrains)、Office 套件、系统内置功能 (Windows Copilot) 等“隐形”AI。
- **动态黑名单**: 维护一个 `ai-domains.json`，持续更新最新的 AI 服务端点。

### 2.2 实验控制 (Experiment Control)
- **时间胶囊 (Timer)**: 用户设定实验时长（如 1小时 - 24小时）。
- **不可逆性 (Hard Mode)**: 在实验期间，提供一种“无法轻易退出”的体验，模拟 AI 彻底离线的绝望感（当然会保留紧急恢复手段）。

### 2.3 依赖度反馈 (Dependency Feedback)
- **日志记录**: (未来规划) 尝试记录被拦截的请求数量，并在实验结束后生成一份报告：“在过去的 24 小时内，你的设备尝试呼叫 AI 1,024 次。”
- **可视化**: 直观展示拦截频率。

### 2.4 安全协议 (Safety Protocol)
- **自动回滚**: 实验时间结束后，自动恢复网络设置。
- **紧急逃生**: 生成物理文件 `Emergency_Restore.bat`，用于在软件失效时手动恢复系统状态。

---

## 3. 技术架构 (Technical Architecture)

### 3.1 技术栈
- **语言**: Python 3.10+
- **GUI 框架**: PySide6 (Qt) - 追求一种冷峻的、仪表盘式的科幻 UI。
- **打包**: Nuitka / PyInstaller

### 3.2 实现原理 (The Mechanism)
采用 **Hosts 文件劫持 + DNS 缓存刷新** 作为最基础且有效的拦截手段。

#### 流程图
1.  **Initiate**: 用户设定时长 -> 点击 "Initiate Blackout"。
2.  **Backup**: 备份 `hosts` 文件。
3.  **Inject**: 写入 AI 域名黑名单，指向 `0.0.0.0`。
4.  **Flush**: 执行 `ipconfig /flushdns`。
5.  **Monitor**: 倒计时运行，(可选) 监听网络请求失败日志。
6.  **Restore**: 倒计时结束或触发紧急停止 -> 恢复 `hosts` -> 刷新 DNS。

### 3.3 目标域名列表 (Target Domains Draft)
*该列表将作为核心资产持续维护*

**Core LLMs:**
- `api.openai.com`, `chatgpt.com`
- `anthropic.com`, `claude.ai`
- `gemini.google.com`

**Dev Tools (The Hidden AI):**
- `copilot-proxy.githubusercontent.com` (GitHub Copilot)
- `cursor.sh`, `repo.cursor.sh`
- `codeium.com`

**System Integrated:**
- `copilot.microsoft.com`
- `edgeservices.bing.com` (Bing Chat)

---

## 4. 风险与对策 (Risks & Mitigation)

| 风险 | 对策 |
| :--- | :--- |
| **意外断网** | 提供 `Emergency_Restore.bat` 脚本；设置开机自启的检查服务，若超时未恢复则强制恢复。 |
| **误伤非 AI 服务** | 域名列表需精细化维护，接受社区反馈。 |
| **软件冲突** | 检测杀毒软件是否拦截 Hosts 修改，给出提示。 |

---

## 5. UI 设计概念 (UI Concept)

**风格**: **Sci-Fi / Terminal / Industrial**
- 深色背景，霓虹蓝/红配色。
- 字体采用等宽字体 (Monospace)。
- 界面元素模仿飞船控制台或服务器仪表盘。
- 状态显示: "LINK STATUS: CONNECTED" (正常) -> "LINK STATUS: SEVERED" (阻断后)。

---

## 6. 开发路线图 (Roadmap)

- [ ] **Phase 1 (The Switch)**: 核心 Python 脚本，实现 Hosts 的备份、修改、恢复。
- [ ] **Phase 2 (The Console)**: 构建 GUI 界面，实现倒计时和状态显示。
- [ ] **Phase 3 (The Report)**: (进阶) 尝试统计拦截次数，生成依赖度报告。
