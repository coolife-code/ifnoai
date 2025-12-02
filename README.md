# IfNoAI

> **A Sci-Fi Experiment on your Desktop.**  
> 一个桌面端的科幻实验：假如未来某一天，AI 突然消失了。

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Platform](https://img.shields.io/badge/platform-Windows-blue)

## 🌌 概念 (Concept)

**IfNoAI** 是一个基于 Windows 的实验性项目。它构建了一个模拟场景：在一个被 AI 高度渗透的数字世界中，如果所有的云端智能突然静默，我们的设备会变成什么样？

> **"When we lose the assistance of the cloud brain, can we still solve problems efficiently?"**  
> **"当我们失去了云端大脑的辅助，我们还能高效地解决问题吗？"**

这不仅仅是一个屏蔽工具，更是一场**社会实验**与**AI 依赖度探针**。通过在系统底层切断对 OpenAI, Copilot, Gemini 等数百个 AI 服务的连接，我们可以直观地观测到：

*   有多少软件突然变得“智障”或功能失效？
*   操作系统中嵌合了多少我们未曾察觉的 AI 触角？
*   我们自己是否还能流畅地完成工作？

## �️ 功能 (Features)

- **The Blackout (大停电)**: 一键模拟 AI 服务离线。通过修改系统 Hosts 文件，将主流 AI 服务的网络请求重定向至虚空（0.0.0.0）。
- **Reality Check (现实检验)**: 尽可能覆盖所有已知的 AI 服务端点，包括浏览器、IDE 插件、系统级 Copilot 以及各类第三方应用。
- **Time Capsule (时间胶囊)**: 设定一段“无 AI”的持续时间，体验一种复古的、纯粹的计算环境。
- **Safety Protocol (安全协议)**: 内置自动恢复机制与紧急逃生脚本，确保实验结束后能够安全返回“智能时代”。

## 📄 设计文档 (Design)

详细的技术实现和架构设计请参阅 [DESIGN_DOC.md](./DESIGN_DOC.md)。

## 🚀 快速开始 (Getting Started)

*目前项目处于设计阶段 (Design Phase)*

### 预想的使用方式:

1.  启动 **IfNoAI**。
2.  设定实验时长（例如：24小时）。
3.  点击 **"Initiate Blackout"**。
4.  观察你的电脑，记录下哪些功能失效了，哪些图标变灰了。

## ⚠️ 免责声明 (Disclaimer)

本软件通过修改系统 `hosts` 文件工作，旨在进行技术实验与反思。请确保您了解其工作原理，并妥善保存重要数据。

---
*Looking for the ghost in the machine.*
