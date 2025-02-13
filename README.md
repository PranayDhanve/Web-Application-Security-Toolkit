Web-Application-Security-Toolkit
Web Security Scanner 🚀

A **Python-based Web Security Scanner** that automatically **crawls a website**, identifies **forms and input fields**, and tests for **SQL Injection (SQLi), Cross-Site Scripting (XSS), and Cross-Site Request Forgery (CSRF) vulnerabilities**.  

**🔍 Features**
- **Crawls a target website** and extracts all **linked pages**.
- **Scans all input fields (textboxes, comments, forms, etc.)**.
- **Detects SQL Injection, XSS, and CSRF vulnerabilities**.
- **Saves scan results in a structured CSV report** with severity levels.
- **Lightweight and easy to use**.

**📥 Installation & Setup**
1️⃣** Clone the Repository**
```bash
https://github.com/PranayDhanve/Web-Application-Security-Toolkit.git

2️⃣ Install Dependencies

pip install -r requirements.txt

3️⃣ Run the Scanner

python3 form_scanner.py

💡 Enter the target URL when prompted, and let the scanner do its job!

🛠 Usage Example

Running the Scanner

Enter URL to scan: http://testphp.vulnweb.com/

Sample Output

Scan complete. Report saved as 'report.csv'

📝 Contributing

We welcome contributions! If you’d like to add more payloads, improve crawling, or enhance detection techniques, feel free to fork and submit a pull request.

⚠️ Disclaimer

This tool is intended for educational and ethical security testing purposes only. Do not use it to scan websites without explicit permission. Misuse may lead to legal consequences.

