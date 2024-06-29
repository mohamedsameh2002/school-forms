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



def generate_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val):
    # تهيئة المخزن المؤقت و القماش
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    pdfmetrics.registerFont(TTFont('Amiri-Bold', 'static/fonts/Amiri-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Amiri-Regular', 'static/fonts/Amiri-Regular.ttf'))

    title = "بيانات الطالب"
    title_reshaped = get_display(reshape(title))
    title_font_size = 28
    title_width = pdfmetrics.stringWidth(title_reshaped, "Amiri-Bold", title_font_size)

    # رسم العنوان في المنتصف
    title_x = (letter[0] - title_width) / 2
    title_y = .6 * inch  # ارتفاع العنوان مع التخفيض
    c.setFont("Amiri-Bold", title_font_size)
    c.setFillColorRGB(0, 0, 0)  
    c.drawString(title_x, title_y, title_reshaped)

    # رسم خط تحت العنوان
    line_y = title_y + 20  # ارتفاع الخط تحت العنوان
    c.setStrokeColorRGB(0, 0, 0)   
    c.line(title_x, line_y, title_x + title_width, line_y)  # خط تحت العنوان

    c.setStrokeColorRGB(117, 117, 117)  # اللون الرمادي

    # حساب الأبعاد للمستطيلات بناءً على النص "محمد"
    for i,a,b,d,f in zip([z for z in range(100)],column_1_lable,column_2_lable,column_1_value,column_2_value):
        if 1:
            text1 = f
            text1_reshaped = get_display(reshape(text1))
            text2 = d
            text2_reshaped = get_display(reshape(text2))

            text_font_size = 20
            text1_width = pdfmetrics.stringWidth(text1_reshaped, "Amiri-Regular", text_font_size)
            text2_width = pdfmetrics.stringWidth(text2_reshaped, "Amiri-Regular", text_font_size)
            text_height = pdfmetrics.getAscent("Amiri-Regular", text_font_size) - pdfmetrics.getDescent("Amiri-Regular", text_font_size)

            # تعيين عرض كل مستطيل (40% من عرض الصفحة)
            rect_width = letter[0] * 0.4
            rect_height = text_height + 10  # إضافة بعض الحشو حول النص

            # حساب المواضع للمستطيلات
            gap = 20  # الفجوة بين المستطيلات
            total_width = rect_width * 2 + gap  # العرض الكلي للمستطيلات والفجوة
            start_x = (letter[0] - total_width) / 2  # نقطة البداية للمستطيل الأول

            # حساب المسافة نحو اليمين لعنوان دينامكياً بناءً على عرض الكلمة
            title_above_rect1 = b
            title_above_rect1_reshaped = get_display(reshape(title_above_rect1))
            title1_width = pdfmetrics.stringWidth(title_above_rect1_reshaped, "Amiri-Regular", 22)
            offset_x1 = (rect_width - title1_width) / 1  # المسافة نحو اليمين لعنوان الأول

            title_above_rect2 = a
            title_above_rect2_reshaped = get_display(reshape(title_above_rect2))
            title2_width = pdfmetrics.stringWidth(title_above_rect2_reshaped, "Amiri-Regular", 22)
            offset_x2 = (rect_width - title2_width) / 1  # المسافة نحو اليمين لعنوان الثاني

            # رسم 4 مجموعات من المستطيلات والنصوص
            rect1_y = (letter[1] - rect_height) / 5.5 + i * (rect_height + 1 * inch)
            rect2_y = rect1_y

            # رسم المستطيل الأول
            c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
            c.rect(start_x, rect1_y, rect_width, rect_height, fill=1)
            # كتابة "عنوان" فوق المستطيل الأول بحجم خط 22
            c.setFont("Amiri-Regular", 22)  # حجم الخط للعنوان فوق المستطيل
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(start_x + offset_x1, rect1_y + rect_height - 55, title_above_rect1_reshaped)

            # رسم المستطيل الثاني
            rect2_x = start_x + rect_width + gap
            c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
            c.rect(rect2_x, rect2_y, rect_width, rect_height, fill=1)
            # كتابة "عنوان 2" فوق المستطيل الثاني بحجم خط 22
            c.setFont("Amiri-Regular", 22)  # حجم الخط للعنوان فوق المستطيل
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(rect2_x + offset_x2, rect2_y + rect_height - 55, title_above_rect2_reshaped)

            # تعديل موضع النص "محمد" و "عمرو"
            text_y = rect1_y + (rect_height - text_height) / 2 + 20  # زيادة 10 لتحريكه لأسفل قليلاً
            c.setFont("Amiri-Regular", text_font_size)  # حجم الخط للنص
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(start_x + (rect_width - text1_width) / 2, text_y, text1_reshaped)
            c.drawString(rect2_x + (rect_width - text2_width) / 2, text_y, text2_reshaped)
        else:
            text1 = three_val[2]
            text1_reshaped = get_display(reshape(text1))
            text2 = three_val[0]
            text2_reshaped = get_display(reshape(text2))
            text3 = three_val[1]
            text3_reshaped = get_display(reshape(text3))

            text_font_size = 20
            text1_width = pdfmetrics.stringWidth(text1_reshaped, "Amiri-Regular", text_font_size)
            text2_width = pdfmetrics.stringWidth(text2_reshaped, "Amiri-Regular", text_font_size)
            text3_width = pdfmetrics.stringWidth(text3_reshaped, "Amiri-Regular", text_font_size)
            text_height = pdfmetrics.getAscent("Amiri-Regular", text_font_size) - pdfmetrics.getDescent("Amiri-Regular", text_font_size)

            # تعيين عرض كل مستطيل (25% من عرض الصفحة)
            rect_width = letter[0] * 0.25
            rect_height = text_height + 10  # إضافة بعض الحشو حول النص

            # حساب المواضع للمستطيلات
            gap = 20  # الفجوة بين المستطيلات
            total_width = rect_width * 3 + gap * 2  # العرض الكلي للمستطيلات والفجوتين
            start_x = (letter[0] - total_width) / 2  # نقطة البداية للمستطيل الأول

            rect_y = (letter[1] - rect_height) / 5.5 + i * (rect_height + 1 * inch)

            # رسم المستطيل الأول
            rect1_x = start_x
            c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
            c.rect(rect1_x, rect_y, rect_width, rect_height, fill=1)

            # كتابة "الجنسية" فوق المستطيل الأول بحجم خط 22
            title_above_rect1 = "هل سبق له الدراسة"
            title_above_rect1_reshaped = get_display(reshape(title_above_rect1))
            title1_width = pdfmetrics.stringWidth(title_above_rect1_reshaped, "Amiri-Regular", 22)
            offset_x1 = (rect_width - title1_width) / 2  # المسافة نحو اليمين ديناميكية
            c.setFont("Amiri-Regular", 22)  # حجم الخط للعنوان فوق المستطيل
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(rect1_x + offset_x1, rect_y + rect_height - 55, title_above_rect1_reshaped)

            # رسم المستطيل الثاني
            rect2_x = start_x + rect_width + gap
            c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
            c.rect(rect2_x, rect_y, rect_width, rect_height, fill=1)

            # كتابة "المرحلة الدراسية" فوق المستطيل الثاني بحجم خط 22
            title_above_rect2 = "تاريخ اليلاد"
            title_above_rect2_reshaped = get_display(reshape(title_above_rect2))
            title2_width = pdfmetrics.stringWidth(title_above_rect2_reshaped, "Amiri-Regular", 22)
            offset_x2 = (rect_width - title2_width) / 2  # المسافة نحو اليمين ديناميكية
            c.setFont("Amiri-Regular", 22)  # حجم الخط للعنوان فوق المستطيل
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(rect2_x + offset_x2, rect_y + rect_height - 55, title_above_rect2_reshaped)

            # رسم المستطيل الثالث
            rect3_x = rect2_x + rect_width + gap
            c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
            c.rect(rect3_x, rect_y, rect_width, rect_height, fill=1)

            # كتابة "هل سبق له الدراسة" فوق المستطيل الثالث بحجم خط 22
            title_above_rect3 = "الجنسية"
            title_above_rect3_reshaped = get_display(reshape(title_above_rect3))
            title3_width = pdfmetrics.stringWidth(title_above_rect3_reshaped, "Amiri-Regular", 22)
            offset_x3 = (rect_width - title3_width) / 2  # المسافة نحو اليمين ديناميكية
            c.setFont("Amiri-Regular", 22)  # حجم الخط للعنوان فوق المستطيل
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(rect3_x + offset_x3, rect_y + rect_height - 55, title_above_rect3_reshaped)

            text_y = rect_y + (rect_height - text_height) / 2 + 20  # زيادة 10 لتحريكه لأسفل قليلاً
            c.setFont("Amiri-Regular", text_font_size)  
            c.setFillColorRGB(0, 0, 0)  
            c.drawString(rect1_x + (rect_width - text1_width) / 2, text_y, text1_reshaped)
            c.drawString(rect2_x + (rect_width - text2_width) / 2, text_y, text2_reshaped)
            c.drawString(rect3_x + (rect_width - text3_width) / 2, text_y, text3_reshaped)


    c.showPage()
    c.save()

    buf.seek(0)
    # return buf
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.svg"'
    return response





