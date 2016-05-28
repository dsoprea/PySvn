import os
import subprocess
import logging
import dateutil.parser
import collections
import xml.etree.ElementTree

import svn.constants

_logger = logging.getLogger('svn')


class CommonClient(object):
    def __init__(self, url_or_path, type_, *args, **kwargs):
        self.__url_or_path = url_or_path
        self.__username = kwargs.pop('username', None)
        self.__password = kwargs.pop('password', None)
        self.__svn_filepath = kwargs.pop('svn_filepath', 'svn')
        self.__trust_cert = kwargs.pop('trust_cert', None)

        if type_ not in (svn.constants.LT_URL, svn.constants.LT_PATH):
            raise ValueError("Type is invalid: %s" % (type_))

        self.__type = type_

    def run_command(self, subcommand, args, success_code=0, 
                    return_stderr=False, combine=False, return_binary=False):
# TODO(dustin): return_stderr is no longer implemented.
        cmd = [self.__svn_filepath, '--non-interactive']

        if self.__trust_cert:
            cmd += ['--trust-server-cert']

        if self.__username is not None and self.__password is not None:
            cmd += ['--username', self.__username]
            cmd += ['--password', self.__password]

        cmd += [subcommand] + args

        _logger.debug("RUN: %s" % (cmd,))

        p = subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.STDOUT)

        stdout = p.stdout.read()
        r = p.wait()

        if r != success_code:
            raise ValueError("Command failed with (%d): %s\n%s" % 
                             (p.returncode, cmd, stdout))

        if return_binary is True:
            return stdout

        if combine is True:
            return stdout 
        else:
            return stdout.decode().strip('\n').split('\n')

    def rows_to_dict(self, rows, lc=True):
        d = {}
        for row in rows:
            row = row.strip()
            if not row:
                continue

            pivot = row.index(': ')
            
            k = row[:pivot]
            v = row[pivot + 2:]

            if lc is True:
                k = k.lower()

            d[k] = v

        return d

    def info(self, rel_path=None):
        full_url_or_path = self.__url_or_path
        if rel_path is not None:
            full_url_or_path += '/' + rel_path

        result = self.run_command(
                    'info', 
                    ['--xml', full_url_or_path], 
                    combine=True)

        root = xml.etree.ElementTree.fromstring(result)

        entry_attr = root.find('entry').attrib
        commit_attr = root.find('entry/commit').attrib

        relative_url = root.find('entry/relative-url')
        author = root.find('entry/commit/author')
        wcroot_abspath = root.find('entry/wc-info/wcroot-abspath')
        wcinfo_schedule = root.find('entry/wc-info/schedule')
        wcinfo_depth = root.find('entry/wc-info/depth')

        info = {
            'url': root.find('entry/url').text,

            'relative_url': relative_url.text \
                                if relative_url is not None and \
                                   len(relative_url.text) \
                                else None,

# TODO(dustin): These are just for backwards-compatibility. Use the ones added 
#               below.

            'entry#kind': entry_attr['kind'],
            'entry#path': entry_attr['path'],
            'entry#revision': int(entry_attr['revision']),

            'repository/root': root.find('entry/repository/root').text,
            'repository/uuid': root.find('entry/repository/uuid').text,

            'wc-info/wcroot-abspath': wcroot_abspath.text \
                                        if wcroot_abspath is not None and \
                                           len(wcroot_abspath.text) \
                                        else None,
            'wc-info/schedule': wcinfo_schedule.text \
                                    if wcinfo_schedule is not None and \
                                       len(wcinfo_schedule.text) \
                                    else None,
            'wc-info/depth': wcinfo_depth.text \
                                    if wcinfo_depth is not None and \
                                       len(wcinfo_depth.text) \
                                    else None,
            'commit/author': author.text \
                                    if author is not None and \
                                       len(author.text) \
                                    else None,
            'commit/date': dateutil.parser.parse(
                            root.find('entry/commit/date').text),
            'commit#revision': int(commit_attr['revision']),
        }

        # Set some more intuitive keys, because no one likes dealing with 
        # symbols. However, we retain the old ones to maintain backwards-
        # compatibility.

