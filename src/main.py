from src import filters, github, parser
from src.parser import parse_url, get_parser
from src.analyzer import GithubAnalyzer, GithubRepository, TimeRange
from texttable import Texttable


def main():
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    print(args)
    owner, repo = parse_url(args.url)
    since = args.since
    until = args.until
    branch = args.branch

    try:
        time_range = TimeRange(since, until)
        repo = GithubRepository(owner, repo, branch)
        analyzer = GithubAnalyzer(repo=repo, time_range=time_range)

        contributors = analyzer.get_most_active_contributors()
        table = Texttable()
        table.add_row(("Contributor", "Number of commits"))
        for contributor in contributors:
            table.add_row(contributor)
        print(table.draw())

        table = Texttable()
        table.add_rows(
            [
                ["Description", "count"],
                ["Open pulls created in given range: ", analyzer.get_data(data_type="pulls", state="open")],
                ["Closed pulls in given range: ", analyzer.get_data(data_type="pulls", state="closed")],
                ["Closed pulls in given range: ", analyzer.get_data(data_type="pulls", state="open", old=True)],
                ["Open issues created in given range: ", analyzer.get_data(data_type="issues", state="open")],
                ["Closed issues created in given range: ", analyzer.get_data(data_type="issues", state="closed")],
                ["Open issues created in given range: ", analyzer.get_data(data_type="issues", state="open", old=True)],

            ]
        )
        print(table.draw())
    except github.RateLimitException as error:
        print(error)


if __name__ == '__main__':
    main()
