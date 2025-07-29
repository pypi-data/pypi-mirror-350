#!/usr/bin/env python3

import sys, re, traceback

__doc__ = """
    $python3 my2to3.py file.py [-w/--write]
    """

def main(args):
    opts = [a for a in args if a.startswith('-')]
    args = [a for a in args if a not in opts]
    
    if not args:
        print(__doc__)
        sys.exit()
    
    for filename in args:
        with open(filename) as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                try:
                    l = len(lines)
                    if "()[" in lines[i]:
                      print('WARNING!, unsubscriptable?!?: %d:%s' % (i,lines[i]))
                    replace_print(lines,i,'-v' in opts)
                    replace_except(lines,i)
                    replace_next(lines,i)
                    remove_future(lines,i)
                    if len(lines) == l: #no lines removed                        
                        i += 1

                except Exception as e:
                    print(lines[i])
                    traceback.print_exc()
                    sys.exit(-1)
        
        print(filename)
        if '-w' in opts or '--write' in opts:
            with open(filename,'w') as f:
                f.write(''.join(lines))
        else:
            print('\n'+''.join(lines)+'\n')
            
    return

###############################################################################

def jump_to_endline(lines,index,multiline = '"""'):
    long_string = lines[index].count(multiline) == 1
    for i,l in enumerate(lines[index:]):
        comment = l.count(multiline) == 1
        extend = l.strip().endswith('\\')
        if any((not i and not comment and not extend,
                i and long_string and comment,
                not long_string and not extend)
            ):
            yield index + i

def insert_before_endline(l,c):
    ll = list(l)
    ll.insert(len(l.rstrip()),c)
    return ''.join(ll)
    
def replace_except(lines,index):
    l = lines[index]
    if l.strip().startswith('except ') and ' as ' not in l:
        #tt = l.split(',')[0].split()[1]
        l = l.split(':',1)
        lines[index] = l[0].replace(',',' as ') + ':' + l[1]
        
    if 'raise ' in l and ',' in l and (
            '(' not in l or l.index(',') < l.index('(') ):
        lines[index] = l.replace(',','(')
        index = next(jump_to_endline(lines,index))
        lines[index] = insert_before_endline(lines[index],')')
        
    return lines[index]

def replace_print(lines,index,verbose = False):
    i0 = index
    #if lines[index].split(':',1)[-1].strip().startswith('print ' ):
    if 'print ' in lines[index]:
        
        verbose = verbose and (index,lines[index].rstrip())
        lines[index] = lines[index].replace('print ','print(')    

        index = next(jump_to_endline(lines,index))

        #ll = list(lines[index])
        #ll.insert(len(lines[index].rstrip()),')')
        #lines[index] = ''.join(ll)
        lines[index] = insert_before_endline(lines[index],')')
        if verbose:
            print('%s => %s' % (verbose,(index,lines[index].rstrip())))
            
    return lines[i0:index+1]

def replace_next(lines, index):
    if '.next()' in lines[index]:
        lines[index] = lines[index].replace('.next()','.__next__()')
    return lines[index]

def remove_future(lines, index):
        """
        Strips any of these import lines:

            from __future__ import <anything>
            from future <anything>
            from future.<anything>
            from builtins <anything>

        or any line containing:
            install_hooks()
        or:
            install_aliases()

        Limitation: doesn't handle imports split across multiple lines like
        this:

            from __future__ import (absolute_import, division, print_function,
                                    unicode_literals)
        """
        line = lines[index].strip().strip('#')
        if (line.startswith('from __future__ import ')
                or line.startswith('from past ')
                or line.startswith('from future ')
                or line.startswith('from builtins ')
                or 'install_hooks()' in line
                or 'install_aliases()' in line
                # but don't match "from future_builtins" :)
                or line.startswith('from future.')):
            if not lines[index].startswith(' '):
                print('REMOVED!: '+line) 
                lines.pop(index)
            else:
                nl = lines[index].index(line)
                lines[index] = lines[index][:nl] + 'pass #' + lines[index][nl:]
                print('COMMENTED: '+lines[index].strip()) 
        else:
            return lines[index]
        
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
