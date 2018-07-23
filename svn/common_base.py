import os
import subprocess
import logging

import svn.config
import svn.exception

_LOGGER = logging.getLogger(__name__)


class CommonBase(object):

    @staticmethod
    def external_command_staticmethod(
            cmd, success_code=0, do_combine=False,
            return_binary=False, environment={}, wd=None):
        _LOGGER.debug("RUN: %s" % (cmd,))

        env = os.environ.copy()
        env['LANG'] = svn.config.CONSOLE_ENCODING
        env.update(environment)

        p = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=wd,
            env=env)

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

    def external_command(self, *args, **kwargs):
        return CommonBase.external_command_staticmethod(*args, **kwargs)

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
