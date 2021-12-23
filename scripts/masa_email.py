import argparse
import pandas as pd



def parse_args(args):


def main():

    parser = argparse.ArgumentParser(description='generate email list')
    parser.add_argument('--autonomie-absolue-piscine')
    parser.add_argument('--autonomie-relative-piscine')
    parser.add_argument('--fosse')
    parser.add_argument('--rifaa')
    parser.add_argument('--no-rifaa')
    parser.add_argument('--valid'
                        help="list of email with valid caci")

    parsed_args = parser.parse_args()

    data = pd.read_csv('path', sep='\t', comment='#')

    if parsed_args.autonomie_absolute_piscine:
        emails = autonomie_absolue_piscine(data)
    elif parsed_args.autonomie_relative_piscine:
        emails = autonomie_relative_piscine(data)
    elif parsed_args.fosse:
        emails = fosse(data)
    elif parsed_args.rifaa:
        emails = rifaa(data)
    elif parsed_args.no_rifaa:
        emails = no_rifaa(data)
    else:
        emails = all(data)

    print(", ".join(emails))

