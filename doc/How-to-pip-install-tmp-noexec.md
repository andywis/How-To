# How to pip install when /tmp is mounted NOEXEC
(Jun 2020)

## The problem:
/tmp is mounted NOEXEC on RedHat, for perfectly good security reasons

However, this can prevent the installation of certain modules, e.g. `pip install paramiko`, that attempts to 
compile (and run) things in /tmp


## The Solution:
An alternative temporary folder can be specified by setting TMPDIR before running the "pip install"

`export TMPDIR=/uses/jbloggs/tmp`

## The better solution
Python packages that require compilation are often also available as binary packages. Use `pip download` to obtain the right version of the package, and "pip install" that, either from WHL file, or by installing it on your internal PyPi repository (e.g. Nexus)
