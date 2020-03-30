# Context menu items on 'tests' (so the directory)





# Context menu items on 'test' (so existing individual .py files)





# docstring format

Quote : reStructured text (reST) / Sphinx: This is the Official Python documentation standard.

This means that the current QTextEdit in NewTestWizard.ui (object name = description) 
should be changed to QTextDocument, as QTextDocument supports the reST fromat :-)

Why?

Well, a functionality that will be added later is that the tests in a test program
are automatically documented (Sphinx thus) and then the format is much nicer
than the plane text format.

references:
    https://stackabuse.com/python-docstrings/
    https://www.python.org/dev/peps/pep-0287/ <--- PEP
    https://www.sphinx-doc.org/en/master/usage/quickstart.html
    
    
and ... yes !!! Sphinx is a mandatory package for spyder itself, so nothing
needs to be done at that side !
    