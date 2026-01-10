---
title: "3-Synchronization"
permalink: /articles/comparch/sync
date: 2025-12-20
---

{% include toc %}


Need **memory consistency** and **cache coherence**
# Parallelism
- **ILP**: OOO speculation, RR
- **DLP**: SIMD, SIMT (multithread)
- T(Thread)LP: Synchronization, coherence, consistency, interconnection
Reading: Synthesis lectures on coherence, consistency, and interconnection networks

## Minimal Parallel Computer
To compute `x--`

```
Rx <- ld x
sub Rx, Rx, 1
st Rx -> x
```

# Synchronization
**Issue**: race condition on multiple processors

## Lock
Add a `lock` instruction to the ISA. 
- Acquire: `lock x`, one processor has exclusive access to `x`
- Release: `unlock x`
`lock` and `unlock` signaled to **arbiter**, granting permission to one of the processors.
- `x` is **mutual exclusion**: shared variables can be exclusively handled by a piece of code
- If program fails to unlock: **starvation**: other threads can't make progress

```
lock L
	Rx <- ld x
	sub Rx, Rx, 1
	st Rx -> x
unlock L
```

**Issue**: lock and shared variable is in **memory**. Need to **cache** in processor cache
- After lock updated in cache, need to go to **arbiter** and unlock it.
- `x` needs to be **propagated** to memory so that other processors can get the latest value of `x`
- Operation becomes
	- `Lock L`
	- Shared variable update
	- `Unlock`
		- Tell arbiter to unlock
		- `Flush L`
		- `Flush x`
- May need protocol to **forward** cache values

## Solutions
- Send arithmetic operations to **memory** (**Atomic** RMW (read, modify, write) instruction). Mark certain regions of code for **shared variables** and **locks** as **uncacheable**
	- RMW happens without any interruption
- Make **centralized cache** for shared variables and locks (in GPU)
- **Transactional memory**, detect conflicting operation, rollback, and serialize

## TS
RMW happens without any interruption
Let RMW be "test & set instruction" (**atomic**)

```
TS:                # atomic block
	Rx <- ld x
	st 1 -> x      # unconditional write
```

- Reads the value of `x`, <span style="color:rgb(255, 0, 0)">return</span> the value
- Sets `x=1`
In modern processors, use Compare And Swap (CAS), store the value of a register `Rval` into `x`

Lock routine

```
loop:
	Rx <- TS x
	BNEZ Rx, loop    # spin if Rx == 1
```

Unlock routine

```
	st, 0, x
```

Suppose `T1` locks the variable. 
- Executing `TS`, atomically update `x=1`. Suppose `T2` wants to get lock, reads `x=1` from register
- `T1` Do process. `T2` spins
- After unlock, `T1` reset `x=0`

Shared variables set as **uncacheable**. Everything goes to memory

**Performance**
- Not great, serial section in mutex
- No OOO

Ideally, have some mechanism that will automatically take shared variables and place them into cache.


### Performance
What is the latency of lock acquire and release?
- Need to compute the number of bus transactions needed before a lock acquire/ release

1. **Uncontended** lock acquire  
	1. Lock variable is not in the cache. In `invalid` state
	2. Write: move from `invalid` to `modified`, broadcasting it getting the lock  
2. **Contended** lock acquire (TTS)  
	Assume one other thread wants to acq. Thread 1 has lock in `modified`
	1. Thread 2 tries to read the lock, executes `TS` (unconditionally writes a 1). Need to get a copy of the cache block in **exclusive** state. The write **invalidates** the thread 1 cached copy.
	2. Thread 1 goes from `Modified`->  `Invalid`, thread 2 goes from `Invalid` to `Shared` to `Modified`
		- Thread 2 does **not** get access to the lock, but still writes a "1" to it
		- This write process still invalidate the lock
		- If thread 3, thread 3 also goes to `Invalid`
		- Bus **flooded** with such traffic. Lock release is **slowed down**
		- Worse: the cores keep spinning! Not just one cycle of contention!  
3. **Contended** lock release (terrible performance)
	- Owner can't execute `store 0 -> x` instruction, need to wait for every previous lock write traffic.

## TTS 
**Solution**: TTS lock. Before writing, first `LD` the lock variable. **Check** if lock is acquirable (`BRNZ`)

```
loop:
	LD x
	BRNZ loop
	TS x
	BRNZ loop
```

- Instead of going from `Modified` to `Invalid`, all threads go to `Shared` (read-only copy)
	- At unlock, all `Shared` will be written -> `Invalid`
	- Make unlock very cheap by adding another **test** before TS

