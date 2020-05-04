# -*- coding: utf-8 -*-
'''
Created on 24 Oct 2016

@author: tho

'''

import inspect, imp
import logging
import os, sys, re
import copy
import random
import hashlib
import abc.ABC

Pass = 1
Fail = 0
Undetermined = -1
Unknown = -1

class testABC(abc.ABC):
    '''
    This is the Abstract Base Class for all ATE.org tests.
    '''
    start_state = None
    end_state = None
    input_parameters = {}
    output_parameters = {}
    extra_output_parameters = {}
    patterns = []
    tester_states = []
    test_dependencies = []
    tester = None
    ran_before = False

    def __init__(self):
        self.name = str(self.__class__).split('main__.')[1].split("'")[0]
        tmp = str(inspect.getmodule(self)).split("from '")[1].replace("'", '').replace('>', '').split('/')
        self.test_dir = os.sep.join(tmp[0:-1])
        self.file_name = tmp[-1]
        self.file_name_and_path = os.sep.join(tmp)
        self.project_path = os.sep.join(tmp[0:-3])
        self.project_name = tmp[-3]

        logging.debug("Initializing test '%s' in module '%s'" % (self.name, self.file_name_and_path))

        #self._add_setup_states_to_start_state()
        #self._add_teardown_states_to_end_state()
        self._extract_patterns()
        self._extract_tester_states()




        self._extract_tester()
        self.sanity_check()

    def __call__(self, input_parameters, output_parameters, extra_output_parameters, data_manager):
        '''
        This method is how the test will be called from a higher level
        '''
        # retval = self.do(input_parameters, output_parameters, extra_output_parameters, data_manager)


    def __del__(self):
        pass


    @abc.abstractmethod
    def do(self, ip, op, ep, dm):
        pass

    def _extract_test_dependencies(self):
        '''
        This method will analyze the do method, and extract all the test dependencies (by looking what is accessed in the DataManager (dm) and add them to self.test_dependencies
        '''
        test_dependencies = []
        #TODO: Implement test dependency extraction from do
        self.test_dependencies += test_dependencies
        self.test_dependencies = sorted(set(self.test_dependencies)) # no duplications, sorted alphabetically

    def _extract_tester(self):
        '''
        This method will extract the used tester (firmware) self.tester accordingly.
        '''
        fp, pathname, description = imp.find_module(self.name, [self.test_dir])
        module = imp.load_module(self.name, fp, pathname, description)
        for member in inspect.getmembers(module, inspect.isclass):
            if 'ATE.Tester.' in str(member[1]):
                self.tester = (str(member[1]).split('<class')[1].strip().replace('>', '').replace("'", ''), member[0])

    def _get_imports(self):
        '''
        This method will return a list of all imports of this (test) module.
        Each import is a tuple formatted as follows (from, what, as)
            'from bla.bla.bla import foo as bar" --> ('bla.bla.bla', 'foo', 'bar')
            'import os' --> ('', os, '')
        '''
        fp, pathname, description = imp.find_module(self.name, [self.test_dir])
        module = imp.load_module(self.name, fp, pathname, description)
        for member in inspect.getmembers(module):
            print(member)


    def _get_method_source(self, method):
        '''
        This method will return the source code of the named method of the test class
        '''
        fp, pathname, description = imp.find_module(self.name, [self.test_dir])
        module = imp.load_module(self.name, fp, pathname, description)
        class_of_interest = None
        retval = ''
        for member in inspect.getmembers(module, inspect.isclass):
            if member[0] == self.name:
                class_of_interest = member[1]
        print(method)
        print(class_of_interest)
        if class_of_interest is not None:
            method_of_interest = None
            for member in inspect.getmembers(class_of_interest, inspect.ismethod):
                print(member)
                if member[0] == method:
                    method_of_interest = member[1]
            print(method_of_interest)
            retval = inspect.getsource(method_of_interest)
        return retval

    def _get_if_elif_structure(self, method):
        '''
        This method will return the if/elif structure from the named method in the form of a dictionary.
        It will choke on a else statement!
        '''
        if method == 'pre_do' or method == 'post_do':
            code_lines = self._get_method_source(method).split('\n')
            def_regex = "\s*(?:def)\s+(?P<function_name>\w+)\s*\(\s*self\s*,\s*(?P<switch>\w+)\):"
            def_pattern = re.compile(def_regex)
            if_regex = '''\s*if\s+(?P<switch>[^ =]+)\s*==\s*(?P<quoting>['"])(?P<state>\w+)(?P=quoting):'''
            if_pattern = re.compile(if_regex)
            elif_regex = '''\s*elif\s+(?P<switch>[^ =]+)\s*==\s*(?P<quoting>['"])(?P<state>\w+)(?P=quoting)\s*:'''
            elif_pattern = re.compile(if_regex)
            go_from_regex = "\s*go_from_(?P<from_state>\w+)_to_(?P<to_state>\w+)_state()"
            go_from_pattern = re.compile(go_from_regex)
            split_pattern = "\s*(?:el)+?if\s+(?P<switch>%s.upper())\s+(?:==)"
            base_indent = len(code_lines[0]) - len(code_lines[0].lstrip())
            retval = {0:None}
            chunk = 0
            for code_line in code_lines:
                if code_line.strip() == '': continue
                indent = (len(code_line) - len(code_line.lstrip()) - base_indent)/base_indent
                if chunk == 0: # in function definition or pre-switch config
                    if indent == 0: # in function definition
                        def_match = def_pattern.match(code_line)
                        if not def_match:
                            raise Exception("Couldn't match '%s'" % code_line)
                        else:
                            switch = def_match.group('switch')
                            if method != def_match.group('function_name'):
                                raise Exception("Unexpected method naming ('%s'<->'%s')" % (method, def_match.group('function_name')))
                            retval[0] = (method, switch) # is always chunk 0 !
                    elif indent == 1:
                        if code_line.stip().startswith('if'):
                            pass
                        else:
                            pass
                    else:
                        pass
                else: # in switch definition
                    if indent == 0: # can only be comment !!!
                        pass
                    elif indent == 1: # can only be if/elif statement
                        if code_line.strip().startswith('else'):
                            raise Exception("'%s' can not contain a general else statement !" % method)
                        if code_line.strip().startswith('if') or code_line.strip().startswith('elif'):
                            chunk += 1
                            retval[chunk]=[]
                            if_match = if_pattern.match(code_line)
                            if not if_match:
                                raise Exception("Couldn't match '%s'" % code_line)
                            else:

                                pass
                        else:
                            retval[chunk].append(code_line)

                    elif indent == 2: # switch block code
                        pass
                    else: # switch block code
                        pass


        else:
            raise Exception("'_get_if_elif_structure' only applies to 'pre_do' and 'post_do'")




    def _set_method_source(self, method, source):
        '''

        '''
        pass


    def _add_pre_do_states_to_start_state(self):
        '''
        self.start_state is a string prior to class instantization.
        The __init__ method will call this function to transform the start state in a 2 element tuple,
        the first element being the start state of the do function (=initial assignment to start_state)
        and the second element is a list of all the from_states defined in setup.
        '''
        if type(self.start_state) == tuple:
            self.start_state = self.start_state[0]
        setup_states = []
        code_lines = self._get_method_source('setup').split('\n')
        switch = code_lines[0].strip().split(',')[1].strip().replace(',', ')').split(')')[0].strip()
        for code_line in code_lines:
            if 'if' in code_line:
                code_line = code_line.split('if')[1]
                if switch in code_line:
                    code_line = code_line.split(switch)[1].replace(' ','').replace('==', '').replace(':', '')
                    if code_line.startswith("'"):
                        code_line = code_line.replace("'", '')
                    if code_line.startswith('"'):
                        code_line = code_line.replace('"', '')
                    setup_states.append(code_line)
        self.start_state = (self.start_state, setup_states)

    def _add_post_do_states_to_end_state(self):
        '''
        self.end_state is a string prior to class instantization.
        The __init__ method will call this function to transform the start state in a 2 element tuple,
        the first element being the end state of the do function (=initial assignment to end_state)
        and the second element is a list of all the to_states defined in teardown.
        '''
        if type(self.end_state) == tuple:
            self.end_state = self.end_state[0]
        setup_states = []
        print

        code_lines = self._get_method_source('teardown').split('\n')
        switch = code_lines[0].strip().split(',')[1].strip().replace(',', ')').split(')')[0].strip()
        for code_line in code_lines:
            if 'if' in code_line:
                code_line = code_line.split('if')[1]
                if switch in code_line:
                    code_line = code_line.split(switch)[1].replace(' ','').replace('==', '').replace(':', '')
                    if code_line.startswith("'"):
                        code_line = code_line.replace("'", '')
                    if code_line.startswith('"'):
                        code_line = code_line.replace('"', '')
                    setup_states.append(code_line)
        self.end_state = (self.end_state, setup_states)


