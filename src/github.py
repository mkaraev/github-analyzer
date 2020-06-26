import requests

BASE_URL = "https://api.github.com/repos/{owner}/{repo}"
COMMITS_URL = f"{BASE_URL}/commits"
PULLS_URL = f"{BASE_URL}/pulls"
ISSUES_URL = f"{BASE_URL}/issues"


def getter_fabric(url_pattern: str):
    def get_data(*args, **kwargs):
        url = url_pattern.format(owner=args[0], repo=args[1])
        response = requests.get(url=url, params=kwargs)
        if response.status_code != 200:
            raise Exception(response.json()["message"])

        data = response.json()
        return data

    return get_data


get_commits = getter_fabric(COMMITS_URL)
get_pulls = getter_fabric(PULLS_URL)
get_issues = getter_fabric(ISSUES_URL)
