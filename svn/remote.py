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

        cmd_output = self.run_command('checkout', cmd)
        return cmd_output

    def __repr__(self):
        return '<SVN(REMOTE) %s>' % self.url
