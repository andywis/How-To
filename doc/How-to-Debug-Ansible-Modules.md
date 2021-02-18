# How to Debug Ansible Modules.

(Oct 2020)

Here are some tips on how to debug Ansible modules.
I tried to follow the documentation
[at docs.ansible.com](https://docs.ansible.com/ansible/latest/dev_guide/debugging.html)
but I struggled to get it to work. 

To run an Ansible Module on its own (so you can insert debug), do the following...

## Running a module on its own
Create a file called args.json.

It should look like this:

    {
      "ANSIBLE_MODULE_ARGS": {
          "param_1_name": "param_1_value",
          "param_2_name": "param_2_value"
          // etc...
      }
    }

It **must** be valid JSON (e.g. comments are NOT allowed)

Now run your module as follows (here, the module is called "my_module"):

    python ./library/my_module.py < args.json

**Note**
* You still can't "import pdb" in your Python
* you can `print()` things out, but remember to delete them afterwards
* you should use logging instead!!

## Testing a lookup using "ansible-hacking"
Get hold of the [Ansible](https://github.com/ansible/ansible) repository
from Github.

Let's assume you've put it in `/Users/andywis/git/ansible/ansible/`

Now you can execute the lookup with the following (here, the lookup is called my_lookup)

```bash
lookup_name=my_lookup.py
/Users/andywis/git/ansible/ansible/hacking/test-module \
        -m /Users/andywis/git/path/to/my/plugins/lookup/${lookup_name} \
        -a @zz_args.yaml
```

Another way to run a lookup is to execute it as a python program, but it needs
to be fed in the right way. 
The lookup under test is called "my_lookup.py"

```bash
. ~/bin/envs_rc_dev.sh  # load the ENV variables required by the module
. ~/venv/py3/bin/activate  # virtualenv containing Ansible
python3 -c "import my_lookup;L=my_lookup.LookupModule();L.run(['term1','term2'], variables={'ansible_facts': {'env': {}}})"

```
