---
title: "OS Notes: Scheduling"
permalink: /articles/os/2-sched
---

{% include toc %}

# 12. Scheduling
> How synchronization works

**Dispatcher**
- Low-level *mechanism*
- Responsible for **context switch** (`context_switch()`)
**Scheduler**
- High-level *policy*
- *Decide* which process to run
	- `pick_next_tesk()`
## Metric
- Min waiting tie
- Max CPU util
- Max throughput
	- As many processes as possible per unit time
	- For batch jobs
- Min response time
- Fairness

## Policies
### 1. FIFO
- Non-preemptive (you can run as long as you want)
- Implementation: FIFO queue
- **Good:** 
	- Simple
	- Fair
- **Bad:** 
	- Waiting time depends on arrival order
	- Short process stuck waiting (Convoy effect)
### 2. Short Job First (SJF),
*without preemption*
- On the waiting queue, run shortest job first
### 3. Shortest Remaining Time First (SRTF)
- If a process arrives with shorter time than the **remaining** current process time, schedule new process
- aka SJF *with* preemption
- **Good:** 
	- Reduces **average** waiting time
		- Proven to be **optimal!**
- **Bad**: 
	- Starves long jobs
		- Avoid starving: prioritize processes with long wait time
	- **Not practical** to *predict* burst time
		- Use past to predict future