### Load linked and Store conditional
Make store in TS conditional on writes that have happened in other cores
- `LL x`
	- Load `x`
	- Internally remember the <span style="color:rgb(255, 0, 0)">link</span>, set a **flag** if someone else writes to this location
- `SC x`
	- Attempts to store to `x` only if it's **not written** by someone else after last `LL`
	- Else, go back and get lock again

```
Lock:
	Rx <- LL x
	BRNZ Rx, Lock                # if x != 0, someone has the lock, retry
	Rx <- SC x
	BRNZ, Rx, Lock               # if SC failed, retry 
```

# Consistency Mechanism
Suppose you have location `x` and `y` in memory

```
Thread 1: 
	1 ld x
	2 st x
Thread 2:
	3 ld y
	4 st y
```

**Consistency**: How does each thread see updates to **other** variables in the memory?
- Can I interleave the updates of location `y` with location `x`?
- Are all orders of 1234 OK? What are the valid orders in which **multiple** memory locations can be updated
	- Coherence is about one memory location

Consistency model: rules for memory

### 1. Sequential Consistency (SC)
Can't be reordered
- If $$LD(x) <_{po} LD(y)$$, then $$LD(x) <_{eo} LD(y)$$
- Same for `st`
- If $$LD(x) < _{po} ST(y)$$, then $$LD(x) <_{eo} ST(y)$$
- Same other for `st` followed by `ld`
Forbids OOO memory reordering in a single core

### 2. Relaxed Consistency
Reordering is forbidden only when the programmer *wants* it to happen
Introduces a new `fence` instruction: stop reordering instructions **across** the fence

```
Block A
------- Fence
Block B
------- Fence
Block C
```

When `fence` on, OOO turned off
- When `fence` decoded in HW, fetching is stopped, until `fence` becomes the <span style="color:rgb(255, 0, 0)">oldest</span> instruction in the pipeline. 
	- **Drain** all memory  buffers in pipeline
	- (Decode serialization)
	- `mfence`: Do not allow reordering between the timing routine and other instructions that has happened before
- $$LD(x) <_{po} Fence$$, then $$LD(x)<_{eo} Fence$$
- $$Fence <_{po} LD(x)$$, ...
- Same for store
- $$Fence_x <_{po} Fence_y$$, then $$Fence_x < _{eo} Fence_y$$

### 3. Total Store Ordering (TSO)
Everything else can't, but **Store -> Load** may be violated
- TSO has a **store buffer**

## Lock-Free Algorithm
E. used to update a stack/linked list
Use atomic operations (RMW)
- CAS (read a value from memory, compare it conditionally. If condition is true, write a different value back to a location): hardware instruction that does read, compare, and write in a single step
- E. adding two nodes simultaneously a linked list, when executing CAS, read the tail pointer, and atomically swap to the pointer to one of the the two algorithms

# Cache Coherence
if multiple cores R/W to the **same** address, which value is the correct one?
Must provide two protocols
- **Read request**
- **Write request** with ack

## **Invariant** rules
- **SWMR** (Single Writer Multiple Reader)
	- Multiple writes not allowed
	- Either
		- A single core has **RW** access
		- Multiple cores have read only access
- **LVI**: (Last Value Invariant)
	- If multiple writes followed by a read, read always gets the **last** written value

Attach little **controllers** near **cache** and **memory** to communicate to ensure the properties above
- Communicating FSM

### Assumptions
- Operate on cache block addresses. All transactions happen at granularity of cache lines (64 bytes)
- Request and responses are **ordered**
	- Suppose core C1 sends a request. It needs to wait for its **response** before sending a second request (**Snoopy protocol**, bus)
		- Across cores, it may be interleaved
	- Else: pipelined
	- Else: unordered (may get second response before the first). Need **directory protocol**, P2P

## Cache Controller
> Take state definitions, and use SIMD table. Here's a partially filled table of state transactions. Based on given info, fill out the rest  
> Application of concepts. Don't memorize specific states, maybe given a new set of definitions  
> Practice: Coherence questions 1.1-7  
> Given a program, find outputs that legal under sequential consistency  
{: .notice--warning}


## Design Space
**Dirty** block: modified in lower-level cache but not in higher-level
- Need writeback after eviction
### States
- **Validity**: has the **most recent** value
- **Dirtiness**: has the most recent value, but updates not written back to memory
- **Exclusivity**: only have **one** private copy
	- Except in the shared LLC
- **Ownership**: responsible for **responding** the cache requests
	- May not be evicted without transferring ownership

