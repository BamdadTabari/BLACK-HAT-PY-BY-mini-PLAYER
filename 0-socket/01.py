import socket
from bs4 import BeautifulSoup

target_host = "www.google.com"
target_port = 80

# Create a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the client
client.connect((target_host, target_port))

# Send some data
#client.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
client.send(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n indexof: python")

# Receive some data
response = client.recv(4096)

# Decode the response
html_content = response.decode()

# Close the connection
client.close()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find all links on the page
links = soup.find_all('a')
for link in links:
    print(link.get('href'))

# Search for the word "python"
if "python" in html_content.lower():
    print("The word 'python' was found.")
else:
    print("The word 'python' was not found.")
