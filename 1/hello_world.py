"""
This file contains a "hello world" program!
"""
# fmt: off
class UserDefinedType: ...

instance = UserDefinedType()
instance.message = "Hello world."
print(f'{instance.message=}')