- `Modified`: valid, exclusive, owned, and potentially dirty
	- Cache only has one valid copy
	- Can read or write
- `Shared`: valid but not exclusive, not dirty, not owned
	- Read-only copy
- `Invalid`: Not valid

### Transactions
- `Get`: Obtain a block
- `Put`: **Evict** a block

### Protocols
- **Snooping**: Request by **broadcasting** a message to all other controllers. Owners respond
	- Simple, can't scale
- **Directory**: Requests managed to memory controller, and forwarded to appropriate caches
	- Scalable, but slower (sent to home)

## Snooping Protocols
- `Modified`
	- Can read or write
- `Shared`
	- Read only
- `Invalid`
	- Can't read or write

**Actions**:
- Issue `BusRd`, `BusEx`
- Send data if owner

### Snoopy
Assume transactions are observable by all other cache controllers
 - Implemented on a **bus**
 - All cache controllers can observe bus traffic
 - **Ordered** requests and responses
In cache line, add additional **coherence** metadata to track the state
Every cache block can be in one of three states:

![](/images/comparch/MSI_state.png)

`Invalid`
- `LD(x)`
	- Miss, issue `BusRD(x)`
	- Transition to `Shared`
- `ST(x)`
	- Miss, issue `BusEx(x)` to ask for exclusive access
	- Transition to `Modified`
- Receive `BusRd(x)` or `BusEx(x)`
	- Don't care
`Shared` 
- `LD(x)`
	- Hit, stay in `Shared`
- `St(x)`
	- Issue `BusEx(x)`
	- Transition to `Modified`
- Receive `BusRD(x)`
	- NOP, let them read
	- Optionally let them read
- Receive `BusEx(x)`
	- **Evict** the cached item, 
	- Drop to `Invalid`
`Modfied`
- `LD(x)` or `ST(x)`
	- Hit, stay in `Modified`
- Receive `BusRD(x)`
	- **Forward data**, or writeback (`updateMem`)
	- Drop to `Shared`
- Receives `BusEX(x)`
	- Forward or writeback
	- Drop to `Invalid`

### Pipelined
FIFO buffer to handle requests and responses
- More buffer states in state machine
- More efficient


# Directory protocols
Broadcast-based protocol (E. Snoopy) does *not scale*

A **directory** that maintains a global coherence view
- **No state machine**, all lookups happen at the central space
- **Directory**: computes the local LUT tracks which thread his the current owner to your director.
- Assume point-to-point ordering

## Setup
 8-core multiprocessor, shared `SNUCA` (you know exactly the cache bank from the address-)
64 MB chip shared L12 cache
 L1: 4 banks (that build each L1 chunk), address interleaved, set-associative,  Multiple outstanding load misses (miss status handling), one `rd`, one `wr` port
- Allows simultaneous L/W in the **same cycle**, pipeline
- Store merging: when cache misses, take a break, and wait a while for new loads to come out, and then scare the original circuit. Share mass bulks of cache misses
**L2:** 64 banks, address interleaved, SA, writeback, write-**allocated** (fetch data from low level, allocate it into cache), one `rd/wr` port
	- L1 L2 connected with on -chip network
	- Requests and replies are **ordered** (to the same node (dimensional order))
	- Network header has 40 bits 
**Physical implementation:** along each L1 block, that hold all cache results from upper level to 

## Protocol
**Metadata**
- L1: Load, store, spill, directory message
- L2: directory transition table

### States
- `inv`
- `shared`
- `modified`
- `SM` (S->M in progress, need to invalidate other sharers)
- `MM` (M->M in progress, need owner to writeback & invalidate)
Transactions take **multiple cycles** (assumed to be atomic in snoopy)

### Messages
Processor -> Directory
- `Share`: request a shared cache
- `Modify`: request an exclusive cache
- `rDAB` (dirty writeback + eviction): send latest data from cache, **unregister** it from directory
- `rINV` (clean eviction)
Directory -> Processor (commands)
- `NACK`: Negative ACK, **try again later**
- `MACK`: ACK for **modify** request
- `cDAB`: Dirty Acknowledge back **and invalidate**
- `cINT`: **Invalidate**: ask to **invalidate** its copy

