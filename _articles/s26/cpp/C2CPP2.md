---
title: "C2cpp Notes: Iterators and Metaprogramming"
permalink: /articles/cpp/2new
---

{% include toc %}

---
# 11. Iterators
> **Template territory**  
> - Generalized concept of a pointer
{: .notice--warning}


## Examples
### Array Iterator
```cpp
template <typename I, typename F>
void For_Each(I b, I e, F f) {
    while (b != e) {
        f(*b);
        ++b;
    }
}
```

```cpp
void print_int(int x) { cout << x << ' '; }

int a[5] = { 100, 101, 102, 103, 104 };
For_Each(a + 1, a + 5, &print_int); 
```
- `I`: type **pointer** (E. `int*`)
	- Half interval `[b, e)`
	- `b`: first element
	- `e`: **one past** last element (`b` + size)
- `F`: **function** pointer (E. `void (*) int`)

### Vector Iterator
Vector guarantees contiguous memory, same thing
```cpp
vector<int> v { 100, 101, 102, 103, 104 };
For_Each(&v[0], &v[0] + 5, &print_int);      // raw pointers
For_Each(v.begin(), v.end(), &print_int);    // iterators
```
- Don't forget `&`

- `v.begin()`, `v.end()` return **iterators** of type `std::vector<int>::iterator`!
	- Behave like `int*`
	- Defined inside `vector` class
	- `operator*()` defined to call `f(*b)`
	- `operator++()` defined
	- **Pointing** *one past* the last element is fine
		- As long as you don't dereference it

`F` may not be a function, but a class that defines function operator
- Function object

### List Iterator
Also works same way with list!
```cpp
list<int> v { 100, 101, 102, 103, 104 };
For_Each(v.begin(), v.end(), &print_int);
```
Can't be implemented with a raw pointer
```cpp
template <typename T>
class list {
	class iterator {
		operator!=();
		operator*();
		iterator& operator++();   // ++i
		// ...
	};
};
```

- Not all iterators are equal. They have different categories, with different methods
	- `list<T>::iterator` does not define `op<=()`, use `op!=()` instead

> **Why `++b`, not `b++`?**  
> More efficient return value
{: .notice--info}


CPP defines:
```cpp
// ++b prefix
iterator& operator++() {
	curr = curr -> next;
	return *this;
}

// b++ postfix
iterator operator++(int unused) {
	iterator prev(*this)     // need CC previous iteator
	curr = curr -> next;
	return prev;
}
```


## Range-Based `for` Loop
Declare iterator `list<int>::iterator`
- **Nested class** under `list`
- Dereferencing gives `int&`

```cpp
for (list<int>::iterator i = v.begin(); i != v.end(); ++i) {
	*i += 200;
}
```

Declare **const** iterator `list<int>::const_iterator`
- Different nested class
- Can't change the underlying element
- Dereferencing gives `const int&`


`auto`: Let compiler figure out type
```cpp
for (auto i = v.begin(); i != v.end(); ++i) {
	cout << *i << ' ';
}
```

Can also do **range-based** for loop
- Translated to `auto& x = *i;`
- **Only** works if *container* `v` defines a `begin()` and `end()`

```cpp
for (auto& x : v) {
	cout << x << ' ';
}
```


## Vector Initialization
### Default Initialization
```cpp
template <typename SrcIter, typename DestIter>
DestIter copy(SrcIter b_src, SrcIter e_src, DestIter b_dest) {
    while (b_src != e_src) {
        *b_dest = *b_src;
        ++b_src;
        ++b_dest;
    }
    return b_dest;
}
```
- Assume destination has **sufficient room**, and overwrites each element

```cpp
vector<int> v1 { 100, 101, 102, 103, 104 };
vector<int> v2;      // uninitialized
copy(v1.begin(), v1.end(), v2.begin());
```
> **Crashes**  
> `v2` **not initialized**. Dereferencing `v2.begin()` crashes.
{: .notice--danger}


Need **initializer** to **default** construct 5 elements:
```cpp
vector<int> v2(5);       
```

### Initializer List
**Curly braces**: `vector(std::initializer_list<T>)`
- Compiler will construct a temporary object of `initializer_list`, a **pointer** to begin and end of actual elements
	- Elements are constructed in RO memory
	- Has `begin()` and `end()` (container)
- On construction, an `initializer_list` is passed, and constructs `v1`
	- `vector` only has constructor that takes an `initializer_list`
- Elements may not be constant: `{ 1, f() }`
	- Compiler will construct array, construct initializer, and manage its lifetime
**Parentheses**: `vector(size_t)`
- Initializes vector with default constructed elements

## Iterator Adapters
### Back Inserter
> **Fancy way to implement the iterator**  
> - Works with uninitialized vectors by decoupling the operations
> - Simplified version of `std::back_insert_iterator`
{: .notice--info}


Class template with `Container`
- Pass `<vector<int>>`

```cpp
template <typename Container>
struct IteratorThatPushes {
    Container& c;

	// noop dummdies
    explicit IteratorThatPushes(Container& c) : c(c) {}
    IteratorThatPushes& operator*()     { return *this; }
    IteratorThatPushes& operator++()    { return *this; }
    IteratorThatPushes  operator++(int) { return *this; }

    IteratorThatPushes& operator=(const typename Container::value_type& other) {
        c.push_back(other);
        return *this;
    }
};
```
- `explicit`: **Prevents** implicit construction promotion

