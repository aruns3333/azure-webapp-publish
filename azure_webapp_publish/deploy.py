import os.path
from fnmatch import filter as fnfilter
from datetime import datetime
from isodate import UTC

VERBOSE = True

def get_deployment_files(root):
    """Scan the root folder and return a list of tuples of two elements.

    Element one is normalized path, used for comparison
    Element two is original path in URL format, in case we need to create it
    Element three is relative path from current dir and can be used to open the file locally.

    :param str root: A local folder to consider as equivalent root of wwwroot
    :return: A list of tuple (distant filename from wwwroot, localpath relative to curdir)
    """

    all_files = []
    for dirpath, dirnames, filenames in os.walk(root):
        # Dirpath contains "root", use relpath to extract "root"
        reldirs = [os.path.relpath(os.path.join(dirpath, d), root) for d in dirnames]
        relfiles = [os.path.relpath(os.path.join(dirpath, f), root) for f in filenames]
        all_files.extend((os.path.normcase(f), f.replace('\\','/'), os.path.join(root, f)) for f in relfiles)

    return all_files


class ActionListVisitor(object):
    def __init__(self):
        self.action_list = []

    def accept(self, action, kudu_urlpath, localfile_path):
        self.action_list.append((action, kudu_urlpath, localfile_path))

class UploaderVisitor(object):
    def __init__(self, kudu_session, vfs_basepath='site/wwwroot/'):
        self.kudu_session = kudu_session
        self.vfs_basepath = vfs_basepath

    def accept(self, action, kudu_urlpath, localfile_path):
        print(action, '  ', localfile_path, '->', kudu_urlpath)
        if action in ["Create", "Update"]:
            with open(localfile_path, 'rb') as f:
                self.kudu_session.put('vfs/{}/{}'.format(self.vfs_basepath,kudu_urlpath), data=f, stream=True)
        elif action in ["Delete"]:
            self.kudu_session.delete('vfs/{}/{}'.format(self.vfs_basepath,kudu_urlpath))
        else:
            raise ValueError('Unknown action ', action)

def apply_actions(local_files, deployed_files, visitor):
    """Get actions to do "Update, Delete, Create"
    - LocalFiles is a list of tuple (KuduPath, openable path)
    - DeployedFiles is dict KuduPath as key, meta as value

    return a list of tuple (action, KuduPath, openable path)
    """
    deployed_files_copy = dict(deployed_files) # Copy, I will pop it
    for comparable_name, pretty_name, localpath in local_files:
        # print("Working on "+comparable_name)
        kudumeta = deployed_files_copy.pop(comparable_name, None)
        if not kudumeta:
            # print("Didn't found a Kudu file, PUT")
            visitor.accept("Create", pretty_name, localpath)
            continue
        # print("Found Kudu file! Checking meta for update")

        last_modified_time_local = datetime.fromtimestamp(os.path.getmtime(localpath), UTC)
        last_modified_time_distant = kudumeta['mtime']
        # print("\t"+pretty_name)
        # print("\tDist: {}".format(last_modified_time_distant))
        # print("\tLocl: {}".format(last_modified_time_local))
        if last_modified_time_local > last_modified_time_distant:
            visitor.accept("Update", pretty_name, localpath)
    for meta in deployed_files_copy.values():
        visitor.accept("Delete", meta['urlpath'], None)
