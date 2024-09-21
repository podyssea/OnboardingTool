import os

from git_functions.git_functions import onboard_new_repo


def replace_in_files(repo_path, old_string, new_string):
    for subdir, dirs, files in os.walk(repo_path):  # Traverse all subdirectories and files
        for file in files:
            file_path = os.path.join(subdir, file)

            # Read the file content with error handling for encoding issues
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace the old string with the new string
                if old_string in content:
                    content = content.replace(old_string, new_string)

                    # Write the modified content back to the file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

                    print(f"Replaced '{old_string}' with '{new_string}' in {file_path}")

            except Exception as e:
                print(f"An error occurred while processing {file_path}: {e}")


def replace_parameters_in_files(repo_path, replacements):
    for subdir, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(subdir, file)

            # Read and modify file content
            with open(file_path, 'r') as f:
                content = f.read()

            # Replace parameters based on the provided mapping
            for old_string, new_string in replacements.items():
                if old_string in content:
                    content = content.replace(old_string, new_string)
                    print(f"Replaced '{old_string}' with '{new_string}' in {file_path}")

            # Write the changes back to the file
            with open(file_path, 'w') as f:
                f.write(content)


def remove_code_for_platform(repo_path, platform_choice):
    platform_markers = {
        'MT4': ('# BEGIN_MT4', '# END_MT4'),
        'MT5': ('# BEGIN_MT5', '# END_MT5')
    }

    for subdir, dirs, files in os.walk(repo_path):
        for file in files:
            file_path = os.path.join(subdir, file)

            # Read and modify file content
            with open(file_path, 'r') as f:
                lines = f.readlines()

            new_content = []
            inside_mt4_block = False
            inside_mt5_block = False

            for line in lines:
                # Handle MT4 blocks
                if platform_choice != 'MT4' and platform_markers['MT4'][0] in line:
                    inside_mt4_block = True
                if inside_mt4_block and platform_markers['MT4'][1] in line:
                    inside_mt4_block = False
                    continue  # Skip the line

                # Handle MT5 blocks
                if platform_choice != 'MT5' and platform_markers['MT5'][0] in line:
                    inside_mt5_block = True
                if inside_mt5_block and platform_markers['MT5'][1] in line:
                    inside_mt5_block = False
                    continue  # Skip the line

                # If not inside a block to be removed, keep the line
                if not inside_mt4_block and not inside_mt5_block:
                    new_content.append(line)

            # Write the modified content back to the file
            with open(file_path, 'w') as f:
                f.writelines(new_content)

def onboard_new_repo_and_customize(old_repo_url, new_repo_url, repo_path, branch_name, replacements, platform_choice):
    try:
        # Phase A: Clone the repo
        # onboard_new_repo(old_repo_url, new_repo_url, repo_path)

        # Phase B: Replace all references of NPGL with the branch name
        replace_in_files(repo_path, 'NPGL', branch_name)

        # Phase C: Replace keys, ports, and passwords
        replace_parameters_in_files(repo_path, replacements)

        # Phase D: Remove or comment code based on the platform (MT4, MT5, or both)
        remove_code_for_platform(repo_path, platform_choice)

        print("Customization process completed successfully!")

    except Exception as e:
        print(f"Error during the customization process: {e}")

# Example mapping provided by the user (these would be collected via the frontend)
# replacements = {
#     'DB_PORT': '5432',
#     'DB_USERNAME': 'user123',
#     'DB_PASSWORD': 'password456',
#     'API_KEY': 'apikey789'
# }
#
# # Example Usage:
# replace_parameters_in_files(repo_path="./repo-clone", replacements=replacements)