![[Pasted image 20260302192852.png]]
### 4. Round Robin (RR)
- aka preemptive FIFO
- Each process runs a predetermined time slide, then preempt and move back to queue
- Need optimal time slice ((wait time > **response** time) vs # context switch)
- **Good:** 
	- Low *response* time, fair allocation, 
	- Low average waiting time
		- Even when job lengths **vary widely**
- **Bad:** 
	- Poor average waiting time when jobs have **similar lengths**
	- Performance depends on time slice length

## Priorities
Associated with each process ("niceness")

- Run highest-priority process that's ready
	- **Round-robin** among equal priority

- Can be statically assigned
- Also dynamically *changed* by OS
	- **Aging** for long queuing process

```c
for (pp = proc; pp < proc+NPROC; pp++) {
	if (pp->prio != MAX)
		pp->prio++;
	if (pp->prio > curproc->prio)
		reschedule();
}
```

### Priority Inversion
If a high-priority process depends on low priority process (E. to release a lock)
- When a medium-priority process runs
- High-p process wastes CPU cycles
- Med-p process has high *effective* priority -> priority **inversion**

**Solution**:  (Temporarily) inherit the priority of waiting process
- Inheritance chain
- Reset

### Multi-Level Feedback Queue (MFQ)
Queues with different priority levels
- Process priority changes based on observed behavior

**Parameters**
- Number of queues (140 in Linux)
- Scheduling algorithm for each queue
- When to upgrade/demote a process
- Default queue a process will start in

**Rules**
1. If `p(A) > p(B)`, A runs
2. If `p(A) = p(B)`, A and B runs in RR using the *time slice* of the queue
3. When a job enters the system, starts in highest priority queue
4. Once a job uses its allocated time at a level, priority **reduced**
5. After some time period, move all jobs to the highest priority queue

## Multicore Strategies
**Setup:** Symmetric Multiprocessing (SMP)
- Identical CPU
- Same access time to main memory
- Private cache

### 1. Global Queue of Processes
- **Good:** 
	- Good CPU util
	- Fair to all processes
- **Bad:**
	- Global queue lock (not scalable)
	- Poor cache locality
### 2. Dispatcher Core
Dispatcher core handles the scheduling and synchronization
- **Bad:** one fewer core

### 3. Per-CPU Queue
**Static** partition to individual CPUs
- **Good:** 
	- Simple
	- Scalable
	- Cache locality
- **Bad:**
	- Load-imbalance
	- Unfair
	- Lower CPU util

### 4. Hybrid Approaches
Modern OS
- Global and per-CPU queues
- Migrate processes across per-CPU queues
- Cache recent processes on the *same* CPU



# 13. Linux Scheduler History
## 1. $O(N)$
Scan the *entire* list of runnable processes to select
- Global RQ
	- More contention for multicore
- Preemptive time slicing: jiffies
- Slices: when blocked before slice ends, half of the remaining slide is added to the next epoch
	- ana. increase in priority
## 2. $O(1)$
### Policies
**Non-real time** policies
- `SCHED_OTHER` based on nice value
- `SCHED_BATCH` derived from `SCHED_OTHER` to optimize **throughput**
- `SCHED_IDLE` derived from `SCHED_OTHER`, but with *nice values* lower than 19
**Real-time** policies
- `SCHED_FIFO`, until finish, or preempted by a higher priority
- `SCHED_RR` derived from `SCHED_FIFO`, but with RR
- `SCHED_DEADLINE` uses **Global Earliest Deadline First** (GEDF)

### Implementation
- 2 Independent RQ for **each CPU**
	- `active` and `expired` array
	- Each is an *array* of RQs
- Task are in **array**, indexed according to priority
	- Real time: assigned **static** priorities
	- Nice values: dynamic priorities
		- $\pm 5$ range
		- More **interactive** tasks will be blocked longer
- Decay when *quantum* used up
	- Timer count drops to -1
	- Immediate reset, *recalculate* priority, and put into **higher queue**
	- Over time, `active` array empty out to `expired`
	- When `active` completely empty, **exchange**

Need to find the highest priority queue that is *not empty*
- `ffz()` find first zero
- Only examines fixed-size *bitmaps* of queue states
- `dequeue_front()`

## 3. CFS
> Maintain fairness and balance

- Balance timer
- Determine virtual runtime

Use dynamic time slice on `EPOCH` definition
- `EPOCH` controlled via `sched_latency` (E. 48 ms)
- Each task in a RQ gets an *equal* share of `EPOCH
	- Can configure `min_grannularity` (E. 6 ms)
Runtime then **weighed** based on nice value, with a map
$$\texttt{time\_slice}_k = \frac{\texttt{weight}_k}{\sum_{i=0}^{n-1} \texttt{weight}_i} \cdot \textcolor{blue}{\texttt{sched\_latency}}$$
- `vruntime` **normalizes** actual `runtime` based on **priority**
	- CPU "debt account"
$$\texttt{vruntime}_i = \texttt{vruntime}_i + \frac{\texttt{weight}_0}{\texttt{weight}_i} \cdot \texttt{runtime}_i$$

### Data Structure
> Extract task with minimum `vruntime`

**Time-order** RB tree
- Operations $O(\log n)$
- High need at lower-left, pick the leftmost

![[Pasted image 20260309210044.png]]

### Scheduling **Class***
> [!warning] 
> If someone spawns a lot of threads, Need to **group** for fairness
- `proc` interface

`sched_class` provides a common set of functions that define scheduler behavior
- ana. CPP `vtable`

### Load Balancing
**Scheduling domains** allow grouping processors for load balancing/segregation
- Processors can share, or independent

> [!info] Goal: equalize load across all cores
> While maximizing **locality**
>- E. Sleeping tasks will be put on a *single* core

1. When *idle*, steal other people's work
	- Locality: steal *close* cores
		- Hierarchical balancing
2. When *busy*, push tasks out for others

Maintain a load average and history to determine **stability**
Neighbor check
- Level in hierarchy: cost to migrate
- Make small changes by pulling from *other* CPU
	- Ensure upper hierarchies are balanced (less frequently checked)
- Load calculated by the **leftmost** node


## 4. EEVDF
> [!info] Earliest Eligible Virtual Deadline First

**Address** CFS issues:
- Lack of latency guarantee
- Sleeper fairness
- Too much heuristics/tuning

**Lag**: difference between idea and actual

Time slice = base time slice / weight
**Deadline** = vruntime + time slice **+ lag**


# HW 4
## Slab Allocator
- Free list: block of available, already allocated data structures (object cache)
	- Problem: no global control
Slab layer: generic data-structure caching layer
- Cache frequently used data structures
- One cache per object type
- `kmalloc()` built on top of it

States of slabs
- Full: all allocated
- Empty: none allocated
	- If no empty slab, one is created
- Partial: some allocated, satisfies kernel request first


# HW 5 Implementation of the Scheduler
> [!info] Overview
> - What task to run enxt
> - How  long does it have to run
> - Where should it run


> [!danger] Use Version 6.8!


## `schedule()` Function
> [!info] Every CPU calls `schedule()` individually
> - If too busy, try to redistribute tasks
> - A wrapper

`schedule()` function: perform context switch
1. Suspend current task
2. **Pick** a new task from runqueue based on scheduling policies
3. Resume new task
- No need for time slice, only consider **wait time** of a process
	- Waiting time sorted in a **red-black tree**
		- Increases when waiting
		- Decreases when running
	- **Virtual clock**: slower if more processes waiting (`fair_clock`)
	- Kernel sorts by `fair_clock - wait_runtime`
- When task running, its running interval subtracted from `wait_runtime`
	- Moved right to the tree
	- Anoth
## Data Structures
1. **Scheduling class**: decide which task runs next
	- Scheduling policies and classes (modular)
2. After selecting task, **context switch**
```c
struct task_struct { 
... 
	int prio, static_prio, normal_prio; 
	unsigned int rt_priority; 
	
	struct list_head run_list; 
	const struct sched_class *sched_class; 
	struct sched_entity se; 
	
	unsigned int policy; 
	cpumask_t cpus_allowed; 
	unsigned int time_slice; 
... 
}
```
- **Priority**

	- `static_prio`: static, assigned when **started**
		- Can only be modified by `nice` `sched_setscheduler`
	- `normal_prio`: dynamic computed from static and **scheduling policy**
		- Inherited with `fork()`
	- `prio` considered by the **scheduler**
		- When kernel needs to boost (very temporary change)
	- `rt_priority`: real time process
		- 0 lowest, 99 highest (differ from nice values)
- `sched_class`
	- Scheduler can also schedule **groups** (instance of `sched_entity`)
- Data
	- `policy`
		- `SCHED_NROMAL` handled by **completely fair** scheduler
		- `SCHED_BATCH`, `SCHED_IDLE`: completely fair, but less important
		- `SCHED_RR`, `SCHED_FIFO`: real-time scheduler class!
	- `run_list`: list head by RR scheduler
	- `time_slice`: remaining time quantum
### Scheduler
> [!info] Connect generic & individual scheduler
> Function pointers in special structure
> - Need to set a few function pointers

```c
struct sched_class { 
	const struct sched_class *next; 
	
	void (*enqueue_task) (struct rq *rq, struct task_struct *p, int wakeup); 
	void (*dequeue_task) (struct rq *rq, struct task_struct *p, int sleep); 
	void (*yield_task) (struct rq *rq); 
	
	void (*check_preempt_curr) (struct rq *rq, struct task_struct *p); 
	
	struct task_struct * (*pick_next_task) (struct rq *rq); 
	void (*put_prev_task) (struct rq *rq, struct task_struct *p);
	void (*set_curr_task) (struct rq *rq); 
	void (*task_tick) (struct rq *rq, struct task_struct *p); 
	void (*task_new) (struct rq *rq, struct task_struct *p); 
};
```
**Hierarchy**
1. Real-time processes
2. Completely fair
3. Idle task
- Connects `next` scheduling class in the hierarchy
	- `schedule()` searches from top to bottom
Operations:
- `enqueue_task()` adds a new process to RQ (sleeping -> runnable)
	- E. `fork()` a child past
- `deque_task()` (runnable -> unrunnable)
	- Or changed priority
	- E. reading from a slow hard drive
- `yield_task()` triggered by `sched_yield()` syscall from process
- `pick_next_task()` selects next `task_struct` supposed to run
	- **First** call `put_prev_task()` (take CPU away, clean up the previous process)
	- Context switch still required
- `task_tick()` called by [[#Periodic Scheduler]]
- `new_task()` sets up `fork()`

---
**Bouncers**:
- `select_task_rq`: select RQ for a task, called during wakeup on **multicore** systems
- `wakeup_preempt`: called immediately after a task is **woken up**
	- E. choose to kick low-priority off CPU for high-priority tasks
**Lifecycles**:
- `task_fork`: called when child created
	- Decides parent timeslice
- `task_dead()`: cleanup after termination
**Configurations**
- `switched_to`, `switch_from`: called when user changes policy
- `balance` called by idle CPU to steal tasks from another CPU
- `migrate_task_rq` called when moving tasks between CPU RQs
	- **Problem**: synchronization between CPUs. Need locking!
	- Need draw out life cycle, and **check for deadlock!**

### Example
Task `DB_QUERY` sleeping for a network packet
1. `select_task_rq`
2. `migrate_task_rq`
3. `enqueue_task` onto RQ
4. `check_wakeup_preempt`: is a task currently running? 
	- Is it more important than me? 
	- If not, kick it off (raise a reschedule flag)
5. `pcik_next_task`: `DB_QUERY`
6. `set_next_task`: update CPU register

If swapping CPUs:
7. `set_cpus_allowed`: sets the task to not allowed to run on current core
8. `put_prev_task`: cleanup
9. Now CPU idle, call `balance` for tasks
	- If so, pull tasks here
10. `context_switch`: actual hardware switch, move cur process to new CPU
11. `yield_task` or `dequeue_task` when giving up needed
12. `task_dead`: cleanup function
### Run Queue
> Per CPU. Each active process only on one run queue

```c
static DEFINE_PER_CPU_SHARED_ALIGNED(struct rq, runqueues);
struct rq { 
	unsigned long nr_running; 
	#define CPU_LOAD_IDX_MAX 5 
	unsigned long cpu_load[CPU_LOAD_IDX_MAX]; 
	
	struct load_weight load; 
	
	struct cfs_rq cfs; 
	struct rt_rq rt; 
	
	struct task_struct *curr, *idle
	; 
	u64 clock;
};
```
- `nr_running`: process number on the queue
- `cpu_load` tracks past load behavior
- `load` is a *measure* of current load on RQ (weighted)
- `cfs`, `rt`: sub RQ for fair and RT schduler
	- Holds the actual queue!
- `curr`: current running `task_struct`
- `idle`: `task_struct` called when no other runnable process is available
- `clock` updated each time periodic scheduler called
	- `update_rq_clock()`

Macros:
```c
#define cpu_rq(cpu)     (&per_cpu(runqueues, (cpu))) 
#define this_rq()       (&__get_cpu_var(runqueues)) 
#define task_rq(p)      cpu_rq(task_cpu(p)) 
#define cpu_curr(cpu)   (cpu_rq(cpu)->curr)
```

### Scheduling Entities
> Units more than task


## Priorities
### Kernel Representation
`nice` command, `[-20, +19]`, lower more priority
- Mapped to 100-139 in kernel
- 0-99 are reserved for real time processes
```c
#define MAX_USER_RT_PRIO 100 
#define MAX_RT_PRIO MAX_USER_RT_PRIO 
#define MAX_PRIO (MAX_RT_PRIO + 40) 
#define DEFAULT_PRIO (MAX_RT_PRIO + 20)
 
#define NICE_TO_PRIO(nice) (MAX_RT_PRIO + (nice) + 20) 
#define PRIO_TO_NICE(prio) ((prio) - MAX_RT_PRIO - 20) 
#define TASK_NICE(p) PRIO_TO_NICE((p)->static_prio)
```

### Computation
`prio`, `normla_prio`, `static_prio`

Dynamic `prio` is simply a **booster** if RT priority
- If not RT boost restore it to normal priority
- E. holding lock
```c
p->prio = efffective_prio(p);

static int effective_prio(struct task_struct *p) {
	p->normal_prio = normal_prio(p);
	if (!rt_prio(p->prio))
		return p->normal_prio;
	return p->prio;
}
```


```c
static inline int normal_prio(struct task_struct *p) {
	int prio; 
	if (task_has_rt_policy(p)) 
		prio = MAX_RT_PRIO-1 - p->rt_priority; 
	else 
		prio = __normal_prio(p); 
	return prio; 
}
static inline int __normal_prio(struct task_struct *p)
	return p->static_prio;
```
- For RT, since higher `rt_priority` is more important, need subtraction
- For regular, just return static priority
![[Pasted image 20260402141047.png]]
- `static_prio`: base priority, purely from nice values for normal tasks
- `normal_prio`: priority "entitled" based on *scheduling policy*
	- Same as `static_prio` for non-RT
	- Higher for RT tasks
- `prio`: **effective** priority, used by scheduler **right now**
	- Can be boosted
### Load Weights
```c
struct load_weight {
	unsigned long weight, inv_weight;    // inv for division
};
```
**Idea**: process one nice level down gets 10% more CPU power
- Kernel converts priority to weights
- Nice level -> priority -> weights (`prio_to_weight[40]`)
- `SCHED_IDLE` tasks will get a very small weight (like 2)


```c
static void set_load_weight(struct task_struct *p) { 
	// RT: global load balancing
	if (task_has_rt_policy(p)) { 
		p->se.load.weight = prio_to_weight[0] * 2; 
		p->se.load.inv_weight = prio_to_wmult[0] >> 1; 
		return; 
	} 
	if (p->policy == SCHED_IDLE) { 
		p->se.load.weight = WEIGHT_IDLEPRIO; 
		p->se.load.inv_weight = WMULT_IDLEPRIO; 
		return; 
	} 
	// load the acutal weight
	p->se.load.weight = prio_to_weight[p->static_prio - MAX_RT_PRIO]; 
	p->se.load.inv_weight = prio_to_wmult[p->static_prio - MAX_RT_PRIO]; 
}
```
- For RT tasks, fill a very high `prio_to_weight`
	- Not actually used, tells scheduler that this CPU is very busy
### Modify Weights
Modify `struct load_weight`
```c
static inline void update_load_add(struct load_weight *lw, unsigned long inc) 
	lw->weight += inc;
static inline void inc_load(struct rq *rq, const struct task_struct *p) 
	update_load_add(&rq->load, p->se.load.weight);
static void inc_nr_running(struct task_struct *p, struct rq *rq) 
	rq->nr_running++; inc_load(rq, p);
```
- Doesn't calculate `inv_weight` for simplicity (avoids division)
- Only `.weight` is needed for load balancing and calculating time slices
- `.invweight` used to calculate `vruntime`

## Core Scheduler
### Periodic Scheduler
Function called by the kernel with frequency `HZ`
**Tasks**
1. Manage kernel scheduling stats (incrementing counters)
2. Activate **periodic scheduling method** of the schedule class for the current process
```c
void scheduler_trick(void) {
	int cpu = smp_processor_id();
	struct rp *rq = cpu_rq(cpu);
	struct task_struct *curr = rq->curr;
	
	__update_rq_clock(rq)
	update_cpu_load(rq);
	
	if (curr != rq->idle)
		curr->sched_class->task_tick(rq, curr);
}
```
- `__update_rq_clock()` advances time stamp of current `struct rq`
	- Hardware clock interface
- `update_cpu_load()` updates `cpu_load[]` history (inserts at begin)

### Main Scheduler: `schedule()`


**Prefix** `__sched` to decorate function that can potentially call `schedule()`

1. Determine the current RQ and save the `task_struct *` of current active process to `prev`
	- If task yields, check if there are anything to run
	- If so, deactivate the task
```c
asmlinkage void __sched schedule(void) {
	sturct task_struct *prev, *next;
	struct rq *rq;
	int cpu;
need_resched:
	cpu = smp_processor_id();
	rq = cpu_rq(cpu);
	prev = rq->curr;}
```
2. Update RQ clock, clear the reschedule flag of the current running task
```c
	__update_rq_clock(rq);
	clear_tsk_need_resched(prev);
```
3. Delegate the work to the scheduling classes
	- If task trying to sleep, but willing to be woken up for a signal, makes it running
	- Else `deactivate_task()` calls `sched_class->deque_task()`, make it sleep
		- Calls `p->sched_class->dequeue_task(rq, p)`
		- I need to implement the `dequeue_task()`
			- Make sure it's done within a locked region
```c
	if ((prev->state & TASK_INTERRUPTIBLE) && signal_pending(prev))
		prev->state = TASK_RUNNING;
	else
		deactivate_task(rq, prev, 1);
```
4. `put_prev_task()` makes `sched_class` update stats, and pick next task
	- If nothing, runs the `idle` task (low power state)
```c
	prev->sched_class->put_prev_task(rq, prev);
	next = pick_next_task(rq, prev);
```
5. If an `pick_next_task()` selects a new task, `constxt_switch()` at hardware level
	- Architecture-specific
	- Save CPU registers and stack pointer, load next, change address space
```c
	if (prev != next) {
		rq->curr = next;
		// memory barrier here: make sure all previous operations complete
		context_switch(rq, prev, next);
	}
```
6. If no context switch is performed, execution resumes:
	- If `TIF_NEED_RESCHED`, scheduler has found a better candidate, go back
		- Executes when scheduler decides to stay with current task, or just switched back
		- "Exit gate" for the scheduling logic
```c
	if (test_thread_flag(TIF_NEED_RESCHED)) 
		goto need_resched;
```

### `fork()`


## HW Tips
> [!warning] Per-CPU kthreads: some tasks can only run on a **specified CPU**
> - May be **very bad!!**

Locking too!
## Debugging
> [!info] First make the number of CPUs to 1
> Then slowly add things, and slowly take debugging flags out
> - Check if locks grabbed? If locks not grabbed?

https://columbia-os.github.io/dev-guides/kernel-debugging.html
## KConfig
- `DEBUG_INFO`
- `KALLSYMS`
- `DEBUG_BUGVERBOSE`
- `PRINTK_CALLER`: for multithreaded debugging

### `printk()`
- Print `KERN_ERR` and `KERN_DEBUG`
- Seen by `sudo demsg`

**Serial Console**
- Redirect messages to a file on host machine via virtual serial port
- Need edit boot parameters

### dd
`kernel/sched/core.c`
```c
sched_init(void)
	BUG_ON
```
`BUG_ON` crashes earlier than `dmesg`
- Specify the assumptions (`assert`)
Also `panic()` function to print info, instead of `BUG_ON`