Hold a reference to **container**, instead of elements
`*b_dest = *b_src;`
- `opeator*()`: trick to not actually dereference, but return the **iterator itself**
- Triggers the `opeartor=()` on the **iterator**, not the element
	- `*b_src` has type `Container::value_type&`
		- Nested type of every container
		- For nested type, need prefix `typename`
		- Or it may not know `value_type` is a *type*, or a *class variable*
`++b_dest` has no effect.

**Usage**
```cpp
vector<int> v1 { 100, 101, 102, 103, 104 };
vector<int> v2;               // uninitialized!

copy(v1.begin(), v1.end(), IteratorThatPushes<vector<int>>{v2});
```

In STL:
```cpp
copy(v1.begin(), v1.end(), back_inserter(v2));
```

### `ostream_iterator`
Adapter that wraps an `ostream`
- **Write** by **copying** elements into `ostream_iterator`
- Re-casting of `opeator<<()`

```cpp
ostream_iterator<int> oi {cout, /*delim*/ "\n"};
copy(v.begin(), v.end(), oi);       // prints
```

### `isteam_iterator`
```cpp
vec<int> v;
istream_iteartor<int> iib {cin};
istream_iterator<int> iie {};      // need an end for copy()

copy(iib, iie, back_inserter(v));
```
- Construction: performs `op>>`
- `op++()` performs another `op>>`
- `op*()` returns the last read value
- `op!=()` compares internal state pointers
	- On EOF, or default construction, internal set to `nullptr`

## Iterator Categories
> **Not actual types**  
> Renamed into iterator concepts in C++20, all old becomes "Legacy"
{: .notice--warning}

- `LegacyOutputIterator`: writing through single-pass **increment**
	- "Single-pass": once read it, can't go back again
		- `++` might invalidate copies!
	- Alternating assignment and increment
	- `op=(end)` only!
	- E. `back_insert_iterator` and `ostream_iterator`
1. `LeagacyInputIterator`: reading through single-pass increment
	- Read exactly once
	- E. `istream_iterator`
2. `LegacyForwardIterator`: Supports input iterator and **multi-pass** increment
	- Iterator can only be incremented, *but* range can be **traversed** with multiple iterators
	- `op=()` anywhere
	- E. `std::forward_list::iterator` can only go forward
3. `LegacyBidirectionalIterator`: + **decrement**
	- E. `std::list::iterator`
4. `LegacyRandomAccessIterator`: + $O(1)$ element access
	- `op<()` allowed
	- E. `std::deque::iterator`
5. `LegacyContiguousIterator`: + Contiguous elements in memory
	- `std::vector::iterator`, `std::array::iterator`

---
# 12. Associative Containers
> Data stored based on a **key**, rather than index

## Map
> **`std::map` and `std::unordered_map`**  
> For `op[]`, if no entries exist, will **default construct one**!
> - Not a `const` operation, though
{: .notice--info}


`std::map` is a sorted, *associative* **Container** of `<key,value>` pairs
- Dictionary in Python
- **Unique** key (associative)
- **Sorted**: need `op<` for keys
	- Implemented with binary (red black) tree in cpp
- No other pointers, references, iterators are **invalidated** in insertion/removal
	- How to traverse? Using parent, left, right pointers

