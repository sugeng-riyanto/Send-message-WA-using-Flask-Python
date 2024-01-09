from flask import Flask, render_template, request, flash
import pandas as pd
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# WhatsApp Business API credentials
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
PHONE_NUMBER = 'YOUR_WHATSAPP_PHONE_NUMBER'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_messages', methods=['POST'])
def send_messages():
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                contacts = read_contacts(file)
                if contacts:
                    sent_count = send_whatsapp_messages(contacts)
                    flash(f"Messages sent to {sent_count} contacts successfully!", 'success')
                    return render_template('index.html')
            flash('Invalid file or no contacts found.', 'error')
    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')

    return render_template('index.html')

def allowed_file(filename):
    return filename.lower().endswith(('.csv', '.xlsx'))

def read_contacts(file):
    try:
        if file.filename.endswith('.csv'):
            return read_csv(file)
        elif file.filename.endswith('.xlsx'):
            return read_excel(file)
    except Exception as e:
        raise RuntimeError(f"Error reading contacts file: {str(e)}")

def read_csv(file):
    try:
        df = pd.read_csv(file)
        if all(col in df.columns for col in ['Phone', 'Name', 'Text', 'Other Message']):
            return df[['Phone', 'Name', 'Text', 'Other Message']].dropna().astype(str).to_dict(orient='records')
    except Exception as e:
        raise RuntimeError(f"Error reading CSV file: {str(e)}")

def read_excel(file):
    try:
        df = pd.read_excel(file)
        if all(col in df.columns for col in ['Phone', 'Name', 'Text', 'Other Message']):
            return df[['Phone', 'Name', 'Text', 'Other Message']].dropna().astype(str).to_dict(orient='records')
    except Exception as e:
        raise RuntimeError(f"Error reading Excel file: {str(e)}")

def send_whatsapp_messages(contacts):
    sent_count = 0
    for contact in contacts:
        message = {
            "phone": contact['Phone'],
            "body": f"Hello {contact['Name']}!\n{contact['Text']}\n{contact['Other Message']}"
        }
        if send_message_to_whatsapp_api(message):
            sent_count += 1
    return sent_count

def send_message_to_whatsapp_api(message):
    try:
        url = f"https://api.whatsapp.com/send?phone={message['phone']}&text={message['body']}"
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for bad responses
        return True
    except requests.RequestException as e:
        raise RuntimeError(f"Error sending message to {message['phone']}: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
