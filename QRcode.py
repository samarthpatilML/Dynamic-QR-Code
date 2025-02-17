from flask import Flask, redirect, url_for
import qrcode
from io import BytesIO
from flask import send_file

app = Flask(__name__)

@app.route('/generate-qr/<data>')
def generate_qr(data):
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")
    
    # Save the image in a BytesIO object
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    src= bitcode
    
    return send_file(buffer, mimetype='image/png')

@app.route('/dynamic-link')
def dynamic_link():
    # This could be a dynamic link, for example, based on database content
    return redirect("https://www.example.com")

if __name__ == "__main__":
    app.run(debug=True)