```cpp
template <
	class Key,
	class T,
	class Compare = std::less<Key>,
	class Allocator  //...            // special allocation, instead of new
> class map;
```
- `std::less` is a [functor](#function-object), with `op()`

### `op[]`
> Atomic find-insert

```cpp
map<string,int> m;     // declare empty map

for (string s; cin >> s; ) {
	++m[s];
}
```
- Read a string from `cin`
- Increments key `s`
- If key is not there, `operator[]` will put a default constructed value (0)
	- aka value initializing
- Return `T&`

### `find()`
`std::map` has a `find() const` function for keys
- Returns an **iterator**
	- `m.end()` if not found

```cpp
auto it = m.find("string");
if (it != m.end()) {
	auto& [s, n] = *it;
}
```
### Iterator
Print output:
```cpp
for (auto i = m.begin(); i != m.end(); ++i) {
	cout << setw(20) << (*i).first << '|';
	cout << i->second << '\n';
}
```
- Printed in alphabetical order
	- In-order traversal of binary tree with iterator `i`
- Deref `*i` to get **pair**
	- `i->first` and `i->second`
	- Iterators have `operator->` defined
		- If LHS of `operator->` is not a **raw pointer** , keep applying `->`
		- Will uncover `i`

or do:

```cpp
for (auto& e : m)
// e.first...

for (auto& [s, n] : m)     // structured binding
	cout << s << '|' << n << '\n';
```


## Unordered Map
`std::unorderedmap`

```cpp
unordered_map<string,int> m;
```
Stored with **hash table**
- Lookup is usually $$O(1)$$
**Requirements**
- Key must be **equality** comparable
	- Regular map requires `<`
- Key hashing

```cpp
template<
	class Key,
	class T,
	class Hash = std::hash<Key>,
	class KeyEqual = std::equal_to<Key>,
	class allocator
> class unordered_map;

template< class Key >
struct hash;
```

- No reference/pointers invalidated
- Iterators **can be invalidated**, if insertion causes **rehashing**
	- Iterator needs to contain information of current bucket
	- Hash table is implemented with a *single* **singly** linked list
		- Bucket points to different places in the list
		- Point to *one before* the element, due to singly linking
		- Messed up at re-bucket

## Ordered Multimap
`std::multimap` is a `map` with multiple entries of the same key
- Sorted by key

```cpp
unordered_map<string, int> word_to_freq;  // construct it...
multimap<int,string> freq_to_words;

for (const auto& [word, freq] : word_to_freq) {
	freq_to_words.insert( {freq, word} );   // reverse pair
}
```
- `.insert` takes a `std::pair<int,string> {freq, word}`
	- `pair<>` omitted for simple structures. Will directly invoke the `pair` construction.

To find, can't directly use iterator `find()`:

```cpp
auto [b, e] = freq_to_words.equal_range(3);
if (b != e) {
	auto& freq = b->first;
	auto num_words = distance(b, e);
}
```
- `equal_range(key)`: return a **pair of iterators**:
	- Iterator to first element; to one past last element
- `std::distance()` gives distance between **two iterators**
	- Implemented by increment walk
	- Can do `e - b` if continuous. How do you know?

---
# 13. Template Metaprogramming
> Computations and validations at **compile** time!
{: .notice--warning}

## Intro
`MyDistance ()` takes two **iterators**
```cpp
template <typename I>
size_t MyDistance(I b, I e)
	return e - b;
```
- Only works if `op-()` works (random access)

```cpp
int main() {
    vector v { 100, 101, 102, 103, 104 };           // OK
    forward_list v { 100, 101, 102, 103, 104 };     // compiler error

    auto b = ranges::begin(v);
    auto e = ranges::end(v);
    cout << "Number of elements: " << MyDistance(b, e) << '\n';
}
```
- `ranges::begin(v)` instead of `v.begin()`, to be compatible with **raw** `int[]`
	- Function template. Specialization for raw types

Want to tell at **compile** time, decide what `I` is, and invoke different codes

## Tag Dispatching
C++ defines **empty** `struct`s: **iterator tags**:
```cpp
struct input_iterator_tag {};
struct output_iterator_tag {};
struct forward_iterator_tag : public input_iterator_tag {};
struct bidirectional_iterator_tag : public forward_iterator_tag {};
struct random_access_iterator_tag : public bidirectional_iterator_tag {};
struct contiguous_iterator_tag : public random_access_iterator_tag {};
```

Each STL iterator has an `iterator_category` type inside (`typdef`)
```cpp
template <typename T>
struct vector {
	struct iterator {
		// ...
		using iterator_category = forward_iterator_tag;
		// ...
	};
};
```

Allows choosing implementations (**tag dispatching**)
- Passing tag `vector<int>::iterator::iterator_category{}` to match the right version
- `I` becomes `vector<int>::iterator`

```cpp
template <typename I>
size_t __doMyDistance(I b, I e, random_access_iterator_tag) {
    return e - b;
}

template <typename I>
size_t __doMyDistance(I b, I e, forward_iterator_tag) {
    size_t n = 0;
    while (b != e) {
        ++n;
        ++b;
    }
    return n;
}

template <typename I>      // vector<>::iterator
size_t MyDistance(I b, I e) {
	// for containers
    return __doMyDistance(b, e, typename I::iterator_category{});
	// for raw pointers
    return __doMyDistance(b, e, typename iterator_traits<I>::iterator_category{});
}
```

### Raw Pointer
`int*` doesn't have `::iterator_category`!
- Use `iterator_traits<int*>`, whose `iterator_category` resolves to the tag.

```cpp
template <typename I>
struct iterator_traits {
    using iterator_category = typename I::iterator_category;
    // ...
};

// Specialization for raw pointer, speical type T
template <typename T>
struct iterator_traits<T*> {
    using iterator_category = contiguous_iterator_tag;
    // ...
};
```
- For iterators, simply return its `::iterator_category`
- For raw pointers, assign it to `contiguous`
Compiler will match the second, more specific version with `<T*>` (**template specialization**)

## SFINAE
Substitution Failure Is Not An Error
### `std::enable_if`
Class template with (value, type)
```cpp
template <bool B, typename T>
struct enable_if {};
 
// Specialization for `true` value parameter
template <typename T>
struct enable_if<true, T> { using type = T; };
```
Specialized so if `true`, defined with a *nested* `type` that resolves to `T`
```cpp
enable_if<true, size_t>::type x = 5;   // Same as: size_t x = 5;
enable_if<false,size_t>::type y = 5;   // Compiler error
```

### `std::is_same_v`
```cpp
template <typename T, typename U>
struct is_same {
    static constexpr bool value = false;
};
 
// Specialization for T == U
template <typename T>
struct is_same<T, T> {
    static constexpr bool value = true;
};
```
- `static`: per **class**, not per instance
	- Referred to as `Class::value`
- `constexpr` tells compiler to evaluate at compile time

```cpp
template <typename T, typename U>
constexpr bool is_same_v = is_same<T, U>::value;
```
- STL uses `std::is_same_v` to access the `::value`
	- **Variable** template (vs function temp, class temp)

### `MyDistance()` Implementation
Fancy way to write the **return type** of `MyDistance()` (`size_t`)
- If iterator type match, will be `size_t`
- If mismatch, `enable_if<>::type` will be **ill-formed**
	- Compiler error, but compiler will look for other matches
	- SFINAE!

```cpp
template <typename I>
std::enable_if<
	is_same_v<
		random_access_iterator_tag,     // not contiguous tag due to legacy
		typename iterator_traits<I>::iterator_category
	>, 
	size_t
>::type MyDistance(I b, I e) {
    return e - b;
}

template <typename I>
std::enable_if<
	is_same_v<
		forward_iterator_tag,
		typename iterator_traits<I>::iterator_category>, 
	size_t>::type
MyDistance(I b, I e) {
    size_t n = 0;
    while (b != e) {
        ++n;
        ++b;
    }
    return n;
}
```

> **Fail if the container is `list`**  
> We've only checked exact iterator tag matches
{: .notice--warning}


## `if constexpr`
- Only choose one branch to compile
	- `if` not evaluated at **runtime!**

```cpp
template <typename I>
size_t MyDistance(I b, I e) {
    if constexpr (is_base_of_v<random_access_iterator_tag,
                        typename iterator_traits<I>::iterator_category>) {
        return e - b;
    } else {
        size_t n = 0;
        while (b != e) {
            ++n;
            ++b;
        }
        return n;
    } 
}
```
- If `random_access_iterator_tag` is a base class of `iterator_traits<I>::iterator_category`
	- Similar to `is_same_v`
- More readable version of 

If we pass nonsense expressions `MyDistance("AAA"s, "BBB"s);`
- Won't compile, because no expression `iterator_traits<string>::iterator_category`
- Can we limit `I` to be iterator? [Concepts!](#concepts)

## Concepts
> Explicitly states type requirement

- Compile time, evaluate predicate
- `requires` `I` to be a forward iterator
	- `forward_iterator` is a concept
	- Enforce `I` to satisfy the constraints of `forward_iterator`
		- can be deref, increment, has iterator tag derived from `forward_iterator_tag`

```cpp
template <typename I>
    requires {forward_iterator<I>}
size_t MyDistance(I b, I e) { ... }
```
Or, merge with `typename`

```cpp
template <forward_iterator I>
size_t MyDistance(I b, I e) { ... }
```

### Concepts to constrain `auto`
```cpp
random_access_iterator auto b = ranges::begin(v);
```
If not `ra_iterator`, won't compile!
- E. `v` is a list

### Define concepts
> Compile-time Boolean predicates

```cpp
template <typename I>
concept MyBidirectionalIterator =
    forward_iterator<I> &&
    derived_from<
	    typename iterator_traits<I>::iterator_category,
        bidirectional_iterator_tag
    > &&
    requires (I i) {
        { --i } -> std::same_as<I&>;
        { i-- } -> std::same_as<I>;
    };
```
1. Enforce `forward_iterator<I>`
2. Additional functionality: check the iterator category of `I` is derived from `bidir_iter_tag`
	- `derived_from` is also a concept
3. `requires`: tries to compile with dummy `i`
	- Check if expressions `{i--}` compiles and has the right return type
	- Further require the type using `std::same_as<>`
		- Also a concept
		- Compiled as `std::same_as<decltype(--i), I&>`

---
# 14. Functional Programming
## Function Object
> aka Functor

```cpp
void print_int(int x)    {cout << x << ' '; }
struct IntPrinter {
    void operator()(int x) const { cout << x << ' '; }
};
```
A `struct` (`class`), that defines `operator()()`!
- No data, just a method

```cpp
  For_Each(v2.begin(), v2.end(), &print_int);    cout << '\n';
  For_Each(v2.begin(), v2.end(), IntPrinter{});  cout << '\n';
```
- Can pass *pointer* to function
- Or **object** (instance of) `IntPrinter{}`, default constructed
	- Callable object!
Call to `f(*b)` invokes `op()` of the object
- A functor can store **state** information

### Stateless Functors
```cpp
For_Each(v2.begin(), v2.end(), negate<int>{});
For_Each(v2.begin(), v2.end(), IntPrinter{});  cout << '\n';
```
`std::negate` can be defined as:
```cpp
constexpr T operator()(const T& arg) const {
    return -arg;
}
```
No effect, since `negate` doesn't **assign** back to `arg`

Need to define `transform()`
```cpp
template <typename SrcIter, typename DestIter, typename F>
DestIter Transform(SrcIter b_src, SrcIter e_src, DestIter b_dest, F f) {
    while (b_src != e_src) {
        *b_dest = f(*b_src);
        ++b_dest;
        ++b_src;
    }
    return b_dest;
}

transform(v1.begin(), v1.end(), back_inserter(v2), negate<int>{});
For_Each(v2.begin(), v2.end(), IntPrinter{});  cout << '\n';
```
- Same as `copy()`, using iterator `back_inserter(v2)`
	- Turn assignment `*b_dest = ...` into `.push_back()` call

### Stateful Functors
```cpp
struct AddX {
    int x;
    AddX(int x) : x(x) {}
    int operator()(int y) const { return x + y; }
};
```
When `operator()` called, adds `x`

Can also let functor to carry around a **parameterized** function to call
```cpp
template <typename F>
struct OpX {
    F op;      // operator
    int x;     // number
    OpX(F op, int x) : op(op), x(x) {}
    int operator()(int y) const { return op(x, y); }
};

transform(v1.begin(), v1.end(), back_inserter(v2),
	OpX{plus<int>{}, 300});
```
- For construction, pass operator and number: `OpX{ plus<int>{}, 300 }`
	- `OpX` is parameterized by any invocable type `F`
- `std::plus<int>` is also a **functor** (binary)
	- `OpX` **binds** first argument to `x`, yielding a **unary** functor `plus(300, y)` that can be called by `transform()` with one argument!

```cpp
template <typename T>
constexpr T operator() (const T& lhs, const T& rhs) const {
	return lhs + rhs;
}
```

## Bind Expressions
### `bind_front`
STL provides **function** template `bind_front()` that can take a partial list of argument
- More efficient that `std::bind()`

```cpp
void f(arg1, arg2, arg3);
auto g = bind_front(f, arg1, arg2);

// same as:
g(arg3);

transform(v1.begin(), v1.end(), back_inserter(v2),
    bind_front(plus<int>{}, 300));
```

Also `bind_back`

### `bind`
Use placeholders to specify unbound arguments
- Clumsy, not used much

```cpp
struct SubSubSub {
    int operator()(int a, int b, int c, int d) const
        return a - b - c - d;
};
auto f = bind(
	SubSubSub{},       // default construction 
	1000,              // a: 1000
    placeholders::_2,  // b: second new argument
    placeholders::_1,  // c: first new argument
    placeholders::_1   // d: first new argument again
);

f(100, 500);           // same as SubSubSub(1000 - 500 - 100 - 100)
```
- `bind()` always take the same arguments (4)

```cpp
transform(v1.begin(), v1.end(), back_inserter(v2),
    bind(plus<int>{}, 300, placeholders::_1));
```

### Function Composition Binding
Let `f(x) = 300 + g(x)`, `g(x) = -x`
```cpp
transform(v1.begin(), v1.end(), back_inserter(v2),
	bind(
		plus<int>{}, 
		300,
		bind(negate<int>{}, placeholders::_1)   // g(x) = -arg1
	)
);
```
Same as:
```cpp
auto g = bind(negate<int>{}, placeholders::1);
auto f = bind(plus<int>{}, 300, g);       // plus<int> is a type; g is an instance
transform(..., f);
```

## Lambda
Return **unnamed functors**
```cpp
transform(v1.begin(), v1.end(), back_inserter(v2), 
	[] (int x) {
		return 300 + -x;
	}
);
```
- Start with `[]`: **lambda introducer**
- Rest of it looks like function
- No need to deduce return type!

### Closures
> Lambda provides closure, a function that **captures the local environment**

```cpp
vector<int> v1 { 100, 101, 102, 103, 104 };
vector<int> v2;

// local variables
int a = 2, b = 100;
auto lambda = [&a, b] (int x) {
	return a * x + b;
};

a = 4, b = 1'000'000;  // update local variable, b to 1 million unaffected!
transform(v1.begin(), v1.end(), back_inserter(v2), lambda);
// return 4 * x + 100
```
- Variable `lambda` holding the function
- `[&a, b]` allows `lambda` to access the **local variables**
	- `&a` captures `a` as a **reference**
	- `b` copies `b` by value
- If `lambda` **outlives** the captured variable, undefined behavior!!

> **What class is `lambda`?**  
> With `auto`, compiler will make a *unnanmed temporary* class with an internal name
{: .notice--info}


### Lambda Internals
```cpp
struct L1 {
	int& a;
	int  b;
	L1(int&a, int b) : a(a), b(b) {}
	int operator()(int x) const { return a * x + b; }   // const member function!
}；
int a = 2, b = 100;
auto lambda = L1{a, b};     // same type as L1
a = 4, b = 1000000;
```
- To make `operator()` not `const`, use [`mutable`](#lambda)

## Ranges
> Concept generalization of a **sequence** of elements in STL denoted by half-open interval

`std::ranges::range` is a **concept** that has `begin()` and `end()`
- E. any container
- E. C array
```cpp
template <typename T>
concept range = requires(T& t) {
	ranges::begin(t);
	ranges::end(t);
};
```
- `begin()` is an iterator
- `end()` is a **sentinel** (generalization of iterator)
	- Just need an **object** that implements `op==` to compare if **iterator** has reached the end.
	- E. Infinite range: `op==` always returns `false`

### Views
> **Counterpart of a container; subset of `concept range`**  
> Lightweight, **read-only** range that doesn't *own* the elements, but **wraps another range**
> - Has a rule to apply for each element (E. transform)
> - Also a range, but typically holds a transformation object
{: .notice--info}


Created as `transform_view{ range, functor }` object 
```cpp
auto v1_view = ranges::transform_view{
	ranges::transform_view{ v1, negate<int>{} },  // range
	bind_front(plus<int>{}, 300)                  // functor
};
```
- **Underlying range**: `v1` vector
	- required to be a `range` concept
- **Transformation function**: functor `negate<int>{}`
	- If read from this view, will always apply the function
- Returns **another range**!

```cpp
ranges::copy(v1_view, back_inserter(v2));
ranges::for_each(v2, IntPrinter{}); 
```
- Copy the view to an std vector `v2`
	- Different from `std::copy(begin, end, dst)`
	- `ranges::copy(range/view, iterator)`
- `ranges::for_each(range, functor)`


### `op|`: Iterator Adaptor Closure
> **ana lambda**  
> Similar as Unix piping, connecting transforms
{: .notice--info}


```cpp
auto v1_view = v1 | views::transform(negate<int>{})
				  | views::transform(bind_front(plus<int>{}, 300));
```
- `views::transform()`: **function** template
	- Takes a **functor** (anything callable)
	- Returns a *range adapter [closure](#closures)*
- `op|(range r, range_adapter_closure C)` 
	- `R | C` equivalent to `C(R)`
	- Returns a new range that can be chained
	- `R | views::transform(C)` becomes `ranges::transform_view{R, C}`


Append `ranges::to<vector<int>>()` to create a new vector `v3`
- Back-insert to the newly-constructed vector and return by *value*
	- Takes a view
	- `v3` gets move-constructed

```cpp
auto v3 = v1 | views::transform(negate<int>{})
			 | views::transform(bind_front(plus<int>{}, 300))
			 | ranges::to<vector<int>>();
```

```cpp
auto v = views::iota(100)
		 | views::take(5)
		 | views::transform(negate<int>{})
		 | views::transform(bind_front(plus<int>{}, 300))
		 | views::filter([](int x) { return x % 2 == 0; });
```
- `iota(100)`: creates an *infinite* range starting from 100
- `take(5)`: takes first 5 (100, 101, 102, 103, 104)
- `transform`s
- `filter()` with a lambda function (returns T/F)
	- (200, 198, 196)

---
# 15. RNG
## Native Engine
### C
Uniformly generates in the range of `[-10, 10]`
```cpp
srandom(time(nullptr));
auto engine = &random;  // random() in the C library as engine
auto distro = [] (auto& some_engine) {
	return some_engine() % 21 - 10;
};
```
- `engine`: pointer to `random()` function
	- `random()` returns numbers from 0 to 2^31 - 1
- `distro`: **Lambda functor** that distribute it from -10 to 10

**Usage**
```cpp
map<int,int> m;
for (int i = 0; i < 1'000'000; ++i) {
	int x = distro(engine);
	++m[x];
}
```

### Cpp
> Make `rd`, `engine` and `distro` as functors

```cpp
// seed generation, taking advantage of real-RNG
random_device rd;
random_device::result_type seed;
seed = (rd.entropy() > 0) ? rd() : time(nullptr);

// construct engine and distro
default_random_engine engine { seed };
uniform_int_distribution<> distro { -10, 10 };

int x = distro(engine);
```
- `default_random_engine`
- `distro` functor `uniform_int_distribution`
	- Templatized with different integer types

**Seed generation**
- `std::random_device`: implementation-dependent **real** RNG
	- E. in Linux: `/dev/random`, generated by IO events (*entropy* event)
	- `rd.entropy()` tells if `rd` is actually random, or deterministic (`=0`)

1. `rd()` return a seed
2. `engine()` computes random number
3. `distro()` distributes the number

## Mersenne Twister engine
```cpp
// same setup as generating the seed
mt19937 engine { seed };
normal_distribution<> distro { 0.0, 3.5 };

map<int,int> m;
int maximum = 0;

// round to
int x = lround( distro(engine) );
```
- `mt19937`: Mersenne Twister (another algorithm)
- Smeared through `normal_distribution` floats with $$\mu = 0, \sigma = 3.5$$

### Mechanism
C `random()` has a very large *period*. Mersenne Twister's period is *much* larger!
- Fast
- Almost never repeats
- Very tunable
- High memory requirement

### Narrowing Conversion
What if I remove `lround()`:
```cpp
int x = distro(engine);       // silently fails
int x { distro(engine) };     // compiles with warning 
```
- Native conversion throws away the decimal portion!
	- Allowed in C, but **broke** in Cpp

Need `static_cast<int>`
```cpp
int x { static_cast<int>(lround(distro(engine))) };
```

## Stateful Functors
Use `bind()` to **compose** `distro` with `engine`
```cpp
for (int i = 0; i < 1000000; ++i) {
	auto generator = bind(distro, engine);
	int x = lround( generator() );
}
```

> **Fails to work**  
> Every run generates the same number every time
> - `bind()` makes a **copy** of the **functor** and its arguments
> - `engine()` holds **state** of current random number
> - In each `for` loop, `engine` copied with just the seed!
>   
> Also runtime is significantly **longer**, due to copying
{: .notice--danger}


```cpp
mt19937 engine { seed };

cout << "typeid(engine).name():\n" << typeid(engine).name() << '\n';
cout << "\nsizeof(engine): " << sizeof(engine) << '\n';
```
- `mt19937` is a specialization of template `std::mersenne_twister_engine<>` with tuned parameters
- **Name** internally will create a *name* with all these template parameters embedded
- **Size**: 5000 bytes!

In contrast, `default_random_engine` only has 8 bytes
- Specialization of `std::linear_congruential_engine<>` template
- Only need to carry state of the current number, and 3 parameters


- Can be fixed by defining `generator()` out of the `for` loop, or:

### `ref()`
> Pointer wrapper that behaves like a reference

Use `std::ref()` to pass by **reference**
```cpp
auto generator = bind(distro, ref(engine));
```

Implemented by holding a pointer `v_ptr`
- `bind()` holds a copy, which is just a pointer
- When `bind()` actually uses it, behaves similar
	- `operator T&`: behavior when automatically converted to `T&`

```cpp
template <typename T>
class reference_wrapper {
public:
    reference_wrapper(T& v) : v_ptr(&v) {}
    operator T&() const { return *v_ptr; }
    // ...
private:
    T* v_ptr;
};

template <typename T>
reference_wrapper<T> ref(T& v) {
    return reference_wrapper<T>(v);
}
```

### Lambdas
```cpp
auto generator = [distro, engine] () { return distro(engine); };  
```
Will **fail**, since copying by value
- Fails to **compile**. `operator() const`, but `distro(engine)` changes **state** of `engine`!

```cpp
auto generator = [distro, engine] () mutable { return distro(engine); };
auto generator = [=] () mutable { return distro(engine); };
```
- `mutable` does not enforce `const`ness of `op()`
- Compiles, but fails to run due to copying
- `[=]` shorthand for automatically listing `[distro, engine]`

```cpp
auto generator = [&distro, &engine] () { return distro(engine); };
auto generator = [&] () { return distro(engine); };  
```
- Works, by reference
- No `mutable` needed, since **pointer** references not mutated.
	- `const T* q`: const object
	- `T* const p`: stuck pointer (this case)
- `[&]` shorthand for listing `[&distro, &engine]`

---
# 16. Forwarding Reference and Variadic
Recall that these are **not allowed**
```cpp
X x;
const X x_c;

X&& x1 = x;     // cannot assigned named variable to R-value ref
X&& x2 = x_c;
X& x3 = x{};    // about to die
X& x4 = x_c;    // violates const
```
## Value Categories
### L-Value and R-Value
Define a wrapper for **heap-allocated** `double`
```cpp
struct D {
    D(double x = -1.0) : p{new double(x)} { cout << "(ctor:" << *p << ") "; }
    ~D() { cout << "(dtor:" << (p ? *p : 0) << ") "; delete p; }

    D(const D& d) : p{new double(*d.p)} { cout << "(copy:" << *p << ") "; }
    D(D&& d) : p{d.p} { d.p = nullptr; cout << "(move:" << *p << ") "; }

    D& operator=(const D& d) = delete;
    D& operator=(D&& d) = delete;

	// allows conversion to double
    operator double&() { return *p; }
    operator const double&() const { return *p; }

    double* p;
};
```

```cpp
D d1 { 1.0 };       // lvalue
D&& rrd4 = D(4.0);  // rvalue
rrd4 += 0.1;        // rvalue reference is mutable!
```
`D(4.0)` is a temporary object on stack, but when they are bound to references, lifetime **extended**, until references are destroyed!
- After `rrd4` goes out of **scope**, *destructor* called
- If not assigned, `D(4.0)` destroyed at end of semicolon

### Binding R-Value Reference
```cpp
D&& rrd4_1 = rrd4;
```
**Fails to compile**
- `rrd4` is a **reference variable** with a name. The reference `rrd4` *itself* is an **L-value**
	- What it references might be an R-value
- Can't bind it to R-value referenced `D&& rrd4_1`

Need cast `rrd4` to an R-value reference by `std::move()`
```cpp
D&& rrd4_1 = std::move(rrd4);
```
> `std::move()` does not **move**! Now both `rrd4_1` and `rrd4` point to the temp R-value.

Now consider!
```cpp
D& rrd4_2 = rrd4;
```
**OK**
- Bind a temporary object to a L-value reference `D& rrd4_2`
- Loophole: normally you can't assign R-value to L-value!

### Summary
- L-value
	- Named variable, function call returning by **reference**
	- C string literals `"abc"`, since they have addresses
	- R-value *itself*, since it has a name
	- GL-value: L-value + X-value
- R-value: two subcategories
	- PR-value (Pure R-value, no address)
		- Literals (`2.0`), function call returning by **value** (`s + s`)
	- X-value (eXpiring values, has address, but will die)
		- Return/cast to R-value **ref**  (E. `std::move(s)`)

## Forwarding Reference
### 1. Pass by value
```cpp
template <typename T> void f1(T t)   { t += 0.1; }
{
	D d1 {1.0};  // C(1)
	f1(d1);      // CC(1), D(1.1)
	f1(D(2.0));  // C(2), (CC elided), D(2.1)    
}  // D(1)
```
Take `t` as a regular passing by **value** parameter
- Works with all sorts of values

### 2. Pass by L-value Reference
```cpp
template <typename T> void f2(T& t)  { t += 0.2; }
{
	D d1 {1.0};  // C(1)
	f2(d1);      // no CC or D!
	// f2(D(2.0)); // err: cannot bind rvalue to T&
} // D(1.2)
```
Take L-value reference
### 3. Pass by Forwarding Reference
```cpp
template <typename T> void f3(T&& t) { t += 0.3; }
{
	D d1 {1.0};  // C(1)
	f3(d1);
	f3(D(2.0));  // C(2), D(2.3)
} // D(1.3)
```
Cpp changed the rule that `T&&` is no longer a *regular* R-value reference, but **forwarding** reference
- Can pass both L-value and R-value
	- Only works for **function** template, not class template!
- R-value reference: `T` resolves to `D`, so`T&&` resolves to `D&&` 
- L-value reference: `T` resolves to `D&`, so `T&&` becomes `D& &&`, collapsing into `D&`

**Collapsing Rules**
```
X&  &  collapses to X&
X&  && collapses to X&
X&& &  collapses to X&
X&& && collapses to X&&
```

### 4. Pass Forwarding Reference to Another Function
> Templates `T&&` only. Doesn't work for `int&&`
{: .notice--warning}


Any **named** reference, whether L-value of R-value, is an L-value!
```cpp
template <typename T> void f4(T&& t) { 
	D d{t};     // CC(1); CC(2): further forwarding
	d += 0.4; 
} // D(1.4); D(2.4)
{
	D d1 {1.0};  // C(1)
	f4(d1);     
	f4(D(2.0));  // C(2), D(2)
} // D(1)
```
> **All CC called, no MC!**  
> - `t` becomes **named** in the function. Will CC
{: .notice--warning}


### 5. Perfect Forwarding
`std::forward()` **preserves** the original value category
- Carry R-value forward!
- Shouldn't use `t` anymore in the function!

```cpp
template <typename T> void f5(T&& t) { 
	D d{std::forward<T>(t)};    // perfect forwarding, CC becomes MC
	d += 0.5; 
}
{
	D d1 {1.0};
	f5(d1);
	f5(D(2.0));
}
```
Now CC for L-values, MC for R-values

### 6. My Perfect Forwarding
> A function that casts input `T&` back to `T&&`

Define some helper class templates:
```cpp
template<typename T> struct remove_reference { using type = T; };
// specialization
template<typename T> struct remove_reference<T&> { using type = T; };
// changes nested type to be T w/o &
template<typename T> struct remove_reference<T&&> { using type = T; };

template<typename T> using remove_reference_t = typename remove_reference<T>::type;
```
- E. `remove_reference_t<int&> t = 5` same as `int t = 5`;

Use it:
```cpp
template<typename T>
T&& forward(remove_reference_t<T>& z) noexcept {
    return static_cast<T&&>(z);
}
```

```cpp
template<typename T> void f5(T&& t) { D d{ forward<T>(t) }; }
```

For **L-value** `f5(d1)`,
- `T = D&`, `T&& = D& && = D&` 
- When `forward<T>(t);` called, becomes `forward<D&>(t)`

```cpp
D& && forward(remove_reference_t<D&>& z) noexcept {
	return static_cast<D& &&>(z);
}
```
which evaluates to:

```cpp
D& forward(D& z) noexcept {
	return static_cast<D&>(z);
}
```


For **R-value** `f5(d{ 2.0 })`
- `T = D`, `T&& = D&&`
- `forward<D>(t)` becomes:

```cpp
D&& forward(remove_reference_t<D>& z) noexcept {
    return static_cast<D&&>(z);
}
```
No reference to remove, so just `D`:
```cpp
D&& forward(D& z) noexcept {
    return static_cast<D&&>(z);
}
```
- `t` is `D&&`, but also a named L-value, so it's okay to pass it as L-value in `forward(D& z)`
- Casted back to R-value reference!

> Arguments always passed in as `D&`, but `forward()` can recover the return type based on template evaluations
> - Question: are these all static?
{: .notice--info}


## Variadic Templates
> **Use `...` for more types**  
> - `typename` > type name > variable name
> Compile time!
{: .notice--info}


**Recursion template** (3 levels)
- **Template parameter pack:** `template <typename... Ts> `
- **Function parameter pack:** `f(Ts... args)`
- **Packed expansion:** `f(args...);` (usage)

```cpp
void print_v1() { cout << '\n'; } // base case for template recursion

template <typename T, typename... Ts>    
void print_v1(T arg0, Ts... args) {
    cout << arg0 << ' ';
    print_v1(args...);
}
```

Can do anything
```cpp
print_v1(s, "ABC", 45, string{"xyz"});

// compiler will generate recursively in object file:
void print_v1(string arg0, const char* arg1, int arg2, string arg3) {...}
void print_v1(const char* arg0, int arg1, string arg2) {...}
void print_v1(int arg0, string arg1) {...}
void print_v1(string arg0) {...}
```
until pack is depleted

### Forwarding References
We are currently passing by **value**
```cpp
print_v1(s, "ABC", 45, string{"xyz"}, D{3.14});
```
Passing by **value**, so at each recursive call (before printing), constructor called (5 times), same for D.

For **reference**, need to handle L-value and R-value
- Take `MoreTs&&`
	- `...` will apply to such a `&&` pattern
- Use `std::forward()` for perfect forwarding
	- Same as `print_v2(forward<string>(arg1), forward<string>(arg2), ...)`

```cpp
template <typename T, typename... MoreTs>
void print_v2(T&& arg0, MoreTs&&... more_args) {
    cout << arg0 << ' ';
    print_v2(std::forward<MoreTs>(more_args)...);
}
```
Just a single C beginning, D end


### Fold Expression
> **Not on exam**  
 `...` in an expression
{: .notice--info}



```cpp
(...  binary_op pack)	            // unary left fold
(pack binary_op  ...)	            // unary right fold
(init_expr binary_op ... op pack)	// binary left fold
(pack binary_op ... op init_expr)	// binary right fold
```

```cpp
template <typename... Types>
void print_v3(Types&&... args) {
    // Binary left fold without printing spaces
    (cout << ... << args) << '\n';

    // Unary right fold with comma operator to print spaces
    ((cout << args << ' '), ...) << '\n';
}
```
`(cout << ... << args) << '\n';`: binary left fold
- `(((cout << arg0) << arg1) << arg2)`
- `init_expr`: `cout`
- `binary_op`: `<<`
- `...`
- `op`: `<<`
- `pack`: `args`
- Expanded to `(arg0 bin_op (arg1 bin_op (arg2)))`

`((cout << args << ' '), ...)`: unary right fold
- `pack`: `(cout << args << ' ')`
- `binary_op`: `,` (!)
- `...`

