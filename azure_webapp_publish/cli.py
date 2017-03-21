import argparse
import sys
import json
from .kudu import KuduSession
from .deploy import get_deployment_files, apply_actions, ActionListVisitor, UploaderVisitor


def main():

    parser = argparse.ArgumentParser(description='Azure Webapp Publish')
    parser.add_argument('publishsettings', metavar='publishsettingspath',
                        help='The path to publish settings file')
    parser.add_argument('--deploy', dest='deploy', nargs='?', default='.',
                        help='Deploy. Optional parameter is local folder to look for (default current dir)')
    parser.add_argument('--dry-run', dest='dry_run',
                        action='store_true',
                        help='Deploy dry run, just print file list and action as JSON')
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
    if args.deploy:
        # Get from Kudu
        deployed_files = {filepath: meta for filepath, meta in kudu_session.get_deployed_files()}
        # Get local files
        local_files = get_deployment_files(args.deploy)
        # Apply actions actions
        if args.dry_run:
            visitor = ActionListVisitor()
            apply_actions(local_files, deployed_files, visitor)
            print(json.dumps(visitor.action_list))
        else:
            visitor = UploaderVisitor(kudu_session)
            apply_actions(local_files, deployed_files, visitor)
        sys.exit(0)

    for ext_id in args.add_extensions:
        kudu_session.put('siteextensions/'+ext_id)


if __name__ == '__main__':
    main()
