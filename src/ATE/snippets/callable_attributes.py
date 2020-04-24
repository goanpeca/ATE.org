# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 16:40:44 2020

@author: hoeren
"""
import abc

class testABC(abc.ABC):
    
    def __init__(self):
        self.do_you_know = 'FUBAR'
    
    @abc.abstractmethod
    def do(self):
        pass
    
    def _my_targets(self):
        '''
        this method returns a dictionary with as key the 'do' and 'do_' methods defined,
        and as value a tuple (sha512_hash_of_method_source, default) where default
        indicates if the 'do' function is called or not.
        Note that of course the 'do' method itself is always 'default'🙂
        '''
        import inspect, hashlib
        my_members = inspect.getmembers(self)
        retval = {}
        for member in my_members:
            if member[0]=='do' or member[0].startswith('do_'):
                if inspect.ismethod(member[1]):
                    source = inspect.getsource(member[1])
                    stripped_source = '\n'.join(source.split('\n')[1:])
                    stripped_plain_source = stripped_source.encode('ascii', 'ignore')
                    stripped_plain_source_hash = hashlib.sha512(stripped_plain_source).hexdigest()
                    if member[0]=='do':
                        retval[member[0]] = (stripped_plain_source_hash, True)
                    else:
                        last_statement_of_stripped_source = stripped_source.split('\n')[-2]
                        if last_statement_of_stripped_source == '        return self.do()':
                            retval[member[0]] = (stripped_plain_source_hash, True)
                        else:
                            retval[member[0]] = (stripped_plain_source_hash, False)
        if 'do' not in retval:
            raise Exception("What the fuck!, where is the default implementation ?!?")
        return retval
    

class A(testABC):

    def do(self):
        # foo
        pass
    
    def do_target1(self):
        '''
        docstring
        '''
        retval = {}
        return retval
                
    def do_target2(self):
        # some comment
        return self.do()
    
    def do_target3(self):
        return self.do()

if __name__ == '__main__':
    
    a = A()
    targets = a._my_targets()
    print(targets)
