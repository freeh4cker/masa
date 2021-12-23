import sys
import argparse
import pandas as pd

import masa


def parse_args(args):
    parser = argparse.ArgumentParser(description='generate email list')
    parser.add_argument('--autonomie-absolue-piscine')
    parser.add_argument('--autonomie-relative-piscine')
    parser.add_argument('--fosse')
    parser.add_argument('--rifaa')
    parser.add_argument('--no-rifaa')
    parser.add_argument('--valid',
                        help="list of email with valid caci")

    parsed_args = parser.parse_args()
    return parsed_args


def main(args=None):
    args = sys.argv[1:] if args is None else args
    parsed_args = parse_args(args)

    data = pd.read_csv('./data/masa.tsv', sep='\t', comment='#')

    if parsed_args.autonomie_absolute_piscine:
        emails = masa.autonomie_absolue_piscine(data)
    elif parsed_args.autonomie_relative_piscine:
        emails = masa.autonomie_relative_piscine(data)
    elif parsed_args.fosse:
        emails = masa.fosse(data)
    elif parsed_args.rifaa:
        emails = masa.rifaa(data)
    elif parsed_args.no_rifaa:
        emails = masa.no_rifaa(data)
    else:
        emails = all(data)

    print(", ".join(emails))

