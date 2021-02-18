# How to monkey-patch a class in Python

(Oct 2020)

Let's imagine you've got a Python class.

In your application, you want to use a brand new feature in that class, which
might not be avaiable in the released versions yet. 

You can "monkey-patch" the new feature into the class within your application.

Let's imagine you want to add a new method called "update_subnet" in a class
called widget.WidGet in a module called  

```python

import widget 

# ------------------------------------------------------------
# Monkey-patch the WidGet class to add the new update_subnet method


def new_update_subnet(self, data):
    """ update a subnet """
    
    # <<< the implementation would go here... >>>
    return response

try:
    widget.WidGet.update_subnet
    # WidGet already has this method. Carry on
except AttributeError:
    # older WidGet; patch it to use the new function.
    widget.WidGet.update_subnet = new_update_subnet

#
# End of Monkey-patching
# ------------------------------------------------------------

def run():
    w = widget.WidGet()
    # do stuff ...
    w.update_subnet(data)
```

## Notes:
* the method new_update_subnet() takes self as a first arg because
  it will be inserted into a class as a method, even though it looks like 
  a global function at the moment
* I have omitted the functionality in the example above.
* Once you are comfortable that all users will have access to the new
  method in the widget.WidGet class, you can delete the monkey-patching
  section from your app