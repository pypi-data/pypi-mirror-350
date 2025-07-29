<!-- README.md -->

<div align="center">
  
  <img src="https://bitbytelab.github.io/assets/logos/bitbytelab.png" alt="BitByteLab Logo" height="120">
  <h1 align="center">📞 WhatXtract</h1>

  <p>
    🕵️‍♂️ A powerful multithreaded CLI tool to <strong>extract and verify WhatsApp numbers</strong> using <strong>WhatsApp Web</strong> — no API needed.
  </p>

  <p>
    WhatXtract is a <strong>robust</strong>, <strong>easy-to-use</strong> WhatsApp data extraction and automation toolkit built in Python. It lets you <strong>verify, extract, and validate contact numbers</strong> directly via WhatsApp Web with headless automation — powered by <code>selenium</code> and <code>undetected-chromedriver</code>.
  </p>

  <p>
    Designed for <strong>developers</strong>, <strong>growth hackers</strong>, <strong>marketers</strong>, and <strong>data analysts</strong>, WhatXtract enables you to:
    <ul align="left" style="text-align: left;">
      <li>✅ Verify which numbers are active WhatsApp users</li>
      <li>📤 Extract and clean up phone lists for lead gen or CRM sync</li>
      <li>⚙️ Build custom WhatsApp workflows with automation at the core</li>
    </ul>
  </p>

  <p>
    <img src="https://img.shields.io/github/tag-version/bitbytelab/?style=flat-square" alt="GitHub Release Badge" />
    <img src="https://img.shields.io/badge/license-MIT-red?style=flat-square" alt="License Badge" />
    <img src="https://img.shields.io/pypi/pyversions/whatxtract?style=flat-square" alt="Python Version" />
    <img src="https://img.shields.io/badge/status-Beta-orange?style=flat-square" alt="Project Status" />
    <img src="https://img.shields.io/pypi/v/whatxtract?style=flat-square" alt="PyPI Version" />
    <img src="https://img.shields.io/pypistats/monthly/whatxtract?style=flat-square" alt="PyPI Downloads" />
    <img src="https://img.shields.io/github/languages/top/bitbytelab/whatxtract?style=flat-square" alt="Top Language" />
    <a href="https://github.com/astral-sh/ruff">
      <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff Code Quality" />
    </a>
  </p>
</div>

---

## 🌟 Features

- ✅ **Detect Active/Inactive WhatsApp Numbers**
- 🧠 **Intelligent Login Handling** (QR scan and session reuse)
- 🔀 **Concurrent Multi-Account Checking**
- 🛡️ **Proxy Support** (optional, per account)
- 🗃️ **Persistent Profiles** – saves WhatsApp login sessions
- 🕶️ **Headless Mode** – optional
- 🕓 **Customizable Delays** – mimic human-like behavior
- 📂 **Custom Config Support** (`whatschecker.config.json`)
- 📈 **Built with Selenium + Undetected ChromeDriver**
- 💥 **Auto dependency installs on first run**
- 📇 **Extracts valid WhatsApp numbers from saved contacts on the device**

---

## 📦 How It Works

WhatXtract uses a multistep pipeline to extract valid WhatsApp users from your own contact list in a semi or fully-automated fashion:

1. **Prepare a `.txt` file** with phone numbers — one per line.
2. **WhatXtract converts this into a `.vcf` file** of ~5000 contacts per batch.
3. **Import the `.vcf` file to your WhatsApp installed Phone**.
4. **Launch WhatsApp and wait for sync.**
5. **Extracts relevant `stores` from WhatsApp IndexedDB**.
6. **Parses contacts** to extract name and number of valid users.
7. **Exports to a timestamped CSV file.**

> ℹ️ All the above steps can be performed automatically in sequence. <br>
> For now perform Step 3 and 4 manually.

---

## 🚀 Usage

### 1. 📦 Installation

```bash
git clone https://github.com/bitbytelab/WhatXtract.git
cd WhatXtract
chmod +x whatxtract.py
```

### 2. 🧪 First-time Setup (Scan QR)

```bash
./whatxtract.py --add-account
```

Scan the QR code to save your WhatsApp session. You can add multiple accounts this way.

---

### 3. 📤 Checking Numbers

Prepare an input file (e.g., `numbers.txt`) with **one number per line**:

```
+12025550123
+447911123456
+8801711123456
```

Run the checker:

