import os
import sys
import subprocess
import logging

import svn.config
import svn.exception

_LOGGER = logging.getLogger(__name__)


class CommonBase(object):
    def external_command(self, cmd, success_code=0, do_combine=False, 
                         return_binary=False, environment={}, wd=None):
        _LOGGER.debug("RUN: %s" % (cmd,))
        # print("RUN:", cmd)

        env = os.environ.copy()
        env['LANG'] = svn.config.CONSOLE_ENCODING
        env.update(environment)

        kwargs = {
            'stdout': subprocess.PIPE,
            'stderr': subprocess.STDOUT,
            'cwd': wd,
            'env': env,
        }

        try:
            # Don't open Command Prompt on Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            kwargs['startupinfo'] = startupinfo
        except AttributeError:
            pass

        p = subprocess.Popen(cmd, **kwargs)
        stdout = p.stdout.read()
        r = p.wait()
        p.stdout.close()

        if r != success_code:
            raise svn.exception.SvnException(
                "Command failed with ({}): {}\n{}".format(
                p.returncode, cmd, stdout))

        if return_binary is True or do_combine is True:
            return stdout

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
