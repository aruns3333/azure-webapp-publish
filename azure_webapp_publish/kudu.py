import os.path
from requests import Session, RequestException
from xml.etree import ElementTree
from isodate import parse_datetime

class KuduSession(object):

    def __init__(self, publishsettingspath):
        try:
            profile = ElementTree.parse(publishsettingspath)
            data = profile.getroot().find('./publishProfile[@publishMethod="MSDeploy"]')
        except OSError:
            print("Unable to read the profile at {}.".format(publishsettingspath), file=sys.stderr)
            print("Please restart deployment and provide the path to your publishing profile.", file=sys.stderr)
            raise

        self.session = Session()
        self.session.auth = data.get('userName'), data.get('userPWD')
        self.session.headers['If-Match'] = '*'   # allow replacing files on upload
        self.api_url = 'https://{}/api/'.format(data.get('publishUrl'))

    def _request(self, operation_function, kudupath, **kwarg):
        r = operation_function(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r

    def get(self, kudupath, **kwarg):
        return self._request(self.session.get, kudupath, **kwarg)

    def head(self, kudupath, **kwarg):
        return self._request(self.session.head, kudupath, **kwarg)

    def delete(self, kudupath, **kwarg):
        return self._request(self.session.delete, kudupath, **kwarg)

    def put(self, kudupath, **kwarg):
        return self._request(self.session.put, kudupath, **kwarg)

    def post(self, kudupath, **kwarg):
        return self._request(self.session.post, kudupath, **kwarg)

    def command(self, command, workingdir=r'D:\home\site\wwwroot'):
        '''Execute a command.

        :param str command: The command to execute
        :param str workingdir: The current working dir while executing the command. Default wwwroot
        :return: The json
        '''
        cmd = {
            'command': command,
            'dir': workingdir
        }
        return self.post('command', json=cmd)

    def get_deployed_files(self, vfs_basepath='site/wwwroot/'):
        """Return a list of deployed files in this Webapp as a generator.

        This method also:
        - Parse mtime and crtime as datetime
        - Add a urlpath key with path fragment for future URL callable
        - Keys are normalized using normcase for future comparison with the system.
        """
        # Kudu accepts a // ended path. Let's keep thing simply and always append an ending slash.
        kudu_folderpath = 'vfs/{}/'.format(vfs_basepath)
        for element in self.get(kudu_folderpath).json():
            if element['mime'] == "inode/directory":
                for subelement, submeta in self.get_deployed_files(vfs_basepath+element['name']+'/'):
                    submeta['urlpath'] = "/".join([element['name'], submeta['urlpath']])
                    yield os.path.normcase(submeta['urlpath']), submeta
            else:
                for key in ["mtime", "crtime"]:
                    element[key] = parse_datetime(element[key])
                element['urlpath'] = element['name']
                yield os.path.normcase(element['name']), element