```bash
./whatxtract.py --input numbers.txt --valid active.txt --invalid inactive.txt
```

You can also run in headless mode:

```bash
./whatxtract.py --input numbers.txt --valid active.txt --invalid inactive.txt --headless
```

---

### 4. 📇 Contacts Extraction

To extract valid WhatsApp numbers from your saved contacts:

```bash
python -m whatxtract --input contacts
```

This will:

1. Launch WhatsApp Web and log you in.
2. Extract contacts from WhatsApp database. 
3. Save valid WhatsApp numbers along with name, about, and avatar info to a CSV.

The generated CSV will be saved as:

```
valid_whatsapp_contacts_YYYY_mm_dd_HH_MM.csv
```

📁 Example output preview:

| name         | about                        | user_avatar                                     |
|--------------|------------------------------|-------------------------------------------------|
| 019xxxxxxxxx | Always learning               | https://media.whatsapp.net/...                  |
| 018xxxxxxxxx | Big brother watching you 😊   | default                                         |

📝 **Note:** Contact names must be saved as numbers (i.e., "017xxxxxxx") to work properly with this feature.



### 5. 🧩 Optional Arguments

| Flag            | Description                                      |
|-----------------|--------------------------------------------------|
| `--input`       | Input file with numbers                          |
| `--valid`       | Output file for active numbers                   |
| `--invalid`     | Output file for inactive numbers                 |
| `--delay`       | Base delay in seconds between number checks      |
| `--proxies`     | List of proxies (e.g., `http://ip:port`)         |
| `--headless`    | Run Chrome in headless mode                      |
| `--add-account` | Launch new profile and scan QR to add account    |

---

### 6. ⚙️ Config File Support

You can also define your settings in a `whatschecker.config.json` file:

```json
{
  "input": "numbers.txt",
  "valid": "active.txt",
  "invalid": "inactive.txt",
  "delay": 8,
  "proxies": ["http://127.0.0.1:8000", null]
}
```

Then just run:

```bash
./whatxtract.py
```

---

## 🔐 Session Management

Saved WhatsApp sessions are stored in:

```bash
./WAProfiles/account1
./WAProfiles/account2
...
```

Remove a folder to reset that session.

---

## 🧰 Dependencies

- Python `3.9+`
- [undetected-chromedriver](https://github.com/ultrafunkamsterdam/undetected-chromedriver)
- [selenium](https://pypi.org/project/selenium)

📦 Auto-installs on first run if not found!

---

## 📂 Folder Structure

<!-- START FOLDER STRUCTURE -->


<!-- END FOLDER STRUCTURE -->

---

## ❓ FAQ

**Q: Will my WhatsApp account get banned?**  
A: This script mimics human behavior using real browser sessions and delays. Use proxies and multiple accounts to reduce risk. No API violations.

**Q: Is this open source?**  
A: Yes! MIT licensed. Use it responsibly and contribute back.

---

Here’s a clean and friendly **Contribution** section you can add to your `README.md`:

---

## 🤝 Contribution

Contributions are welcome and appreciated!

* Feel free to **submit pull requests (PRs)** to improve features, fix bugs, or enhance documentation.
* Please ensure your code follows standard conventions and is well-tested where applicable.
* If you're planning a major change, consider opening an issue first to discuss it.

Let’s make this project better together! 💡

---

## ⚠️ Disclaimer

This tool is provided **for educational and research purposes only**.

* **Use at your own risk.**
* The author is **not responsible** for any misuse, damages, or consequences arising from the use of this tool.
* Automated or excessive interaction with WhatsApp services **may violate their Terms of Service** and **can lead to account bans or other penalties**.
* By using this tool, you agree that you understand the risks and take **full responsibility** for any outcomes.

> Always respect the platforms you interact with. This project is not affiliated with, endorsed by, or associated with WhatsApp or Meta in any way.

---

## 👨‍💻 Author
[Hasan Rasel](https://github.com/rsmahmud)  
Made with ❤️ by [BitByteLab](https://github.com/bitbytelab)  
📧 Contact: [bbytelab@gmail.com](mailto:bbytelab@gmail.com)

---

## 📄 License

MIT License – see [LICENSE](LICENSE) file for details.

---

## ⭐️ Star this project

If you find this useful, please consider starring the repo!  
👉 [github.com/bitbytelab/WhatXtract](https://github.com/bitbytelab/WhatXtract)