def send_email_with_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val,email):
    subject = "PDF Attachment"
    body = "Please find the PDF attached."
    from_email = 'sistar32.m@gmail.com'

    pdf_buffer = generate_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val)
    email = EmailMessage(subject, body, from_email, ['wzoneuk@gmail.com'])
    email.attach('hello.pdf', pdf_buffer.getvalue(), 'application/pdf')

    try:
        email.send()
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {str(e)}")











def registration_in_school (request):
    if request.method == 'POST':
        text_lines = [
        f"تاريخ الميلاد : {request.POST['date_of_birth']}",
        f"الجنسية : {request.POST['nationality']}",
    ]
        
        stud_name=request.POST['student_name']
        civil_no=request.POST['civil_no']
        date_of_birth=request.POST['date_of_birth']
        nationality=request.POST['nationality']
        previous_school=request.POST['previous_school']
        guardian_name=request.POST['guardian_name']
        phone_number=request.POST['phone_number']
        educational_level=request.POST['educational_level']
        the_job=request.POST['the_job']
        guardian_civil_no=request.POST['guardian_civil_no']
        prev_studied=request.POST['prev_studied']
        email=request.POST['email']
        
        column_1_lable=['اسم الطالب','اسم المدرسه السابقة','_','اسم ولي الامر','رقم الهاتف']
        column_2_lable=['الرقم المدني','المرحله الدراسيه','_','الوظيفة',' الرقم المدني لولي الأمر']
        column_1_value=[stud_name,previous_school,'_',guardian_name,phone_number]
        column_2_value=[civil_no,educational_level,'_',the_job,guardian_civil_no]
        three_val=[date_of_birth,nationality,prev_studied]
        return generate_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val)
    # return send_email_with_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val,email)
    return render(request,'forms/registration_in_school.html')