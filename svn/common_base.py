import os
import subprocess
import logging

import svn.config
import svn.exception

_LOGGER = logging.getLogger(__name__)


class CommonBase(object):
    def external_command(
            self, cmd, success_code=0, do_combine=False, return_binary=False,
            environment={}, wd=None, do_discard_stderr=True):
        _LOGGER.debug("RUN: %s" % (cmd,))

        env = os.environ.copy()

        lang = os.environ.get('LANG', svn.config.CONSOLE_ENCODING)
        env['LANG'] = lang

        env.update(environment)

        decode_text = return_binary is False

        kwargs = {}

        if do_discard_stderr is True:
            kwargs['stderr'] = subprocess.PIPE
        else:
            kwargs['stderr'] = subprocess.STDOUT

        p = \
            subprocess.Popen(
                cmd,
                cwd=wd,
                env=env,
                stdout=subprocess.PIPE,
                universal_newlines=decode_text,
                **kwargs)

        stdout, stderr = p.communicate()
        return_code = p.returncode

        if return_code != 0:
            # do_discard_stderr is False
            if stderr is None:
                stderr = "<combined with STDOUT, above>"

            raise svn.exception.SvnException(
                "Command failed with ({}): {}\nSTDOUT:\n\n{}\nSTDERR:\n\n{}".format(
                return_code, cmd, stdout, stderr))

        if return_binary is True or do_combine is True:
            return stdout

        return stdout.strip('\n').split('\n')

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
