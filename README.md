# Interlock Python API

#### Dependencies
### Ouimeaux - Belkin Wemo Control

`pip install ouimeaux`

**Important!**

If you get this error

`No module named 'gevent.wsgi'`

Go to the `venv\lib\site-packages\ouimeaus\subscribe.py` file and replace
```python
from gevent.wsgi import WSGIServer
```
to
```python
from gevent.pywsgi import WSGIServer
```
That should fix the problem

### SoCo
`pip install soco`

### phue

`pip install phue`