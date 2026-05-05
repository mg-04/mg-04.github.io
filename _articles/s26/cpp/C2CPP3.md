---
title: "C2cpp Notes: Smart Pointers and Concurrency"
permalink: /articles/cpp/3new
---

{% include toc %}

---
# 17. Smart Pointers
> **Suicidal Pointer**: gracefully cleans itself up when no longer referred  
> A class with **pointer inside** and acts like a pointer (`op*()`, `op->()`)
> - Self-delete when goes out of scope
> - How making two copies? Who's deleting it?
> 	- Shared pointer: know each other; deleted only after all gone
> 	- Unique pointer: Only one can hold it; can only be moved
{: .notice--info}

## Shared Pointer

### Implementation
```cpp
template <typename T> class SharedPtr {
	T* ptr;
	int* count;	
public:
	explicit SharedPtr(T* p = nullptr): ptr{p}, count{new int{1}} {}
	~SharedPtr() {
		if(--*count == 0) {
			delete count; delete ptr;
		}
	}

	T& operator*() const { return *ptr; }
	T* operator->() const { return ptr; }
	
	operator void*() const { return ptr; }   // for if (sp)
	T* get_prt() const { return ptr; }       // get() in STL
	int get_count() const { return *count; }
```
- Constructed with a pointer (E. `new string{}`)
- Manages **heap-allocated** data and `count`
- Last one out of scope is responsible for deletion

```cpp
	SharedPtr*(const SharedPtr<T>& sp): ptr(sp.ptr), count(sp.count) {
		++*count;
	}
	SharedPtr<T>& operator=(const SharedPtr<T>& sp) {
		if (this != &sp) {    // delete, and then construct
			if (--*count == 0) {delete count; delete sp;}
			ptr = sp.ptr;
			count = sp.count;
			++*count;
		}
		return *this;
	}
};
```
- Copy constructor makes a **shallow copy** of `ptr` and `count`; increments `*count`
- Copy assignment, need **detach first**

**Example**
```cpp
SharedPtr<string> p1 = {new string{"hello"}};
auto foo = [=] (SharedPtr<string> p) {  // take p by value, CC!
	cout << p.get_count() << endl;
}
foo(p1);
```
This will invoke copy constructor, incrementing `count`
After `foo()` returns, `p` goes out of scope, and `count` decrements back

### Vector
Let `SharedPtr<string>` contain a `string*` inside
```cpp
auto create_vec1() {
	SharedPtr<string> p1 { new string{"hello"} };
	SharedPtr<string> p2 { new string{"c"} };
	SharedPtr<string> p3 { new string{"students"} };

	vector v { p1, p2, p3 };
	return v;
}

vector v1 = create_vec1();
```
1. Shared pointers themselves `p1`... are stack-allocated
	- `string` objects are heap allocated
2. When creating a vector, will make another **copy** of the string!
	- Should be `vector<SharedPtr<s`
3. Return by value: `v` will get moved/elided
	- Stack-allocated `p1` goes out of scope, `count` goes back to 1

![](/articles/s26/cpp/img/17-vec-1 1.svg)

When `create_vec1()` returns, stack pointers destroyed, and `v` moved/elided
Now modify it:
```cpp
vector v2 = v1;   // copy pointers, but still same underlying string
*v2[1] = "c2cpp";
*v2[2] = "hackers"; 

// print v1 again
for (auto&& p : v1) { cout << *p + " "; } cout << '\n';
```
1. **Copy construct** `v1` to `v2`
	- `count` goes up to 2
2. Modify `v2`: Dereference `SharedPtr` as *raw* pointer and modify it! 
3. Print original `v1`: **also modified**!

![](/articles/s26/cpp/img/17-vec-3 1.svg)

### Loop Types

