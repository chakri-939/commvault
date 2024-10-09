from flask import Flask, request, render_template, Response, redirect, url_for
import boto3
from cryptography.fernet import Fernet

app = Flask(__name__)

# AWS S3 configuration
BUCKET_NAME = 'your-s3-bucket-name'

# Function to generate encryption key
def generate_key():
    return Fernet.generate_key()

# Function to encrypt image data
def encrypt_image(image_data, key):
    fernet = Fernet(key)
    return fernet.encrypt(image_data)

# Function to decrypt image data
def decrypt_image(encrypted_data, key):
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_data)

# Function to upload image
def upload_image_to_s3(file, encrypt=False):
    s3 = boto3.client('s3')

    # Read image file
    image_data = file.read()
    
    if encrypt:
        # Generate encryption key and encrypt image
        key = generate_key()  # Store the key securely
        encrypted_data = encrypt_image(image_data, key)

        # Store the encrypted image in S3
        s3_key = f'encrypted/{file.filename}'
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=encrypted_data)

        # Store the encryption key securely (you'll need a safe way to store it)
        return s3_key, key
    else:
        # Upload the original image
        s3_key = f'original/{file.filename}'
        s3.put_object(Bucket=BUCKET_NAME, Key=s3_key, Body=image_data)

        return s3_key, None  # No key for non-encrypted images

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['image']
    encrypt = 'encrypt' in request.form

    s3_key, key = upload_image_to_s3(file, encrypt)
    
    if encrypt:
        # Show the encryption key for downloading later
        return f'Uploaded successfully: {s3_key} <br> Encryption Key: {key.decode()} <br> <a href="/">Upload More Images</a>'
    return f'Uploaded successfully: {s3_key} <br> <a href="/">Upload More Images</a>'

@app.route('/list', methods=['GET'])
def list_images():
    s3 = boto3.client('s3')
    
    # Check if we need to filter by encrypted images
    show_encrypted = 'show_encrypted' in request.args

    # List objects in the bucket
    objects = s3.list_objects_v2(Bucket=BUCKET_NAME)
    images = []

    for obj in objects.get('Contents', []):
        if show_encrypted and not obj['Key'].startswith('encrypted/'):
            continue  # Skip non-encrypted images
        images.append(obj['Key'])
    
    return render_template('list_images.html', images=images)

@app.route('/download/<path:s3_key>', methods=['GET'])
def download_image(s3_key):
    s3 = boto3.client('s3')

    # Get the object from S3
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
    image_data = obj['Body'].read()

    # Send the encrypted file directly
    return Response(image_data, mimetype='application/octet-stream', headers={'Content-Disposition': f'attachment; filename={s3_key.split("/")[-1]}'})

@app.route('/decrypt/<path:s3_key>', methods=['GET', 'POST'])
def decrypt_image_view(s3_key):
    if request.method == 'POST':
        key = request.form['key'].encode()

        # Get the object from S3
        s3 = boto3.client('s3')
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=s3_key)
        encrypted_data = obj['Body'].read()

        try:
            # Decrypt the image
            decrypted_data = decrypt_image(encrypted_data, key)
            return Response(decrypted_data, mimetype='image/png', headers={'Content-Disposition': f'attachment; filename={s3_key.split("/")[-1]}'})
        except Exception as e:
            return f'Failed to decrypt: {str(e)}'
    
    return render_template('decrypt.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80,debug=True)