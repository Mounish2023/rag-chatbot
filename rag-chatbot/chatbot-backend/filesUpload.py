import requests

# The URL to which the request will be sent
url = 'http://localhost:7071/api/DataProcessing'

# The path to the file you wish to upload
file_path = '../../Mounish_Sunkara_Resume.pdf'

# Open the file in binary mode
with open(file_path, 'rb') as file:
    # Define the name of the file field (key) and the file to be uploaded (value)
    files = {'file': (file_path, file)}
    
    # Send a POST request with the file
    response = requests.post(url, files=files)

# Check if the request was successful
if response.status_code == 200:
    print('File uploaded successfully.')
else:
    print('Failed to upload the file.')

# Print the server's response
print(response.text)
