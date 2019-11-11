
import posixpath

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

    def list_recursive(self, rel_path=None, yield_dirs=False,
                       path_filter_cb=None):
        q = [rel_path]
        while q:
            current_rel_path = q[0]
            del q[0]

            for entry in self.list(extended=True, rel_path=current_rel_path):
                if entry['is_directory'] is True:
                    if current_rel_path is not None:
                        next_rel_path = \
                            posixpath.join(current_rel_path, entry['name'])
                    else:
                        next_rel_path = entry['name']

                    do_queue = True
                    if path_filter_cb is not None:
                        result = path_filter_cb(next_rel_path)
                        if result is False:
                            do_queue = False

                    if do_queue is True:
                        q.append(next_rel_path)

                if entry['is_directory'] is False or yield_dirs is True:
                    current_rel_path_phrase = current_rel_path \
                        if current_rel_path is not None \
                        else ''

                    yield (current_rel_path_phrase, entry)
