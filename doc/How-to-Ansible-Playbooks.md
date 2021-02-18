# Tips for Ansible Playbooks

(May 2020)

## I have a module that I want to run on the controller only
In this example, I have a module called **d42_is_logged_in**
which takes various parameters. I want to make sure this runs
on the Ansible controller only, as it requires certain Python
libraries to talk to my "D42" system.

The hosts file looks like this: 
```text
localhost       ansible_connection=local      ansible_python_interpreter=/Users/andy/venv/py3/bin/python
andy-centos-002 ansible_connection=ssh        ansible_user=andy
```
note that:
* the localhost node uses a "local" connection
* the localhost node has a specific python interpreter, which
  gives us the VENV.

and here's the playbook.

```yaml
- hosts: all
  tasks:
  
  - name: "Ensure credentials for D42 are correct"
    d42_is_logged_in:
      usename: "{{ a_var_with_username }}"
      password: "{{ a_var_with_password }}"
    delegate_to: localhost
    run_once: true
```
* delegate_to: localhost ensure the task runs on localhost only
* run_once ensure it runs once, not once-per-host.

### Other techniques:
* lookups always run on the controller. You can "run_once" to prevent the
  variable being discovered multiple times, e.g. if you have a *lookup* to
  ensure you're logged in:
  
```yaml
  - name: Confirm logged in to D42
    set_fact:
      logged_in_to_d42: "{{ lookup('d42_ensure_logged_in') }}"
    run_once: true
```

### The inverse:
* I want to run things on _not_ the controller.
* you can't say "when hostname != localhost" because Ansible works out the
  hostname of the device. 
* One option is to run on everything that's not got a local connection:
```yaml
  - template:
      src: templates/my_app_env.j2
      dest: /tmp/my_app_envs.sh 
      mode: '0644'
    when:
      - ansible_connection != "local"
```