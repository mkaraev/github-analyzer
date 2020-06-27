import time

from texttable import Texttable

from src.analyzer import GithubAnalyzer, GithubRepository, TimeRange
from src.parser import parse_url, get_parser


def main():
    arg_parser = get_parser()
    args = arg_parser.parse_args()
    print("Args: ", args)
    owner, repo = parse_url(args.url)
    since = args.since
    until = args.until
    branch = args.branch

    for i in range(args.retry):
        wait = i * 10
        print(f"Try to get data after {wait} second")
        time.sleep(wait)
        try:
            time_range = TimeRange(since=since, until=until)
            repo = GithubRepository(owner, repo, branch)
            analyzer = GithubAnalyzer(repo=repo, time_range=time_range)

            contributors = analyzer.get_most_active_contributors()
            contributors_table = Texttable()
            contributors_table.add_row(("Contributor", "Number of commits"))
            for contributor in contributors:
                contributors_table.add_row(contributor)

            table = Texttable()
            table.add_rows(
                [
                    ["Description", "count"],
                    ["Open pulls created in given range: ", analyzer.get_data_count(data_type="pulls", state="open")],
                    ["Closed pulls in given range: ", analyzer.get_data_count(data_type="pulls", state="closed")],
                    ["Old pulls in given range: ", analyzer.get_data_count(data_type="pulls", state="open", old=True)],
                    ["Open issues created in given range: ", analyzer.get_data_count(data_type="issues", state="open")],
                    ["Closed issues created in given range: ", analyzer.get_data_count(data_type="issues", state="closed")],
                    ["Old issues created in given range: ",
                     analyzer.get_data_count(data_type="issues", state="open", old=True)],

                ]
            )
            print(contributors_table.draw())
            print(table.draw())
            return
        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()
