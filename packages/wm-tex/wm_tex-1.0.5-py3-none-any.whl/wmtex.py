import argparse
import datetime
import sys
from waybackpy import WaybackMachineSaveAPI, WaybackMachineCDXServerAPI

user_agent = "Mozilla/5.0 (X11; Linux x86_64; rv:138.0) Gecko/20100101 Firefox/138.0"

def print_bibtex(url: str, wurl: str, n: datetime.datetime, o: datetime.datetime):
    hp = '\\href{' + wurl + '}{' + url + '}'
    print(f"""@misc{{xxx{o.strftime('%Y')[2:4]},
  title   = {{{{}}}},
  author  = {{}},
  day     = {{{o.strftime('%d')}}},
  month   = {{{o.strftime('%m')}}},
  year    = {{{o.strftime('%Y')}}},
  url     = {{{wurl}}},
  howpublished = {{{hp}}},
  urldate = {{{n.strftime('%Y-%m-%d')}}},
}}""")
    return

def save(url: str):
    # Save it on access time for future reference
    save_api = WaybackMachineSaveAPI(url, user_agent)
    wurl     = save_api.save()
    accessed = save_api.timestamp()
    # Query oldest reference (might be access time as the first one)
    cdx_api  = WaybackMachineCDXServerAPI(url, user_agent)
    oldest   = cdx_api.oldest()
    # Print bibtex
    print_bibtex(url, wurl, accessed, oldest.datetime_timestamp)
    return

def main():
    parser = argparse.ArgumentParser(
        description="Automatically reference a URL with the wayback machine in BibTeX")

    parser.add_argument(
        'url',
        help="URL to run command"
    )

    args = parser.parse_args()
    assert(args is not None)
    assert(args.url is not None and args.url.strip() != "")

    save(args.url)
    return

if __name__ == "__main__":
    main()
