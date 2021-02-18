
"""
Ansible lookup testing items in a dict.

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

        ret = [
            {'lang': 'es', 'word': 'perro'},
            {'lang': 'fr', 'word': 'chien'},
            {'lang': 'de', 'word': 'hund'},
            {'lang': 'en', 'word': 'dog'},
        ]

        if len(terms) > 1 and terms[1] == "one-item":
            ret = [ret[0]]

        if terms[0] == "list":
            return ret
        if terms[0] == "list-of-lists":
            return [ret]

        return ret
