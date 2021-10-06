
"""
File with classes meant for the simple Behaviour Tree decision making of the player.
"""

class Atomic():
    """Atomic action"""
    
    def __init__(self, func):
        self.func = func

    def run(self):
        return self.func()

class Task(object):
    """Task class"""
    def __init__(self, *children):
        self._children = []
        for child in children:
            self._children.append(child)

class Selector(Task):
    """Selector"""

    def __init__(self, *children):
        super().__init__(*children)
        self.run()
    
    def run(self):
        for c in self._children:
            if c.run():
                return True
        return False

class Sequence(Task):
    """Sequence"""
    
    def __init__(self, *children):
        super().__init__(*children)
        self.run()
    
    def run(self):
        for c in self._children:
            if not c.run():
                return False
        return True
