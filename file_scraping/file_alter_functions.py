import os


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
