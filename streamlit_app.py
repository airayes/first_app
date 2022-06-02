import streamlit as st
from uttlv import TLV
import base64
import qrcode
from io import BytesIO

title_label = "**كيو ار كود الفاتورة الضريبية (QR Code)**"
name_label = "الاسم: "
tax_num_label = "رقم التسجيل الضريبي: "
invoice_date_label = "تاريخ الفاتورة: "
total_label = "المبلغ الاجمالي (بدون الضريبة): "
vat_label = "مبلغ الضريبة: "
submit_label = "إنشاء"
qr_info = "**بيانات الكيو ار كود**"
warning_lable = "فضلاً ادخل جميع البيانات المطلوبة"
wrong_tax_label = "الرقم الضريبي يجب ان يكون من 15 خانة"

st.write(title_label)

right, left = st.columns(2)

my_form = right.form('invoice_info', clear_on_submit=False)
name = my_form.text_input(name_label)
tax_num = my_form.text_input(tax_num_label, max_chars=15)
invoice_date = my_form.date_input(invoice_date_label)
total = my_form.number_input(total_label)
vat_amount = my_form.number_input(vat_label)
submit = my_form.form_submit_button(label=submit_label, help=None, on_click=None, args=None, kwargs=None)


def get_qrcode_b64():
    t1 = TLV()
    t1[1] = name
    t1[2] = tax_num
    t1[3] = f'{invoice_date.strftime("%Y-%m-%d")}T15:30:00Z'
    t1[4] = "{0:.2f}".format(total)
    t1[5] = "{0:.2f}".format(vat_amount)
    b64 = base64.b64encode(t1.to_byte_array())
    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(b64)
    img = qr.make_image()
    return convert_png_to_b64(img)


def convert_png_to_b64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    return img_str


if submit:
    if not name or not tax_num or not total or not vat_amount:
        left.warning(warning_lable)
        st.stop()
    if len(tax_num) != 15:
        left.warning(wrong_tax_label)
        st.stop()
    left.image(f"data:image/png;base64,{get_qrcode_b64().decode()}")
    left.write(qr_info)
    left.write(name_label + name)
    left.write(tax_num_label + tax_num)
    left.write(invoice_date_label + invoice_date.strftime("%Y-%m-%d"))
    left.write(total_label + "{0:.2f}".format(total))
    left.write(vat_label + "{0:.2f}".format(vat_amount))

style = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''

st.markdown(style, unsafe_allow_html=True)
