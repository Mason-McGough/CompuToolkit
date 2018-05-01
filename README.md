# HistoToolkit

A graphical user interface for prototyping histology and cytology image processing workflows.

### To-do
##### Essentials
* Store manually entered inputs
* Verify if input is valid (assume string only if enclosed in '' or "")
* Create file menu to swap with operations menu
* Implement /run-graph route

##### Desirables
* Change style of invalid param paths
* Prevent Run from being triggered again until response is received
* Attach event to collapse folders in menu
* Prevent loops from being formed in net (server-side for security and client-side for user-friendliness)
* Allow Node constructor to use ordered list for params as input
* Make output names for nodes optional (option to unpack values if possible?)

#### Notes
* Launch server
```
python run.py
```

* Run scripts in app/test as __main__:
```
python -m app.test.test_script
```
