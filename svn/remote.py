import svn

from svn import common


class RemoteClient(common.CommonClient):
    def __init__(self, url, username=None, password=None, *args, **kwargs):
        self.username = username
        self.password = password
        super(RemoteClient, self).__init__(url, svn.T_URL, *args, **kwargs)

    def checkout(self, path, revision=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.url, path]
        if self.username is not None:
            cmd += ['--username', self.username]
            cmd += ['--password', self.password]

        self.run_command('checkout', cmd)

    def __repr__(self):
        return ('<SVN(REMOTE) %s>' % (self.url))
