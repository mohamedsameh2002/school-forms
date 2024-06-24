from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.http import HttpResponse,FileResponse
from django.core.mail import EmailMessage
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import reshape



def generate_pdf(lines):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    pdfmetrics.registerFont(TTFont('Amiri', 'static/fonts/Amiri-Bold.ttf'))

    # Set up the title
    title = "بيانات الطالب"
    title_reshaped = get_display(reshape(title))
    title_font_size = 28
    title_width = pdfmetrics.stringWidth(title_reshaped, "Amiri", title_font_size)

    # Draw the title in the center
    c.setFont("Amiri", title_font_size)
    c.setFillColorRGB(1, 0, 0)  # red color
    c.drawString((letter[0] - title_width) / 2, 1 * inch, title_reshaped)


    text_y_position = 2 * inch
    for line in lines:
        c.setFont("Amiri", 17)
        c.setFillColorRGB(0, 0, 0)  # black color
        c.drawString(5.5 * inch, text_y_position, get_display(reshape(line)))
        text_y_position += 0.4 * inch  # move to the next line

    # Finalize the PDF
    c.showPage()
    c.save()

    buf.seek(0)

    return buf
    # response = HttpResponse(buf, content_type='application/pdf')
    # response['Content-Disposition'] = 'filename="report.svg"'
    # return response





def send_email_with_pdf(text_lines):
    subject = "PDF Attachment"
    body = "Please find the PDF attached."
    from_email = 'sistar32.m@gmail.com'

    pdf_buffer = generate_pdf(text_lines)
    email = EmailMessage(subject, body, from_email, ["mohamed.403.sameh@gmail.com"])
    email.attach('hello.pdf', pdf_buffer.getvalue(), 'application/pdf')

    try:
        email.send()
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {str(e)}")











def registration_in_school (request):
    if request.method == 'POST':
        text_lines = [
        f"الاسم : {request.POST['student_name']}",
        f"الرقم المحلي : {request.POST['civil_no']}",
        f"تاريخ الميلاد : {request.POST['date_of_birth']}",
        f"الجنسية : {request.POST['nationality']}",
    ]
        return send_email_with_pdf(text_lines)
    return render(request,'forms/registration_in_school.html')
