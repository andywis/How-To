# Ansible - Console output with sane linebreaks

(Jun 2020)

By default Ansible will output "\n" linebreaks as text in the console output. 
Ansible 2.5.0 started shipping with a YAML callback, which can render this 
output with human-friendly formatting (eg. actual newlines).

To use it, edit your ansible.cfg file (either global, in 
/etc/ansible/ansible.cfg, or a local one in your playbook/project), and 
add the following lines under the [defaults] section:

```
[defaults]
# Use the YAML callback plugin.
stdout_callback = yaml
 
# Use the stdout_callback when running ad-hoc commands.
bin_ansible_callbacks = True
```

(Thanks to [Agar the Tiger](https://agarthetiger.github.io/mkdocs/) for this tip)


