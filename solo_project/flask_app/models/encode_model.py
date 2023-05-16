from flask import send_file
import io

def encode_ducky(ducky_script):
    # Implement the logic to encode the Ducky Script
    # You can use any encoding algorithm or library here
    encoded_script = ducky_script.upper()  # Example: convert the script to uppercase

    # Create a file-like object in memory
    file_stream = io.BytesIO(encoded_script.encode())

    # Send the file as a downloadable attachment
    response = send_file(
        file_stream,
        mimetype='text/plain'
    )
    response.headers.set('Content-Disposition', 'attachment', filename='encoded_script.txt')

    return response
