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
* **TODO:** Mention abstract interpretation


# Review of Python's type system

## Type Annotations

* `29-Sep-2014` [PEP 526 – Syntax for Variable Annotations](https://peps.python.org/pep-0526/#non-goals)
* `19-Dec-2014` [PEP 483 – The Theory of Type Hints](https://peps.python.org/pep-0483/)
* `08-Jan-2015` [PEP 482 – Literature Overview for Type Hints](https://peps.python.org/pep-0482/)
* `09-Aug-2016` [PEP 484 – Type Hints](https://peps.python.org/pep-0484/#non-goals)

## Nominal Subtyping

* "Nominal Subtyping" refers to the "name-based" class hierarchies you can create in most OOP languages.

```py
class Base1:
    x: int

class Base2:
    y: int

class Derived1(Base1):
    y: int

class Derived2(Base1, Base2):
    pass
```

![nominal_subytyping_example_hierarchy](./img/nominal_subytyping_example_hierarchy.svg)

Pros:
* simple, easy to implement and understand
* traditional, explicit

Cons:
* many "essentially equivalent types" (see `Derived1` and `Derived2`)
* traditional, explicit

## Towards structural subtyping

* Protocols
* Abstract Base Classes

Consider the following classes:

```python
class Point2D:
    x: int
    y: int

class PointZ2:
    x: int
    y: int
```

In *nominal subtyping* we have that `Point2D` and `PointZ2` are incomparable.  But we can carelessly use an instance of one in place of the other, as long as we don't use information about the *type*.

Suppose we forget about the *names* of classes, and focus on the *fields.*  We would like to define a *type* that represents all classes with an `x: int` and a `y: int` field.  This leads to *structural subtyping*, known in python as [`typing.Protocol`](https://peps.python.org/pep-0544/#protocol-members).  It's all quite interesting and useful, but it's a technical complication that we should further abstract.

# A simplified type system

Let's now forget about the names of *fields,* and focus on the *type* and *offset*.  For example, we could represent `Point2D` and `PointZ2` as a `tuple[int,int]`.  Observe:

```python
def isomorphism(point_or_tuple) -> 'tuple_or_point':
    if isinstance(point_or_tuple, tuple): return Point2D(t[0], t[1])
    else: return (point_or_tuple.x, point_or_tuple.y)
```


# A simplified type system

* [`Callable`](https://docs.python.org/3.10/library/typing.html#callable)
* [`tuple` and PEP 585 – Type Hinting Generics In Standard Collections](https://peps.python.org/pep-0585/)

## Base Types (Built-in types)

[The standard type hierarchy](https://docs.python.org/3.10/reference/datamodel.html#the-standard-type-hierarchy)

The *essential* types

* **`None`**
* **`bool`**
* **`tuple`**
* **`Callable`**
* We'll probably use **`int`** just to make our discussions more *concrete*

Other special types:

* Specials
    - `NotImplemented`
    - `Ellipsis`
* Numeric
    - `float`
    - `complex`
* Immutable Sequences
    - `str`
    - `bytes`
* Mutable Sequences
    - `list`
    - `bytearrays`
    - `complex`
* Miscellaneous
    - sets, dicts, functions, classes, generators, coroutines...

## Abstraction: the operators and built-ins that we need...

* **`bool`**
* Product
* Function
* Subtype...

Let's also notice that we can restrict our consideration to functions of only one variable.  Consider:

```python
def curry(f: Callable[[T, U], R]) -> Callable[[T], Callable[U, R]]:
    return lambda t: lambda u: f(t, u)
```

In principle, we should only need to consider the `None` type, but we'll also allow `int`, `bool`, and `str` to make our type system feel more "concrete."

Our type system will then be:

* Built-in types `None`, `int`, `bool`, and `str`, however we will typically use sets $0 = \empty, 1 = \{0\}, \dots,n+1 = \{n\}\cup n$
* for any types `T1`, `T2`, ..., `TN`, a *product type* `tuple[T1, T2, ..., TN]`, or $T_1 \times T_2 \times \cdots \times T_n$
* for any types `T`, `U`, a *function type* `Callable[T, U]`, or $T \rightarrow U$

We will take a subset of python as our the *language* we will consider.  Our language $Py$ will consist of:

## Declarations

**Variable Declaration**

```python
x: int
f: Callable[[int], str]
```

**Type Aliases**

```python
T = str
U = int
f: Callable[T,U]
```

## Expressions

**Tuple Formation and Indexing**

```python
(x, y)
t[0]
```

**Function call**

```python
f(s)
```

We omit the formalities, but also allow expressions like `f(t[x])` and `t[f(u[0])]` - roughly speaking, the variables above could be replaced by any expression.

## Context

We will adopt the following convention.  We will always consider a fixed *context* (or $\Gamma$), where all our declarations will be placed.  This way we can focus on the *expressions*, the interesting part of our language.

## Typing

Consider the following typing rules.

* **Introduction Rules**
* if `u_x: U` and `def f(x: T): return u_x`, then `f: Callable[[T], U]`
* if `ti: Ti` for `1 <= i <= n`, then `(t1, t2, ..., tn): tuple[T1, T2, ..., Tn]`
* **Elimination Rules**
* if `x: T` and `f: Callable[[T], U]` then `f(x): U`
* if `t: tuple[T1, T2, ..., TN]` and `i: int` and `1 <= i <= n`, then `t[i]: Ti`

# The Curry-Howard correspondence

Consider the following statements:

* If I know that $\phi$ is true, and I know that $\phi \Rightarrow \psi$, then I know that $\psi$ is true
* If I know that $\phi_1 \land \phi_2 \land \cdots \land \phi_n$ is true, then for an $i: 1\leq i\leq n$, $\phi_i$ is true

These are remarkably similar to our typing rules.  These statements describe a framgent of *propositional logic* consisting of $\{\land, \Rightarrow\}$.  We shall investigate this relationship now.

## Interpretation (set-theoretic implementation)

Typically, when we describe an abstraction, we would like to make sure that it actually exists (more specifically, that it's possible for it to exist).  The study of this pursuit is known as *Model Theory.*  We'll keep it simple (for my sake), and state the following purpose:

> Implement our type system and fragment of logic with sets and set theory.

Hopefully, after "implementing" our abstractions, we will see more clearly the connection between the two.

### Logic

The fragment's grammar is:

* $T \mapsto p$ where $p,q,r,\dots$ are variables
* $T \mapsto T \land T \dots \land T$
* $T \mapsto T \Rightarrow T$

A *context* for our grammar, denoted $\Gamma$, is a subset of the propositional variables.  Specifically, we will take $\Gamma$ to be the variables that get assigned **true**.  We need to create a system of sets and operations so that the semantics given by the rules above are satisfied.

There is a straightforward way of doing this, but some notation will be helpful.  We use variable like $\phi$ and $\psi$ to range of the fragment.  We use the notation $\mathrm{Set}(\phi)$ to denote the set which represents $\phi$ in our model.  We define the function $\mathrm{Set}()$ inductively:

* if $p$ is **true**, then $\mathrm{Set}(p) = \{\empty\}$, otherwise $\mathrm{Set}(p) = \empty0$
* $\mathrm{Set}(\phi \land \psi) = \mathrm{Set}(\phi) \times \mathrm{Set}(\psi)$
* $\mathrm{Set}(\phi \Rightarrow \psi) = \mathrm{Set}(\psi)^{\mathrm{Set}(\phi)}$

**Exercise:** verify that the above interpretation does indeed satisfy the semantics of our fragment.

### Types

We use the mathematical notation $T \rightarrow U$ and $T \times U$ for `Callable` and `tuple`, respectively.

* $\mathrm{Set}(T)$ is any set with cardinality equal to the cardinality of $T$ (we suppose "collisions" are avoided...)
* $\mathrm{Set}(T \times U) = \mathrm{Set}(T) \times \mathrm{Set}(U)$
* $\mathrm{Set}(T \rightarrow U) = \mathrm{Set}(U)^{\mathrm{Set}(T)}$

**Exercise:** verify that the above interpretation does indeed satisfy the semantics of our fragment.

## The Big Idea

Let's see if we can use type theory to directly model logic.  We need an *empty type* `Never` and a type with one inhabitant: `None`.  Proceeding as obviously as possible, we inductively define

* $\mathrm{Type}(p)$ is `None` if $p$ is true, otherwise `Never`
* $\mathrm{Type}(A \land B)$ is $\mathrm{Type}(A)\times\mathrm{Type}(B)$
* $\mathrm{Type}(T \rightarrow U) = \mathrm{Type}(U)^{\mathrm{Type}(T)}$

**Exercise:** verify that the above interpretation does indeed satisfy the semantics of our fragment.

We must observe that we have a problem with $\land$ and $\times$ - one is symmetric, while the other is not.  This hasn't been a problem now because $0 \cdot 1 = 1 \cdot 0 = 0$.  To fix this "assymetry," we need to continue our abstractive process from earlier.  First, we forgot the names of *types*, then we forgot the names of *fields*, giving them all an index instead.  Now we must also forget about the *index,* and discover a generalization which does not depend on *position.*  Here's our requirements:

* $\mathrm{Type}(A \land B) = \mathrm{Type}(B \land A) \simeq \mathrm{Type}(A) \times \mathrm{Type}(B)$
* We need two functions: $\pi: \mathrm{Type}(A \land B) \rightarrow A$ and $\rho: \mathrm{Type}(A \land B) \rightarrow B$

This line of thinking naturally leads to the [*categorical product*](https://en.wikipedia.org/wiki/Product_(category_theory)).  We will be satisfied in knowing that this inconsistency is not all that important - once we resolve the symmetry issue we'll be left with an object that is *isomorphic* to $\mathrm{Type}(A) \times \mathrm{Type}(B)$, so it seems like if we would rather just use $\mathrm{Type}(A) \times \mathrm{Type}(B)$ then we can.

<!-- | Type Theory | Logic | Note |
|--|--|--|
| Type | Proposition | *Types ARE Propositions, built-in types ARE Propositional Variables*
| implementation | proof | type-checking is proof-verification |
| $\rightarrow$ | $\Rightarrow$ | *It may be that $\phi$ implies $\psi$, but $\phi \Rightarrow \psi$ IS a proposition* |
| $\times$ | $\land$ | *Is $\times$ symmetric? Is $\land$ ?* |
| `\|` | $\lor$ |*Is* `\|` *symmetric? Is $\lor$ ?* | -->

## Application: Disjoint Union

Now that we've shown some sort of connection between logic and type-theory, it is natural to try and extend our theory on one side, and interpret it on the other.  For example, let's interpret the logical $\lor$ symbol.  To get an idea of what we're doing, let's consider how we prove $ \phi \lor \psi \Rightarrow \rho $.

> Suppose we know $\phi \lor \psi$.  If we know that both $\phi \Rightarrow \rho$ and $\psi \Rightarrow \rho$, then we can deduce $\rho$.  We don't know if $\phi$ or $\psi$ (or both) is true, but it doesn't matter, in either **case** we can deduce $\rho$.

According to the correspondence, it seems that we need a $\mathrm{Type}(\phi \lor \psi)$.  Then, given an instance of $\mathrm{Type}(\phi \lor \psi)$, if we have a function $\mathrm{Type}(\phi) \rightarrow \mathrm{Type}(\rho)$ and a function $\mathrm{Type}(\psi) \rightarrow \mathrm{Type}(\rho)$, we can construct a $\rho$ from our instance of $\mathrm{Type}(\phi \lor \psi)$.

### Python Implementation

To make this more concrete, we extend our subset of python.  We repeat the subset for convenience:

**Tuple Formation and Indexing**

```python
(x, y)
t[0]
```

**Function call**

```python
f(s)
```

**Disjoint Union (new)**

```python
z: X | Y
x if type(z) == X else y
```

And the same for typing rules:

* **Introduction Rules**
* if `u_x: U` and `def f(x: T): return u_x`, then `f: Callable[[T], U]`
* if `ti: Ti` for `1 <= i <= n`, then `(t1, t2, ..., tn): tuple[T1, T2, ..., Tn]`
* if `x: X`, then `x: X | T1 | T2 | ... | Tn`
* **Elimination Rules**
* if `x: T` and `f: Callable[[T], U]` then `f(x): U`
* if `t: tuple[T1, T2, ..., TN]` and `i: int` and `1 <= i <= n`, then `t[i]: Ti`
* if `t: T1 | T2 | ... | Tn`, and for all `1 <= i <= n` it holds that `ti_t: T`, then 

`t1_t if type(t) == T1 else t2_t if type(t) == T2 else ... else tn  : T`

Notice, because we used `type(t) == T1` to check types, the `|` operator is *symmetric.*  What happens if we use `isinstance`?

Formally, we interpret:

* $\mathrm{Set}(T_1 \;|\; T_2 \;|\; \dots T_n) = \bigcup \big\{ \{i\} \times \mathrm{Set}(T_i) : 1 \leq i \leq n \big\}$
* $\mathrm{Type}(\phi_1 \lor \phi_2 \lor \dots \lor \phi_n) = \mathrm{Type}(\phi_1) \;|\;\mathrm{Type}(\phi_2) \;|\; \dots \;|\; \mathrm{Type}(\phi_n)$

Exercise: play around with the type system...

**Technical Note:** we did something bad.  We let `x: X` all of the sudden assume *multiple types!*  We've seen something like this before with subtyping, but we have not introduced it into our formal system.  This problem is typically addressed in formal treatments by introducing a *type constructor*, that will essentially *wrap* a value, and then *unwrap* it later.  This is very strange in python, and would be awkward.

**BUT** there is good news.  Disjoint union pops up a lot in programming, we will take a look at [`C++ union`](https://en.cppreference.com/w/cpp/language/union).  Question: why can't (couldn't, shouldn't?) unions have virtual methods?

# Classic vs Intuitionist logic

Now let's try to interpret logical negation.  First, we need a notion of "falsity," typically denoted $\bot$ (the *bottom* type).  In propositional logic, $1 \Rightarrow 0$ is false.  In type theory, we have that $\mathrm{Type}(1) \rightarrow \mathrm{Type}(0)$ is *uninhabited* - that is, there is no function from $\mathrm{Type}(1)$ to $\mathrm{Type}(0)$.  To see this, remember that for a function $f$ to have the type $f: T \rightarrow U$ it must satisfy:

$$(\forall t \in T )(\exists ! u \in U) : f(t) = u$$

Then if $U$ is empty, no $f$ can satisfy this formula unless $T$ is also empty.  **Exercise** interpret that logically.

Once we have $\bot$, it is natural to identify

$$ \mathrm{Type}(\lnot \phi) = \mathrm{Type}(\phi) \rightarrow \bot $$

> By the type $\lnot T$, we mean that we know $T$ is uninhabited.  We "know" this because we have a function that can take a *value* of type $T$ and produce a *value* of type $\bot$ - which is impossible.

These are rather satisfactory definitions, but further inspection can yield valuable insight.  In *classical logic*, we typically assume that for any proposition $\phi$, we have both

$$\phi \Rightarrow \lnot \lnot \phi$$
$$\lnot \lnot \phi \Rightarrow \phi$$

The first of these transfers over to our extended type theory.

> Suppose we know that $t: T$, that is, $T$ is inhabited.  We need to show that there is a function of type $(T \rightarrow \bot) \rightarrow \bot$.  We can show this by implementing it!
> $$\Big((\lambda f: T \rightarrow \bot) (\lambda t: T) . f(t) \Big) : (T \rightarrow \bot) \rightarrow \bot$$

**Exercise: type-check the above implementation**

What about the second formula?

> Suppose we have a function $f$, which can take a function $T \rightarrow \bot$ and produce a $\bot$.  Since this function exists, it seems like there should be some $t :T$, but can we prove it?  In particular, can we *construct* such a value, given $f$?

Exercise: decide for yourself.

## Heyting algebras

The mathematical structures typically chosen to represent logic are algebras of some sort.  We will forgoe formal definitions, and skip straight to an interesting example.

### Toplogical Prerequisites

* Let $b(x, r) = \{y \in \mathbb{R^2}: ||x - y|| < r \}$.
* A set $A \subseteq \mathbb{R^2}$ is called **open** if $ (\forall x \in A) (\exists r > 0) : b(x,y) \subseteq A$
* Let $\bar{A} = \mathbb{R^2} \setminus A$
* Let $\mathcal{O_2}$ denote the open subsets of $\mathbb{R^2}$.
* A set $A$ is called **closed** if $\bar{A} \in \mathcal{O_2}$.
* Let $\partial A$ denote the **boundary** of $A$: 
$\partial A = \Big\{x: (\forall r > 0) \; \big( b(x, r)  \cap A \neq \empty \big) \land \big( b(x, r) \cap \bar{A} \neq \empty \big) \Big\} $
* Let the **interior** of $A$ be defined as $\mathrm{Int}(A) = \cup \{O : O \in \mathcal{O_2} \land O \subseteq A \}$

**Claim** the *interior* of a set is *open* (obvious...)

**Claim** a set is *open* iff its equal to its interior: $A \in \mathcal{O_2} \iff \mathrm{Int}(A) = A$

> Proof $\mathrm{Int}(A) \subseteq A$ by definition (it's the union of subsets of $A$).  On the other hand, if $a \in A$ then there is an open set $b(a, r_a) \subseteq A$, so $a \in A \Rightarrow a \in \mathrm{Int}(A)$ $\square$.

**Claim** a set is *open* iff it does not intersect it's boundary: $A \in \mathcal{O_2} \iff \partial A \cap A = \empty$

**Claim** a set is *closed* iff it contains it's boundary: $\bar{A} \in \mathcal{O_2} \iff \partial A \subseteq A$

Exercise: prove the claims.

**Question:** which sets, if any, are both *opened* and *closed*?

**Answer:** $\mathbb{R^2}$ and $\empty$

> Proof sketch: suppose $A$ is *open*, *closed*, and not empty.  Let $\a \in A$, and consider $\rho_a = \sup_{r > 0} b(a, r) \subseteq A$.  We know that $\rho_a > 0$ since $A$ is open.  Suppose $\rho_a < \infty$.  Let $x \not\in A$ such that $||x - a|| = \rho_a$.  Then "clearly" $x \in \partial A$ which means that $x \in A$ (since $A$ is closed), a contradiction $\square$.

Therefore, we know that if some set $A$ is not $\empty$, $\mathbb{R^2}$, and $A$ is open, then $\bar{A} \not \in \mathcal{O_2}$.

### Semantics of intuitionist logic through $\mathcal{O_2}$

We consider the fragment of intuitionist logic consisting of:
* Propositional variables
* $\land$, $\lor$, $\Rightarrow$

We interpret the sets of $\mathcal{O_2}$ as propositions, and consider the following interpretation operator $\mathrm{Heyting}(\phi)$:

* $\mathrm{Heyting}(p) =$ the set assigned to $p$ for propositional variable $p$
* $\mathrm{Heyting}(\phi \land \psi) = \mathrm{Heyting}(\phi) \cap \mathrm{Heyting}(\psi)$
* $\mathrm{Heyting}(\phi \lor \psi) = \mathrm{Heyting}(\phi) \cup \mathrm{Heyting}(\psi)$
* $\mathrm{Heyting}(\phi \Rightarrow \psi) = \mathrm{Int}\Big(\overline{\mathrm{Heyting}(\phi)} \cup \mathrm{Heyting}(\psi)\Big)$

To understand the last interpretation, recall that in classical logic $\phi \Rightarrow \psi$ is equivalent to $\lnot \phi \lor \psi$.  Here we see how Heyting Algebras give us a good model: if $A$ and $B$ are open, then $\bar{A} \cup B$ is not necessarily open!  (*Exercise: example*!)  So, we take the "largest open set" which is contained in $\bar{A} \cup B$, i.e. we "project" this set down to an open one.

To finish the discussion, lets try to see if what our model says about $\lnot \lnot \phi$.  Denote $A = \mathrm{Heyting}(\phi)$, and note that $\mathrm{Heyting}(\bot) = \empty$.  We should interpret $\lnot \lnot \phi$ as:

$$ \mathrm{Heyting} \Big( (\phi \Rightarrow \bot) \Rightarrow \bot \Big)$$
$$ \mathrm{Int}\Big(\overline{\mathrm{Heyting} (\phi \Rightarrow \bot)} \cup \empty\Big)$$
$$ \mathrm{Int}\Big(\overline{\mathrm{Int}(\overline{A} \cup \empty)}\Big)$$
$$ \mathrm{Int}\Big(\overline{\mathrm{Int}(\overline{A})}\Big)$$

**Exercise:** come up with a set $A \in \mathcal{O_2}$ such that $ \mathrm{Int}\Big(\overline{\mathrm{Int}(\overline{A})}\Big) \neq A$.  *Hint:* what happens when you puncture $\mathbb{R^2}$?


## Math vs Programming

There is a cute asymmetry here in what is considered important.  A mathematician would like to get rid of all *unnecessary* information: the fact that we must refer to $0, 1 \in \mathbb{N}$ in order to get the values from our $\mathrm{Type}(A \land B)$ is unacceptable.  Why should the creation of a *product type* depend on our knowledge of *natural numbers?*  This is an unnecessary dependency, and we can get rid of it and replace our operators with more primitive notions.

A programmer, however, will probably want to be a little more pragmatic.  We also don't like unnecessary dependencies, but we are not going to be praised for writing code that does not depend on any notion of *number* (you *would* have, about 100 years ago...).  Plus, as engineers, we typically like to give ourselves useful, but contradictory advice:

* **KISS:** keep it simple stupid
* **WTPA:** (don't) waste time on pointless abstractions

On the one hand, by removing all dependencies we are trying to make our program simpler.  There is no *"our program is correct, assuming all the dependencies are properly implemented."*  On the other hand, we had better have a very good reason for introducing very strange objects and abstractions, since these *increase* the complexity of our program.  And most people won't find the reason "we don't want to assume that numbers exist" very convincing (except for mathematicians - that's because they know that numbers don't really exist anyways).

## Axioma vs Programming: the *implementation* of mathematics

Here are some axioms from set theory:

| Axiom | Form | Meaning | Use |
|--|--|--|--|
| Existence             | $$\exists x$$ | A set exists | We know the universe is not *empty* |
| Extensionality        | $$ \forall z (z \in x \Leftrightarrow z \in y) \Rightarrow x = y $$ | If two sets have the same elements they are equal | We can check for equality (what about $\Leftarrow$ ?) |
| ~~Foundation~~        | $$\forall x (x \notin x)$$ | No set is an element of itself | Technical, hard to justify conceptually... It disallows "circular definitions" which are actually useful in programming (e.g. *recursive types*)|
| **Comprehension**     | $$\{x \in y : \phi(x) \}$$ | Subsets given by *formulas* are sets | Fundamental operation for creating new sets |
| **Union**             | $$\cup z = \{x : \exists y (x \in y \land y \in z)\}$$ | The union of any *family of sets* is a set | Fundamental operation for creating new sets |
| **Replacement**       | $$\{y : \exists x, y \; \phi(x, y) \}$$ | The *range* of a *formula* is a set | Fundamental operation for creating new sets |
| **Powerset**          | $$\{ x : x \subseteq y \}$$ | The set of all subsets of a set exists | Fundamental operation for creating new sets |
| ~~Infinity~~          | $$\exists x(0 \in x \land (n \in x \Rightarrow n + 1 \in x)$$ | An infinite set exists | Construct $\omega$ (aka $\mathbb{N}$) |
| ~~Axiom of Choice~~   | $\forall X \exists f (x \in X \Rightarrow f(x) \in x)$ | All sets can be well ordered? | Either AoC or something like it is required to develop analysis |

We can relate many of these axioms to the concepts we've been developing.

| Axiom | Type-theoretic counterpart | Notes |
|--|--|--|
| Existence | Built-in types | The exact "origin" of values seems to be more interesting from a mathematical perspective.  Without any "values" we probably wouldn't even be programming, let alone considering type systems. |
| Extensionality | structural subtyping | sets carry no information about "names" |
| *formula* | a function we can implement | We create sets using *formulas*, we'll create types using *functions* |
| **Comprehension** | the *inverse-map* defines a new type (something like a custom `isinstance` implementation) | say $f : T \rightarrow \mathrm{bool}$.  Then we can define a type $T'$ such that $\Gamma \vdash t: T'$ $\Leftrightarrow$ $\Gamma \vdash t: T$ **and** $f(t) = \mathrm{True}$ |
| **Replacement** | The range of a function is a type | discussion: must our functions be *computable*? |
| **Union** | **disjoint-union** + **Replacement** | proof: exercise |
| **Powerset** | **function-type** | proof: exercise |

### Conclusion
Draw your own conclusions.

# Recursive types

## Introduction

Suppose we have a python type like the following:

```python
from __future__ import annotations # what the heck is this?

class ListInt:
    value: int
    next: ListInt | None
```

This type will not be strange to anyone familiar with OOP.  But the definition of `ListInt` is circular!  That is, in order to define `ListInt` we must first know what `ListInt` is.

I don't want to waste a lot of time on the obvious, intutitive stuff.  We'll do two exercises, then discuss notation, then do a rather unorthodox presentation of the formalities.

**Exercise:** How do you define recursive types in C++?

**Exercise:** What would happen if we defined `ListInt` like so:
```python
class ListInt:
    value: int
    next: ListInt
```

## Notation for $\mu$-types

These types are introduced in a mathematical setting by using a $\mu$-binding-operator.

We start off by presenting the $\mu$-type representing `ListInt`.  Let $Z$ denote `int`, and consider:

$$ \mu L. Z \times (1 \;|\; L)$$

This binding operator is used to express the equation:

$$ L = Z \times (1 \;|\; L)$$

Somewhat more formally, we extend our *mathematical* type system by allowing types which conform to the following grammar:

* $T \mapsto $ built-in type
* $T \mapsto (T)$
* $T \mapsto T \times T$
* $T \mapsto T \;|\; T$
* $T \mapsto T \rightarrow T$
* $T \mapsto \mu V.T$ where $V$ is an *identifier*

**Note**: our grammar is ambiguous.  We will resolve all ambiguities when discussing examples, and our "unorthodox" treatment later will not suffer from the same issues.

**Note**: while our grammar allows for binding multiple variables (e.g. $\mu A \mu B . A \times B$), this doesn't actually accomplish anything and we won't bother about it.  

**Note**: our grammar intentionally allows for nested recursive definitions, which are useful.  For instance:

$$ Z \times \big(\mu L. Z \times (1 \;|\; L)\big) \big(\mu L. Z \times (1 \;|\; L)\big)$$

Compare this to:

```python
class TwoListInts:
    z: int
    list1: ListInt
    list2: ListInt
```

**Exercise:** write the type of a binary tree (of `int`s) in $\mu$-type notation

## Towards Algebraic Data Types (ADTs)

Let $T$ and $U$ be types.

* A *conversion between $T$ and $U$* is a pair of functions, $T^\to_U: T \to U$ and $U^\to_T: U \to T$
* A *conversion between $T$ and $U$* is *lossless* if $(\lambda t: T).U^\to_T(T^\to_U(t))$ is the *identity function*
* One type is *isomorphic* to another if there is a lossless conversion between them, denoted $T \simeq U$

**Exercise:** argue that $\simeq$ is an equivalence relation

Let's change our notation slightly, and use $+$ in place of $|$ for disjoint union.  Later we will also write $T\to U$ as $U^T$.

**Exercise:** prove the following:

| Form | Name |
|--|--|
| $ T + (U + V) \simeq (T + U) + V$ | *associativity* |
| $ T \times (U \times V) \simeq (T \times U) \times V$ | *associativity*  |
| $ T + U \simeq U + T $ | *commutativity* |
| $ T \times U \simeq U \times T $ | *commutativity*  |
| $ T \times (U + V) \simeq T \times U + T \times V$ | *distributivity* |
| $ (T + U) \times V \simeq T \times V + U \times V$ | *distributivity* |
| $ T + 0 \simeq T $ | *identity* |
| $ T \times 1 \simeq T $ | *identity* |
| $ T \times 0 \simeq 0 $ | *annihilator* |

Okay, you get the idea, we can cast our type theory to some sort of arithmetic over non-negative integers.  This is mostly cute, but sometimes it is useful...

**Exercise:** Prove (and name) the following formula:

$$ A^{B \times C} \simeq {A^C}^B $$

Note that ${A^C}^B = (A^C)^B$ by convention, and does not (cannot?) be "proven."

## ADTs and $\mu$-types

Recall that $\frac{1}{1-x} = \sum_{k=0}^{\infty} x^k$.  Let's try to "solve" our recursive type formula for `ListInt`:

$$T = Z \times (1 + T)$$

If we pretend that those variables are real numbers, the we have:

* $T = Z \times (1 + T)$
* $T = Z + Z \times T$
* $T - Z \times T = Z$
* $T \times (1 - Z) = Z$
* $T = \frac{Z}{1-Z} = Z \times \sum_{k=0}^{\infty} Z^k = \sum_{k=1}^{\infty} Z^k$

**Discussion:** why is this reasoning *nonsense?*
**Discussion:** why is this reasoning *correct?*

## Formalities

### Infinite Tree Types

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