import subprocess
import time

def execute_command_from_file(file_path):
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        command = lines[-1].strip()  # Get the last line in the file
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Write the output back to the file
        file.write("\nCommand Output:\n")
        file.write(result.stdout)
        file.write(result.stderr)

def main():
    file_path = "/tmp/test"  # Replace with the path to your text file
    line_count = sum(1 for line in open(file_path))  # Get the initial number of lines in the file
    new_line_count = line_count

    while True:
        new_line_count = sum(1 for line in open(file_path))  # Get the current number of lines in the file
        if new_line_count > line_count:  # If a new command has been added
            execute_command_from_file(file_path)
            line_count = new_line_count  # Update the line count

        time.sleep(1)  # Wait for 1 second before checking the file again

if __name__ == "__main__":
    main()

