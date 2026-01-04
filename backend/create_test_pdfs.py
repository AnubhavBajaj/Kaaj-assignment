from reportlab.pdfgen import canvas
import os

def create_test_pdfs():
    os.makedirs("lender_pdfs", exist_ok=True)
    
    # EF Credit Box / Stearns Bank Test
    c = canvas.Canvas("lender_pdfs/EF Credit Box 4.14.2025.pdf")
    c.drawString(100, 800, "Stearns Bank N.A.")
    c.drawString(100, 780, "Standard Program Details:")
    c.drawString(100, 760, "Min FICO: 700")
    c.drawString(100, 740, "Min PayNet: 650")
    c.drawString(100, 720, "Time in Business: 2 years")
    c.drawString(100, 700, "Excluded Industries: Cannabis, Gambling")
    c.save()

    # Apex Test
    c = canvas.Canvas("lender_pdfs/Apex_Policies.pdf")
    c.drawString(100, 800, "Apex Commercial Capital")
    c.drawString(100, 780, "A Credit: 650+ FICO, 2 Years TIB")
    c.drawString(100, 760, "Restricted States: CA, NV, ND, VT")
    c.save()
    
    print("PDFs created successfully.")

if __name__ == "__main__":
    create_test_pdfs()
