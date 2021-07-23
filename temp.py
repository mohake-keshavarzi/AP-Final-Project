from github import Github
from github import InputGitTreeElement
import os
acsses_token = "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"
g = Github(acsses_token)

repo = g.get_user().get_repo("images")
all_files = []
contents = repo.get_contents("")
while contents:
    file_content = contents.pop(0)
    if file_content.type == "dir":
        contents.extend(repo.get_contents(file_content.path))
    else:
        file = file_content
        all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))
for file_name in os.listdir("images2"):
    with open("images2/"+file_name , 'rb') as file:
        content = file.read()

    # Upload to github
    git_prefix = 'images2/'
    git_file = git_prefix + file_name
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", content, contents.sha, branch="master")
        print(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", content, branch="master")
        print(git_file + ' CREATED')