from collections import namedtuple


def asCmdParameter(self):
    cmdparam = ["--non-interactive"]
    params = self._asdict()
    if "username" in params:
        cmdparam.extend(("--username", params["username"]))
    if "password" in params:
        cmdparam.extend(("--password", params["password"]))
    if params["revision"] is not None:
        cmdparam.extend(("-r", str(params["revision"])))
    return cmdparam


SvnOptions = namedtuple('SvnOptions', 'username password revision')
SvnOptions.asCmdParameter = asCmdParameter
