import subprocess
import logging
import dateutil.parser
import collections
import xml.etree.ElementTree

import svn

_logger = logging.getLogger('svn')


class CommonClient(object):
    def __init__(self, url_or_path, type_):
        self.__url_or_path = url_or_path

        if type_ not in (svn.T_URL, svn.T_PATH):
            raise ValueError("Type is invalid: %s" % (type_))

        self.__type = type_

    def run_command(self, subcommand, args, success_code=0, 
                    return_stderr=False, combine=False, return_binary=False):
        cmd = ['svn', subcommand] + args

        _logger.debug("RUN: %s" % (cmd,))

        p = subprocess.Popen(cmd, 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)

        (stdout, stderr) = p.communicate()
        if p.returncode != success_code:
            raise ValueError("Command failed with (%d): %s\n%s\n%s" % 
                             (p.returncode, cmd, stdout, stderr))

        s = stderr if return_stderr is True else stdout
        if return_binary is True:
            return s

        s = s.decode('ASCII')

        return s if combine is True else s.split("\n")

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

    def info(self):
        result = self.run_command(
                    'info', 
                    ['--xml', self.__url_or_path], 
                    combine=True)

        root = xml.etree.ElementTree.fromstring(result)

        entry_attr = root.find('entry').attrib
        commit_attr = root.find('entry/commit').attrib

        author = root.find('entry/commit/author')
        wcroot_abspath = root.find('entry/wc-info/wcroot-abspath')
        wcinfo_schedule = root.find('entry/wc-info/schedule')
        wcinfo_depth = root.find('entry/wc-info/depth')

        info = {        
            'entry#kind': entry_attr['kind'],
            'entry#path': entry_attr['path'],
            'entry#revision': int(entry_attr['revision']),
            'url': root.find('entry/url').text,
            'relative_url': root.find('entry/relative-url').text,
            'repository/root': root.find('entry/repository/root').text,
            'repository/uuid': root.find('entry/repository/uuid').text,
            'wc-info/wcroot-abspath': wcroot_abspath.text \
                                        if wcroot_abspath is not None and \
                                           len(wcroot_abspath) \
                                        else None,
            'wc-info/schedule': wcinfo_schedule.text \
                                    if wcinfo_schedule is not None and \
                                       len(wcinfo_schedule) \
                                    else None,
            'wc-info/depth': wcinfo_depth.text \
                                    if wcinfo_depth is not None and \
                                       len(wcinfo_depth) \
                                    else None,
            'commit/author': author.text \
                                    if author is not None and \
                                       len(author) \
                                    else None,
            'commit/date': dateutil.parser.parse(
                            root.find('entry/commit/date').text),
            'commit#revision': int(commit_attr['revision']),
        }

        return info

    def export(self, path):
        self.run_command('export', [self.__url_or_path, path])

    def cat(self, rel_filepath):
# TODO(dustin): Verify that this handles binaries well.
        return self.run_command(
                'cat', 
                [self.__url_or_path + '/' + rel_filepath], 
                return_binary=True)

    def log_default(self, timestamp_from_dt=None, timestamp_to_dt=None, 
                    limit=None):
        """Allow for the most-likely kind of log listing: the complete list, a 
        FROM and TO timestamp, a FROM timestamp only, or a quantity limit.
        """

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

        if limit is not None:
            args += ['-l', str(limit)]

        result = self.run_command(
                    'log', 
                    args + ['--xml', self.__url_or_path], 
                    combine=True)

        root = xml.etree.ElementTree.fromstring(result)
        c = collections.namedtuple(
                'LogEntry', 
                ['date', 'msg', 'revision', 'author'])
        
        for e in root.findall('logentry'):
            entry_info = dict([(x.tag, x.text) for x in e.getchildren()])

            yield c(
                msg=entry_info['msg'],
                author=entry_info['author'],
                revision=int(e.get('revision')),
                date=dateutil.parser.parse(entry_info['date']))

    @property
    def url(self):
        if self.__type != svn.T_URL:
            raise EnvironmentError("Only the remote-client has access to the URL.")

        return self.__url_or_path

    @property
    def path(self):
        if self.__type != svn.T_PATH:
            raise EnvironmentError("Only the local-client has access to the path.")

        return self.__url_or_path
