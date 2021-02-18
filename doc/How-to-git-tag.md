# How to add a tag in Git

(Apr 2019)

You need to know how to tag a release in Git. 
 
It’s dead easy:
 
On the command line, ensure you are on the main branch and up to date, then 
identify the SHA of the commit that you wish to tag. Let’s assume you want to 
tag this SHA with the tag “3.14”. you would do something like this:
 
     git tag 3.14 f54708823c1
     git push --tags origin
 
That’s it.
 
Note that a tag can contain alphabetic characters as well.
I think you can omit the SHA if you want to tag the HEAD of tree.
 
More here: https://git-scm.com/book/en/v2/Git-Basics-Tagging