import re
import difflib
from ansible import errors

def diff(pre_change, post_change=''):

    try:
        netdiff = list(
            difflib.unified_diff(
                pre_change.splitlines(),
                post_change.splitlines()
            )
        )
        if netdiff:
            header = ''.join(netdiff[0:3])
            result = '\n'.join(netdiff[4:])
            final = header + result
            return final

    except Exception, e:
        raise errors.AnsibleFilterError('diff plugin error: %s' % str(e) )


class FilterModule(object):
    ''' A filter to diff two strings. '''
    def filters(self):
        return {
            'diff' : diff
        }
