import os, sys
import uuid
import subprocess

def split_domain_file(input_filename, output_dir, num_files=10):
    """
    Splits a large domain name file into a specified number of smaller files
    in a uniquely named output directory.

    :param input_filename: Path to the input domain name file.
    :param num_files: Number of smaller files to create.
    :return: The name of the output directory.
    """
    if not os.path.isfile(input_filename):
        print(f"Error: The file {input_filename} does not exist.")
        return

    
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    with open(input_filename, 'r') as file:
        domains = file.read().splitlines()
    
    total_domains = len(domains)
    domains_per_file = total_domains // num_files
    remainder = total_domains % num_files

    start_index = 0
    for i in range(num_files):
        end_index = start_index + domains_per_file + (1 if i < remainder else 0)
        with open(os.path.join(output_dir, f"domains_part_{i+1}.txt"), 'w') as out_file:
            out_file.write('\n'.join(domains[start_index:end_index]) + '\n')
        start_index = end_index
    
    print(f"Successfully split {total_domains} domains into {num_files} files in '{output_dir}'.")
    return output_dir  # Return the name of the output directory


# def open_terminal_for_files(directory, script_name):
#     """
#     Opens a new terminal window for each file in the specified directory
#     and runs the given script to process each file.

#     :param directory: Path to the directory containing files.
#     :param script_name: The script to run for processing each file.
#     """
#     if not os.path.isdir(directory):
#         print(f"Error: The directory {directory} does not exist.")
#         return

#     # List all files in the directory
#     files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

#     for file in files:
#         file_path = os.path.join(directory, file)
#         # Command to open a new terminal and run the script
#         # Adjust the command based on your OS (e.g., 'gnome-terminal', 'xterm', etc.)
#         command = f"python {script_name} {file_path}"
        
#         # For Linux (using gnome-terminal)
#         subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', command + '; exec bash'])

#         # For macOS (using Terminal)
#         # subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "{command}"'])

#         # For Windows (using cmd)
#         # subprocess.Popen(['start', 'cmd', '/k', command], shell=True)

#     print(f"Opened terminal windows for {len(files)} files.")

def open_terminal_for_files(directory, script_name):
    """
    Opens a new terminal tab for each file in the specified directory
    and runs the given script to process each file after activating a virtual environment.

    :param directory: Path to the directory containing files.
    :param script_name: The script to run for processing each file.
    :param venv_path: Path to the Python virtual environment to activate.
    """
    if not os.path.isdir(directory):
        print(f"Error: The directory {directory} does not exist.")
        return

    # List all files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    for file in files:
        file_path = os.path.join(directory, file)
        # Command to run the script after activating the virtual environment
        command = f"python {script_name} {file_path}"
        
        # For Linux (using gnome-terminal to open a new tab)
        # subprocess.Popen(['gnome-terminal', '--tab', '--', f'bash -c "{command}; exec bash"'])
        subprocess.Popen(command, shell=True)

        # For macOS (using Terminal)
        # subprocess.Popen(['osascript', '-e', f'tell application "Terminal" to do script "source {venv_path}/bin/activate && python {script_name} {file_path}"'])

        # For Windows (using PowerShell)
        # subprocess.Popen(['start', 'powershell', '-NoExit', f'source {venv_path}/Scripts/activate && python {script_name} {file_path}'], shell=True)

    print(f"Opened terminal tabs for {len(files)} files.")

if __name__ == "__main__":
    try:
        input_filename = sys.argv[1]  # The large file containing domains
        num_files = int(sys.argv[2])
        # Generate a unique ID for the output directory
        unique_id = str(uuid.uuid4())
        output_dir = f"split_domains_{unique_id}"
        # num_files = 10  # Desired number of output files
        

        # Split the large domain name file into smaller files
        split_domain_file(input_filename, output_dir, num_files)

        # Now open a terminal for each split file
        open_terminal_for_files(output_dir, 'main4.py')

    except Exception as err:
        print(f"Usage: python main.py <filename>\n{err}")