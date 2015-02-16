import svn

from svn import common


class RemoteClient(common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        super(RemoteClient, self).__init__(url, svn.T_URL, *args, **kwargs)

    def checkout(self, path, revision=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.url, path]

        self.run_command('checkout', cmd)

    def __repr__(self):
        return ('<SVN(REMOTE) %s>' % (self.url))
