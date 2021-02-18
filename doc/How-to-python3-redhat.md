# How to install a Python3 Virtualenv on RedHat 7

(June 2020)

In RedHat, Python3 is installed in /opt/rh via the "scl" command

This has the advantage that you can have several installations of Python, side by side.

The disadvantage is not knowing where they are.

You can create a Python3.6 virtualenv as follows. This example uses the standard path for SCL version of Python3

`/opt/rh/rh-python36/root/usr/bin/python3 -m venv myvenv`

# How to install a Python3 Virtual env on Centos 7

Use the following to install Python 3.6. 
```
sudo ifup enp0s3
sudo yum install centos-release-scl
sudo yum install rh-python36
/opt/rh/rh-python36/root/usr/bin/python3.6 -m venv myvenv
. myvenv/bin/activate
```
You can, of course, install other Python versions as well, e.g. rh-python38 for Python 3.8.

**Tip** to enable networking by default, see [Bullet 2 of the Centos7 FAQ](https://wiki.centos.org/FAQ/CentOS7)
