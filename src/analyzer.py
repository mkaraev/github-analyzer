from src import github, parser
from src.filters import *
from copy import deepcopy


class TimeRange:
    def __init__(self, since=None, until=None):
        self.since = since
        self.until = until
        if since:
            self.since = parser.string_to_datetime(since)
        if until:
            self.until = parser.string_to_datetime(until)


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
            "sha": self.repo.branch,
            "since": time_range.since,
            "until": time_range.until
        }

    def get_most_active_contributors(self, n=30):
        commits = github.get_commits(self.repo.owner, self.repo.name, **self.params)
        author_commits = dict()
        for commit in commits:
            if commit["author"]:
                login = commit["author"]["login"]
                cnt = author_commits.get(login, 0) + 1
                author_commits[login] = cnt

        contributors = sorted(list(author_commits.items()), key=lambda x: x[1], reverse=True)[:n]
        return contributors

    def get_data_count(self, data_type="pulls", state="open", old=False):
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
