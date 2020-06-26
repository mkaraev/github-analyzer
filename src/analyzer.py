from src import github, parser
from src.filters import *
from copy import deepcopy


class TimeRange:
    def __init__(self, since=None, until=None):
        self.since = since
        self.until = until


class GithubRepository:
    def __init__(self, owner, repo, branch="master"):
        self.owner = owner
        self.name = repo
        self.branch = branch


class GithubAnalyzer:
    OLD_ISSUE_DAYS = 14
    OLD_PULLS_DAYS = 30

    OLD_DAYS = {
        "issues": OLD_ISSUE_DAYS,
        "pulls": OLD_PULLS_DAYS
    }

    github_api = {
        "issues": github.get_issues,
        "pulls": github.get_pulls,
    }

    def __init__(self, repo: GithubRepository, time_range: TimeRange):
        self.repo = repo
        self.time_range = time_range

        self.params = {
            "sha": self.repo.branch
        }
        if time_range.since:
            self.params["since"] = parser.string_to_datetime(time_range.since)
        if time_range.until:
            self.params["until"] = parser.string_to_datetime(time_range.until)

    def get_most_active_contributors(self, n=30):
        commits = github.get_commits(self.repo.owner, self.repo.name)
        contributors = get_most_active_authors(commits, n)
        return contributors

    def get_data(self, data_type="pulls", state="open", old=False):
        params = deepcopy(self.params)
        params["state"] = state

        filters = [range_filter_fabric(self.time_range.since, self.time_range.until), ]
        if old:
            filters.append(old_filter_fabric(
                GithubAnalyzer.OLD_DAYS[data_type])
            )

        get_data = apply_filters(filters)(GithubAnalyzer.github_api[data_type])
        pulls = get_data(self.repo.owner, self.repo.name, **params)
        return len(pulls)
