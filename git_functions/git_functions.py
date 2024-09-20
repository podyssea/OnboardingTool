import subprocess
import git
import os
import shutil


def clone_mirror_repo(old_repo_url, new_repo_path):
    subprocess.run(["git", "clone", "--mirror", old_repo_url, new_repo_path], check=True)


def change_directory(new_repo_path):
    os.chdir(new_repo_path)


def remove_origin_remote():
    repo = git.Repo(os.getcwd())
    repo.delete_remote('origin')


def remove_all_branches_except_master():
    subprocess.run("git branch | grep -v 'master' | xargs git branch -D", shell=True, check=True)


def add_new_remote(new_repo_url):
    repo = git.Repo(os.getcwd())
    repo.create_remote('origin', new_repo_url)


def push_all_branches():
    repo = git.Repo(os.getcwd())
    repo.git.push('--all', 'origin')


def push_all_tags():
    repo = git.Repo(os.getcwd())
    repo.git.push('--tags', 'origin')


def onboard_new_repo(old_repo_url, new_repo_url, new_repo_path):
    try:
        # Step 1: Clone the repo with --mirror
        clone_mirror_repo(old_repo_url, new_repo_path)

        # Step 2: Change directory to the newly cloned repo
        change_directory(new_repo_path)

        # Step 3: Remove the old origin remote
        remove_origin_remote()

        # Step 4: Remove all branches except master
        remove_all_branches_except_master()

        # Step 5: Add new remote
        add_new_remote(new_repo_url)

        # Step 6: Push all branches
        push_all_branches()

        # Step 7: Push all tags
        push_all_tags()

        print("Repository successfully onboarded!")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except git.exc.GitCommandError as e:
        print(f"Git error: {e}")


def delete_existing_folder(repo_path):
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        print(f"Deleted folder: {repo_path}")
    else:
        print(f"Folder {repo_path} does not exist.")


def clone_new_repo(new_repo_url, repo_path):
    repo = git.Repo.clone_from(new_repo_url, repo_path)
    print(f"Cloned repo from {new_repo_url} to {repo_path}")
    return repo  # Return the repo object for further actions


def modify_dev_syncer(client_name, file_path='dev_syncer.sh'):
    with open(file_path, 'r') as file:
        content = file.read()

    updated_content = content.replace("Nullpoint_Demo", client_name)

    with open(file_path, 'w') as file:
        file.write(updated_content)

    print(f"Modified {file_path} to replace 'Nullpoint_Demo' with '{client_name}'")


def git_add_all(repo):
    repo.git.add(A=True)  # Adds all changes
    print("Added all changes to staging.")


def git_commit(repo, client_name):
    commit_message = f"Initial {client_name} commit"
    repo.index.commit(commit_message)
    print(f"Committed with message: {commit_message}")


def git_push_to_master(repo):
    repo.git.push('origin', 'master')
    print("Pushed changes to origin/master.")


def finalize_repo_setup(new_repo_url, repo_path, client_name):
    try:
        # Step 1: Delete the existing folder
        delete_existing_folder(repo_path)

        # Step 2: Clone the new repo
        repo = clone_new_repo(new_repo_url, repo_path)

        # Step 3: Modify dev_syncer.sh with the client name
        dev_syncer_path = os.path.join(repo_path, 'dev_syncer.sh')
        modify_dev_syncer(client_name, dev_syncer_path)

        # Step 4: Git add all changes
        git_add_all(repo)

        # Step 5: Git commit with client name
        git_commit(repo, client_name)

        # Step 6: Git push to master
        git_push_to_master(repo)

        print("Repository setup finalized!")

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
    except git.exc.GitCommandError as e:
        print(f"Git error: {e}")
