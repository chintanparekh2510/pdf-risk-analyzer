# Multimodal Document Analyzer 🔍

A Python tool that analyzes PDF documents using both visual and textual features to detect risks, anomalies, and important patterns. Unlike traditional text-only analysis, this tool "sees" documents like humans do.

## 🚀 What Makes This Special

Traditional PDF analysis: `PDF → Extract Text → Analyze Text`  
**This approach**: `PDF → Extract Text + Visual Features → Combined Analysis`

The analyzer can detect:
- 📝 Missing or suspicious signatures
- 🔴 Visual tampering indicators
- 💰 Financial risks and monetary amounts
- ⚖️ Legal risk keywords and patterns
- 🎯 Layout inconsistencies

## 📋 Prerequisites

- Python 3.8+
- Windows users need [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) for PDF to image conversion
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) (optional, for enhanced text extraction)

## 🛠️ Installation

1. Clone this repository:
```bash
git clone https://github.com/chintanparekh2510/pdf-risk-analyzer.git
cd pdf-risk-analyzer
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. **For Windows users**: 
   - Download Poppler from [here](https://github.com/oschwartz10612/poppler-windows/releases/)
   - Extract and add the `bin` folder to your PATH

## 🎯 Quick Start

1. Place your PDF file in the project directory and name it `test_document.pdf` (or run `python create_test_pdf.py` to generate one)

2. Run the analyzer:
```bash
python document_analyzer_simple.py
```

3. Check the results:
   - Console output shows the formatted report
   - `analysis_results.json` contains detailed analysis data

## 📊 Example Output

```
╔══════════════════════════════════════════════════════════════╗
║          MULTIMODAL DOCUMENT ANALYSIS REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

📄 Document: contract.pdf
📅 Analysis Date: 2024-01-19

🎯 Overall Risk Score: 72.5/100
   Text Risk: 65/100
   Visual Risk: 85/100

📊 Document Statistics:
   • Pages: 5
   • Words: 2,341
   • Risk Keywords: 13

💰 Monetary Amounts Found:
   • $5,000,000
   • $250,000
   • $1.5M

🖼️ Visual Features:
   • Signatures Detected: 0
   • Official Stamps: 3
   • Layout Consistency: 0.82

⚠️ HIGH RISK: Recommend legal review before signing
📝 No signatures detected - ensure proper signing
```

## 🔧 How It Works

1. **Text Analysis**: Extracts text and searches for risk keywords, monetary amounts, and concerning clauses
2. **Visual Analysis**: Processes document as images to detect signatures, stamps, and visual anomalies
3. **Risk Scoring**: Combines both analyses to generate a comprehensive risk score
4. **Recommendations**: Provides actionable insights based on findings

## 🎨 Customization

You can modify risk keywords and visual patterns in the `MultimodalDocumentAnalyzer` class:

```python
self.risk_keywords = [
    'liability', 'penalty', 'breach', 'termination', 
    # Add your domain-specific keywords
]

self.visual_patterns = {
    'signature_region': {'min_area': 5000, 'aspect_ratio_range': (2, 6)},
    # Adjust detection parameters
}
```

## 📝 Use Cases

- **Contract Review**: Identify high-risk clauses before signing
- **Document Verification**: Detect potential tampering or forgery
- **Compliance Checking**: Ensure documents meet visual standards
- **Due Diligence**: Quick risk assessment of legal documents

## ⚠️ Limitations

- This is a demonstration tool, not a replacement for legal review
- Visual analysis accuracy depends on document quality
- Best results with standard business documents

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

MIT License - feel free to use in your projects! 