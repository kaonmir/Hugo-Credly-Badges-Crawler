from github import Github, GithubException

from settings import REPOSITORY, GH_TOKEN, GH_API_URL, COMMIT_MESSAGE, CREDLY_DIR
import sys, base64
import json


class GithubRepo:
    def __init__(self):
        self.COMMIT_MESSAGE = COMMIT_MESSAGE

        # Automatic GitHub API detection.
        g = Github(base_url=GH_API_URL, login_or_token=GH_TOKEN)

        try:
            self.repo = g.get_repo(REPOSITORY)
        except GithubException:
            print(
                "Authentication Error. Try saving a GitHub Token in your Repo Secrets or Use the GitHub Actions Token, which is automatically used by the action."
            )
            sys.exit(1)
        try:
            self.contents_repo = self.repo.get_contents(CREDLY_DIR)
        except Exception:
            print("The JSON file cannot be obtained!")

    def save_json(self, new_json):
        new_content = json.dumps(new_json, indent=4)

        try:
            old_json = self.get_json()

            if old_json == new_json:
                print("No changes in the JSON file")
                return

            self.repo.update_file(
                path=CREDLY_DIR,
                message=self.COMMIT_MESSAGE,
                content=new_content,
                sha=self.contents_repo.sha,
                branch="main",
            )
        except AttributeError:
            self.repo.create_file(
                path=CREDLY_DIR,
                message=self.COMMIT_MESSAGE,
                content=new_content,
                branch="main",
            )

    def get_json(self):
        return json.loads(str(base64.b64decode(self.contents_repo.content), "utf-8"))
