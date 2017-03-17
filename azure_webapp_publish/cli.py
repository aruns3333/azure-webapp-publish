import argparse
import sys
from .kudu import KuduSession

def main():

    parser = argparse.ArgumentParser(description='Azure Webapp Publish')
    parser.add_argument('publishsettings', metavar='publishsettingspath',
                        help='The path to publish settings file')
    parser.add_argument('--add-extensions', dest='add_extensions', nargs='*', default=[],
                        help='optional extensions to install')
    parser.add_argument('--list-installed-extensions', dest='list_installed_extensions',
                        action='store_true',
                        help='List installed extensions and exit')
    parser.add_argument('--list-available-extensions', dest='list_available_extensions',
                        action='store_true',
                        help='List available extensions and exit')

    args = parser.parse_args()

    kudu_session = KuduSession(args.publishsettings)

    if args.list_available_extensions:
        print(kudu_session.get('extensionfeed').text)
        sys.exit(0)
    if args.list_installed_extensions:
        print(kudu_session.get('siteextensions').text)
        sys.exit(0)

    for ext_id in args.add_extensions:
        kudu_session.put('siteextensions/'+ext_id)


if __name__ == '__main__':
    main()