import os.path

import svn.constants
import svn.common


class LocalClient(svn.common.CommonClient):
    def __init__(self, path_, *args, **kwargs):
        if os.path.exists(path_) is False:
            raise EnvironmentError("Path does not exist: %s" % path_)

        super(LocalClient, self).__init__(
            path_,
            svn.constants.LT_PATH,
            *args, **kwargs)

    def __repr__(self):
        return '<SVN(LOCAL) %s>' % self.path

    @staticmethod
    def checkout(repo_path, checkout_path, *args, **kwargs):
        def urlize(path):
            return "file://" + os.path.abspath(path)
        cmdlist = [
            'svn',  # {TODO: allow variance in a standard way here}
            '--non-interactive',
            'checkout',
            urlize(repo_path),
            checkout_path,
        ]
        LocalClient.external_command_staticmethod(cmdlist)
        return LocalClient(checkout_path, *args, **kwargs)

    def add(self, rel_path):
        self.run_command(
            'add',
            [rel_path],
            wd=self.path)

    def commit(self, message, rel_filepaths=[]):
        args = ['-m', message] + rel_filepaths

        self.run_command(
            'commit',
            args,
            wd=self.path)

    def update(self, rel_filepaths=[], revision=None):
        cmd = []
        if revision is not None:
            cmd += ['-r', str(revision)]
        cmd += rel_filepaths
        self.run_command(
            'update',
            cmd,
            wd=self.path)

    def cleanup(self):
        self.run_command(
            'cleanup',
            [],
            wd=self.path)
