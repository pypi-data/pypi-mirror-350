"""Poll Ecowitt weather and return an APRS WX string"""

from argparse import ArgumentParser
import requests
from requests.exceptions import HTTPError
import yaml


__all__ = ["transform"]


def find(d, path):
    keys = path.split("/")
    rv = d
    for key in keys:
        rv = rv[key]

    return float(rv["value"])


def ecowitt_to_aprs(content):
    if content["code"] != 0:
        raise HTTPError("Malformed response", content)

    wx = content["data"]

    float_data = [
        find(wx, "wind/wind_direction"),
        find(wx, "wind/wind_speed"),
        find(wx, "wind/wind_gust"),
        find(wx, "outdoor/temperature"),
        find(wx, "rainfall/hourly") * 100,
        find(wx, "rainfall/daily") * 100,
        find(wx, "rainfall/daily") * 100,
        find(wx, "outdoor/humidity"),
        find(wx, "pressure/absolute") * 33.8639 * 10,
    ]

    aprs_str = "{:03.0f}/{:03.0f}g{:03.0f}t{:03.0f}r{:03.0f}p{:03.0f}P{:03.0f}h{:02.0f}b{:05.0f}"

    return aprs_str.format(*float_data)


def transform(url, app_key, api_key, mac_addr):
    """Transform Ecowitt-formated JSON to APRS Complete Weather Report

    Args:
      url: the Ecowitt API base URL
      app_key: the Ecowitt Application Key
      api_key: the Ecowitt API key
      mac_addr: MAC address of the local Ecowitt device

    Returns:
      Nothing.  The APRS-formatted string is printed to stdout.
    """

    response = requests.get(
        url,
        params={
            "application_key": app_key,
            "api_key": api_key,
            "mac": mac_addr,
            "call_back": "all",
        },
    )

    response.raise_for_status()
    aprs_wx_str = ecowitt_to_aprs(response.json())
    print(aprs_wx_str)


def parseargs():
    argparser = ArgumentParser()
    argparser.add_argument(
        "-c", "--config", type=str, required=True, help="path to configuration file"
    )

    return argparser.parse_args()


def main():
    args = parseargs()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    transform(
        config["ecowitt_url"],
        config["ecowitt_app_key"],
        config["ecowitt_api_key"],
        config["ecowitt_mac_addr"],
    )


if __name__ == "__main__":
    main()
