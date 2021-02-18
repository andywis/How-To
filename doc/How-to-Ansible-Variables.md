# Example playbooks with Ansible variables

(Oct 2020)

## Basics
| **What** | **Ansible variable** |
| ---- | --- |
| current hostname | `{{ ansible_hostname }}` |
| Now | `{{ ansible_date_time.date }}` |

e.g.
```yaml
  tasks:
    - name: "Print the device name"
      debug:
        msg: "{{ ansible_hostname }}"
```

## Dates, Times
This playbook shows some data manipulation.

Run it with: `ansible-playbook -i localhost, playbook.yml`
```yaml
---
- hosts: all
  connection: local  # don't attempt to SSH

  vars:
     date001: "{{ '2020-10-20 09:00:00' | to_datetime }}"

  tasks:
    - name: "A date from a string in a variable, converted using the to_datetime filter"
      debug:
        msg: "{{ date001 }}"

    - name: "The datetime object"
      debug:
        var=ansible_date_time
  
    # We can obtain individual properties from andible_date_time
    # (Note that debug.msg can take a list)
    - debug: 
        msg: 
          - "the current date is {{ ansible_date_time.date }}"
          - "the current time is {{ ansible_date_time.time }}"

    # This doesn't work because .datetime does not exist
    # - debug: 
    #     msg:" The date+time is {{ ansible_date_time.datetime}}"

    # This doesn't work because the to_datetime filter expects 
    # a string and we are passing it a datetime object.
    # - debug: 
    #     msg: "the current date is {{ ansible_date_time.date | to_datetime }}"
```