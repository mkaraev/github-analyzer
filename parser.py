import argparse
from datetime import datetime


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", dest="url", type=str, help="Github repository url")
    parser.add_argument("--since", dest="since", type=str,
                        help="Date from which analyzing should be done. Format YYYY-MM-DD.")
    parser.add_argument("--until", dest="until", type=str,
                        help="Date until which analyzing should be done. Format YYYY-MM-DD")
    parser.add_argument("--branch", dest="branch", default="master",
                        help="Branch should be analyzed")
    return parser


def string_to_datetime(s):
    """Converts string to datetime. Uses iso8601_to_datetime function for converting,
    if datetime format's will change it's needed to write new converter and be called here."""

    return iso8601_to_datetime(s)


def iso8601_to_datetime(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S%z")


def parse_url(url: str):
    parts = url.split("/")
    owner = parts[-2]
    repo = parts[-1].split(".")[-1]
    return owner, repo
