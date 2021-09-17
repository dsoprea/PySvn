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

    def remove(self, rel_path, message, do_force=False):
        args = [
            '--message', message,
        ]

        if do_force is True:
            args.append('--force')

        url = self._pathjoin(self.url, rel_path)

        args += [
            url
        ]

        self.run_command(
            'rm',
            args)

    def _pathjoin(self, *args):
        clean_args = []
        for i, arg in enumerate(args):
            if i != 0 and arg.startswith('/'):
                arg = arg[1:]

            if i != len(args) - 1 and arg.endswith('/'):
                arg = arg[:-1]

            clean_args.append(arg)

        return '/'.join(clean_args)

    def __repr__(self):
        return '<SVN(REMOTE) %s>' % self.url
