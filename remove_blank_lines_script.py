import csv

def remove_empty_lines(in_fnam, out_fnam):
    with open(in_fnam, newline='') as in_file:
        with open(out_fnam, 'w', newline='') as out_file:
            writer = csv.writer(out_file)
            for row in csv.reader(in_file):
                if row:
                    writer.writerow(row)


INPUT_FILE_PATH = 'cleaned_data_copy.csv'
OUTPUT_FILE_PATH = 'cleaned_data_no_blanks.csv'

remove_empty_lines(INPUT_FILE_PATH, OUTPUT_FILE_PATH)