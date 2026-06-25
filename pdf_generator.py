from reportlab.pdfgen import canvas

def create_pdf(name, domain, score):

    filename = f"{name}_report.pdf"

    c = canvas.Canvas(filename)

    c.drawString(
        100,
        750,
        f"Candidate: {name}"
    )

    c.drawString(
        100,
        720,
        f"Domain: {domain}"
    )

    c.drawString(
        100,
        690,
        f"Score: {score}/10"
    )

    c.save()

    return filename