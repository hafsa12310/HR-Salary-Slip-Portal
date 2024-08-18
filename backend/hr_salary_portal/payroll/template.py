from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle


def draw_payslip_layout(c, employee, width, height, logo_path):
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(0.5*inch, 0.5*inch, width - 1*inch, height - 1*inch, stroke=1, fill=0)

    logo_height = height - 2.2*inch
    c.drawImage(logo_path, inch, logo_height, width=2.5*inch, height=1*inch)

    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - inch, height - 1.2*inch, "Unikrew Solutions")
    c.setFont("Helvetica", 10)
    c.drawRightString(width - inch, height - 1.4*inch, "230/C1, Block - 02 P.E.C.H.S.")
    c.drawRightString(width - inch, height - 1.6*inch, "Karachi, Pakistan")
    c.drawRightString(width - inch, height - 1.8*inch, "Phone: (021) 33261303")

   
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 2.2*inch, f"PaySlip")


    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, height - 3.2*inch, f"Employee: {employee['first_name']} {employee['last_name']}")
    c.setFont("Helvetica", 10)
    c.drawString(inch, height - 3.5*inch, f"Employee ID: {employee['emp_id']}")
    c.drawString(inch, height - 3.8*inch, f"Department: {employee['department']}")
    c.drawString(inch, height - 4.1*inch, f"Position: {employee['position']}")
    c.drawString(inch, height - 4.4*inch, f"Email: {employee['email']}")

    data = [
        ["Description", "Amount"],
        ["Base Pay", f"PKR{employee.get('base_pay', 0.00):,.2f}"],
        ["Allowances", f"PKR{employee.get('allowances', 0.00):,.2f}"],
        ["Deductions", f"PKR{employee.get('deductions', 0.00):,.2f}"],
        ["Net Salary", f"PKR{employee.get('net_salary', 0.00):,.2f}"],
    ]

    table = Table(data, colWidths=[3*inch, 3*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
        ('TOPPADDING', (0, 1), (-1, -1), 10),
    ]))

    table.wrapOn(c, width, height)
    table.drawOn(c, inch, height - 7.3*inch)

    c.setFont("Helvetica-Oblique", 8)
    c.drawString(inch, inch, "This is a computer-generated document and does not require a signature.")
