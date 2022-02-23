import os

import svn.common
import svn.local
import svn.remote
import svn.constants

def get_client(url_or_path, *args, **kwargs):
    if url_or_path[0] == '/':
        return svn.local.LocalClient(url_or_path, *args, **kwargs)
    else:
        return svn.remote.RemoteClient(url_or_path, *args, **kwargs)

def get_common_for_cwd():
    path = os.getcwd()
    uri = 'file://{}'.format(path)

    cc = svn.common.CommonClient(uri, svn.constants.LT_URL)
    return cc
