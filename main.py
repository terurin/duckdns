import requests as req
import schedule
import sys
import argparse
import json
import logging
import time


def main():
    # configurate parsers
    parser = argparse.ArgumentParser(description='tool for duckdns')
    parser.add_argument('--init', action='store_true',
                        help='create settings.json')
    parser.add_argument(
        '-m', '--mode', choices=['shot', 'repeat'], default='repeat')
    parser.add_argument('-o', '--out', default='log.out', help='save log file')
    parser.add_argument('-s', '--settings',
                        default='settings.json', help='settings file')
    args = parser.parse_args()
    # initialie logger
    fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
    logging.basicConfig(filename=args.out, format=fmt, level=logging.WARN)
    if args.init == True:
        init(args.settings)
    else:
        settings = load(args.settings)
        if args.mode == 'shot':
            run(settings)
        elif args.mode == 'repeat':
            schedule.every(settings['interval']).minute.do(
                lambda: run(settings))
            while True:
                schedule.run_pending()
                time.sleep(1)


def init(file):
    data = {"domain": "<<your domain>>",
            "token": "<<your token>>", "interval": 10}
    with open(file, 'w') as file:
        json.dump(data, file, indent=4)


def load(file):
    with open('settings.json', 'r') as file:
        data = json.load(file)
    return data


def run(settings):
    url = "https://www.duckdns.org/update"
    params = {'domains': settings['domain'], 'token': settings['token']}
    response = req.get(url, params=params)
    if response.status_code != 200:
        logging.warning(response.text)
    else:
        logging.debug(response.text)


if __name__ == "__main__":
    main()