# ---    
            
    def _get_method_info(self, method_object):
        '''
        this method returns a tuple (source_file, source_lines, line_number, doc_string) of obj.
        obj **must** be a method object!
        '''
        if not inspect.ismethod(method_object):
            raise Exception("What is going on ?!? 'obj' should be a menthod !!!")
        source_file = inspect.getfile(method_object)
        source_lines, line_number = inspect.getsourcelines(method_object)
        doc_string = inspect.getdoc(method_object)
        return(source_file, source_lines, line_number, doc_string)

    def _calculate_hash(self, source_lines, doc_string):
        '''
        this method calculates tha hash of the source_lines (excluding the
        doc_string and any commented out lines).
        '''
        def cleanup(source_lines, doc_string, block_size):
            '''
            this method removes the doc_string and any comments from source_lines
            and returns the concateneted ASCII version of the source_lines in a
            list of block_size chunks.
            '''
            pure_ascii_code = b''
            my_doc_string = ''
            in_doc_string = False
            for index in range(1, len(source_lines)):
                line = source_lines[index].lstrip()
                if in_doc_string:
                    if line.rstrip().endswith("'''") or line.rstrip().endswith('"""'):
                        in_doc_string = False
                        if line.rstrip()[:-3] != '':
                            my_doc_string += line.rstrip()[:-3]
                        else:
                            my_doc_string = my_doc_string.rstrip()
                        continue
                    else:
                        if line == '':
                            my_doc_string += '\n'
                        else:
                            my_doc_string += line
                else:
                    if line.startswith("'''") or line.startswith('"""'):
                        if line.rstrip().endswith("'''") or line.rstrip().endswith('"""'):
                            pass
                        else:
                            in_doc_string = True
                            if line[3:].strip() != '':
                                my_doc_string += line[3:]
                            continue
                    else:
                        pure_ascii_code += source_lines[index].encode('ascii', 'ignore')
            if my_doc_string == '':
                my_doc_string = None
                
                
                
            print(source_lines[0].strip())
            print('-'*len(source_lines[0].strip()))
            print(my_doc_string)
            print('='*100)
            print(doc_string)
            print('-'*99, '>', my_doc_string == doc_string)
                






            if len(pure_ascii_code)>block_size:
                pure_ascii_code_chunks = [pure_ascii_code[i*block_size:(i+1)*block_size] for i in range(int(len(pure_ascii_code)/block_size))]
                if len(pure_ascii_code)%block_size!=0:
                    pure_ascii_code_chunks+=[pure_ascii_code[int(len(pure_ascii_code)/block_size):]]    
            else:
                pure_ascii_code_chunks = [pure_ascii_code]
            return pure_ascii_code_chunks

        method_hash = hashlib.sha512()
        pure_ascii_code_chunks = cleanup(source_lines, doc_string, method_hash.block_size)
        for pure_ascii_code_chunk in pure_ascii_code_chunks:
            method_hash.update(pure_ascii_code_chunk)
        return method_hash.hexdigest()

    def _get_targets(self):
        '''
        this method returns a dictionary with as key the 'do' and 'do_' methods defined,
        and as value a tuple (method_code_hash, default, source_file_name, line_number) 
        where default indicates if the 'do' function is called (directly) or not.
        line_number is the line number on which the method is defined.
        Notes
            - Of course the 'do' method itself is always 'default' 🙂
        TODO:
            - exclude the docstring from the code prior to hashing
            - get how 'do' is called, and use that for all members (instead of static compare)
        '''
        retval ={}
        all_members = inspect.getmembers(self)
        members_of_interest = {}
        for member in all_members:
            if member[0]=='do' or member[0].startswith('do_'):
                if inspect.ismethod(member[1]):
                    members_of_interest[member[0]] = member[1]
        if not 'do' in members_of_interest:
            raise Exception("What the fuck!, where is the default 'do' implementation ?!?")

        for member in members_of_interest:
            source_file, source_lines, line_number, doc_string = self._get_method_info(members_of_interest[member])
            method_code_hash = self._calculate_hash(source_lines, doc_string)
            if member == 'do':
                members_of_interest[member] = (method_code_hash, True, source_file, line_number)
            else:
                if source_lines[-1].strip() == 'return self.do()':
                    members_of_interest[member] = (method_code_hash, True, source_file, line_number)
                else:
                    members_of_interest[member] = (method_code_hash, False, source_file, line_number)

        return members_of_interest    



    def run(self, from_state, to_state, ip, op, eop=None, dm=None):
        logging.debug("Running test '%s' from start_state '%s' to end_state '%s' with parameters '%s'" % (self.name, from_state, to_state, ip))
        if from_state != self.start_state[0]:
            if from_state in self.start_state[1]:
                logging.debug("   Executing setup(%s)" % from_state)
                self.pre_do(from_state)
            else:
                msg = "Test '%s' doesn't support running from '%s' state" % (self.name, from_state)
                logging.critical(msg)
                raise Exception(msg)
        else:
            logging.debug("   Skipping pre_do")
        logging.debug("   Executing do(%s, %s, %s, %s)" % (ip, op, eop, dm))
        retval = self.do(ip, op, eop, dm)
        logging.debug("   do returned '%s'" % retval)
        if to_state != self.end_state[0]:
            if to_state in self.end_state[1]:
                logging.debug("   Executing teardown(%s)" % to_state)
                self.post_do(to_state)
            else:
                msg = "Test '%s' doesn't support running to '%s' state" % (self.name, to_state)
                logging.critical(msg)
                raise Exception(msg)
        else:
            logging.debug("   Skipping post_do")
        bin_code = int(random.uniform(0, 100)) #TODO: pass op & eop to the data manager and get a bincode back.
        logging.debug("   data manager returned (soft) bincode '%s'" % bin_code)
        if not self.ran_before:
            self.ran_fefore = True

def isEmptyFunction(func):
    '''
    This function will determine if the passed func (or method) is empty or not.
    A doc-string may be present but doesn't influence this function, nor does multiple pass statements.
    '''
    def empty_func():
        pass

    def empty_func_with_doc():
        """Empty function with docstring."""
        pass

    return func.__code__.co_code == empty_func.__code__.co_code or func.__code__.co_code == empty_func_with_doc.__code__.co_code

if __name__ == '__main__':
    pass
    #TODO: Implement the unit tests here ...
