# minaki_apt_cli

# 🚀 Minaki APT CLI

> Secure. Scalable. Authenticated APT Package Hosting — From the Command Line.

[![PyPI version](https://badge.fury.io/py/minaki-cli.svg)](https://badge.fury.io/py/minaki-cli)
Minaki APT CLI gives developers and ops teams the ability to push, delete, and manage private `.deb` packages to a secure APT repository protected by **API keys**, **Keycloak authentication**, and full **audit trails**.

---

### ✨ Features

- 🔐 Upload `.deb` packages to your private repo
- 🧾 Authenticated via API key + Kong Gateway
- 🗂 Track and list available versions
- 🧨 Delete packages safely (with audit history)
- 🛡️ Auto-prevents overwrite of deleted versions

---

### 🧪 Quick Start

#### 🔧 Install
```bash
pip install minaki-apt

⚙️ Configure

minaki-cli config
# Enter your API key and backend URL

🚀 Upload a Package

minaki-cli push my-package_1.0_amd64.deb

📜 List All Packages

minaki-cli list

❌ Delete a Package

minaki-cli delete my-package 1.0 amd64


⸻

🔐 Authentication

All actions require a valid API Key, securely issued via Kong Gateway + Keycloak. Each package is mapped to a unique user identity, and deletions are archived in a tamper-proof history log.

⸻

📘 Full Documentation

📖 https://www.minaki.io/docs

⸻

🧪 Alpha Status

Minaki is in early alpha. We encourage internal use, experimentation, and feedback — but recommend caution before production use. Expect rapid iteration and improvement.

⸻

📄 License

