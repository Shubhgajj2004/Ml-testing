# Define the file path for the text file
file_path = "info.txt"

# Read the content of the text file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Extract the values
index = int(lines[0].strip())  # First value is the index
text_file1 = lines[1].strip()  # Second line is text_file1
text_file2 = lines[2].strip()  # Third line is text_file2

# Print or use the extracted values
print(f"Index: {index}")
print(f"Text File 1: {text_file1}")
print(f"Text File 2: {text_file2}")

index = 0  # First value is the index
text_file1 = lines[1].strip()  # Second line is text_file1
text_file2 = lines[2].strip()

with open(file_path, 'w') as file:
    file.write(f"{index}\n")
    file.write(f"{text_file1}\n")
    file.write(f"{text_file2}\n")
