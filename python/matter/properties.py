from __future__ import print_function

class Property(object):

    def __init__(self, name, doc):
        self.name = name
        self.doc = doc
        self.val = None
        return

    def __get__(self, obj, type=None):
        if obj is None: return type.__dict__[self.name]
        return obj.__dict__.get(self.name)


    def __set__(self, obj, value):
        obj.__dict__[self.name] = value
        return value


    def __delete__(self, obj):
        del obj.__dict__[self.name]

    pass


class ReadOnlyProperty(Property):


    def __set__(self, obj, value):
        raise AttributeError("property {0!s} is readonly".format(self.name))


    pass # end of ReadOnlyProperty



class InferredProperty(ReadOnlyProperty):


    def __init__(self, name, doc, infer_function):
        ReadOnlyProperty.__init__(self, name, doc)
        self.infer_function = infer_function
        return
    

    def __get__(self, obj, type=None):
        rt = ReadOnlyProperty.__get__(self, obj, type)
        #print('obj',obj)
        #print('rt',rt)
        
        if rt is None:
            rt = self.infer_function(obj)
            #print('new rt',rt)
            Property.__set__(self, obj, rt)
            pass
        
        return rt


    pass # end of InferredProperty
        


class CtorArg(Property):

    def __set__(self, obj, value):
        if self.__get__(obj) is None:
            return Property.__set__(self, obj, value)
        raise AttributeError("{0!s} is not setable. Please create a new {1!s} object".format(
            self.name, obj.__class__.__name__))


    def __delete__(self, obj):
        raise AttributeError("{0!s} is not deletable.".format(self.name))
    
    pass # end of CtorArg



class State(Property):

    def __get__(self, obj, type=None):
        rt = Property.__get__(self, obj, type)
        if rt is None:
            raise AttributeError("State {0!s} has not been set".format(self.name))
        return rt

    pass # end of State
