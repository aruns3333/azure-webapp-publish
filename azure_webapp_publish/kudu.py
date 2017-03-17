from requests import Session
from xml.etree import ElementTree


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

    def get(self, kudupath, **kwarg):
        r = self.session.get(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r

    def head(self, kudupath, **kwarg):
        r = self.session.head(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r

    def delete(self, kudupath, **kwarg):
        r = self.session.delete(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r

    def put(self, kudupath, **kwarg):
        r = self.session.put(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r

    def post(self, kudupath, **kwarg):
        r = self.session.post(self.api_url+kudupath, **kwarg)
        r.raise_for_status()
        return r        