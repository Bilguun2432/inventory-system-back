import io
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from ssl import create_default_context
import qrcode
from fastapi.encoders import jsonable_encoder


class MailBody:
    def __init__(self, body: str, to: list, subject: str):
        self.body = body
        self.to = to
        self.subject = subject

HOST = "smtp.gmail.com"
PORT = 587
USERNAME = "hazardsober540@gmail.com"
PASSWORD = "eoqkirhvsnjlywxm"


def send_mail(email: str, number: str, jsonString: str ):
    data = jsonable_encoder(jsonString)
    amount = data['data']['amount']
    vat = data['data']['vat']
    date = data['data']['date']
    lottery = data['data']['lottery']
    merchantId =  data['data']['merchantId']
    qrData =  data['data']['qrData']
    billId = data['data']['billId']
    # return True
    try:
        data = {
        "body": "Qrcode email",
        "to": [email],
        "subject": "Ebarim qrcode"
        }
        msg = MailBody(**data)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qrData)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_byte_stream = io.BytesIO()
        qr_img.save(qr_byte_stream)
        qr_byte_stream.seek(0)

        message = MIMEMultipart()
        body = f"""
        <html>
            <body>
                <div style="border: 2px solid black; width: 350px; padding: 15px; " >
                    <table style=" width: 350px;">
                        <tr>
                            <td colspan="2" style="padding: 10px; text-align: center; font-weight: bold;">"ЖИ-МОБАЙЛ" ХХК</td>
                        </tr>
                        <tr>
                            <td colspan="2" style="font-size: 14px; padding-bottom: 10px; padding-left: 5px; padding-right: 5px; text-align: center; font-weight: 600;">ҮҮРЭН ХОЛБОНЫ ҮНДЭСНИЙ ОПЕРАТОР БЭЛЭН МӨНГӨНИЙ ТООЦООНЫ ХУУДАС</td>
                        </tr>
                        <tr>
                            <td  >Баримтын №</td>
                            <td style="text-align: end;">{billId}</td>
                        </tr>
                        <tr>
                            <td  >Хэвлэсэн огноо:</td>
                            <td style="text-align: end;">{date}</td>
                        </tr>
                        <tr>
                            <td>Салбар:</td>
                            <td style="text-align: end;">01</td>
                        </tr>
                        <tr>
                            <td>Гүйлгээний дугаар:</td>
                            <td style="text-align: end;">{merchantId}</td>
                        </tr>
                    </table >

                    
                    <table style=" width: 350px;">
                        <tr>
                            <td colspan="3" style="background-color: black; height: 2px;"></td>
                        </tr>
                        <tr>
                            <td>ТӨРӨЛ</td>
                            <td>ДУГААР</td>
                            <td>ҮНЭ</td>
                        </tr>
                        <tr>
                            <td>Төлбөр төлөх</td>
                            <td>{number}</td>
                            <td>{amount}</td>
                        </tr>
                    </table>
                    <table style=" width: 350px;">
                        <tr>
                            <td colspan="4" style="background-color: black; height: 2px;"></td>
                        </tr>
                        <tr>
                            <td rowspan="2" style="padding: 10px; text-align: center;">
                                <img style="width: 150px;" src="cid:qr_image" alt="QR Code">
                            </td>
                            <td rowspan="2" style="text-align: right;">
                                <table style=" height:100%; width: 100%; "  >
                                    <tr >
                                        <td colspan="2" style=" text-align: end; font-weight: bold;">{lottery}</td>
                                    </tr>
                                    <tr>
                                        <td> 
                                            <br>
                                            <br>
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>НӨАТ 10%</td>
                                        <td style="text-align: end;">{vat}</td>
                                    </tr>
                                    <tr>
                                        <td>НИЙТ ДҮН</td>
                                        <td style="text-align: end;"> {amount}</td>
                                    </tr>
                                </table >
                            </td>
                        </tr>
                    </table>
                    <table style="width: 350px;">
                        <tr>
                            <td colspan="3" style="padding-top: 5px; text-align: center;">Та төлбөрийн баримтаа хадгална уу</td>
                        </tr>
                        <tr>
                            <td colspan="3" style="text-align: center;">ЖИМОБАЙЛ ХХК-Р ҮЙЛЧЛҮҮЛСЭН ТАНД БАЯРЛАЛАА</td>
                        </tr>
                        <tr  >
                            <td>Утас: 98103636</td>
                            <td>Лавлах: 3636</td>
                            <td>Факс: 311195</td>
                        </tr>
                    </table>
                </div>
            </body>
        </html>
        """
        html_body = MIMEText(body, 'html')
        message.attach(html_body)

        qr_image = MIMEImage(qr_byte_stream.read())
        qr_image.add_header('Content-ID', '<qr_image>')
        qr_image.add_header('Content-Disposition', 'attachment', filename='qr_code.png')
        message.attach(qr_image)

        message['From'] = USERNAME
        message['To'] = ', '.join(msg.to)
        message['Subject'] = msg.subject

        ctx = create_default_context()
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.sendmail(USERNAME, msg.to, message.as_string())
            server.quit()
        return True
    except:
        return False
    
    