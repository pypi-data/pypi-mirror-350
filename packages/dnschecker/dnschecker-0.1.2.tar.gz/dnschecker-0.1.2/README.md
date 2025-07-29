# 🔍 dns-checker

A powerful and flexible Python CLI tool for querying and inspecting DNS records across multiple domains, supporting custom DNS servers, advanced search, and color highlighting.

---

## 🚀 Overview

**dns-checker** lets you:

- Query DNS records (A, MX, TXT, SPF, CNAME, etc.) for one or more domains
- Use custom DNS servers for queries
- Search for specific values, IPv4, or IPv6 addresses within records
- Highlight and summarize search results for quick analysis
- Handle SPF records with special logic (extracted from TXT records)
- Get clear, color-coded output for easy interpretation

Perfect for sysadmins, DevOps, and anyone needing to audit or troubleshoot DNS configurations!

---

## ✨ Features

- 🔎 **Flexible Record Support:** Query any DNS record type (A, MX, TXT, SPF, CNAME, etc.)
- 🌐 **Custom DNS Servers:** Specify one or more DNS servers to use for queries
- 🕵️ **Advanced Search:** Find specific values, IPv4, or IPv6 addresses within DNS records
- 🎨 **Color Highlighting:** Results are color-coded for fast visual scanning
- 🛡️ **Robust Error Handling:** Graceful handling of NXDOMAIN, timeouts, and other DNS errors
- 📋 **Batch Domain Support:** Check multiple domains in a single run
- 🧪 **SPF Logic:** Accurately extracts SPF records from TXT records

---

## 📦 Installation

Install from PyPI:
```
pip install dnschecker
```

---

## 📝 Usage

Run the tool from the command line:
```
pip install dnschecker
```
dns-checker --domains example.com example.org --type MX
```

**Main options:**

- `--domains`: List of domains to check (required)
- `--type`: DNS record type (A, MX, TXT, SPF, CNAME, etc.) (default: A)
- `--dns-servers`: Space-separated list of DNS server IPs to use (default: 1.1.1.1 1.0.0.1)
- `--find`: Search for a specific value in the records
- `--find-ipv4`: Search for a specific IPv4 address in the records
- `--find-ipv6`: Search for a specific IPv6 address in the records

**Examples:**

Query A records for multiple domains using default DNS servers:
```
dns-checker --domains example.com example.org
```

Query MX records using Google DNS:
```
dns-checker --domains example.com --type MX --dns-servers 8.8.8.8 8.8.4.4
```

Search for a specific value in TXT records:
```
dns-checker --domains example.com --type TXT --find "google-site-verification"
```

Find a particular IPv4 address in SPF records:
```
dns-checker --domains example.com --type SPF --find-ipv4 192.0.2.1
```

---

## 📚 Output Example
```
Using DNS servers: 8.8.8.8
Record type: MX
Domain: example.com
→ 10 mail.example.com.
→ 20 backup.example.com.
```

With search highlighting:
```
Searching for: google-site-verification
Domain: example.com
✅ google-site-verification in: v=spf1 include:_spf.google.com ~all "google-site-verification=abc123"
```

---

## ⚙️ Dependencies

- Python 3.6+
- [dnspython](https://pypi.org/project/dnspython/)

Install dependencies with:
```
pip install dnspython
```

---

## 🛡️ License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome!  
Please open an issue or submit a pull request on GitHub.

---

## 🙋 Support

For questions or support, open an issue on GitHub or contact [your.email@example.com](mailto:your.email@example.com).

---

> _Effortlessly audit and troubleshoot DNS records across your domains!_

---

**Replace placeholder links and emails with your actual information before publishing to PyPI.**
