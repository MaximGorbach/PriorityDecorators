from dataclasses import dataclass
import types
import functools
from sortedcontainers import SortedList
import itertools

class DecoratedFunction:
    decorating_class: bool
    decorators: SortedList
    original: any = None
    __name__ = "Decorated Function"

    def __init__(self, original, decorating_class: bool = False):
        self.decorating_class = decorating_class
        self.decorators = SortedList()
        self.original = original
        self.__name__ = f"Decorated '{original.__name__}'"

    def set_original(self, func):
        self.original = func

    def add_decorator(self, decorator: 'Decorator'):
        self.decorators.add(decorator)

    def remove_decorator(self, decorator: 'Decorator'):
        self.decorators.remove(decorator)

    def empty(self):
        return len(self.decorators) == 0

    def class_method(self):
        def f(obj, *args, **kwargs):
            self.__call__(obj, *args, **kwargs)
        return f

    def __call__(self, obj, *args, **kwargs):
        if self.decorating_class:
            decorator_iter = itertools.chain(iter(self.decorators[1:]), [lambda *a, **kw: self.original(obj, *a, **kw)])
        else:
            decorator_iter = itertools.chain(iter(self.decorators[1:]), [self.original])

        if self.empty():
            if self.decorating_class:
                self.original(obj, *args, **kwargs)
            else:
                self.original(*args, **kwargs)
        else:
            self.decorators[0](decorator_iter, obj, *args, **kwargs)


    

@functools.total_ordering
class Decorator:
    priority: int
    func: any

    def __init__(self, func, priority = 5):
        self.func = func
        self.priority = priority

    def __call__(self, decorator_iter, obj, *args, **kwargs):
        next_decorator = decorator_iter.__next__()
        if isinstance(next_decorator, Decorator):
            self.func(obj, lambda *a, **kw: next_decorator(decorator_iter, obj, *a, **kw), *args, **kwargs)
        else:
            self.func(obj, lambda *a, **kw: next_decorator(*a, **kw), *args, **kwargs)

    def __lt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.priority == other.priority



@dataclass
class DecoratorHandle:
    """ Use `undecorate()` on the handle to remove the decorator """
    Decorated_func: DecoratedFunction
    decorator: Decorator

    def undecorate(self):
        """ Removes the decorator from the object/class """
        if not self.used():
            self.Decorated_func.remove_decorator(self.decorator)
            self.Decorated_func = None
            self.decorator = None

    def used(self):
        return self.Decorated_func is None or self.decorator is None



def decorate_object(obj_method, func, priority = 5) -> DecoratorHandle:
    """ 
    Adds a decorator to the object method. \\
    Higher priority decorators will be executed first. \\
    Decorator functions should have arguments:
    * `obj` - this is equivalent to self; the object the function is being called on
    * `next_decorator` - this is the next decorator in the queue, or the original function
    * The rest of the arguments should be the same as the arguments for the original function
    
    Returns a `DecoratorHandle` which can be used to undecorate
    """
    new_decorator = Decorator(func, priority=priority)
    if isinstance(obj_method.__func__, DecoratedFunction):
        obj_method.add_decorator(new_decorator)
        h = obj_method
    else:
        h = DecoratedFunction(obj_method)
        h.add_decorator(new_decorator)
        setattr(obj_method.__self__, obj_method.__name__, types.MethodType(h, obj_method.__self__))
    return DecoratorHandle(h, new_decorator)


def decorate_class(cls, cls_func, decorate_func, priority = 5) -> DecoratorHandle:
    """ 
    Adds a decorator to the class function. \\
    Higher priority decorators will be executed first. \\
    Decorator functions should have arguments:
    * `obj` - this is equivalent to self; the object the function is being called on
    * `next_decorator` - this is the next decorator in the queue, or the original function
    * The rest of the arguments should be the same as the arguments for the original function

    Returns a `DecoratorHandle` which can be used to undecorate
    """
    new_decorator = Decorator(decorate_func, priority=priority)
    closure = cls_func.__closure__
    if closure is not None and isinstance(closure[0].cell_contents, DecoratedFunction):
        h = closure[0].cell_contents
        h.add_decorator(new_decorator)
    else:
        h = DecoratedFunction(cls_func, decorating_class=True)
        h.add_decorator(new_decorator)
        setattr(cls, cls_func.__name__, h.class_method())
    return DecoratorHandle(h, new_decorator)









if __name__ == "__main__":
    class A:
        num: int = 2

        def get_num(self):
            print(self.num)

        def greeting(self, name):
            print(f"Hi {name}, I'm {self.num}")


    def f1(obj, next_hook, name):
        print("hi")
        next_hook(name + "1")

    def f2(obj, next_hook, name):
        print("bye")
        next_hook(name + "2")

    handle1 = decorate_class(A, A.greeting, f1)
    handle2 = decorate_class(A, A.greeting, f2)
    a = A()
    # handle1 = hook_object(a.greeting, f1, priority=6)
    # handle2 = hook_object(a.greeting, f2)
    a.greeting("Max")
    handle1.undecorate()
    handle2.undecorate()
    a.greeting("Max")