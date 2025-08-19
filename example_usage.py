#!/usr/bin/env python3
"""
Example usage of the PDF Risk Analyzer
Created by @ChintanParekhAI (https://x.com/ChintanParekhAI)
"""

from document_analyzer_simple import SimpleDocumentAnalyzer
import sys
import os

def main():
    print("\n" + "="*60)
    print("PDF Risk Analyzer - Example Usage")
    print("Created by @ChintanParekhAI")
    print("="*60 + "\n")
    
    # Check if PDF file is provided
    if len(sys.argv) < 2:
        print("Usage: python example_usage.py <pdf_file>")
        print("Example: python example_usage.py contract.pdf")
        return
    
    pdf_file = sys.argv[1]
    
    if not os.path.exists(pdf_file):
        print(f"Error: File '{pdf_file}' not found!")
        return
    
    # Create analyzer instance
    analyzer = SimpleDocumentAnalyzer()
    
    # Analyze the document
    try:
        print(f"Analyzing: {pdf_file}")
        results = analyzer.analyze_document(pdf_file)
        
        # Display key findings
        risk_level = results['risk_assessment']['risk_level']
        risk_score = results['risk_assessment']['overall_risk']
        
        print(f"\n📊 QUICK SUMMARY:")
        print(f"   Risk Level: {risk_level}")
        print(f"   Risk Score: {risk_score}/100")
        print(f"   Keywords Found: {results['text_analysis']['risk_keywords_found']}")
        
        # Show top recommendations
        print(f"\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(results['recommendations'][:3], 1):
            print(f"   {i}. {rec}")
        
        print("\n✅ Analysis complete! Check 'analysis_results.json' for full details.")
        print("\n🔗 Follow @ChintanParekhAI on X for more AI tools and updates!")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 