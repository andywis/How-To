
"""
Ansible lookup.
From https://github.com/ansible/ansible/issues/10291
"""
# import os
# from ansible import utils, errors

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display


class LookupModule(LookupBase):
    """ test Ansible lookup """

    def run(self, terms, variables=None, **kwargs):
        """ entrypoint """

        display = Display()
        display.v("terms: %r" % terms)
        display.vvvv("variables: %r" % variables)
        display.vvvv("**kwargs: %r" % kwargs)

        ret = ['gato', 'chat', 'katze', 'miau']

        if len(terms) > 1 and terms[1] == "one-item":
            ret = ['moggie']

        if terms[0] == "list":
            return ret
        if terms[0] == "list-of-lists":
            return [ret]

        return ret
