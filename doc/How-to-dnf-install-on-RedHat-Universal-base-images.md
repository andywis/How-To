# How to install packages on a RedHat UBI-minimal

(May 2020)

## The problem:
On The RedHat Universal Base image "ubi-minimal", there isn't a "dnf search"
facility. In fact, there's only "microdnf".

How do you work out what a package is called so that you can install it?

## The solution:
The solution is to use the non-minimal base image to do the search.

The "ubi" image has Yum instead of microdnf, but the package names are the
same, so you can just run `yum search <program name>` to find the thing
you are looking for:

```bash
$ docker run -ti ubi:x.x.x /bin/bash
# yum search <program name>
```

This will give you the package name, which you can use in your ubi-minimal
container, or in its Dockerfile.

## Example

to find out the name of the python **requests** package:

```bash
$ docker run -ti --rm  registry.access.redhat.com/ubi7/ubi:latest /bin/bash
[root@52e5fb878233 /]# yum search requests
```
- this gives us a perl module, two NodeJS modules, and the python module that
  we are looking for; the output looks a bit like this...

```
==================== N/S matched: requests ==============================
perl-CGI.noarch : Handle Common Gateway Interface requests and responses
python-requests.noarch : HTTP library, written in Python, for human beings
rh-nodejs8-nodejs-got.noarch : Simplified HTTP/HTTPS requests
rh-nodejs8-nodejs-timed-out.noarch : Timeout HTTP/HTTPS requests
```

You can now test this in your ubi-minimal container to prove that it works:

```bash
$ docker run -ti  registry.access.redhat.com/ubi7/ubi-minimal:latest /bin/bash
bash-4.2# microdnf install python-requests
```

and you can then bake it in to your Dockerfile.

```dockerfile
RUN microdnf install python-requests ; microdnf clean all
```

## Further notes
Yes, I know that you should really be installing **requests** using `pip`
instead of `microdnf`. That's not the point!
