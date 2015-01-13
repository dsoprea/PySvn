import svn

from svn import common


class RemoteClient(common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        self.username = kwargs.pop('username', None)
        self.password = kwargs.pop('password', None)
        super(RemoteClient, self).__init__(url, svn.T_URL, *args, **kwargs)

    def checkout(self, path, revision=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        if self.username is not None:
            cmd += ['--username', self.username]
            cmd += ['--password', self.password]

        cmd += [self.url, path]

        self.run_command('checkout', cmd)

    def __repr__(self):
        return ('<SVN(REMOTE) %s>' % (self.url))
