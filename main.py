# import and install
import csv
import requests
import os


# Open the CSV file
input_file = input("Enter the filePath to the CSV: ")
# output_file = input("Enter the output folder for the new CSV: ")


def run():

    with open(input_file, 'r') as file:
        # Create a CSV reader
        reader = csv.reader(file)

        # Get the headers from the first line
        CSVHeaders = next(reader)

        # Store the rows
        rows = list(reader)

        ticket_id_index = CSVHeaders.index("ID")

    # Prepare the data for the new CSV file
    new_rows = []

    # Loop over the rows
    for row in rows:

        ticket_id_value = row[ticket_id_index]
        print(ticket_id_value)
        # Create a dictionary mapping headers to row entries
        # data = {header: value for header, value in zip(headers, row)}

        # Make the API call
        # response = requests.get('your_api_endpoint', params=data, headers={
        #                         'Authorization': 'Bearer your_api_key'})

        url = "https://comms-gpt.aws-otk-stage-general-use1-001.otk.twilioinfra.com/v1/tasks/analyze-tts?ticketId={}".format(
            ticket_id_value)

        payload = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        print(response.text)

        # Add the API response to the row
        row.append(response.json())

        # Add the row to the new rows
        new_rows.append(row)

    # Add the new header
    CSVHeaders.append('api_response')

    # Write the new CSV file
    with open('your_file_with_responses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSVHeaders)
        writer.writerows(new_rows)

    return None


def main():
    run()


if __name__ == "__main__":
    main()
