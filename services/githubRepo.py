from github import Github, GithubException

from settings import REPOSITORY, GH_TOKEN, GH_API_URL, COMMIT_MESSAGE, CREDLY_DIR
import sys, base64


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
        if self.contents_repo and self.contents_repo.content == new_json:
            print("No changes in the JSON file")
            return
        elif not self.contents_repo:
            self.repo.create_file(
                path=CREDLY_DIR,
                message=self.COMMIT_MESSAGE,
                content=new_json,
            )
        else:
            self.repo.update_file(
                path=CREDLY_DIR,
                message=self.COMMIT_MESSAGE,
                content=new_json,
                sha=self.contents_repo.sha,
            )

    def get_json(self):
        return str(base64.b64decode(self.contents_repo.content), "utf-8")
