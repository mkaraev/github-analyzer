from src import github, parser
from src.filters import *
from copy import deepcopy


class GithubAnalyzer:

    def __init__(self, owner, repo, branch="master", since=None, until=None):
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.since = since
        self.until = until

        self.params = {
            "sha": branch
        }
        if since:
            self.params["since"] = parser.string_to_datetime(since)
        if until:
            self.params["until"] = parser.string_to_datetime(until)

    def get_most_active_contributors(self, n=30):
        commits = github.get_commits(self.owner, self.repo)
        print(commits)
        contributors = get_most_active_authors(commits, n)
        return contributors

    def get_pulls_stats(self, state="open", old=False):
        params = deepcopy(self.params)
        params["state"] = state

        filters = [range_filter_fabric(self.since, self.until), ]
        if old:
            filters.append(old_filter_fabric(OLD_ISSUE_DAYS))

        get_pulls = apply_filters(filters)(github.get_pulls)
        pulls = get_pulls(self.owner, self.repo, **params)
        return len(pulls)

    def get_issues_stats(self, state="open", old=False):
        params = deepcopy(self.params)
        params["state"] = state

        filters = [range_filter_fabric(self.since, self.until), ]
        if old:
            filters.append(old_filter_fabric(OLD_PULLS_DAYS))

        get_issues = apply_filters(filters)(github.get_issues)
        issues = get_issues(self.owner, self.repo, **params)
        return len(issues)
