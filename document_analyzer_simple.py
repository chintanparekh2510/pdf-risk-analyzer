#!/usr/bin/env python3
"""
Multimodal Document Analyzer - Simplified Version
Works without poppler dependency - analyzes text and metadata
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List
import re
from PyPDF2 import PdfReader
import warnings
warnings.filterwarnings('ignore')


class SimpleDocumentAnalyzer:
    """Simplified analyzer that works without image processing dependencies"""
    
    def __init__(self):
        self.risk_keywords = [
            'liability', 'penalty', 'breach', 'termination', 'indemnify',
            'damages', 'lawsuit', 'arbitration', 'confidential', 'proprietary',
            'non-compete', 'exclusive', 'irrevocable', 'perpetual', 'waive',
            'default', 'violation', 'prosecution', 'negligence', 'warranty'
        ]
        
        self.high_risk_patterns = [
            r'unlimited\s+liability',
            r'personal\s+guarantee',
            r'joint\s+and\s+several',
            r'automatic\s+renewal',
            r'no\s+right\s+to\s+terminate',
            r'waive\s+all\s+rights'
        ]
    
    def analyze_document(self, pdf_path: str) -> Dict:
        """Main analysis function"""
        print(f"\n🔍 Analyzing document: {pdf_path}")
        
        results = {
            'filename': os.path.basename(pdf_path),
            'timestamp': datetime.now().isoformat(),
            'metadata': {},
            'text_analysis': {},
            'risk_assessment': {},
            'recommendations': []
        }
        
        # Extract metadata
        results['metadata'] = self.extract_metadata(pdf_path)
        
        # Extract and analyze text
        results['text_analysis'] = self.extract_text_features(pdf_path)
        
        # Perform risk assessment
        results['risk_assessment'] = self.assess_risks(results['text_analysis'])
        
        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def extract_metadata(self, pdf_path: str) -> Dict:
        """Extract PDF metadata"""
        print("  📋 Extracting metadata...")
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                metadata = reader.metadata
                
                return {
                    'pages': len(reader.pages),
                    'title': str(metadata.title) if metadata and metadata.title else 'Unknown',
                    'author': str(metadata.author) if metadata and metadata.author else 'Unknown',
                    'subject': str(metadata.subject) if metadata and metadata.subject else 'Unknown',
                    'creator': str(metadata.creator) if metadata and metadata.creator else 'Unknown',
                    'producer': str(metadata.producer) if metadata and metadata.producer else 'Unknown',
                    'creation_date': str(metadata.creation_date) if metadata and metadata.creation_date else 'Unknown',
                    'modification_date': str(metadata.modification_date) if metadata and metadata.modification_date else 'Unknown',
                    'encrypted': reader.is_encrypted
                }
        except Exception as e:
            print(f"    ⚠️  Metadata extraction error: {e}")
            return {'error': str(e)}
    
    def extract_text_features(self, pdf_path: str) -> Dict:
        """Extract and analyze textual content from PDF"""
        print("  📄 Extracting text features...")
        
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                full_text = ""
                page_count = len(reader.pages)
                
                # Extract text from all pages
                for page_num in range(page_count):
                    page = reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        full_text += page_text + "\n"
                
                # Analyze text
                text_lower = full_text.lower()
                
                # Count risk keywords
                keyword_counts = {}
                total_risk_keywords = 0
                for keyword in self.risk_keywords:
                    count = text_lower.count(keyword)
                    if count > 0:
                        keyword_counts[keyword] = count
                        total_risk_keywords += count
                
                # Find monetary amounts
                money_patterns = [
                    r'\$[\d,]+\.?\d*[MKB]?',
                    r'\d+\s*(?:million|thousand|billion|dollars|usd)',
                    r'USD\s*[\d,]+\.?\d*',
                    r'[€£¥]\s*[\d,]+\.?\d*'
                ]
                
                monetary_amounts = []
                for pattern in money_patterns:
                    matches = re.findall(pattern, full_text, re.IGNORECASE)
                    monetary_amounts.extend(matches)
                
                # Find dates
                date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})\b'
                dates_found = re.findall(date_pattern, full_text, re.IGNORECASE)
                
                # Find email addresses
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                emails_found = re.findall(email_pattern, full_text)
                
                # Check for signatures
                signature_indicators = ['signature', 'signed by', 'authorized signature', '/s/', 'by:', 'name:']
                signature_count = sum(1 for indicator in signature_indicators if indicator in text_lower)
                
                return {
                    'total_characters': len(full_text),
                    'total_words': len(full_text.split()),
                    'page_count': page_count,
                    'risk_keywords_found': total_risk_keywords,
                    'keyword_breakdown': keyword_counts,
                    'monetary_amounts': monetary_amounts[:10],  # Top 10
                    'dates_found': dates_found[:10],  # Top 10
                    'emails_found': emails_found[:5],  # Top 5
                    'signature_indicators': signature_count,
                    'high_risk_sections': self.find_high_risk_sections(full_text)
                }
                
        except Exception as e:
            print(f"    ⚠️  Text extraction error: {e}")
            return {'error': str(e), 'risk_keywords_found': 0}
    
    def find_high_risk_sections(self, text: str) -> List[Dict]:
        """Find sections of text with high risk indicators"""
        sections = []
        
        # Check for high-risk patterns
        for pattern in self.high_risk_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                start = max(0, match.start() - 100)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                sections.append({
                    'pattern': pattern,
                    'context': context,
                    'risk_level': 'HIGH'
                })
        
        # Find paragraphs with multiple risk keywords
        paragraphs = text.split('\n\n')
        for i, para in enumerate(paragraphs):
            para_lower = para.lower()
            risk_count = sum(1 for keyword in self.risk_keywords if keyword in para_lower)
            
            if risk_count >= 3:
                sections.append({
                    'pattern': f'{risk_count} risk keywords',
                    'context': para[:300] + '...' if len(para) > 300 else para,
                    'risk_level': 'MEDIUM' if risk_count < 5 else 'HIGH'
                })
        
        return sections[:10]  # Return top 10 high-risk sections
    
    def assess_risks(self, text_analysis: Dict) -> Dict:
        """Assess document risks based on text analysis"""
        print("  ⚡ Assessing risks...")
        
        risk_scores = {
            'keyword_risk': 0,
            'financial_risk': 0,
            'compliance_risk': 0,
            'signature_risk': 0,
            'overall_risk': 0
        }
        
        # Keyword risk (0-40 points)
        keyword_count = text_analysis.get('risk_keywords_found', 0)
        risk_scores['keyword_risk'] = min(40, keyword_count * 2)
        
        # Financial risk (0-30 points)
        monetary_amounts = text_analysis.get('monetary_amounts', [])
        if monetary_amounts:
            risk_scores['financial_risk'] = min(30, len(monetary_amounts) * 5)
            
            # Check for high amounts
            for amount in monetary_amounts:
                if 'million' in amount.lower() or 'M' in amount:
                    risk_scores['financial_risk'] = 30
                    break
        
        # Compliance risk (0-20 points)
        high_risk_sections = text_analysis.get('high_risk_sections', [])
        risk_scores['compliance_risk'] = min(20, len(high_risk_sections) * 4)
        
        # Signature risk (0-10 points)
        if text_analysis.get('signature_indicators', 0) == 0:
            risk_scores['signature_risk'] = 10
        
        # Calculate overall risk
        risk_scores['overall_risk'] = sum([
            risk_scores['keyword_risk'],
            risk_scores['financial_risk'],
            risk_scores['compliance_risk'],
            risk_scores['signature_risk']
        ])
        
        # Determine risk level
        overall = risk_scores['overall_risk']
        if overall >= 70:
            risk_level = 'HIGH'
        elif overall >= 40:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'LOW'
        
        risk_scores['risk_level'] = risk_level
        
        return risk_scores
    
    def generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        risk_assessment = results['risk_assessment']
        text_analysis = results['text_analysis']
        
        # Overall risk recommendation
        risk_level = risk_assessment['risk_level']
        if risk_level == 'HIGH':
            recommendations.append("⚠️ HIGH RISK: Strongly recommend legal review before signing")
            recommendations.append("🚨 Multiple risk factors detected - proceed with extreme caution")
        elif risk_level == 'MEDIUM':
            recommendations.append("⚡ MEDIUM RISK: Review highlighted sections carefully")
            recommendations.append("💡 Consider consulting legal counsel for specific clauses")
        else:
            recommendations.append("✅ LOW RISK: Document appears standard, but always review before signing")
        
        # Specific recommendations
        if risk_assessment['signature_risk'] > 0:
            recommendations.append("📝 No signature indicators found - ensure proper execution")
        
        if risk_assessment['financial_risk'] >= 20:
            recommendations.append("💰 High financial exposure detected - verify all monetary commitments")
        
        if risk_assessment['compliance_risk'] >= 15:
            recommendations.append("⚖️ Multiple compliance concerns - ensure regulatory alignment")
        
        if len(text_analysis.get('high_risk_sections', [])) > 5:
            recommendations.append("🔍 Numerous high-risk sections found - detailed review essential")
        
        # Add specific clause recommendations
        keyword_breakdown = text_analysis.get('keyword_breakdown', {})
        if 'indemnify' in keyword_breakdown or 'indemnification' in keyword_breakdown:
            recommendations.append("🛡️ Indemnification clauses present - review liability exposure")
        
        if 'termination' in keyword_breakdown:
            recommendations.append("🚪 Review termination clauses and exit strategies")
        
        if 'confidential' in keyword_breakdown or 'proprietary' in keyword_breakdown:
            recommendations.append("🔒 Confidentiality obligations present - ensure compliance capability")
        
        return recommendations


def create_detailed_report(results: Dict) -> str:
    """Create a formatted report from analysis results"""
    risk = results['risk_assessment']
    text = results['text_analysis']
    meta = results['metadata']
    
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║            DOCUMENT RISK ANALYSIS REPORT                     ║
╚══════════════════════════════════════════════════════════════╝

📄 Document: {results['filename']}
📅 Analysis Date: {results['timestamp'][:10]}

═══════════════════════════════════════════════════════════════
                    RISK ASSESSMENT SUMMARY
═══════════════════════════════════════════════════════════════

🎯 Overall Risk Level: {risk['risk_level']} ({risk['overall_risk']}/100)

📊 Risk Breakdown:
   • Keyword Risk:     {risk['keyword_risk']}/40
   • Financial Risk:   {risk['financial_risk']}/30
   • Compliance Risk:  {risk['compliance_risk']}/20
   • Signature Risk:   {risk['signature_risk']}/10

═══════════════════════════════════════════════════════════════
                    DOCUMENT METADATA
═══════════════════════════════════════════════════════════════

📋 Document Properties:
   • Pages: {meta.get('pages', 'Unknown')}
   • Author: {meta.get('author', 'Unknown')}
   • Created: {str(meta.get('creation_date', 'Unknown'))[:19]}
   • Modified: {str(meta.get('modification_date', 'Unknown'))[:19]}
   • Encrypted: {meta.get('encrypted', 'Unknown')}

═══════════════════════════════════════════════════════════════
                    TEXT ANALYSIS RESULTS
═══════════════════════════════════════════════════════════════

📊 Content Statistics:
   • Total Words: {text.get('total_words', 0):,}
   • Risk Keywords Found: {text.get('risk_keywords_found', 0)}
   • Signature Indicators: {text.get('signature_indicators', 0)}

🔑 Top Risk Keywords:
"""
    
    # Add keyword breakdown
    keyword_breakdown = text.get('keyword_breakdown', {})
    if keyword_breakdown:
        sorted_keywords = sorted(keyword_breakdown.items(), key=lambda x: x[1], reverse=True)[:5]
        for keyword, count in sorted_keywords:
            report += f"   • {keyword}: {count} occurrences\n"
    else:
        report += "   • None found\n"
    
    report += f"""
💰 Financial Exposures:
"""
    monetary = text.get('monetary_amounts', [])
    if monetary:
        for amount in monetary[:5]:
            report += f"   • {amount}\n"
    else:
        report += "   • No monetary amounts detected\n"
    
    report += f"""
⚠️ High Risk Sections: {len(text.get('high_risk_sections', []))} found

═══════════════════════════════════════════════════════════════
                    RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

"""
    
    for rec in results['recommendations']:
        report += f"{rec}\n"
    
    report += """
═══════════════════════════════════════════════════════════════

📌 Note: This is an automated analysis. Always consult with
   qualified professionals for final decision-making.
"""
    
    return report


def main():
    """Main function to run the analyzer"""
    print("\n🚀 Simple Document Analyzer v1.0")
    print("=" * 50)
    
    # Check if test PDF exists
    test_pdf = "test_document.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"\n❌ No {test_pdf} found in current directory")
        print("Please provide a PDF file named 'test_document.pdf' to analyze")
        
        # List available PDFs
        pdfs = [f for f in os.listdir('.') if f.endswith('.pdf')]
        if pdfs:
            print(f"\nAvailable PDFs: {', '.join(pdfs)}")
        return
    
    # Create analyzer instance
    analyzer = SimpleDocumentAnalyzer()
    
    # Analyze the document
    try:
        results = analyzer.analyze_document(test_pdf)
        
        # Generate and print report
        report = create_detailed_report(results)
        print(report)
        
        # Save results to JSON
        with open('analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("\n💾 Detailed results saved to: analysis_results.json")
        
        # Save report to text file
        with open('analysis_report.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        print("📄 Report saved to: analysis_report.txt")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 