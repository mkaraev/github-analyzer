from src import filters, github, parser
from src.parser import parse_url, get_parser


def commits_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch
    }
    if since:
        params["since"] = parser.string_to_datetime(since)
    if until:
        params["until"] = parser.string_to_datetime(until)

    commits = github.get_commits(owner, repo, **params)
    return filters.get_most_active_authors(commits, 30)


def open_pulls_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "open"
    }
    pulls = github.get_pulls(owner, repo, **params)
    open_pulls_filter = filters.filter_applier_fabric(
        [
            filters.range_filter_fabric(since=since, until=until),
        ]
    )
    pulls = open_pulls_filter(pulls)
    return {
        "Open pulls created in given range: ": len(pulls)
    }


def closed_pulls_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "closed"
    }
    pulls = github.get_pulls(owner, repo, **params)
    closed_pulls_filter = filters.filter_applier_fabric(
        [
            filters.range_filter_fabric(since=since, until=until),
        ]
    )
    pulls = closed_pulls_filter(pulls)
    return {
        "Closed pulls in given range: ": len(pulls)
    }


def old_pulls_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "open"
    }
    pulls = github.get_pulls(owner, repo, **params)
    old_pulls_filter = filters.filter_applier_fabric([
        filters.old_filter_fabric(days=filters.OLD_PULLS_DAYS),
        filters.range_filter_fabric(since=since, until=until)
    ])

    pulls = old_pulls_filter(pulls)
    return {
        "Old pulls in given range: ": len(pulls)
    }


def open_issues_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "open"
    }
    issues = github.get_issues(owner, repo, **params)
    open_issues_filter = filters.filter_applier_fabric(
        [
            filters.range_filter_fabric(since=since, until=until),
        ]
    )
    issues = open_issues_filter(issues)
    return {
        "Open issues created in given range: ": len(issues)
    }


def closed_issues_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "closed"
    }
    issues = github.get_issues(owner, repo, **params)
    closed_issues_filter = filters.filter_applier_fabric(
        [
            filters.range_filter_fabric(since=since, until=until),
        ]
    )
    issues = closed_issues_filter(issues)
    return {
        "Closed issues in given range: ": len(issues)
    }


def old_issues_stats(owner, repo, branch, since, until):
    params = {
        "sha": branch,
        "state": "open"
    }
    issues = github.get_issues(owner, repo, **params)
    old_issues_filter = filters.filter_applier_fabric([
        filters.old_filter_fabric(days=filters.OLD_ISSUE_DAYS),
        filters.range_filter_fabric(since=since, until=until)
    ])

    issues = old_issues_filter(issues)
    return {
        "Old issues in given range: ": len(issues)
    }


def main():
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    print(args)
    owner, repo = parse_url(args.url)
    since = args.since
    until = args.until
    branch = args.branch

    #print(old_pulls_stats(owner=owner, repo=repo, branch=branch, since=since, until=until))

    stats_functions = [commits_stats, open_pulls_stats, closed_pulls_stats, old_pulls_stats,
                       open_issues_stats, closed_issues_stats, old_issues_stats]

    for stats_function in stats_functions:
        print(stats_function(owner=owner, repo=repo, branch=branch, since=since, until=until))


if __name__ == '__main__':
    main()
