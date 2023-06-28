import re
from services.credly import Credly
from services.githubRepo import GithubRepo

if __name__ == "__main__":
    git = GithubRepo()
    credly_badges = Credly()

    credly_json = credly_badges.get_json()
    git.save_json(credly_json)
