#!/usr/bin/env python3
"""
Multimodal Document Analyzer
A simple demonstration of analyzing PDFs using both visual and textual features
"""

import os
import json
import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

# Core libraries
try:
    from PIL import Image
    import cv2
    from pdf2image import convert_from_path
    from PyPDF2 import PdfReader
    import re
except ImportError as e:
    print(f"Missing required library: {e}")
    print("Please run: pip install -r requirements.txt")
    exit(1)


class MultimodalDocumentAnalyzer:
    """Analyzes PDFs using both visual and textual features"""
    
    def __init__(self):
        self.risk_keywords = [
            'liability', 'penalty', 'breach', 'termination', 'indemnify',
            'damages', 'lawsuit', 'arbitration', 'confidential', 'proprietary',
            'non-compete', 'exclusive', 'irrevocable', 'perpetual'
        ]
        self.visual_patterns = {
            'signature_region': {'min_area': 5000, 'aspect_ratio_range': (2, 6)},
            'stamp_region': {'min_area': 3000, 'circularity_threshold': 0.7}
        }
        
    def analyze_document(self, pdf_path: str) -> Dict:
        """Main analysis function that combines visual and text analysis"""
        print(f"\n🔍 Analyzing document: {pdf_path}")
        
        results = {
            'filename': os.path.basename(pdf_path),
            'timestamp': datetime.now().isoformat(),
            'visual_analysis': {},
            'text_analysis': {},
            'combined_risk_score': 0,
            'risk_factors': [],
            'recommendations': []
        }
        
        # Extract text features
        text_features = self.extract_text_features(pdf_path)
        results['text_analysis'] = text_features
        
        # Extract visual features
        visual_features = self.extract_visual_features(pdf_path)
        results['visual_analysis'] = visual_features
        
        # Combine analyses for final risk score
        results['combined_risk_score'] = self.calculate_combined_risk(
            text_features, visual_features
        )
        
        # Generate recommendations
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def extract_text_features(self, pdf_path: str) -> Dict:
        """Extract and analyze textual content from PDF"""
        print("  📄 Extracting text features...")
        
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            full_text = ""
            page_count = len(reader.pages)
            
            for page_num in range(page_count):
                page = reader.pages[page_num]
                full_text += page.extract_text() + "\n"
        
        # Analyze text
        risk_keyword_count = sum(
            full_text.lower().count(keyword) 
            for keyword in self.risk_keywords
        )
        
        # Find monetary amounts
        money_pattern = r'\$[\d,]+\.?\d*[MKB]?|\d+\s*(?:million|thousand|billion)'
        monetary_amounts = re.findall(money_pattern, full_text, re.IGNORECASE)
        
        # Calculate text risk score
        text_risk_score = min(100, risk_keyword_count * 5)
        
        return {
            'page_count': page_count,
            'total_words': len(full_text.split()),
            'risk_keywords_found': risk_keyword_count,
            'monetary_amounts': monetary_amounts[:5],  # Top 5
            'text_risk_score': text_risk_score,
            'high_risk_sections': self.find_high_risk_sections(full_text)
        }
    
    def extract_visual_features(self, pdf_path: str) -> Dict:
        """Extract and analyze visual features from PDF"""
        print("  🖼️  Extracting visual features...")
        
        # Convert first page to image for analysis
        try:
            images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=150)
            if not images:
                return {'error': 'Could not convert PDF to image'}
                
            # Convert PIL image to OpenCV format
            img_pil = images[0]
            img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
            
            # Detect visual elements
            signatures = self.detect_signature_regions(img_cv)
            stamps = self.detect_stamp_regions(img_cv)
            layout_score = self.analyze_layout_consistency(img_cv)
            
            # Calculate visual risk score
            visual_risk_score = 0
            if len(signatures) == 0:
                visual_risk_score += 30  # No signature found
            if len(stamps) > 2:
                visual_risk_score += 20  # Too many stamps might indicate tampering
            if layout_score < 0.7:
                visual_risk_score += 25  # Inconsistent layout
                
            return {
                'signatures_detected': len(signatures),
                'stamps_detected': len(stamps),
                'layout_consistency_score': round(layout_score, 2),
                'visual_risk_score': visual_risk_score,
                'anomalies': self.detect_visual_anomalies(img_cv)
            }
            
        except Exception as e:
            print(f"    ⚠️  Visual analysis error: {e}")
            return {'error': str(e), 'visual_risk_score': 50}
    
    def detect_signature_regions(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detect potential signature regions in the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Use edge detection to find signature-like regions
        edges = cv2.Canny(gray, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        signatures = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > self.visual_patterns['signature_region']['min_area']:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / h if h > 0 else 0
                min_ar, max_ar = self.visual_patterns['signature_region']['aspect_ratio_range']
                if min_ar <= aspect_ratio <= max_ar:
                    signatures.append((x, y, w, h))
        
        return signatures
    
    def detect_stamp_regions(self, image: np.ndarray) -> List[Tuple[int, int, int]]:
        """Detect circular stamp-like regions"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect circles using Hough transform
        circles = cv2.HoughCircles(
            gray, cv2.HOUGH_GRADIENT, dp=1, minDist=100,
            param1=50, param2=30, minRadius=30, maxRadius=100
        )
        
        if circles is not None:
            circles = np.uint16(np.around(circles))
            return [(c[0], c[1], c[2]) for c in circles[0, :]]
        return []
    
    def analyze_layout_consistency(self, image: np.ndarray) -> float:
        """Analyze overall layout consistency"""
        # Simple layout analysis based on text region detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Threshold to find text regions
        _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
        
        # Calculate text density in different quadrants
        h, w = binary.shape
        quadrants = [
            binary[0:h//2, 0:w//2],
            binary[0:h//2, w//2:w],
            binary[h//2:h, 0:w//2],
            binary[h//2:h, w//2:w]
        ]
        
        densities = [np.mean(q) / 255 for q in quadrants]
        
        # Consistency score based on standard deviation
        consistency = 1 - (np.std(densities) / np.mean(densities) if np.mean(densities) > 0 else 0)
        return min(1.0, max(0.0, consistency))
    
    def detect_visual_anomalies(self, image: np.ndarray) -> List[str]:
        """Detect potential visual anomalies"""
        anomalies = []
        
        # Check for unusual color distributions (might indicate tampering)
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [50, 60], [0, 180, 0, 256])
        
        if np.max(hist) > np.mean(hist) * 10:
            anomalies.append("Unusual color concentration detected")
        
        # Check for copy-paste artifacts (repeated patterns)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        orb = cv2.ORB_create()
        kp, des = orb.detectAndCompute(gray, None)
        
        if len(kp) > 500:
            anomalies.append("High number of similar features (possible copy-paste)")
        
        return anomalies
    
    def find_high_risk_sections(self, text: str) -> List[str]:
        """Find sections of text with high risk indicators"""
        sections = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            risk_count = sum(keyword in line.lower() for keyword in self.risk_keywords)
            if risk_count >= 2:
                context = ' '.join(lines[max(0, i-1):min(len(lines), i+2)])
                sections.append(context[:200] + "...")
                
        return sections[:3]  # Return top 3 high-risk sections
    
    def calculate_combined_risk(self, text_features: Dict, visual_features: Dict) -> float:
        """Calculate combined risk score from all features"""
        text_score = text_features.get('text_risk_score', 0)
        visual_score = visual_features.get('visual_risk_score', 0)
        
        # Weighted combination (text gets more weight for legal documents)
        combined = (text_score * 0.6 + visual_score * 0.4)
        
        # Add penalties for specific conditions
        if visual_features.get('signatures_detected', 0) == 0:
            combined += 10  # No signature is a red flag
            
        if len(text_features.get('monetary_amounts', [])) > 3:
            combined += 5  # Multiple monetary amounts increase risk
            
        return min(100, combined)
    
    def generate_recommendations(self, results: Dict) -> List[str]:
        """Generate actionable recommendations based on analysis"""
        recommendations = []
        risk_score = results['combined_risk_score']
        
        if risk_score >= 70:
            recommendations.append("⚠️ HIGH RISK: Recommend legal review before signing")
        elif risk_score >= 40:
            recommendations.append("⚡ MEDIUM RISK: Review highlighted sections carefully")
        else:
            recommendations.append("✅ LOW RISK: Standard document, safe to proceed")
            
        if results['visual_analysis'].get('signatures_detected', 0) == 0:
            recommendations.append("📝 No signatures detected - ensure proper signing")
            
        if len(results['text_analysis'].get('high_risk_sections', [])) > 0:
            recommendations.append("🔍 Review high-risk sections for unfavorable terms")
            
        if results['visual_analysis'].get('anomalies', []):
            recommendations.append("🚨 Visual anomalies detected - verify document authenticity")
            
        return recommendations


def create_sample_report(results: Dict) -> str:
    """Create a formatted report from analysis results"""
    report = f"""
╔══════════════════════════════════════════════════════════════╗
║          MULTIMODAL DOCUMENT ANALYSIS REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

📄 Document: {results['filename']}
📅 Analysis Date: {results['timestamp'][:10]}

═══════════════════════════════════════════════════════════════
                    RISK ASSESSMENT
═══════════════════════════════════════════════════════════════

🎯 Overall Risk Score: {results['combined_risk_score']:.1f}/100
   Text Risk: {results['text_analysis']['text_risk_score']}/100
   Visual Risk: {results['visual_analysis']['visual_risk_score']}/100

═══════════════════════════════════════════════════════════════
                    TEXT ANALYSIS
═══════════════════════════════════════════════════════════════

📊 Document Statistics:
   • Pages: {results['text_analysis']['page_count']}
   • Words: {results['text_analysis']['total_words']:,}
   • Risk Keywords: {results['text_analysis']['risk_keywords_found']}

💰 Monetary Amounts Found:
   {chr(10).join('   • ' + amt for amt in results['text_analysis'].get('monetary_amounts', ['None'])[:3])}

═══════════════════════════════════════════════════════════════
                    VISUAL ANALYSIS
═══════════════════════════════════════════════════════════════

🖼️ Visual Features:
   • Signatures Detected: {results['visual_analysis'].get('signatures_detected', 'N/A')}
   • Official Stamps: {results['visual_analysis'].get('stamps_detected', 'N/A')}
   • Layout Consistency: {results['visual_analysis'].get('layout_consistency_score', 'N/A')}

🔍 Anomalies:
   {chr(10).join('   • ' + a for a in results['visual_analysis'].get('anomalies', ['None']))}

═══════════════════════════════════════════════════════════════
                    RECOMMENDATIONS
═══════════════════════════════════════════════════════════════

{chr(10).join(results['recommendations'])}

═══════════════════════════════════════════════════════════════
"""
    return report


def main():
    """Main function to run the analyzer"""
    print("\n🚀 Multimodal Document Analyzer v1.0")
    print("=" * 50)
    
    # Check if sample PDF exists
    sample_pdf = "sample.pdf"
    
    if not os.path.exists(sample_pdf):
        print(f"\n❌ No {sample_pdf} found in current directory")
        print("Please provide a PDF file named 'sample.pdf' to analyze")
        return
    
    # Create analyzer instance
    analyzer = MultimodalDocumentAnalyzer()
    
    # Analyze the document
    try:
        results = analyzer.analyze_document(sample_pdf)
        
        # Generate and print report
        report = create_sample_report(results)
        print(report)
        
        # Save results to JSON
        with open('analysis_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        print("💾 Detailed results saved to: analysis_results.json")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")


if __name__ == "__main__":
    main() 