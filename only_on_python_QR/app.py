from flask import Flask, request, redirect, url_for, send_file, jsonify
import qrcode
from io import BytesIO

app = Flask(__name__)

# In-memory storage for dynamic links (you can replace this with a database)
qr_code_data = {}

# Route to generate a dynamic QR code based on a codeId
@app.route('/generate-qr/<codeId>', methods=['GET'])
def generate_qr(codeId):
    if codeId not in qr_code_data:
        return jsonify({'error': 'QR Code not found.'}), 404

    # Generate the QR code pointing to the dynamic link
    url = url_for('dynamic_link', codeId=codeId, _external=True)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # Serve the image as a response
    return send_file(buffer, mimetype='image/png')

# Route to dynamically redirect users to the target URL associated with the codeId
@app.route('/dynamic-link/<codeId>', methods=['GET'])
def dynamic_link(codeId):
    if codeId not in qr_code_data:
        return jsonify({'error': 'Link not found.'}), 404

    # Redirect to the target URL
    return redirect(qr_code_data[codeId])

# API route to create a new dynamic QR code entry
@app.route('/create-qr', methods=['POST'])
def create_qr():
    try:
        # Parse JSON request data
        data = request.get_json()
        if not data or 'codeId' not in data or 'targetUrl' not in data:
            return jsonify({'error': 'Invalid request data. Must include codeId and targetUrl'}), 400
        
        codeId = data['codeId']
        targetUrl = data['targetUrl']

        # Save the dynamic URL in memory (you can save this in a database)
        qr_code_data[codeId] = targetUrl

        return jsonify({'message': f'QR Code created for {codeId} pointing to {targetUrl}'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# API route to update an existing QR code target URL
@app.route('/update-qr/<codeId>', methods=['PUT'])
def update_qr(codeId):
    try:
        data = request.get_json()
        if not data or 'newUrl' not in data:
            return jsonify({'error': 'Invalid request data. Must include newUrl'}), 400
        
        newUrl = data['newUrl']

        if codeId not in qr_code_data:
            return jsonify({'error': 'QR Code not found.'}), 404

        # Update the target URL
        qr_code_data[codeId] = newUrl

        return jsonify({'message': f'QR Code {codeId} updated to point to {newUrl}'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
