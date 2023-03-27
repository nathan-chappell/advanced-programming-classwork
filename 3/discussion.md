# Where we left off

## Context Managers

There is a convenient way of creating context managers: [`@contextlib.contextmanager`](https://docs.python.org/3.10/library/contextlib.html#contextlib.contextmanager).

BUT! This requires we use
* [**decorators**](https://docs.python.org/3.10/glossary.html#term-decorator), a type of [Higher-order function](https://en.wikipedia.org/wiki/Higher-order_function#:~:text=In%20mathematics%20and%20computer%20science,a%20function%20as%20its%20result.)
* [**generator iterators**](https://docs.python.org/3.10/glossary.html#term-generator-iterator), which are best seen as a *stream* or *process*

*Type theory* provides an interesting and useful common conceptual framework for understanding these entities.  It has powerful relationships with different forms of logic, and it's generalization eventually leads to [Category theory](https://en.wikipedia.org/wiki/Category_theory).

## Recommended reading:

* [Types and Programming Languages - Benjamin C. Pierce](https://www.amazon.com/Types-Programming-Languages-MIT-Press/dp/0262162091)
* [Category Theory for Programmers](https://bartoszmilewski.com/2014/10/28/category-theory-for-programmers-the-preface/)
* [Lectures on the Curry-Howard Isomorphism](https://disi.unitn.it/~bernardi/RSISE11/Papers/curry-howard.pdf)
---

# Type Theory: Outlook

**GOAL**: We should know enough type theory to understand the [*JSON type*](https://www.json.org/json-en.html) -- i.e. we should be able to write a type in our favorite language which contains any object described by *JSON*.

## Path forward

* Review Python's type-system
    - `class` and *algorithmic subtyping*
    - *nominal subtyping* vs *structural subtyping*
    - different ways of introducing types and aliases
* Extract the fundamental abstractions from Python's type-system
    - remove unnecessary operators, "noise" and other information not interesting to mathematics
    - develop some notations
* Develop a set-theoretic "implementation" of our abstract type-system
    - what does that mean?
    - let $\mathcal{O_2}$ denote the open subsets of $\mathbb{R}^2$.  Is $\mathcal{O_2} \in \pi$?  Is that even a valid query?
    - little review of set theory (i.e. the *data model* of mathematics)
* Demonstrate the relationship between logic and type-theory
    - Brief introduction to the *Curry-Howard correspondence*
* Recursive types
    - Infinite tree types
    - Regular tree types and their relationship with [*regular languages*](https://en.wikipedia.org/wiki/Regular_language)
    - $\mu$-notation
* Polymorphism
    - Subtype polymorphism
    - Parametric polymorphism
    - Ad-hoc polymorphism and dependent types.


## Executive summary

* Practically speaking, a *type* is metadata associated to a variable or parameter in a program.
* Proper use of *type annotations* and a *type checker* can help ensure program correctness.
* Different *type systems* have different expressive power - some are even turing complete.
* Some tools are capable of *type inference,* which can reduce tedious and error prone coding practices.
* Some languages offer the ability to read, and even modify, information about types *at runtime.*  Such techniques are broadly called *reflection.*


# Review of Python's type system

## Type Annotations

* `29-Sep-2014` [PEP 526 – Syntax for Variable Annotations](https://peps.python.org/pep-0526/#non-goals)
* `19-Dec-2014` [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
* `08-Jan-2015` [PEP 482 – Literature Overview for Type Hints](https://peps.python.org/pep-0482/)
* `09-Aug-2016` [PEP 484 – Type Hints](https://peps.python.org/pep-0484/#non-goals)


https://peps.python.org/pep-0483/
## Nominal Subtyping

## Towards structural subtyping

# A simplified type system

## Base Types

## Type constructors

# Interpretation (set-theoretic implementation)

## Review of how math itself is implemented

# Curry howard correspondence

# Recursive types

## Intuition

## Formalities

## Notation

## `JSON` excercise

# Polymorphism

## Subtype polymorphism

## Parametric polymorphism

## Ad-hoc polymorphism

## System-F

# General Discussion

## The basic problems in typing

## Complexity, decidability

## Which lambda terms can be given a type?