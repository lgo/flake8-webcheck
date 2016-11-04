# flake8-webcheck

A [flake8](http://flake8.pycqa.org/en/latest/) extension to do static analysis on projects. This package has been tested against flake8 3.0.4 and python 3.5.2

Currently the functionality being built out is to check for the presence of decorators. A use case is outlined below:


### Decorator presence check
Given a set of API RequestHandler classes, from [Tornado](http://www.tornadoweb.org/), check if each request function has a permission level set by a decorator. Doing this check ensures that changes always explicitly define a permission to make sure no security slips are created, causing open APIs.

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
