import svn.constants
import svn.common


class RemoteClient(svn.common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        super(RemoteClient, self).__init__(
            url, 
            svn.constants.LT_URL, 
            *args, **kwargs)

    def checkout(self, path, revision=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.url, path]

        self.run_command('checkout', cmd)

    def __repr__(self):
        return '<SVN(REMOTE) %s>' % self.url

    def forcecopy(self, path1, path2):
        cmd = ['-m', '"remove"', path2]
        self.run_command('delete', cmd)
        cmd = [path1, path2, '-m', 'copy']
        self.run_command('copy', cmd)