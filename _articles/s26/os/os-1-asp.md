---
title: "OS Notes: ASP"
permalink: /articles/os/1-asp
---

{% include toc %}


# 1-2. Intro
- **Abstraction**
	- Manages and hides detail
- **Protection**
## Early OS
Just a **library** of standard features
- Assume one program at a time
- No malicious program
- Poor utilization (idle)
**Solution**: protection
- **Preemption**: reclaim CPU from a running process
	- Kernel regains control whenever interval timer fires
	- Supervisor mode
- **Access control**

## Preemption
```c
#include <sys/time.h>
#include <sys/stat.h>
#include <assert.h>

double GetTime() {
    struct timeval t;
    int rc = gettimeofday(&t, NULL);
    assert(rc == 0);
    return (double) t.tv_sec + (double) t.tv_usec/1e6;
}

void Spin(int howlong) {
    double t = GetTime();
    while ((GetTime() - t) < (double) howlong)
		; // do nothing in loop
}
```

```c
int main(int argc, char *argv[]) {
	char *str = argv[1];
	while (1) {
		Spin(1);
		printf("%s\n", str);
	}
}
```

## Protection
Can break the system with `fork()` bomb
- Limit number of processes/CPU
- Kill misbehaving programs

**Interposition**
- Check if accesses are legal

<div style="page-break-after: always;"></div>
## System Call
App invoke kernel, special HW instruction

File descriptors are **inherited** by child processes

## OS Structures
- **Monolithic**: app directly above OS
- **Microkernel**: app with **modular design**, called through system calls
	- Resilience to application bugs

### Memory
> If you can't name it, you can't touch it

Address translation (done in HW)
![[mem.png]]
### Advantages
- Kernel-only VA
	- Can't touched by apps
- Read-only VA
	- Sharing code pages (libraries)
	- Inter-process communication, memory mapping
- Disable execution
## System contexts
- User-level
- Kernel process context: syscall, exception handling
- Kernel code not associated with process: timer/device interrupt
- Context switch code: change the running process
- Idle

### Multitasking
Context switching is not always better, if a lot of memory required
- `strace` tells the traces of the **syscalls**


## Linked List
- Linear movement (not good at random access)
- Circular doubly linked

```c
#include <linux/list.h>

struct list_head {
	struct list_head *next；
	struct list_head *prev;
};

struct fox {
	// data
	struct list_head list;   // value, not pointer
};
```

Find the parent structure with only a pointer to its field (find `fox` from `list_head`)
```c
#define container_of(ptr, type, member) ({ const typeof( ((type *)0)->member ) *__mptr = (ptr);  (type *)( (char *)__mptr - offsetof(type,member) );})
```

```c
struct fox *red_fox;
red_fox = kmalloc(sizeof(*red_fox), GFP_KERNEL);
INIT_LIST_HEAD(&red_fox->list);

```

### List Head
Special head pointer

Created with macro:
```c
static LIST_HEAD(head);
```

### Manipulation
```c
#include <linux/list.h>
list_add(struct list_head *new, struct list_head *head);
// add immediately after head

list_add_tail(struct list_head *new, struct list_head *head);
// add immediately BEFORE head

list_del(struct list_head *entry);
// does not free any memory

list_del_init(struct list_head *entry);
// delete, then reinitialize
```

### Traversal
```c
list_for_each_entry(pos, head, member)
```
- `pos`: a temporary pointer for the iterated variable
- `head`: pointer to the `list_head` node
- `member`: variable name of `struct list_head` in `pos`

**Remove**
```c
list_for_each_entry_safe(pos, next, head, member)
```
- `next` used to store the **next** list entry, so it's safe to remove the current entry


# 3. Linux

1. Firmware code performs a power-on self test, pre-initializes hardware
2. Firmware checks Master Boot Record (MBR) of hard disks to identify a **bootable partition**
3. Bootloader in MBR reads configuration files, loads and launches the kernel from the disk
## Booting Linux
1. Kernel program starts
2. Hardware configures, including VA
3. Start process 0
	- Virtual task
4. Start scheduler
5. Process 0 `fork`s process 1 to run `kernel_init`
6. Process 0 becomes the idle task, calls schedule
7. Schedule context switches to other processes from `runqueue`
8. Process 1 will run and `execve` to "/init"
9. `init` is a regular program, such as `systemd`
10. At some point, we return to kernel again


## Processes
- If a process's parent dies before reaping the child, it becomes an **orphan**, get adopted by process `init`
- If child dies, before the parent reaps it, it's a **zombie** process
	- Becomes `<defunct>` in the process tree

## Signal
```c
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

static void sig_int(int signo)
    printf("stop pressing ctrl-c!\n");

int main()
{
    if (signal(SIGINT, &sig_int) == SIG_ERR) {
		perror("signal() failed");
		exit(1);
    }

    int i = 0;
    for (;;) {
		printf("%d\n", i++);
		sleep(1);
    }
}
```

## Kernel Modules
**Kernel Module** Interface to **dynamically** link object files into running kernel

### Create a Module
```c
#include <linux/module.h>
#include <linux/printk.h>

// called whem loaded
int hello(void) {
	printk(KERN_INFO "Hello\n");
	return 0;    // return an error code
}

// called when removed
void goodbye(void) {
	printk(KERN_INFO "Goodbye\n");
}

// register module entry and exit points
module_init(hello);
module_exit(goodbye);

// metadata
MODULE_DESCRIPTION("A basic Hello World module");
MODULE_AUTHOR("cs4118");
MODULE_LICENSE("GPL");
```

