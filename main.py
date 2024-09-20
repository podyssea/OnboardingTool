from file_scraping.file_alter_functions import replace_in_files
from git_functions.git_functions import onboard_new_repo, finalize_repo_setup

# onboard_new_repo(demo_repo_url, new_repo_url, repo_path)
# finalize_repo_setup(new_repo_url, repo_path, client_name)

# Example Usage:
replace_in_files(repo_path="./Testing", old_string="IQT", new_string="TRT")