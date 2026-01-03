# web-data-extractor
Simple GUI tool to scrape data from any website. Extract text, links, and export to CSV/JSON. No coding required.


# 🌐 Web Scraper Tool

A simple GUI tool to extract data from any website using CSS selectors. No coding required.

![Python](https://img.shields.io/badge/Python-3.14%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- **Easy to Use**: Simple graphical interface
- **Flexible Extraction**: Use CSS selectors to target any element
- **Multiple Export Formats**: Save as CSV or JSON
- **Real-time Preview**: See extracted data immediately
- **Text & Link Extraction**: Extract both text content and hyperlinks

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/web-scraper-tool.git

# Install dependencies
pip install -r requirements.txt

# Run the tool
python web_scraper_tool.py
```

### Requirements

- Python 3.14+
- tkinter (usually included with Python)
- requests
- beautifulsoup4

## 📖 How to Use

1. **Enter Target URL**: Type the website URL you want to scrape
2. **Enter CSS Selector**: Specify the element to extract (e.g., `.price`, `h1`, `#product-name`)
3. **Choose Options**: Select text and/or link extraction
4. **Click "Start Scraping"**: Extract the data
5. **Export Results**: Save as CSV or JSON file

### Example

```
URL: https://example.com/products
Selector: .product-title
Result: All product titles from the page
```

## 🎯 Use Cases

- Price monitoring from e-commerce sites
- News headlines collection
- Product information gathering
- Contact information extraction
- Market research data collection

## ⚠️ IMPORTANT DISCLAIMER

**This tool is provided "AS IS" without warranty of any kind.**

### Legal Compliance
- **You are responsible** for checking the website's Terms of Service before scraping
- Some websites prohibit automated data collection
- Respect robots.txt and rate limits
- **The developer is not liable** for any legal issues arising from misuse

### Technical Limitations
- Website structure changes may break the tool
- No guarantee of 100% accuracy
- Network issues may cause failures
- Some websites may block automated requests

### No Warranty
- No guarantee of uptime or continuous operation
- Data extracted may be incomplete or incorrect
- **Not responsible for business decisions** made with this tool
- No liability for any damages or losses

### Your Responsibility
- Ensure legal compliance in your jurisdiction
- Verify extracted data accuracy
- Use responsibly and ethically
- Check website policies before use

## 🛠️ Troubleshooting

**Problem**: No elements found
- **Solution**: Check if the CSS selector is correct. Use browser DevTools to find the right selector.

**Problem**: Connection timeout
- **Solution**: Check your internet connection. Some websites may be blocking automated requests.

**Problem**: Program freezes
- **Solution**: The website may be slow. Wait or try a smaller page.

## 📝 License

MIT License - Use at your own risk. See LICENSE file for details.

## 🤝 Support

- This is a standalone tool delivered as-is
- For bugs or issues, please open a GitHub issue
- No ongoing support or maintenance included
- Updates for website changes are not guaranteed

## ⚡ Version

**Version 1.0.0** - Initial Release

---

**Built by Dumok Data Lab**

*Remember: Always scrape responsibly and legally.*