# TODO(dustin): Should we be casting the integers?

        info['entry_kind'] = info['entry#kind']
        info['entry_path'] = info['entry#path']
        info['entry_revision'] = info['entry#revision']
        info['repository_root'] = info['repository/root']
        info['repository_uuid'] = info['repository/uuid']
        info['wcinfo_wcroot_abspath'] = info['wc-info/wcroot-abspath']
        info['wcinfo_schedule'] = info['wc-info/schedule']
        info['wcinfo_depth'] = info['wc-info/depth']
        info['commit_author'] = info['commit/author']
        info['commit_date'] = info['commit/date']
        info['commit_revision'] = info['commit#revision']

        return info

    def cat(self, rel_filepath, revision=None):
        cmd = []                 
        if revision is not None: 
            cmd += ['-r', str(revision)]
        cmd += [self.__url_or_path + '/' + rel_filepath]
        return self.run_command('cat', cmd, return_binary=True)

    def log_default(self, timestamp_from_dt=None, timestamp_to_dt=None, 
                    limit=None, rel_filepath=None, stop_on_copy=False,
                    revision_from=None, revision_to=None):
        """Allow for the most-likely kind of log listing: the complete list, a 
        FROM and TO timestamp, a FROM timestamp only, or a quantity limit.
        """

        full_url_or_path = self.__url_or_path
        if rel_filepath is not None:
            full_url_or_path += '/' + rel_filepath

        timestamp_from_phrase = ('{' + timestamp_from_dt.isoformat() + '}') \
                                    if timestamp_from_dt \
                                    else ''

        timestamp_to_phrase = ('{' + timestamp_to_dt.isoformat() + '}') \
                                if timestamp_to_dt \
                                else ''

        args = []

        if timestamp_from_phrase or timestamp_to_phrase:
            if not timestamp_from_phrase:
                raise ValueError("The default log retriever can not take a TO "
                                 "timestamp without a FROM timestamp.")

            if not timestamp_to_phrase:
                timestamp_to_phrase = 'HEAD'

            args += ['-r', timestamp_from_phrase + ':' + timestamp_to_phrase]

        if revision_from or revision_to:
            if timestamp_from_phrase or timestamp_to_phrase:
                raise ValueError("The default log retriever can not take both "
                                 "timestamp and revision number ranges.")

            if not revision_from:
                revision_from = '1'

            if not revision_to:
                revision_to = 'HEAD'

            args += ['-r', str(revision_from) + ':' + str(revision_to)]

        if limit is not None:
            args += ['-l', str(limit)]

        if stop_on_copy is True:
            args += ['--stop-on-copy']

        result = self.run_command(
                    'log', 
                    args + ['--xml', full_url_or_path], 
                    combine=True)

        root = xml.etree.ElementTree.fromstring(result)
        c = collections.namedtuple(
                'LogEntry', 
                ['date', 'msg', 'revision', 'author'])
        
        for e in root.findall('logentry'):
            entry_info = {x.tag: x.text for x in e.getchildren()}

            date = None
            date_text = entry_info.get('date')
            if date_text is not None:
                date = dateutil.parser.parse(date_text)

            yield c(
                msg=entry_info.get('msg'),
                author=entry_info.get('author'),
                revision=int(e.get('revision')),
                date=date)


    def export(self, to_path, revision=None):
        cmd = []

        if revision is not None:
            cmd += ['-r', str(revision)]

        cmd += [self.__url_or_path, to_path]

        self.run_command('export', cmd)

    def list(self, extended=False, rel_path=None):
        full_url_or_path = self.__url_or_path
        if rel_path is not None:
            full_url_or_path += '/' + rel_path

        if extended is False:
            for line in self.run_command(
                                'ls', 
                                [full_url_or_path]):
                line = line.strip()
                if line:
                    yield line

        else:
            raw = self.run_command(
                    'ls', 
                    ['--xml', full_url_or_path], 
                    combine=True)

            root = xml.etree.ElementTree.fromstring(raw)

            list_ = root.findall('list/entry')
            for entry in list_:
                entry_attr = entry.attrib

                kind = entry_attr['kind']
                name = entry.find('name').text
                
                size = entry.find('size')

                # This will be None for directories.
                if size is not None:
                    size = int(size.text)
                
                commit_node = entry.find('commit')
                
                author = commit_node.find('author').text
                date = dateutil.parser.parse(commit_node.find('date').text)

                commit_attr = commit_node.attrib
                revision = int(commit_attr['revision'])

                yield {
                    'kind': kind,

                    # To decouple people from the knowledge of the value.
                    'is_directory': kind == svn.constants.K_DIR,

                    'name': name, 
                    'size': size,
                    'author': author,
                    'date': date,
                    
                    # Our approach to normalizing a goofy field-name.
                    'timestamp': date,

                    'commit_revision': revision,
                }

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
                            os.path.join(current_rel_path, entry['name'])
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
                    current_rel_path_phrase = \
                        current_rel_path \
                            if current_rel_path is not None \
                            else ''

                    yield (current_rel_path_phrase, entry)

    @property
    def url(self):
        if self.__type != svn.constants.LT_URL:
            raise EnvironmentError("Only the remote-client has access to the URL.")

        return self.__url_or_path

    @property
    def path(self):
        if self.__type != svn.constants.LT_PATH:
            raise EnvironmentError("Only the local-client has access to the path.")

        return self.__url_or_path
