# Discussions for `hello_world.py`

## Do you understand all the code written?

|lines | reference|
|-|-|
|1-3|[string-literals](https://docs.python.org/3.10/reference/lexical_analysis.html#string-and-bytes-literals), [help](https://docs.python.org/3/library/functions.html#help), [pydoc](https://docs.python.org/3.10/library/pydoc.html)|
|5|[classes](https://docs.python.org/3.10/reference/datamodel.html#index-32), [class-definitions](https://docs.python.org/3.10/reference/compound_stmts.html#grammar-token-python-grammar-classdef), [...](https://docs.python.org/3.10/library/constants.html#Ellipsis)|
|7|[assignment-statement](https://docs.python.org/3.10/reference/simple_stmts.html#assignment-statements), [calling-classes](https://docs.python.org/3.10/reference/datamodel.html#index-32), module...|
|8|[attribute-ref](https://docs.python.org/3.10/reference/expressions.html#grammar-token-python-grammar-attributeref) - we shall discuss this in some detail|
|9|[formatted-string-literals](https://docs.python.org/3/reference/lexical_analysis.html#f-strings), [print](https://docs.python.org/3/library/functions.html#print)|

## Okay, now that we know what we're looking at here, let's discuss attribute access...

* We should all really read the documentation for `object.__getattr__` and `object.__getattribute__`: [Customizing-attribute-access](https://docs.python.org/3.10/reference/datamodel.html#customizing-attribute-access)
* This should lead to a discussion of inheritance, in particular the notion of a virtual method
* We should ask ourselves, *can we dig any deeper?* - let's check out how all this goes down in cpython
* Hopefully we run into `__get__`

## Exercise: JSON persistent python objects...
* I wan't objects that persist themselves when the interpreter exits...
* Idea: intercept attribute get/set to look at a file (e.g. `./.data.json`)

## Bonus!  You guys can help me figure something out...

* how does accessing a method work?  We can read the docs, but it doesn't say anything about `__get__`
* consider `demo` in `attribute_`... how could we test this theory?
* Answer: debug python itself