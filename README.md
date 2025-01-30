
# Bahria LMS Assignment Checker 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

A streamlined tool to check pending LMS assignments for Bahria University students, featuring automatic login and a modern UI.

![demo-screenshot](https://github.com/user-attachments/assets/2d7ce3ba-0ad1-4e37-9c50-0faac1b211c0)

## Features ✨
- 🔒 Secure LMS login automation
- 📊 Course-wise assignment status tracking
- 📱 Mobile-friendly design
- 📈 Progress indicators for long operations
- 🛡️ Credential privacy protection

## Installation ⚙️

1. **Clone Repository**
   ```bash
   git clone https://github.com/Abdur-Rafay-AR/bahria-LMS-assignment-checker.git
   cd bahria-LMS-assignment-checker
   ```

2. **Install Dependencies**
   ```bash
   pip install streamlit selenium webdriver-manager
   ```

3. **ChromeDriver Setup**
   - Download [ChromeDriver](https://chromedriver.chromium.org/)
   - Place `chromedriver.exe` in project root _or_
   - Set environment variable:
     ```bash
     export CHROMEDRIVER_PATH="/path/to/chromedriver"
     ```

## Usage 🖥️

1. **Run Application**
   ```bash
   streamlit run app.py
   ```

2. **Enter Credentials**
   - Enrollment Number (e.g., `01-234567-001`)
   - LMS Password

3. **View Results**
   - Course-wise assignment status
   - Total pending assignments
   - Visual status indicators

## Technologies 🛠️
- **Python** (Backend Logic)
- **Streamlit** (Web Interface)
- **Selenium** (Browser Automation)
- **ChromeDriver** (Headless Browser Control)

## Contributing 🤝
Contributions welcome! Please:
1. Fork repository
2. Create feature branch
3. Submit PR with detailed description

## License 📄
MIT License - See [LICENSE](LICENSE) for details

## Disclaimer ⚠️
This unofficial tool is not affiliated with Bahria University. Use at your own risk. Credentials are processed securely but users should exercise caution.

---

Developed with ❤️ by [Abdur Rafay](https://github.com/Abdur-Rafay-AR)  
