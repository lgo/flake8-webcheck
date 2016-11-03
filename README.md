# flake8-checks

A flake8 extension to do static analysis on some projects.

Currently the functionality being built out is to check for the presence of decorators. The specific use case is outlined below:


### Decorator presence check
Given a set of API RequestHandler classes, from [Tornado](), check if each request function has a permission level set by a decorator. Doing this check ensures that any changes to the code always explicitly define a permission, making sure nothing slips through and is openly accessibly when not intended.

```
import torando.web

class MyAPIRequestHandler(torando.web.RequestHandler):

  @permission.anonymous # OK, permission is defined
  def get(self):
      ...

  @permission.event.organizer # OK, permission is defined
  def put(self):
    ...


  def post(self): # Error, no permission defined for endpoint
    ...
```
