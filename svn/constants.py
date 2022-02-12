import collections

# Kinds

K_DIR = 'dir'
K_FILE = 'file'

# Repository location types

LT_URL = 'url'
LT_PATH = 'path'

# Status types
#
# http://svn.apache.org/viewvc/subversion/trunk/subversion/svn/schema/status.rnc?view=markup

ST_ADDED       = 1
ST_CONFLICTED  = 2
ST_DELETED     = 3
ST_EXTERNAL    = 4
ST_IGNORED     = 5
ST_INCOMPLETE  = 6
ST_MERGED      = 7
ST_MISSING     = 8
ST_MODIFIED    = 9
ST_NONE        = 10
ST_NORMAL      = 11
ST_OBSTRUCTED  = 12
ST_REPLACED    = 13
ST_UNVERSIONED = 14

STATUS_TYPE_LOOKUP = {
    'added': ST_ADDED,
    'conflicted': ST_CONFLICTED,
    'deleted': ST_DELETED,
    'external': ST_EXTERNAL,
    'ignored': ST_IGNORED,
    'incomplete': ST_INCOMPLETE,
    'merged': ST_MERGED,
    'missing': ST_MISSING,
    'modified': ST_MODIFIED,
    'none': ST_NONE,
    'normal': ST_NORMAL,
    'obstructed': ST_OBSTRUCTED,
    'replaced': ST_REPLACED,
    'unversioned': ST_UNVERSIONED,
}

fields = ['date', 'msg', 'revision', 'author', 'changelist']
LogEntry = collections.namedtuple('LogEntry', fields)

# <path> code in https://svn.apache.org/repos/asf/subversion/trunk/subversion/svn/log-cmd.c
# uses hyphens for the attribute names, but namedtuple field names cannot have hyphens
fields = ['action', 'path', 'copyfrom_path', 'copyfrom_rev', 'kind', 'text_mods', 'prop_mods']
ChangelistEntry = collections.namedtuple('ChangelistEntry', fields)
# NOTE: Python 2's namedtuple doesn't allow for defaults, so need a defaults dict
ChangelistEntryDefaults = {x: None for x in fields[2:]}
