import os.path

import svn
import svn.common


class LocalClient(svn.common.CommonClient):
    def __init__(self, path_, *args, **kwargs):
        if os.path.exists(path_) is False:
            raise EnvironmentError("Path does not exist: %s" % (path_))

        super(LocalClient, self).__init__(path_, svn.T_PATH, *args, **kwargs)

    def __repr__(self):
        return ('<SVN(LOCAL) %s>' % (self.path))
