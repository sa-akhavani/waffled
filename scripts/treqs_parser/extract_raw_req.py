import sys
import ast

def extract_raw_request_byte_strings(filename):
    raw_request_list = []

    with open(filename, 'r') as file:
        for line in file:
            # Convert the string representation of the dictionary to an actual dictionary
            try:
                record = ast.literal_eval(line.strip())
                if 'raw_request_byte_string' in record:
                    raw_request_list.append(record['raw_request_byte_string'])
            except (SyntaxError, ValueError) as e:
                print(f"Skipping line due to parsing error: {line.strip()}")
                continue

    return raw_request_list

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_raw_requests.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    raw_requests = extract_raw_request_byte_strings(input_file)

    for raw_request in raw_requests:
        print(raw_request)

