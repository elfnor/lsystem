import random
import sys
import multiprocessing
import mathutils as mu

import xml.etree.cElementTree as etree
from xml.etree.cElementTree import fromstring

class LSystem:

    """
    Takes an XML string.
    """
    def __init__(self, rules):
        self._tree = fromstring(rules)
        self._maxDepth = int(self._tree.get("max_depth"))
        self._maxThreads = multiprocessing.cpu_count()
        self._availableThreads = self._maxThreads - 1;
        self._progressCount = 0
        self.id  = 0

    """
    Returns a list of "shapes".
    Each shape is a 2-tuple: (shape name, transform matrix).
    """
    def evaluate(self, seed = 0):
        random.seed(seed)
        rule = _pickRule(self._tree, "entry")
        entry = (rule, 0, mu.Matrix.Identity(4), 0)
        shapes = self._evaluate(entry)
        return shapes
        
    def _evaluate(self, entry):
        stack = [entry]
        shapes = []
	idn = 0
        while len(stack) > 0:
    
            if len(shapes) > self._progressCount + 1000:
                print(len(shapes), "curve segments so far")
                self._progressCount = len(shapes)
        
            rule, depth, matrix, idn = stack.pop()
    
            local_max_depth = self._maxDepth
            if "max_depth" in rule.attrib:
                local_max_depth = int(rule.get("max_depth"))
    
            if len(stack) >= self._maxDepth:
                shapes.append(None)
                continue
    
            if depth >= local_max_depth:
                if "successor" in rule.attrib:
                    successor = rule.get("successor")
                    rule = _pickRule(self._tree, successor)
                    stack.append((rule, 0, matrix, idn))
                shapes.append(None)
                continue
        
            for statement in rule:
                xform = _parseXform(statement.get("transforms", ""))
                count = int(statement.get("count", 1))
                for n in range(count):
                    matrix *= xform
                    
                    if statement.tag == "call":
                        rule = _pickRule(self._tree, statement.get("rule"))
                        cloned_matrix = matrix.copy()
                        entry = (rule, depth + 1, cloned_matrix, idn)
                        if True or self._availableThreads <= 0:
                            stack.append(entry)
                        else:
                            self._spawn(entry)
                           
                    elif statement.tag == "instance":
                        name = statement.get("shape")
                        if name == "curve":
                            P = mu.Vector((0, 0, 0))
                            N = mu.Vector((0, 0, 1))
                            P = matrix * P
                            N = matrix * N
                            shapes.append((P, N))
                        else:
                            shape = (name, matrix, idn)
                            shapes.append(shape)
                            idn = idn + 1
                    else:
                        print("malformed xml")
                        quit()
    
        print("\nGenerated %d shapes." % len(shapes))
        return shapes
        # end of _evaluate
        
#    def _spawn(self, entry):
#        with LOCK:
#            self._availableThreads = self._availableThreads - 1
#            insertionPoint = len(self._shapes)
#            
#        def closure():
#            shapes = self._evaluate(entry)
            
           
        
def _pickRule(tree, name):

    rules = tree.findall("rule")
    elements = []
    for r in rules:
        if r.get("name") == name:
            elements.append(r)

    if len(elements) == 0:
        print("Error, no rules found with name '%s'" % name)
        quit()

    sum, tuples = 0, []
    for e in elements:
        weight = int(e.get("weight", 1))
        sum = sum + weight
        tuples.append((e, weight))
    n = random.randint(0, sum - 1)
    for (item, weight) in tuples:
        if n < weight:
            break
        n = n - weight
    return item

_xformCache = {}

def _parseXform(xform_string):
    if xform_string in _xformCache:
        return _xformCache[xform_string]
        
    matrix = mu.Matrix.Identity(4)
    tokens = xform_string.split(' ')
    t = 0
    while t < len(tokens) - 1:
            command, t = tokens[t], t + 1
    
            # Translation
            if command == 'tx':
                x, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Translation(mu.Vector((x, 0, 0)))
            elif command == 'ty':
                y, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Translation(mu.Vector((0, y, 0)))
            elif command == 'tz':
                z, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Translation(mu.Vector((0, 0, z)))
            elif command == 't':
                x, t = float(tokens[t]), t + 1
                y, t = float(tokens[t]), t + 1
                z, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Translation(mu.Vector((x, y, z)))
    
            # Rotation
            elif command == 'rx':
                theta, t = _radians(float(tokens[t])), t + 1
                matrix *= mu.Matrix.Rotation(theta, 4, 'X')
                
            elif command == 'ry':
                theta, t = _radians(float(tokens[t])), t + 1
                matrix *= mu.Matrix.Rotation(theta, 4, 'Y')
            elif command == 'rz':
                theta, t = _radians(float(tokens[t])), t + 1
                matrix *= mu.Matrix.Rotation(theta, 4, 'Z')
    
            # Scale
            elif command == 'sx':
                x, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Scale(x, 4, mu.Vector((1.0, 0.0, 0.0)))
            elif command == 'sy':
                y, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Scale(y, 4, mu.Vector((0.0, 1.0, 0.0)))
            elif command == 'sz':
                z, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Scale(z, 4, mu.Vector((0.0, 0.0, 1.0)))
            elif command == 'sa':
                v, t = float(tokens[t]), t + 1
                matrix *= mu.Matrix.Scale(v, 4)
            elif command == 's':
                x, t = float(tokens[t]), t + 1
                y, t = float(tokens[t]), t + 1
                z, t = float(tokens[t]), t + 1
                mx = mu.Matrix.Scale(x, 4, mu.Vector((1.0, 0.0, 0.0)))
                my = mu.Matrix.Scale(y, 4, mu.Vector((0.0, 1.0, 0.0)))
                mz = mu.Matrix.Scale(z, 4, mu.Vector((0.0, 0.0, 1.0)))
                mxyz = mx*my*mz
                matrix *= mxyz

            else:
                print("unrecognized transformation: '%s' at position %d in '%s'" % (command, t, xform_string))
                quit()

    _xformCache[xform_string] = matrix
    return matrix

def _radians(d):
    return float(d * 3.141 / 180.0)
