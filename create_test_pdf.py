from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import random

def create_test_pdf(filename="test_document.pdf"):
    """Create a test PDF with random contract-like content"""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height - 100, "SERVICE AGREEMENT")
    
    # Date
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 150, f"Date: {datetime.now().strftime('%B %d, %Y')}")
    
    # Parties
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, height - 200, "PARTIES:")
    
    c.setFont("Helvetica", 12)
    text = [
        "This Agreement is entered into between:",
        "1. TechCorp Solutions Inc. ('Service Provider')",
        "2. Global Enterprises Ltd. ('Client')",
        "",
        "WHEREAS, the Service Provider agrees to provide software development",
        "services to the Client under the following terms and conditions:",
        "",
        "1. SCOPE OF SERVICES",
        "The Service Provider shall develop and deliver a custom software solution",
        "with the following specifications:",
        "- Web-based application with user authentication",
        "- Database integration and API development",
        "- Mobile responsive design",
        "- Deployment and maintenance support",
        "",
        "2. PAYMENT TERMS",
        f"Total project cost: ${random.randint(50, 200) * 1000:,}",
        "Payment schedule: 30% upfront, 40% mid-project, 30% on completion",
        "Late payment penalty: 1.5% per month",
        "",
        "3. CONFIDENTIALITY",
        "Both parties agree to maintain strict confidentiality regarding",
        "proprietary information and trade secrets disclosed during this engagement.",
        "",
        "4. LIABILITY AND INDEMNIFICATION",
        "The Service Provider's liability shall be limited to the total contract value.",
        "Each party shall indemnify the other against third-party claims.",
        "",
        "5. TERMINATION",
        "Either party may terminate this agreement with 30 days written notice.",
        "In case of breach, immediate termination is permitted.",
        "",
        "6. GOVERNING LAW",
        "This agreement shall be governed by the laws of Delaware, USA.",
        "",
        "IN WITNESS WHEREOF, the parties have executed this Agreement:",
        "",
        "_______________________                    _______________________",
        "Service Provider                           Client",
        "Name: John Smith                           Name: Jane Doe",
        "Title: CEO                                 Title: VP Operations",
        "Date: _______________                      Date: _______________"
    ]
    
    y_position = height - 250
    for line in text:
        if line.startswith(("1.", "2.", "3.", "4.", "5.", "6.")):
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 11)
        
        c.drawString(100, y_position, line)
        y_position -= 20
        
        # Add new page if needed
        if y_position < 100:
            c.showPage()
            y_position = height - 100
    
    c.save()
    print(f"Created test PDF: {filename}")

if __name__ == "__main__":
    create_test_pdf() 