### Build a Module
```makefile
obj-m += hello.o
all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules
clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```
- `obj-m`: object files to be built for kernel
	- `obj-y`: object file to be linked to main kernel image (we're dynamically loading)
- `-C` changes the directory to `/lib/modules/$(shell uname -r)/build`
	- `$(shell uname -r)`: evaluate `uname -r` (kernel release) with `shell`
- The folder contains the **kernel** `Makefile`
- `M=$(PWD)` allows this `Makefile` to move to module source directory before trying to build `modules` or `clean`

### Load a Module
```shell
sudo su
insmod hello.ko
lsmod        # check mods installed
rmmod hello  # no need for .ko
```

Read the **kernel log buffer**:
```shell
dmesg

dmesg -c     # clean the buffer
dmesg -level=warn
```

### Fault
If a fault happens in your kernel module, kernel will jump to exception handlers
- Kernel provides **two levels** of fault handler.
- Beyond that, kernel crashes
- Due to limited hardware support


# 4.1 Signals
## Process Groups
> How to do other work while a process is running

```shell
proc1 | proc2 &   # send to bg
[1] 7106
proc3
```
- `7106` pid of the **last process**
- `jobs`: list all jobs
- `Ctrl-Z`: suspend foreground job and send to background
- `bg <jobs>`: resume `<job>` in bg
- `fg <jobs>`: bring from bg to fg

## Sending Signals
```c
#include <signal.h>
int kill(pid_t pid, int signo);
int raise(int signo)
```
- If `pid` < 0, signal is sent to process group with `pgid == -pid`
- If `pid` = -1, kills everything

To **foreground** process group
- `Ctrl-C` `SIGINT`
- `Ctrl-\` `SIGQUIT`
- `Ctrl-Z` `SIGTSTP`

```c
typedef void (*sighandler_t) (int);
sighandler_t signal(int signum, sighandler_t handler);
```
Handler can be `SIG_IGN` or `SIG_DFL`

## Issues
Slow system call (`read()`) will be **interrupted** by a signal
- Fix: check `EINTR` at `errno` and restart `read()`
```c
#include "apue.h"

static void	sig_alrm(int);

int main(void)
{
    int		n;
    char	line[MAXLINE];

    if (signal(SIGALRM, sig_alrm) == SIG_ERR)
		err_sys("signal(SIGALRM) error");

    alarm(10);
    if ((n = read(STDIN_FILENO, line, MAXLINE)) < 0)
		err_sys("read error");

    write(STDOUT_FILENO, line, n);
}

static void sig_alrm(int signo) {
    /* nothing to do, just return to interrupt the read */
}
```
**Lost signal**: disposition set with `signal()` is **reset** after each signal
- Fix: set disposition again after detecting the signal
	- Race condition: getting another signal before reset :(
Functions that use **static** data structures `malloc()`, `free()`, `printf()` are not **signal safe**
- Can't be called in **asynchronous** contexts
### Race Condition
```c
static void sig_alrm(int signo) { // sends -EINTR to pause()}

unsigned int sleep(unsigned int seconds) {
	signal(SIGALRM, sig_alrm);
	alarm(seconds); /* start the timer */
	pause(); /* next caught signal wakes us up */
	return alarm(0); /* turn off timer, return unslept time */
}
```
- Race condition before `pause()`
- Each alarm resets the handler
## `sigaction`
Stable handler
- See https://mg-04.github.io/articles/asp/4#portable-solution for detail


# 4.2 File IO
> [!info] Everything is a file in UNIX
> - Good with portability and **permissions**

```c
int open(const char *path int oflag, mode_t mode);
// need to specify mode if file is being created
```
- Creates an entry in the process's File Descriptor Table (FDT)
	- Offset
	- Options
	- Metadata
- Returns the **file descriptor**
```c
int close(int fildes)
```
- Deletes the file table entry
- If the process exits, memory leak, reclaimed by OS
	- Might lose data too
```c
off_t lseek(int fildes, off_t offset, int whence)
```
- `SEEK_SET`, `SEEK_CUR`, `SEEK_END`, plus `offset`
	- A hole in the file useful for storing sparse structures (physical < logical size)
- Returns the new position

```c
ssize_t read(int fildes, void *buf, size_t byte);
ssize_t write(int fildes, const void *buf, size_t nbyte);

// for sockets
ssize_t recv(int socket, void *buffer, size_t length, int flags);
ssize_t send(int sociket, const void *buffer, size_t length, int flags);
```
- Return number of bytes actually read/written, may be less than requested

### C `stdio`
Wrapped version in C `stdio` library
- Reduce the number of **system calls** while performing **stream** operations

```c
FILE *fopen(const char *pathname, const char *mode); // open()
int fclose(FILE *stream);  // close()
int fseek(FILE *stream, long offset, int whence);  // lseek()
size_t fread(void *ptr, size_t size, size_t nmemb, FILE *stream);  // read()
size_t fwrite(const void *ptr, size_t size, size_t nmemb, FILE *stream); 
```

## Kernel Data Structure

![[file.jpg]]
- File table entry may be **shared**
	- **Independent processes** have different process/file table entries, pointing to same v-nodes
- i-node specifies *how* files stored on disk
- v-node: API of i-node

### Process Relations
- If `fork()` before `open()`, `write()` will **overwrite** each other, since each process's file table stores its own **file offset**
- If `open()` before `fork()`, `write()` will **duplicate**, since offsets are updated across the same table.

### `dup()`
```c
int dup(int oldfd);
```
Duplicate the pointer to the **file table entry** and return the next available file descriptor


# 5.1 IPC
## Unnamed Pipe
> A kernel object, not copied over `fork()`

```c
#include <unistd.h>
int pipe(int fd[2]);
```
- `fd[0]` is opened for reading
- `fd[1]` is opened for writing
- Returns 0 if OK, 1 if error

If `fork()`ed, the parent and child will both take the type

Connect the input and output of two processes:
1. Parse `argv`
```c
int main(int argc, char **argv) {
    int fd[2];
    pid_t pid1, pid2;

    // Split arguments ["cmd1", ..., "--", "cmd2", ...] into
    //                 ["cmd1", ...] and ["cmd2", ...]
    char **argv1 = argv + 1; // argv for the first command
    char **argv2;            // argv for the second command

    for (argv2 = argv1; *argv2; argv2++) {
        if (strcmp(*argv2, "--") == 0) {
            *argv2++ = NULL;
            break;
        }
    }
```

2. Piping and `fork()`
```c
    pipe(fd);

    if ((pid1 = fork()) == 0) {
        close(fd[0]);   // Close read end of pipe
        dup2(fd[1], 1); // Redirect stdout to write end of pipe
        close(fd[1]);   // stdout already writes to pipe, close spare fd
        execvp(*argv1, argv1);
        // Unreachable
    }

    if ((pid2 = fork()) == 0) {
        close(fd[1]);   // Close write end of pipe
        dup2(fd[0], 0); // Redirect stdin from read end of pipe
        close(fd[0]);   // stdin already reads from pipe, close spare fd
        execvp(*argv2, argv2);
        // Unreachable
    }
```

3. Parent handling
```c
    // Parent does not need either end of the pipe
    close(fd[0]);
    close(fd[1]);

    waitpid(pid1, NULL, 0);
    waitpid(pid2, NULL, 0);
    return 0;
}
```
- Need error check

```shell
./connect2 ls -ls -- grep "connect"

ls -ls | grep "connect"
```

> [!warning] Pipe is a FIFO
> Data is not broadcasted, only consumed by one reader
> - Atomicity up to 4K

## Named Pipe
```c
#include <sys/stat.h>
int mkfifo(const char *path, mode_t mode);
```
- Creates a FIFO at `path`
- **Half-duplex**

## Unnamed Semaphore
- `sem_post()`: increment
- `sem_wait()`: wait until > 0, then decrement

### Usage
- Binary: lock
- Counting: resource sharing
- Ordering

```c
#include <semaphore.h>
int sem_init(sem_t *sem, int pshared, unsigned int value);
int sem_destroy(sem_t *sem);
```
- Need **shared memory** (`mmap()`)
- Or **named** semaphore

### Named Semaphore
Created under `/dev/shm`
```c
sem_t *sem_open(char *name, int oflag, ... /* mode_t mode, unsigned int value*/ );
int sem_close(sem_t *sem);
int sem_unlink(char *name);   // deletes from fs
```

### Modifying Semaphore
- `sem_trywait()` does not block
- `sem_wait()` blocks
- `sem_timedwait()` blocks either available, or timeout
	- Can't implement with `SIGALRM` due to race conditions

## Memory Mapped IO
Map **file** into address space
- **Private**: changes not flushed to disk or **other processes**
- **Shared**: other processes can see
- **Anonymous**: not backed by file (`fd=-1, flag=MAP_ANON`)
	- `malloc()`: actual allocation
	- `mmap()`: **reservation*** of address space, protection, share, **alignment**
- **Named**

```c
#include <sys/mman.h>
void *mmap(void *addr, size_t len, int prot, int flag, int fd, off_t off);
```
- `addr`: map target
	- If `NULL`, let OS decide
- `len`: size to allocate
- `prot`: read, write, exec
- `flag`
	- `MAP_PRIVATE`
	- `MAP_SHARED`
	- `MAP_ANON`
- `fd`: file we want to map
	- -1 for anonymous
- Returns pointer to the region 

## `counter.c`

Declare a counter with a semaphore lock
```c
#define LOOPS 2000

struct counter {
    sem_t sem;
    int cnt;
};

static struct counter *counter = NULL;

static void inc_loop() {
    for (int i = 0; i < LOOPS; i++) {
        sem_wait(&counter->sem);
        counter->cnt++;
        sem_post(&counter->sem);
    }
}
```

```c
int main(int argc, char **argv) {
    // Create a shared anonymous memory mapping, set global pointer to it
    counter = mmap(
	    /*addr=*/NULL, 
		sizeof(struct counter),
		PROT_READ | PROT_WRITE, // Region is readable and writable
		MAP_SHARED | MAP_ANON, // share with children
		/*fd=*/-1, 
		/*offset=*/0
    );

    // Mapping is already zero-initialized.
    assert(counter->cnt == 0);

    sem_init(&counter->sem, /*pshared=*/1, /*value=*/1);

    pid_t pid;
    if ((pid = fork()) == 0) {
        inc_loop();
        return 0;
    }

    inc_loop();
    waitpid(pid, NULL, 0);

    printf("Total count: %d, Expected: %d\n", counter->cnt, LOOPS * 2);

    sem_destroy(&counter->sem);
    assert(munmap(counter, sizeof(struct counter)) == 0);
    return 0;
}
```

# 5.2 Threads
Share virtual memory **and fd**
- Each thread has its own stack

```c
#include <pthread.h>
int pthread_create(pthread_t *thread, 
	                const pthread_attr_t *attr,
                    void *(*start_routine)(void *), 
                    void *arg); 
int pthread_join(pthread_t thread, void **retval);
```

## Mutex
```c
#include <pthread.h>
int pthread_mutex_init(pthread_mutex_t *mutex, pthread_mutexattr_t *attr);
int pthread_mutex_destroy(pthread_mutex_t *mutex);
int pthread_mutex_lock(pthread_mutex_t *mutex);
int pthread_mutex_trylock(pthread_mutex_t *mutex);  // nonblocking if fail
int pthread_mutex_unlock(pthread_mutex_t *mutex);
#include <time.h>
int pthread_mutex_timedlock(pthread_mutex_t *mutex, struct timespec *tsptr);
```

### Deadlock
- Lock same mutex **twice**
- Mutual lock of 2 mutexes
Need strict lock ordering

## Condition Variables
Signal
```c
#include <pthread.h>

int pthread_cond_init(pthread_cond_t *restrict cond,
                      const pthread_condattr_t *restrict attr);
int pthread_cond_destroy(pthread_cond_t *cond);

int pthread_cond_wait(pthread_cond_t *restrict cond,
                      pthread_mutex_t *restrict mutex);
int pthread_cond_timedwait(pthread_cond_t *restrict cond,
                           pthread_mutex_t *restrict mutex,
                           const struct timespec *restrict tsptr);

int pthread_cond_signal(pthread_cond_t *cond);
int pthread_cond_broadcast(pthread_cond_t *cond);
```

```c
#include <pthread.h>
struct msg {
    struct msg *m_next;
};

struct msg *workq;
pthread_cond_t qready = PTHREAD_COND_INITIALIZER;
pthread_mutex_t qlock = PTHREAD_MUTEX_INITIALIZER;
```

```c
void process_msg(void)
{
    struct msg *mp;

    for (;;) {
        pthread_mutex_lock(&qlock);

        while (workq == NULL)
            pthread_cond_wait(&qready, &qlock);
        
        mp = workq;
        workq = mp->m_next;
        
        pthread_mutex_unlock(&qlock);
    }
}

void enqueue_msg(struct msg *mp)
{
    pthread_mutex_lock(&qlock);
    
    mp->m_next = workq;
    workq = mp;
    
    pthread_cond_signal(&qready);
    pthread_mutex_unlock(&qlock);
}
```

## Other Mechanisms
- Spinlock (used a lot in the kernel, for small hold time)
- Barriers

# 6 Advanced IO
> [!info] Skim this

Nonblocking IO: `io_uring`: avoid polling the kernel through system calls
![[io_ring.png]]

## IO Multiplexing
E. network
- Nonblocking reads alternating
- IO kernel multiplexing
## `select()`
From a fd **set**
```c
#include <sys/select.h>
int select(int maxfdp1, // max fd plus 1, or simply FD_SETSIZE
    /* main params */
    fd_set *readfds,   // see if they're ready for reading
    fd_set *writefds,  // see if they're ready for writing
    fd_set *exceptfds, // see if exceptional condition

    struct timeval *tvptr); // timeout
    
void FD_ZERO(fd_set *fdset);          // initialize fdset
void FD_SET(int fd, fd_set *fdset);   // adds fd to fdset
void FD_CLR(int fd, fd_set *fdset);   // removes fd from fdset
int FD_ISSET(int fd, fd_set *fdset);  // tests if fd is in fdset
    
```
Inefficient
## `poll()`
Modern version, only gives user **one descriptor**
```c
#include <sys/select.h>
struct pollfd {
	int fd;             // fd assigned to fds monitor
	short events;       // POLLIN for read, POLLOUT for write
	short reevents;     // events that actually occur
};

int poll(struct pullfd fds[],
		nfds_t nfds,  // number of fds to monitor
		int timeout);
```

## `epoll()`
Edge-triggered API

## Domain Sockets
- Threads: shared
- Related processes: anonymous `mmap()`
- Unrelated processes: file-backed `mmap()`

To pass data:
- **Related** process: unnamed `pipe()` (half-duplex)
- **Unrelated** process: named `mkfifo()` (half-duplex)
- **Distant** process
	- TCP/UDP sockets (full duplex)
### Unix Domain Sockets
- **Unnamed**: `socketpair(AF_UNIX, ...);`
	- Duplex pipe
- **Named**: `socket(AF_UNIX, ...);`
	- Special file
Can transport **open fd**
- Pass the i-node information

```c
int socketpair(int domain, int type, int protocol, int sv[2]);
```
- Socket "buffers" the data from fd

`recv-unix.c`
```c
int main(int argc, char **argv)
{
    const char *name = argv[1];
    int num_to_recv = atoi(argv[2]);

    struct sockaddr_un un;

    int fd, len;

    // create a UNIX domain datagram socket
    fd = socket(AF_UNIX, SOCK_DGRAM, 0);

    // remove the socket file if exists already
    unlink(name);

    // fill in the socket address structure
    memset(&un, 0, sizeof(un));
    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, name);
    len = offsetof(struct sockaddr_un, sun_path) + strlen(name);

    // bind the name to the descriptor
    if (bind(fd, (struct sockaddr *)&un, len) < 0) 
        die("bind failed");

    char buf[num_to_recv + 1];

    for (;;) {
        memset(buf, 0, sizeof(buf));
        int n = recv(fd, buf, num_to_recv, 0);
        else
            printf("%d bytes received: \"%s\"\n", n, buf);
    }

    close(fd);
    unlink(name);
    return 0;
}
```

`send-unix.c`
```c
int main(int argc, char **argv)
{
    const char *name = argv[1];
    const char *msg = argv[2];
    int num_repeat = atoi(argv[3]);

    struct sockaddr_un	un;

    int fd, len, i;

    // create a UNIX domain datagram socket
    fd = socket(AF_UNIX, SOCK_DGRAM, 0);

    // fill in the socket address structure with server's address
    memset(&un, 0, sizeof(un));
    un.sun_family = AF_UNIX;
    strcpy(un.sun_path, name);
    len = offsetof(struct sockaddr_un, sun_path) + strlen(name);

    for (i = 0; i < num_repeat; i++) {
        int n = sendto(fd, msg, strlen(msg), 0, (struct sockaddr *)&un, len);
        printf("sent %d bytes\n", n);
    }

    close(fd);
    return 0;
```

```shell
./recv-unix filename 1000
./send-unix filename hello 100 
```


# 7. System Calls
## Address Space
Virtually addressed
- The moment you touch something, you will get a backing in physical memory

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define BLKSZ (1<<22)   //  4MB

void wait4input(const char* msg) { puts(msg); getchar(); }

int main() {
	char* arr;
    int i,j;

    printf("mypid=%d\n",getpid());
    wait4input("before big loop");

    for (i=0;i<1000;i++) {
        //wait4input("before malloc");
        arr = malloc( BLKSZ );

        for (j=0;j<BLKSZ;j++)
            arr[j] = '1';
	}
    wait4input("done");
	return 0;
}
```

Go to the process filesystem
```shell
cd /proc/2265
cat maps           # shows entire addresss space
```
Get a block on the heap
Modern allocators use `mmap()` instead of repeatedly calling `brk()`
- Ideally, will get a contiguous region
- `mmap()` more flexible, `brk()` forces a contiguous region

## Interrupts
- **Hardware**
	- Async (network, timer)
- **Exceptions**
	- Synchronous
	- Division by 0, page fault
- **Software**
	- Synchronous
	- syscall, x86 assembly interrupt, **debugger**

On a `read()` call,
```asm
movl __NR_READ, %eax
int 0x80
ret
```
Now enter **kernel mode**
1. Kernel looks `0x80` in **Interrupt Descriptor Table** -> `system_call`
2. Jump to `system_call(registers)`, which access the `system_call_table[%eax]`
3. `system_call_table`is read at `__NR_READ` -> `sys_read`
4. Jumps to `sys_read()`, and do the real read

## Parameters
Passed via **registers**. If larger, use a `struct` pointer (E. `struct sigaction`)

**Convention** for function calls (typical):
- Arguments passed through registers
	- Sometimes as stack offsets
	- Volatile: may be changed on return
	- Non-volatile: must be saved and restored by callee
- Encoded in Application Binary Interface (ABI)

Need to validate buffer, need to check boundary and permissions, to avoid writing to kernel memory, since will enter kernel mode

## Kernel Actions
Need to enter and return kernel mode, branch to the position of `sys_read()` function in the kernel
![[syscall.png]]
## HW3
### System Calls
```c
asmlinkage long sys_getpid(getpid)    // maxro SYSCALL_DEFINE0(getpid)
{ 
	return task_tgid_vnr(current); // returns current->tgid, long
}
```

- `asmlinkage` tell compiler to look only on the stack for arguments
	- Required for any syscalls
- Return `long` in kernel and `int` in user space
- `sys_*` naming convention
### Syscall number
Can't be reused
All registered syscalls in `sys_call_table`

### Implementation
- Verify parameters
	- Pointers
	- `copy_to_user(dst, src, size)` writes into user space
	- `copy_from_user()` reads from user space
		- Return num bytes **failed** to copy on error

```c
SYSCALL_DEFINE3(silly_copy, 
				unsigned long *, src, unsigned long *, dst, unsigned long len)
{
	unsigned long buf;
	if (copy_from_user(&buf, src, len)) 
		return -EFAULT; 
	if (copy_to_user(dst, &buf, len)) 
		return -EFAULT; 
	return len; 
}
```

- Check capability

```c
SYSCALL_DEFINE4(reboot,
				int, magic1, int, magic2, unsigned int, cmd, void __user *, arg)
{
	if (!capable(CAP_SYS_BOOT))
		return -EPERM;
		
	// ...
}
```
### Context
Kernel in **process** context during syscall execution, 
- `current` pointer points to current task
- Can sleep (E. blocking call), preemptible

### Registration
1. Add entry to the **end** of syscall table
	- For each architecture
2. Define syscall number in `<asm/unistd.h>`
3. Compile into **kernel image**

## Kernel Modules
**Exported symbols** are visible to any *loadable module*
- Dynamically linked to the kernel

```c
 #include <linux/module.h>  
 #include <linux/init.h>  
 #include <linux/kernel.h>  
  
static int rday_1 = 1;  
int rday_2 = 2;  
int rday_3 = 3;  
EXPORT_SYMBOL(rday_3);  

static int __init hi(void) {
	 printk(KERN_INFO "module m2 being loaded.n");  
	 return 0;  
}  
  
static void __exit bye(void)  
	printk(KERN_INFO "module m2 being unloaded.n");  
  
module_init(hi);  
module_exit(bye);
```
- `rday_1` does not show in symtab, not show up in kernel space
- `rday_2` and `rday_3` flagged as global data objects
- `rday_3` has an entry in the module string table and symbol table, in `ksymtab` and `kstrtab`

Need to fix syscall table and `syscalls.h`

# 8. Run/Wait Queues
Test code that times `gettimeofday()` calls
- Inconsistent results
- Due to scheduling and interrupts
If test library calls to syscall, **much slower**
- User library reads from kernel directly, avoiding the actual `syscall()` trap overhead
Same for opening a file

## Process States
In Linux, task can be a process/thread
```c
#define TASK_RUNNING          0x0000
#define TASK_INTERRUPTIBLE    0x0001
#define TASK_UNINTERRUPTIBLE  0x0002
```
- Running: runn**able** (running, or waiting to run)
- Interruptible: **sleep waiting** for something, can be awakened if a signal received
- Uninterruptible: also sleep waiting, but **can't** be awakened

## Run Queue
A linked list of `task_struct` via `children` and `sibling`

Each CPU has a `run_queue`, links tasks with `TASK_RUNNING` state
- With a separate `list_head`, and its own **disjoint** run queue

![[run_queue.png]]

## Wait Queue
Not embedded in `task_struct`
- In fact, a parent of `task_struct`
- Since don't know which element to wake up
![[wait_queue.png]]

### Data Structure
```c
struct wait_queue_head {
	spin_lock_t lock;
	struct list_head task_list;
};

struct waitqueue {
	struct task_struct *task;
	wait_queue_func_t func;         // callback function for wait condition
	struct list_head entry;
}
```

### Interface
```c
#include <linux/wait.h>
wait_event_interruptible()
// a bit outdated, doens't account for synchronization
```
Functions:
1. `prepare_to_wait()`: add to wait queue, change state to `TASK_INTERRUPTIBLE`
2. `signal_pending()`: check for signals that interrupt wakeup, if so, break
3. `schedule()`: save state and sleep
4. `finish_wait()`: change state to `TASK_RUNNING`, remove from wait queue

## Scheduling
- `pick_next_task()`: choose a new task from run queue
- `context_switch()`: put current task to sleep, and start running new task

### Sleeping
1. `wait_event()`: issue a wait object
2. Enqueue on wait queue
3. Remove from run queue
4. `schedule()`
	1. `pick_next_task()`
	2. `context_switch()`
5. Run other tasks

### Waking Up
1. When event happens, `wake_up()`
2. Call `try_to_wake_up()` on **each** task
3. Enqueue those on run queue
4. Wait for other task to call `schedule()`. Choose a sleeping task
5. Sleeping task checks condition again. If true, `finish_wake()`
Never go back directly to running on CPU
### States
- **Running on CPU**
	- To sleep, 
![[switch_fsm.png]]

### E. `read()`
1. Trap into kernel
	- Save registers into kernel stack
	- Device driver issues IO request to device
2. Put calling process to *sleep*
	- Another process starts running
3. Device receives input, raise a **hardware interrupt**
	- Trap into kernel again, **enqueue** the next process
4. Current ask eventually calls `schedule()`
	- Another process on the **run** queue starts running

## Context Switch
(easier in ARM)
Current task blocks **OR** preemption via interrupt
**TODO**
- Release CPU registers (written in assembly)
### Preemption
If a process does not give up the CPU
- Use external timer to interrupt
![[force_switch.png]]


# 9. Interrupts
## Interrupt Contexts
Limitations: **can't sleep**
- No associated task running, can't interact with wait queue and `schedule()`
- Don't know when can wake up
- `kmalloc()`, `copy_to_user()` may trigger IO, **can't** be called from interrupt context
All handlers share **one interrupt stack** per processor

## Handling
> Idea: Defer most work for later, only time-critical ones

1. **Top half** (first level)
	- ACK the interrupt
	- Fast, to make CPU get back to work
2. **Bottom Half** (second level)
	- Bulk process when CPU idle (E. large file received over network)
	- Kernel tasklet, threads
- Single interrupts will **not nest**, no need to be reentrant
	- Can be interrupted by another *type* of interrupt

> [!info] E. network package arrival
> - **Top half**: ACK arrival, move from NIC to memory, prepare for future packets
> - **Bottom half**: propagate through networking stack (TCP/IP), can be deferred

## Sync
All concurrent data must be protected
### Mutex (Sleeping)
```c
pthread_mutex_locK(&balance_lock);
++balance;
pthread_mutex_unlock(&balance_lock);
```
Calling task **put to sleep** while waiting for lock

> [!warning] Is sleeping always a good idea?
> - **Bad**: sleep overhead

### Spin Lock
> [!warning] No preemption
> Interrupt still normal, but the task can't be rescheduled
> - With `preempt_count`, only sleepable when 0

```c
int flag = 0;

lock() {
	while (flag == 0) {; }
	flag = 1;
}

unlock() {
	flag = 0;
}
```

**Issues**
- Multithread **race condition**. Need atomic
- Waste CPU cycles
Both threads assume ownership:
![[Pasted image 20260224194546.png]]

Need **atomic instruction** `test_and_set(&flag)`

**Hardware** pseudocode:
```c
int test_and_set(int *lock) {
	 int old = *lock;
	 *lock = 1;
	 return old;
}
```
### Linux Kernel
`spin_lock()` and `spin_unlock()`
- Want keep critical sections **small**
- Must not lose CPU while holding lock
- Must not call any function that may **sleep**
	- E. `kmalloc()`, `copy_from_user()`
- **Prevents kernel preemption** 
	- `++preempt_count`
- OK for hardware interrupt, unless handler also tries to lock
	- Deadlock
- Used by process context or a **single interrupt**

> IRQ: **interrupt request**

`spin_lock_irqsave()`, `spin_lock_irqrestore()`
- Lock a shared resource that may be used by **interrupt handler**
- Saves current **interrupt state**, then **disable** all interrupts on local CPU
	- Restored later
- Used by process and interrupt contexts; or more than 1 interrupts

`spin_lock_irq()`, `spin_unlock_irq()`


## Preemption
Kernel forcefully reclaim CPU
- Track a per-process `TIF_NEED_RESCHED` flag
- `preempt_count` tracks how many atomic states CPU entered. Can't preempt if nonzero
- If set, preemption by calling `schecule()` when:
	1. Return to user space (from syscall or interrupt handler)
	2. Return to kernel from interrupt handler, only if `preempt_count` is zero
	3. `preempt_count = 0`, (E. right after releasing lock)
	4. Task in **kernel mode** calls `schedule()` itself (E. blocking syscall)

# 10. Synchronization
- **Safety**: Mutex
- **Liveliness** (progress): 
	- must allow **one** to proceed; 
	- must not depend on threads out of critical section
- **Bounded waiting**
- No assumptions on speed and CPU count

## 1. Disable Interrupts
```c
lock() { disable_interrupt(); }
unlock() {enable_interrupt(); }
```
**Bad**:
- Privileged operations, user program can't use
- Can't work on **multiprocessors** (`*_interrupt()` only applies for current CPU)
- Can't have long critical sections
## 2. Software Spin Lock
**Peterson's algorithm**
Assume:
- Load and store are **atomic**
- **In-order** execution

```c
int flag[2] = {0, 0};
lock() {
	flag[self] = 1;
	while (flag[1 - self] == 1)
		;
}
unlock()
	flag[self] = 0;
```
**Not live**: can deadlock, race condition

```c
int turn = 0;
lock() {
	while (turn == 1 - self)
		;
}
unlock()
	turn = 1 - self;
```
**Not live**: Can't enter twice in a row

### Peterson
```c
int turn = 0;
int flag[2] = {0, 0};

lock() {
	flag[self] = 1;    // I need lock
	turn = 1 - self;   // I take the turn
	while (flag[1-self] == 1 && turn == 1 - self)
		;
}

unlock()
	flag[self] = 0;
```
Spin while
- Other thread needs lock, **AND**
- It's other thread's turn
`turn` acts as **tie-breaker** to prevent deadlock when both threads are "polite"
- The last thread to write `turn` yields to the other

> [!warning] Bad if reordered
> Memory access (load `flag[1-self]`) will typically be reordered up

## 3. Hardware Spin Lock
### Fence
Ensure all **memory operations** are in-order before processing
- expensive

- `mfence`: all memory
- `lfence`: all loads
- `sfence`: all stores
```c
lock() {
	flag[self] = 1;
	sfence;
	while (flag[1-self] == 1 && turn = 1-self)
		;
}
```

### Atomic TS
x86
Use `xchgl` to **atomically swap** two locations
```c
long test_and_set(volatile long *lock) {
	int old;
	asm("xchgl %0 %1"
		: "=r"(old), "+m"(*lock)    // output
		: "0"(1)                    // input
		: "memory"                  // clobber
		);
	return old;
}
```
- `"=r"(old)` write to (general purpose) register `old`
	- After the swap
- `"+m"(*lock)` read and write to memory `*lock`
- `"0"(1)` initializes `old` to 1
	- Put 1 into operand `0` (`old`, will be returned)
- `"memory"` avoids compiler optimization on memory

## 4. Sleep Lock
```c
lock() {
	while (test_and_set(&flag))) {
		add_wait_queue();
		schedule();
	}
	// do critical section
}

unlock() {
	flag = 0;
	if (/* thread in wait queue */)
		// wake up one thread
}
```
**Issues**
- Lost wakeup
	- After calling TS, **before** adding to wait queue; other thread unlocks
- Wrong thread gets lock
	- Newer threads may steal the lock
	- Fix: make `unlock()` directly transfer to waiting thread

Fix by adding a `guard` lock to avoid losing wakeups
- `prepared_to_yield()` to protect the gap between `guard = 0` and `yield()`
```c
typedef struct mutex_t {
	int flag;
	int guard;
	queue_t *q;
};

void lock(mutex_t *m) {
	while (test_and_set(m->guard))   // begin protected
		;
	if (m->flag == 0) {              // mutex available
		m->flag = 1;
		m->guard = 0;
	} else {                         // unavailable, sleep again
		enqueue(m->q, self);
		prepare_to_yield();          // prepare to yield
		m->guard = 0;                // end protected
		yield();
	}	
}

void unlock(mutex_t *m) {
	while(test_and_set(m->guard))    // begin protected
		;
	if (queue_empty(m->q))
		m->flag = 0;
	else                             // transfer to next thread DIRECTLY
		wakeup(dequeue(m->q));
	m->guard = 0;                    // end protected
}
```

## RW Lock
- **Read lock** (shared): multiple may hold
- **Write lock** (exclusive): only one can hold
```c
struct rwlock_t {
	int nreader;
	lock_t guard;
	lock_t lock;
};

write_lock(rwlock_t *l)
	lock(&l->lock);

write_unlock(rwlock_t *l)
	unlock(&l->lock);
	
read_lock(rwlock_t *l) {
	lock(&l->guard);
	++nreader;
	if (nreader == 1)         // first reader
		lock(&l->lock);
	unlock(&l->guard);
}

read_unlock(rwlock_t *l) {
	lock(&l->guard);
	--nreader
	if (nreader == 0);
		unlock(&l->lock);
	unlock(&l->guard);
}
```
> [!warning] Writer will be starved
> Need to kick readers out for write requests

### Anti-Starve
Use a `writer` lock, so when writer is waiting for the actual `lock`, no new readers can add themselves
- Existing readers will drain and release `lock`
```c
struct rwlock_t {
	int nreader;
	lock_t guard;
	lock_t lock;
	lock_t writer;
};

write_lock(rwlock_t *l) {
	lock(&l->writer);
	lock(&l->lock);
	unlock(&l->writer);
}

read_lock(rwlock_t *l) {
	lock(&l->writer);
	lock(&l->guard);
	++nreader;
	if (nreader == 1)         // first reader
		lock(&l->lock);
	unlock(&l->guard);
	unlock(&l->writer);
}
```

## Semaphore
> Now kernel context
```cpp
class Semaphore {
	int lockvar;       // atomicity
	int value;
	Queue<Thread*> waitQ;
	
	void Init(int v);
	void P();   // down
	void V();   // up
}

void Semaphore::Init(int v) {
	value = v;
	waitQ.init();
}
```

If run out of resources, add yourself to wait queue
- Must be **atomic**
- First line **disable interrupts**
- Last line **enable interrupts**
- Spin lock, since critical
```cpp
void Semaphore::P() {
	lock(&lockvar);
	
	value--;
	if (value < 0) {
		waitQ.add(current_thread);
		current_thread->status = blocked
		unlock(&lockvar);
		schedule();
	} else
		unlock(&lockvar);
}
```

```cpp
void Semaphore::V() {
	lock(&lockvar);
	
	value++;
	if (value <= 0) {
		Thread *thd = waitQ.getNextThread();
		scheduler->addd(thd);
	}
	
	unlock(&lockvar);
}
```

### E. Producer-Consumer
E. Linux pipe
- Block producer when buffer full
- Block consumer if no data

Ring buffer;
```c
Semaphore empty = N;
Semaphore full = 0;
Mutex mutex = 1;

T buffer[N];
int widx = 0, ridx = 0

Producer (T item) {
	P(&empty);
	P(&mutex);
	
	buffer[widx] = item;
	widx = (widx+1) % N;
	
	V(&mutex);
	V(&full);
}

// same for consumer, P(full); V(empty)
```
- If move buffer R/W outside of `mutex`, won't work

### Barrier
Coordinate multiple threads to **all** reach a specific point before allowed to continue
- **Rendezvous**: waiting point
- **Critical point**: no thread allowed to execute until everyone reach Rendezvous
```c
rendezous:
	sem_wait(mutex);
		count++;
		if (count == n)
			sem_post(barrier);
	sem_post(mutex);

	sem_wait(barrier);
	sem_post(barrier);           // reusable barrier, wakes up the next thread

critical_point:
	sem_wait(mutex);               
		count--;
		if (count == 0) 
			sem_wait(barrier);       // comsumes the final post left floating
	sem_post(mutex);
```

Can use interlocking `barrier2` with `barrier` for `critical_points` in a loop


## RCU
Lock-free Synchronization

RW lock very **slow**
- Writes not happen often
- Doesn't scale with large number of CPUs
**Read-Copy-Update**
- Multiple readers **and** one writer and run simultaneously
- Reader may read **old**, but consistent data

For reading, make a **copy** of the shared resource

For writing, (locked) allocate a **new** resource, and shared the pointer to it 

```c
struct foo {
    int a;
    int b;
} *global_foo;

// global_foo initialized elsewhere
DEFINE_SPINLOCK(foo_lock);
```

```c
void get(int *p, int *q) {
    struct foo *copy_foo;

    // 1) begin reading (no lock)
    rcu_read_lock();

    // 2) copy pointer once
    copy_foo = rcu_dereference(global_foo);

    // 3) access data using copy_foo
    *p = copy_foo->a;
    *q = copy_foo->b;

    // 4) end reading (no unlock)
    rcu_read_unlock();
}
```
- `rcu_dereference` grabs the pointer
	- Includes memory barrier

```c
void set(int x, int y) {
    struct foo *new_foo = kmalloc(...);
    struct foo *old_foo;

    // 1) synchronize multiple writers
    spin_lock(&foo_lock);

    // 2) copy old pointer once
    old_foo = rcu_dereference_protected(
        global_foo, lockdep_is_held(&foo_lock));

    // 3) update data
    new_foo->a = old_foo->a + x;
    new_foo->b = old_foo->b + y;

    // 4) switch pointer
    rcu_assign_pointer(global_foo, new_foo);

    spin_unlock(&foo_lock);

    // 5) wait a for old readers to finish
    synchronize_rcu();

    // 6) free old struct
    kfree(old_foo);
}
```
- `synchronize_rcu()`: tells writer to wait until every single active reader has finished
	- safe to `kfree()` after
> [!info] In Linux Kernel
> Implemented as a compiler optimization to reorder the critical sections properly
## Summary
- **Spinlocks:** Small, fast, non-sleeping locks used when holding time is short, such as in interrupt handlers.
- **Mutexes:** Sleeping locks for mutual exclusion, offering better performance for longer critical sections where sleeping is allowed.
- **Semaphores:** Traditional locks that can allow multiple holders, used for complex synchronization.
- **Read/Write Locks (rwlock / rwsem):** Allow multiple simultaneous readers but only one exclusive writer.
- **Read-Copy-Update (RCU):** A mechanism for high-read-frequency scenarios, allowing readers to run without locks.
### Contention
Failed lock acquire
Function of 
- Frequency of attempts
- Lock hold time
- Number of threads
### Monitor
Object with a set of **monitor procedures**
- One one **active thread** at a time
- Java `synchronized`
	- 1 Mutex + N condition variables in a class object

# Midterm Recitation
## Concurrency
- Rule: All need to **respect** the lock
- Risk: deadlock
	- `lock(A); lock(A);`
	- Interleaved locks of `A`, `B`
> [!warning] 
 Prioritize HW, lectures, lecture code examples
