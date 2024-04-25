# import and install
import csv
import requests
import os


def run():

    # Open the CSV file
    input_file = input("Enter the filePath to the CSV: ")
    # output_file = input("Enter the output folder for the new CSV: ")
    runCSVDataInAPI(input_file)


def runCSVDataInAPI(input_file):

    with open(input_file, 'r') as file:
        try:
            # Create a CSV reader
            reader = csv.reader(file)

            # Get the headers from the first line
            CSVHeaders = next(reader)

            # Store the rows
            rows = list(reader)

            ticket_id_index = CSVHeaders.index("ID")
        except FileNotFoundError as err:
            raise SystemExit(
                f"The File could not be found or parsed\nPlease make sure you are using a valid CSV and your file path is correct\nSystem exit code {err}")

    # Prepare the data for the new CSV file
    new_rows = []
    count = 1

    # Loop over the rows
    for row in rows:

        ticket_id_value = row[ticket_id_index]
        print(f"now running {count} of {len(rows)}")

        url = "https://comms-gpt.aws-otk-stage-general-use1-001.otk.twilioinfra.com/v1/tasks/analyze-tts?ticketId={}".format(
            ticket_id_value)

        payload = {}
        headers = {}

        try:
            response = requests.request(
                "GET", url, headers=headers, data=payload)
            responseData = response.json()
            row.append(responseData["data"]["summary"])
            row.append(responseData["data"]["ttsDriver"])
            # print(response.text)
            # Add the row to the new rows
            new_rows.append(row)

        except Exception as err:
            print(f"case {ticket_id_value} gave an error {
                  err} when attempting to run")

        # Add the API response to the row
        # responseData = response.json()
        # row.append(responseData)
        # print(responseData["data"]["summary"])
        # print(responseData["data"]["ttsDriver"])
        # row.append(responseData["data"]["summary"])
        # row.append(responseData["data"]["ttsDriver"])
        count += 1

    # Add the new header
    CSVHeaders.append('summary')
    CSVHeaders.append("TTSDriver")

    createCSV(CSVHeaders, new_rows)


def createCSV(CSVHeaders, new_rows):
    # Write the new CSV file
    with open('your_file_with_responses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(CSVHeaders)
        writer.writerows(new_rows)


def main():
    run()


if __name__ == "__main__":
    main()
