# How to fix a git merge conflict

(May 2020)

You have finished your code, your pull request has been approved, but 
someone's moved the 'main' branch forwards, and now you have a merge conflict. 

These instructions tell you how to fix the merge conflict locally and push it.

(The instructions in Bitbucket tell you how to fix the conflicts and merge
in a single step, which I feel is more dangerous)

Ensure your branch is clean

```
git pull
git checkout main
git pull
git checkout -  # return to your branch
git merge main
```

Now fix each merge conflict, 
`git add` each file you fix

Then `git commit`.

Don't use "-m", because the commit message is already pre-filled for merging from Master.

`git push`

Now take a look at your pull request, and you'll see the merge conflict is
gone, and you can merge your pull request.

