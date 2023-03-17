class Foo:
    def __getattr__(self, name):
        ...

    def __getattribute__(self, name):
        ...


class Method:
    """This is how I think methods are implemented..."""

    def _implementation(self, instance, *args):
        print(f"Method._implementation({id(instance)})")

    def __get__(self, instance, owner=None):
        def invokable(*args):
            return self._implementation(instance, *args)

        return invokable


class Class:
    method = Method()

    @staticmethod
    def demo():
        instance = Class()
        instance.method()
        method = instance.method
        method()


def create_contrived_hierarchy(depth=10):
    class ContrivedHierarchyBase:
        def method(self):
            ...

    most_derived_type = ContrivedHierarchyBase

    for i in range(depth):
        most_derived_type = type(f"ContrivedHierarchy{i}", (most_derived_type,), {})

    return most_derived_type