## Hardware
L2
- Global coherence sate
- <span style="color:rgb(255, 0, 0)">Presume</span> <span style="color:rgb(255, 0, 0)">vector</span> (1 bit/core)
	- Owner ID (for `modified)
- When you see more than 1 ones, the condition will be `Shared` as in SIMR
- Suppose just one 1, state will be `Modified` or `Shared`
- Suppose all 0, all will be `Invalid`, need to decode from M2.

L1
- Current state
- (Optional) LSQ



## L2 Side

Send `NACK` if transitioning to `SM` or `MM`, can't immediately fulfill the request

| State | `share`                                                 | `modify`                                                      | `rDAB` (dirty)                                 | `rINV` (clean)               |
| ----- | ------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------------------- | ---------------------------- |
| I     | Fetch from **memory**<br>Send data<br>-> `Shared`       | Fetch from memory<br>-> `Modified`                            | X                                              | X                            |
| S     | Add to **sharer list**<br>Send data                     | Send `MACK` to requester<br>Send `cINV` to sharers<br>-> `SM` | X                                              | Remove  sharer               |
| M     | Send `cDAB` to M<br>Send `NACK` to requester<br>-> `SM` | Send `cDAB` to M<br>Send `NACK` to requester<br>-> `MM`       | Update data <br>(remove sharer)<br>-> `Shared` | Remove sharer<br>-> `Shared` |
| `SM`  | Send `NACK`                                             | Send `NACK`                                                   | X                                              | Drop message                 |
| `MM`  | Send `NACK`                                             | Send `NACK`                                                   | Update data<br>-> `Shared`                     | -> `Shared`                  |

## L1 Processor Side
### Load
- **Hit:** Return load value
- **Miss:**
	- If can be merged into an existing **MSHR**, send a `share` request
	- If **unmergeable** (standalone miss): one request per cycle
	- **Uncacheable** (not part of coherence protocol): request directly to memory

### Store

| L1 Hit | Load Type                    | Action                                                                                                                                              |
| ------ | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Yes    | Modified                     | No action, update in cache                                                                                                                          |
| Yes    | Shared                       | Request `modify`<br>**Stall** commit until permissions obtained<br>Need to make sure this is the **oldest** store. All speculation must be resolved |
| No     | No matching load miss        | No action, write around to L2                                                                                                                       |
| No     | Matching load miss (in MSHR) | Stall store commit until matching load is serviced. <br>Then request `modify` to the previously written entry                                       |

### Spill
Spill L1 to make room for another block
- If **clean**, send `rINV`
- If **dirty** (modified), send `rDAB`

### L1 Message Handling
If receives... and hit:
- `cDAB` Invalidate + writeback
- `cINV`: Invalidate
- `NACK`: retry again
If miss, ignore message

# Dangers
- L1 stalls do not require circular waits (?)
- Dropped messages are redundant (due to **ordered** communication)
- Priority virtual channels, order:
	1. Mem -> L2
	2. L2 -> L1
	3. L2 -> mem
	4. L1 -> L2
- Buffer, with `NACK` at holding sate

# Interconnect Network
**Bus**, attached to
- Cache -> processor
- Memory
Does not scale!!! You can't tie too many things without affecting frequency
- As number of taps increase, frequency drops **super-linearly**

![](/images/comparch/router.jpg)

Need to add a **router** for point-to-point communications between the processors
- Router only connected to **nearest neighbor**
- Fast, since communication in very short distance
- Gain in clock frequency
- But need **more clocks**
**On-chip** interconnection network
- Packet
	- 1 valid bit
	- Control info (from, to)
	- Payload
- Payload may split to sub-packets (**flit**)

## Design choices
- Topology (E. ring, mesh (2D), torus (2D ring))
	- More complexity has lower latency, but more buffering (space) needed
- Routing
- Flow control
	- What happens if you are unable to send a packet through a link (E. multiple flows to a single direction). Tell the sender to **stop** sending traffic
- Router microarchitecture (E. mesh)
	- 5 input ports, 5 output ports (1 local, 4 from neighbor routers (NSWE))
	- Input ports each has a **fixed-size buffer**
	- Little controller to look at the **head** (control bits) of each buffer, determines which directions to send the package to
	- A few crossbar (MUX) to route to output

![](/images/comparch/interconnect.jpg)

## Conflict
when multiple inputs need to send to same output -> delayed -> need buffering (fairness policy)
- Controller needs to know the number of buffer free slots in **downstream** router (credit-based flow control)
	- Need to report **before** full, not *when* full.
	- Bisection bandwidth: max data can transmit from one end to the other

## Lookup
1. Look at local L1 first
2. If miss, format a packet request and send through the router to neighbors
3. Other core looks up the data and send back the cache line in a packet
4. Receives data, caches into local L1
5. If others also miss, goes to **home** node with M2 data
	- How to locate which L2 **bank** to go to?
	- Take the entire address space, go to the corresponding modulo tile