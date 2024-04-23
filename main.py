# import and install
import csv
import subprocess
import sys
try:
    import requests
except ModuleNotFoundError:
    print("attempting to install requests")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])


# Open the CSV file
with open('your_file.csv', 'r') as file:
    # Create a CSV reader
    reader = csv.reader(file)

    # Get the headers from the first line
    headers = next(reader)

    # Store the rows
    rows = list(reader)

# Prepare the data for the new CSV file
new_rows = []

# Loop over the rows
for row in rows:
    # Create a dictionary mapping headers to row entries
    data = {header: value for header, value in zip(headers, row)}

    # Make the API call
    response = requests.get('your_api_endpoint', params=data, headers={
                            'Authorization': 'Bearer your_api_key'})

    # Add the API response to the row
    row.append(response.json())

    # Add the row to the new rows
    new_rows.append(row)

# Add the new header
headers.append('api_response')

# Write the new CSV file
with open('your_file_with_responses.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(new_rows)
