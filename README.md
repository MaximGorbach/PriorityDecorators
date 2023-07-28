# Priority Decorators
This is a python library that allows adding decorators to object and class methods with priority (the priority controls the order in which decorators will be executed), and also access to the next decorator in the chain.  
This allows for more complex decorators that can be chained together, and also allows for decorators to be easily removed after addition.  
This can be particularly useful in scenarios where you want to add augmentations to an objects functionality in such a way that they can easily affect each other. Personally, I created this technique for use in game development when adding rogue-like style effects to items that can potentially augment any behaviour in the game. This allows for a very flexible system that can be easily extended and modified, without having to even modify the source code for the object being augmented.

## Example
This is a simple example of how to use the decorators.
```python
from prioritydecorators.prioritydecorators import decorate_class, decorate_object

class A:
        num: int = 2

        def greeting(self, name):
            print(f"Hi {name}, I'm {self.num}")


    def f1(obj, next_hook, name):
        print("f1 executed")
        next_hook(name + "1")

    def f2(obj, next_hook, name):
        print("f2 executed")
        next_hook(name + "2")

    a = A()

    # decorated an object method
    # decorators return a handle that can be used to remove the decorator
    # higher priority decorators are executed first
    handle1 = decorate_object(a.greeting, f1, priority=6)
    handle2 = decorate_object(a.greeting, f2)
    a.greeting("Max")

    # removing the decorators
    handle1.undecorate()
    handle2.undecorate()
    a.greeting("Max")

    #### Expected output ####:
    # f1 executed
    # f2 executed
    # Hi Max12, I'm 2
    # Hi Max, I'm 2
```

This is an example of how I would use this in a game. Imagine we want to add some items which will change a players shoot effect to also shoot backwards, and also shoot multiple times. We can do this by adding decorators to the shoot method of the player class. This will mean that we can easily add both effects to the player, without having to manually implement the interaction between the two items, or change the player code.  
Note that here the order of the decorators won't matter, we will get the same result either way, but generally the order will matter, and the priority can be used to control this. Additionally, you have full control of how you utilise `next_hook`, for example you could choose to call it before executing this functions effects (this would effectively reverse the priority order), or not call it at all. For example if I were adding a shield effect decorator to a players `take_damage` method, I could choose not to call the next hook if the shield is active, and instead just return without taking damage. In this case I would want to give the shield decorator a higher priority than the damage decorator, so that the shield is checked first.
```python

```python
from prioritydecorators.prioritydecorators import decorate_class, decorate_object

class Player:
    def shoot(angle):
        print(f"Player shot at {angle}")

def multi_shot_decorator(obj, next_hook, angle):
    print("multi_shot_decorator executed")
    next_hook(angle)
    next_hook(angle + 10)
    next_hook(angle - 10)

def backwards_shot_decorator(obj, next_hook, angle):
    print("backwards_shot_decorator executed")
    next_hook(angle + 180)


player = Player()
decorate_object(player.shoot, multi_shot_decorator)
decorate_object(player.shoot, backwards_shot_decorator)

player.shoot(0)

#### Expected output ####:
# multi_shot_decorator executed
# backwards_shot_decorator executed
# Player shot at 0
# Player shot at 10
# Player shot at -10
# Player shot at 180
# Player shot at 190
# Player shot at 170
```