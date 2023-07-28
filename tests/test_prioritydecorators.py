from prioritydecorators.prioritydecorators import decorate_class, decorate_object

def log_output(new_val, curr_log):
    curr_log.append(new_val)

def test_decorate_object():
    log = []
    exp_log = [
        "f2 executed",
        "f1 executed",
        "Hi Max21, I'm 2",
        "Hi Max, I'm 2"
    ]

    class A:
        num: int = 2

        def greeting(self, name):
            log_output(f"Hi {name}, I'm {self.num}", log)


    def f1(obj, next_hook, name):
        log_output("f1 executed", log)
        next_hook(name + "1")

    def f2(obj, next_hook, name):
        log_output("f2 executed", log)
        next_hook(name + "2")

    a = A()
    handle1 = decorate_object(a.greeting, f1)
    handle2 = decorate_object(a.greeting, f2, priority=6)
    a.greeting("Max")
    handle1.undecorate()
    handle2.undecorate()
    a.greeting("Max")

    assert log == exp_log


def test_decorate_class():
    log = []
    exp_log = [
        "f2 executed",
        "f1 executed",
        "Hi Max21, I'm 2",
        "Hi Max, I'm 2"
    ]

    class A:
        num: int = 2

        def greeting(self, name):
            log_output(f"Hi {name}, I'm {self.num}", log)


    def f1(obj, next_hook, name):
        log_output("f1 executed", log)
        next_hook(name + "1")

    def f2(obj, next_hook, name):
        log_output("f2 executed", log)
        next_hook(name + "2")

    handle1 = decorate_class(A, A.greeting, f1)
    handle2 = decorate_class(A, A.greeting, f2, priority=6)
    a = A()
    a.greeting("Max")
    handle1.undecorate()
    handle2.undecorate()
    a.greeting("Max")

    assert log == exp_log