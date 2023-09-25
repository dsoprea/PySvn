import svn.constants
import svn.common


class RemoteClient(svn.common.CommonClient):

    def __init__(self, url, *args, **kwargs):
        super(RemoteClient, self).__init__(
            url,
            svn.constants.LT_URL,
            *args, **kwargs)

    def checkout(self, path, revision=None, force=False, depth=None, ignore_ext=False):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]
        if force:
            cmd += ["--force"]
        if depth:
            cmd += svn.common.get_depth_options(depth)
        if ignore_ext:
            cmd += ["--ignore-externals"]

        cmd += [self.url, path]

        self.run_command('checkout', cmd)

    def remove(self, rel_path, message, do_force=False):
        args = [
            '--message', message,
        ]

        if do_force is True:
            args.append('--force')

        url = '{}/{}'.format(self.url, rel_path)

        args += [
            url
        ]

        self.run_command(
            'rm',
            args)

    def __repr__(self):
        return '<SVN(REMOTE) %s>' % self.url
