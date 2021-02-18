# Returning collections of data from Ansible Lookups

## The problem:
I wrote a lookup. The data it returns is a list of dictionaries.
However, if the list has a length of 1, Ansible sees a dict, not a list.

This article sets out the problem and identifies the solution.


* **version:** Ansible 2.9.4
* **Date:** 27 March 2020


## testing with a list of strings
The lookups are in a folder called [lookup_plugins](./lookup_plugins)

I have written a simple lookup called "cats" that returns a list of words.
It takes the following arguments:
* "list" or "list-of-lists" controls the return value
* "one-item" (optional) controls whether we return 1 item in the list or 4.

The [playbook](./playbook.yml) executes the lookup with all possible
permutations. To correctly set the environment, see [run.sh](./run.sh)


| Lookup returns | Playbook receives | Result |
|----------------|-------------------|--------|
| list of strings | CSV string       | FAIL   |
| list of list of strings | List     | PASS   |

| loop construct in template | template action | Result |
|----------------|-------------------|--------|
| for k in lookup('cats', 'list') | iterate over chars in str | FAIL |
| for k in lookup('cats', 'list-of-lists') | iterate over items in list | PASS |

So far, it seems that the correct thing to do is to wrap the list in the
lookup in another list when we return it, i.e. if we distill the lookup
to its absolute minimum:


```python
from ansible.plugins.lookup import LookupBase
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = ['gato', 'chat', 'katze', 'miau']
        return [ret]    
```

## testing with a list of dicts
The real problem I have is with more complex data. I really want to return a
list of dicts.

The [dog](./lookup_plugins/dog.py) lookup generates a list of dicts; each item
looks like this
```python
{'lang': 'en', 'word': 'dog'}
```
The lookup returns 4 of these in a list, and the playbook sees a list.
However, if the lookup only returns one item in the list, the playbook sees
a dict. 
* If the list only contains one item, Ansible gives us the thing inside it
* if the list contains several items, Ansible gives us the list.
This is inconsistent behaviour. But in the same way as for the string examples
above, it can be fixed by wrapping the data in another list.


| Lookup returns | Playbook receives  | Result |
|----------------|--------------------|--------|
| list of 4 dicts         | list of 4 dicts | PASS
| list of 1 dict          | dict            | FAIL
| list of list of 4 dicts | list of 4 dicts | PASS
| list of list of 1 dict  | list of 1 dict  | PASS

A distilled version of the "dog" lookup looks like this...

```python
from ansible.plugins.lookup import LookupBase
class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        ret = [
            {'lang': 'fr', 'word': 'chien'},
            {'lang': 'en', 'word': 'dog'},
        ]
        return [ret]

```

Note in both code examples, the correct thing to return is a
list containing a list containing your items



## Documentation
The documentation for lookups is a bit lacking.

there are two development guides

this one tells you about the environment variables around lookups
https://docs.ansible.com/ansible/latest/dev_guide/developing_locally.html

and this one has an example (which doesn't wrap the return value in a list!)
https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html#lookup-plugins


