import svn.local

l = svn.local.LocalClient('/tmp/testsvnwc')

diff = l.diff(5, 6)
# for filepath, hunks_info in diff.items():
#     print(filepath)
#     print('')

#     print("left: {}".format(hunks_info['left_phrase']))
#     print("right: {}".format(hunks_info['right_phrase']))

#     for hunk in hunks_info['hunks']:
#         print('> {}'.format(hunk['lines_phrase']))
#         print('')
#         print(hunk['body'])
#         print('')

# Flat list.

# entries = l.list()
# for filename in entries:
#     print(filename)