```cpp
for (SharedPtr<string> p : v1) { cout << *p + " "; }
for (auto p : v1)              // do something
for (auto& p : v1)
for (const auto& p : v1)
for (auto&& p : v1)
```
- `auto&` grab each by reference
- `const` necessary if `v1` is a `const` object!
- `auto&&` declares a [forwarding reference](#forwarding-reference), can pass both L- and R-values
	- Most general form in **template** code
	- `x` can either be an L-value ref or R-value ref, depending on category of `*v1.begin()`
	- Useful if iterator return is unknown
	- E. `vector<bool>`

> **When could dereferencing an iterator give you an R-value?**  
> `vector<bool>`, since each bit does not have a full address
{: .notice--info}


## Make Shared Pointer
`MakeSharedPtr<T>()` does the `new` with **any number** of arguments to construct `T`
- Variadic function!
- [Forwarding reference](#forwarding-reference)! Perfect forward to `new T{}` expression

```cpp
template <typename T, typename... Args>
SharedPtr<T> MakeSharedPtr(Args&&... args) {
	return SharedPtr<T>{ new T{forward<Args>(args)...} };
}
```

```cpp
auto p1 { MakeSharedPtr<string>("hello") };    // My implementation
auto p2 { make_shared<string>("c") };          // STL

static_assert(is_same_v< decltype(p2), shared_ptr<string> >);
```
Same type as the STL `shared_ptr`
### `std::shared_ptr`
**Usage**
```cpp
string*            p0 { new string(50, 'A') };
shared_ptr<string> p1 { new string(50, 'B') };
shared_ptr<string> p2 { make_shared<string>(50, 'C') };
```

**Memory Footprint**
```cpp
{
	string* p0 { new string(50, 'A') };           // leak string and char[]
	shared_ptr<string> p1 { new string(50, 'B') };
	shared_ptr<string> p2 { new MakeSharedPtr<string>(50, 'C') };
}
```
`MakeSharedPtr` has one **fewer** allocation from Valgrind
- Library notices that `new string` is on the heap, so it combines the control block `count` and `string` in a single allocation (placement `new`)
- Our implementation uses `new string`, no such freedom

![](/articles/s26/cpp/img/17-std-sharedptr-2.svg)

### Custom Deletion
```cpp
{
SharedPtr<string> p0 { new string[2] {"a", "b"} };
}
```
> Deletion **crashes** for `string[2]` ! Need `delete[]`
{: .notice--danger}


Need to write custom lambda functor for `delete`

```cpp
shared_ptr<string> p0 {new string[2] {"a", "b"}, 
	[](string* s) {delete[] s;}
}
```

Can also do for `FILE`s
```cpp
shared_ptr<FILE> sp { fp,
	[](FILE* fp) {fclose(fp);}
}
```

Or, directly put `shared_ptr<string[]>` as the type for STL

### Aliasing
`p2` only points to the `int` portion of `p1`
```cpp
shared_ptr<pair<string,int>> p1 { new pair{"hi"s, 5} };
shared_ptr<int>              p2 { p1, &p1->second };
```
Since `p2` is constructed on `p1`, the point to the **same** control block and share the **ref** count!
- *Managed* pointer same as `p1`
	- Managed pointer `delete`d at the end!
- *Stored* pointer points to the `int` portion of `p1`
	- Can be something random, doesn't even have to be part of `p1`

![](/articles/s26/cpp/img/17-alias.svg)

## Weak Pointer
> Useful for back/circular reference without messing up the cleanup

`std::weak_ptr` points to an existing shared object, but does **not** participate in reference count
- Same stored pointer and control block as shared pointer
- Another block of **weak count**
	- When shared count goes zero, data will be destroyed, but control block remains
	- When **both** shared count and weak count go zero, destroyed.

Define helper lambda
```cpp
auto weak_test = [](weak_ptr<string> wp) {
	shared_ptr<string> sp = wp.lock();
	if (sp) {
		assert(sp.use_count() == 2);
		cout << *sp << '\n';
	} else {
		cout << "weak_ptr expired\n";
	}
};
```
1. Copy `weak_ptr` by **value**
2. Call `wp.lock()` to get a new shared pointer to underlying object
	- You can't **directly** dereference a weak pointer
	- Such shared pointer will participate in use count
	- If `wp` expired (shared reference count = 0), get `nullptr`

```cpp
weak_ptr<string> wp;
{
	auto sp = make_shared<string>("hello");
	assert(sp.use_count() == 1);

	wp = sp;                     // weak_ptr does not increase
	assert(sp.use_count() == 1); // the shared_ptr's ref count

	weak_test(wp); // sp is alive, so is wp
}
weak_test(wp); // sp is gone, so wp is expired
```
> You can attach weak pointer to shared pointer, but when shared pointer goes away, weak pointer expires

- When all shared pointers go 

## Unique Pointer
> **Unique** ownership of a managed object. Smart deletion when out of scope
- Deletes object when destroyed
- **No** reference counting
	- Need ensure only one `unique_ptr`
	- `delete` copy operations, but can be moved
	- Just holds a pointer, size 8 bytes. 
{: .notice--info}


**Usage**: create an array with 1000 `string` objects, wrapped within one `unique_ptr`
```cpp
unique_ptr<string[]> create_array(size_t n, string s) {
	auto up = make_unique<string[]>(n);
	for (size_t i = 0; i < n; ++i) {
		up[i] = s;
	}
	return up;
}

size_t n = 1000;
unique_ptr<string[]> up1 = create_array(n, "hello");

for (size_t i = 0; i < n; ++i) { assert(up1[i] == "hello"s); }
```

**Copy and move operations**
```cpp
unique_ptr<string[]> up2;
assert(!up2);

// up2 = up1;            // can't copy
up2 = std::move(up1);    // can move

// It can also be moved to a shared_ptr
shared_ptr<string[]> sp { std::move(up2) };
```
- After moved away, original one becomes a `nullptr`

Can also convert to a shared pointer, with a custom deleter
```cpp
template <template T, template Deleter>
shared_ptr(std::unique_ptr<T, Deleter>&& r);
```

---

# 18. Concurrency

Measure with `std::chrono::high_resolution_clock`
```cpp
#include <chrono>
auto time0 = high_resolution_clock::now();
auto time1 = high_resolution_clock::now();
auto dt = duration_cast<microseconds>(time1 - time0);
cout << dt.count();
```


## Sequential
```c
struct Args {
    uint64_t* sum_ptr;    // pointer to shared variable
    uint64_t count;
};

void* f1(void* args) {
    Args* p = (Args*)args;
    uint64_t* sum_ptr = p->sum_ptr;
    uint64_t count = p->count;

    while (count--) {
        ++*sum_ptr;
    }
    return NULL;
}
```
`f1()` grabs `sum_ptr` and increments it `count` times

`sum1()` calls `f1()` twice, each incrementing it 1M times
```cpp
uint64_t sum1() {
    constexpr uint64_t count = 1'000'000;
    uint64_t sum = 0;

    Args args1 { &sum, count };
    f1(&args1);

    Args args2 { &sum, count };
    f1(&args2);

    return sum;
}
```
- Time: 3 ms
- Result: 2M

## C `pthread`
> Shared address space, running simultaneously (3 threads)

```cpp
uint64_t sum2() {
    constexpr uint64_t count = 1'000'000;
    uint64_t sum = 0;
    pthread_t t1, t2;

    Args args1 { &sum, count };
    pthread_create(&t1, NULL, &f1, &args1);
    Args args2 { &sum, count };
    pthread_create(&t2, NULL, &f1, &args2);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return sum;
}
```
- Time: 4 ms (**slower!**, bad cache locality)
- Result < 2M

- Load-increment-store may be interleaved. Not atomic.

### Cache Locality
Declare `sum` as an array of two integers. Increment separately
- Time: 4 ms, two `uint64_t` not on same cache line
	- False sharing for 2 CPUs! 
	- Need to put on different cache lines -> 1.8 ms
- Result: 2M

### Locking
Use `pthread_mutex`
```c
pthread_mutex_t mtx = PTHREAD_MUTEX_INITIALIZER;
void* f2(void* args) {
    Args* p = (Args*)args;
    uint64_t* sum_ptr = p->sum_ptr;
    uint64_t count = p->count;

    while (count--) {
        pthread_mutex_lock(&mtx);
        ++*sum_ptr;
        pthread_mutex_unlock(&mtx);
    }
    return NULL;
}
```
- 147 ms, much **slower** :(
- Better performance: atomic variables

## Cpp `thread`
> `-pthread` in Makefile `CXXFLAGS` and `LDFLAGS`

`struct wallet` encapsulate a mutex
```cpp
struct wallet {
    mutex m;
    uint64_t money = 0;
    operator uint64_t() const { return money; }

    wallet& operator++() {
        m.lock();
        ++money;
        m.unlock();
        return *this;
    }
};

void f(wallet& sum, uint64_t count) {
    while (count--) {
        ++sum;
    }
}
```

In `main()`, create a `thread` object:
```cpp
tmeplate<class F, class... Args>
expicit thread(F&& f, Args&&... args);
```
Parameters:
1. Function to run
2. Arguments (default by *value*, need wrap with `ref()`)

```cpp
#include <thread>
constexpr uint64_t count = 1'000'000;
wallet sum;

thread t1 { f, ref(sum), count };
thread t2 { f, ref(sum), count };
t1.join();
t2.join();
```

### Scoped Lock and Threads
> A `mutex` wrapper

- Constructor: call `m.lock()`
- Destructor: `m.unlock()`, as long as **scoped**
- Robust to `throw`ing!

```cpp
#include <mutex>
    wallet& operator++() {
	    {
	        scoped_lock lck{m};
	        ++money;
	    }
	    return *this;
    }
```

Can also construct with **multiple** `mutex` objects
- Internal deadlock prevention algorithm

`jthread` call `join()` at end of scope
```cpp
{
	jthread t1 { f, ref(sum), count };
	jthread t2 { f, ref(sum), count };
}
```
- Main thread needs to call the destructor

## Condition Variables
> For producer-consumer, locking/unlocking becomes hairy. Condition variables manage them in a controlled way

**Example**

Main thread: while loop that reads a line
- `unique_lock` used in conjunction with **condition variable**
- `condition_variable.notify_one()` unblock one waiting thread
	- Notify *while* holding the lock
- When input hits EOF, poison `vec` with empty string
Both threads have access to `vec`, `mtx`, and `cv`

```cpp
vector<string> vec;
string str, line;

mutex mtx;
condition_variable cv;

while (getline(cin, line)) {
	istringstream iss(line);

	unique_lock lck(mtx);  // lck's contructor will lock mtx
	while (iss >> str) { vec.push_back(str); }
	cv.notify_one();  // unblock one waiting thread
}   // unique_lock unlocks when out of scope

{
	unique_lock lck(mtx);
	vec.push_back(""s);  // poison value to tell the thread to exit
	cv.notify_one();
}
```

Child thread: pass lambda function, grabbing everything by *reference*
- Run forever: acquire same lock
- `.wait()` atomically yields `lck`, put itself to **sleep** (blocking)
	- Block until other thread does `cv.notify()`
	- Need to wrap `mtx` with `unique_lock`
	- When you wake up from `notify`, wait for parent to release. `wait()` returns after **reacquired lock**
	- Recheck `while`, in case other consumer takes it
- Print out each word and clear vector
	- Poison value: empty string

```cpp
thread t {
	[&]() {
		while (1) {
			unique_lock lck(mtx);  // lck's contructor will lock mtx
			while (vec.empty()) {
				cv.wait(lck);
			}

			for (const auto& x : vec) {
				if (x == ""s)    // exit thread on poison value
					return;
				cout << x << ' ';
			}
			vec.clear();
		}    // lck's destructor will unlock mtx
	}
};
```

---
# 19. Atomics

This section is under construction, on Jae's end
{: .notice--warning}


## Cpp Memory Models
Gets slower and stricter, but safer (https://en.cppreference.com/cpp/atomic/memory_order)
```cpp
enum memory_order {
    memory_order_relaxed,
    memory_order_consume,
    memory_order_acquire,
    memory_order_release,
    memory_order_acq_rel,
    memory_order_seq_cst
};
```

## Atomic Variable
> Similar to [waller code](#cpp-thread) before

In cpp, you can do an `atomic` of anything, even a `struct`
- May use lock. Can check with `static_assert<atomic<T>::is_always_lock_free`
	- `true` for built-in types, but typically not for complex `struct`s
	- Architecture dependent (E. memory fence)
`atomic.cpp`:
```cpp
#include <atomic>
struct wallet {
    std::atomic<uint64_t> money{0};
    operator uint64_t() const {
        return money;
        // return money.load(std::memory_order_relaxed);
    }

    wallet& operator++() {
        ++money;
        // money.fetch_add(1, std::memory_order_relaxed);
        return *this;
    }
};
```
- If you use atomic variable directly, cpp will default to **most strict** memory model `seq_cst`
	- Can use more relaxing memory model
	- Not too different in `money` example
- **Much** faster than `mutex`, but still *much* slower than native


## Memory Ordering

`producer` increments `x`, and then `y` in a loop
- `y` will never be bigger than `x`
- `consumer` checks that

```cpp
std::atomic<uint64_t> x{0};
std::atomic<uint64_t> y{0};

void producer() {
    for (size_t i = 0; i < 1000'000'000; ++i) {
        x.fetch_add(1, std::memory_order_relaxed);
        y.fetch_add(1, std::memory_order_relaxed);
    }
}

void consumer() {
    for (size_t i = 0; i < 1000'000'000; ++i) {
        uint64_t yy = y.load(std::memory_order_relaxed);
        uint64_t xx = x.load(std::memory_order_relaxed);
        assert(xx >= yy);
    }
}
```
- Works on x86. Less aggressive ordering
- On ARM, fails with `relaxed` :(

If use `y.fetch_add(1, release);` and `yy = y.load(acquire);`, telling compiler to make sure when `y.load()` is called, **all changes before** are visible.

