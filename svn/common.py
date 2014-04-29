import subprocess
import logging

from xml.etree import ElementTree

import svn

_logger = logging.getLogger('svn')


class CommonClient(object):
    def __init__(self, url_or_path, type_):
        self.__url_or_path = url_or_path

        if type_ not in (svn.T_URL, svn.T_PATH):
            raise ValueError("Type is invalid: %s" % (type_))

        self.__type = type_

    def run_command(self, subcommand, args, success_code=0, return_stderr=False, combine=False):
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
        result = self.run_command('info', ['--xml', self.__url_or_path], combine=True)
        root = ElementTree.fromstring(result)
        return root.find('entry')

    def export(self, path):
        self.run_command('export', [self.__url_or_path, path])

    def cat(self, rel_filepath):
# TODO(dustin): Verify that this handles binaries well.
        return self.run_command('cat', [self.__url_or_path + '/' + rel_filepath])

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
