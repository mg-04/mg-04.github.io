---
title: "OS Notes: Disk and IO"
permalink: /articles/os/4-io
---

{% include toc %}


# 18.1. IO
- Issue commands to device
- Catch *interrupts*
- Handle error
Diverse, portability, performance

## Category
- **Block Device**
	- Info stored in **fixed-size** blocks, with its own address
	- Transfer in one or more blocks
	- E. hard disk, CD ROM, USB
- **Character Device**
	- Info sent/received in **stream**
	- Not addressable
	- E. mice, printer, network interfaces

## Controller and Device
Device expose a finite set of **registers** to communicate with CPU
1. Command buffer for start/stop
2. Data buffer that can be read/written
	- E. address, size

## Communication Methods
### IO Port Space
Old interface, **two** address spaces
- IO port, number assigned
- Access with **privileged** instructions
	- `in portnum, target`
	- `out portnum, source`

### Memory-Mapped IO
Mapped to some unique **physical** offset
- Device listens (snoops) a physical range

**Advantages**
- Written in C
- No special protection
- Convenient memory interface

Communicate through `struct pci_config`
- Inspect with `lspci`

Need to **disable cache**!!!
- Through page table `cache_disabled` bit

## Interrupt
Raise interrupt when device finished work (or wants attention)
1. Interrupt controller issues interrupt
2. CPU **ack**s interrupt
### Messaged Signaled Interrupts
- Pin count restrictions
Write a small interrupt-describing data block describing data to a special `mmap()`ed IO address triggers interrupt
- Very programmable

### Precise Interrupts
Simple
- **PC** saved in known place
- All instructions before fully executed
- All instruction after not executed (or no side effects)
- Execution state of PC known
> What if OOO, many instructions *in-flight*? Which instruction gets interrupted??

## IO Software
- Error handling
	- Close to hardware as possible
- Sync vs asyn
- Buffering
- Sharable

## Performing IO
### Programmed IO
- CPU does all work
- Busy-waiting (pooling)

```c
copy_from_user(buffer, p, count);
for (i = 0; i < count; i++) {
	while (*printer_status_reg != READY) 
		;
	*print_data_register = p[i];
}
return_to_user();
```
- Waste CPU cycle

### Interrupt-Drive IO
Process blocked while waiting, another process scheduled
- When ready raises **interrupt**, then copies data

### Direct Memory Access (DMA)
Ask DMA controller to move data as a bulk
- Has access to system, but independent from CPU
- When DMA controller moves data, CPU can do something else
	- aka "copy core"
- Interrupt when done
![[Pasted image 20260406202800.png|566]]

**Memory Protection**
> Security concerns

Protection with another translation table: **IOMMU**
- Similar to page table protects via MMU
- If invalid address, exception raised

## Example Devices
### Clock
**HW**
Crystal oscillator + pulse counter + holding register
- Interrupt when counter becomes 0

**SW**
E. CPU stat, preemption, alarm call, system watchdog (deadlock detection)

When process `sleep(10)`, need to release this process from blocking state after 10 s
Create a **clock header** that wakes a sequence of events

### Network Driver
Receive: Network card need to maintain an ring buffer
- Throttle TCP/IP or device, when either side too frequent
- High degree of concurrency

# 18.2. Storage Devices
## HDD
- Cylinder and sector (512b each)
- RW head

New devices expose uniform Logical Block Address
- Disk controller translates LBA to CHS
- OS views as 1D array of sector groups (blocks)

**Sequential access** much faster than random

### Seek Performance
Move to specific track and keep it there
- Need more accurate for **write**, since errors are catastrophic
1. **Seeking** (track)
	- Critical for small loads
	- Should to be *optimized*, schedule requests to shorten seeks
		- Move some data to memory: file system caching
2. **Rotational delay** (sector)
	- Critical for sequential transfer
3. **Byte transfer**
	- Much wasted

## Disk Management
**Placement/ordering** requests
- Make as sequential as possible
- Group as long seeks
- Con: if **crash**, may leave in inconsistent state

**Considerations**
- Internal/external fragmentation
- File growth
- Sequential/random access time
- Metadata overhead

### 1. Contiguous Allocation
FS allocates space all at **once**
- Space managed by examining bitmap
- Metadata: base, size (simple)

**Pros**
- Easy, low overhead
- Fast *sequential* access
**Cons**
- External fragmentation
	- Can move around
- Hard to grow
### 2. Extent-Based Allocation
Multiple** contiguous regions for file (extent)
- ana. memory segmentation
- Metadata: *array* of (base, size)

### 3. Linked Allocation
Data block part of linked list
- Metadata for next pointer

**Pros**
- No external fragmentation
	- Similar to paging
- File can grow easily
- Easy to implement
**Cons**
- Slow sequential access
- Hard to compute random access
- Some overhead

The LL pointers can be stored in a dedicated **pointer table**
**Pros**
- Faster random access: FAT lookup
**Cons**
- Slow sequential
- Need recovery when crash
### 4. Indexed Allocation
**Metadata**: Array of **pointers** (index) to data blocks
- Blocks allocated on demand
- i-nodes

**Pros**
- No external fragmentation
- Easy growth
	- Multiple levels of indexing
- Fast random access
**Cons**
- Overhead: **index blocks**
- Slow sequential

## Scheduling Disk Requests
### 1. First Come First Served
Process on the order received
**Pros**
- Easy, fair
**Cons**
- No locality
- More average latency

### 2. Shortest Positioning Time First
Pick request with shortest seek time
- High locality, throughput
- Starvation
- Don't know which request fastest

### 3. Elevator
Sweep across disk, serving all requests passed
- SPTF, but only in one direction
- Switch direction only if no further requests

- Locality, bounded waiting


## SSD
### Organization
Page -> block -> plane (parallel access) -> die -> chip

**Functions
- Read
	- Very random! Less power, faster
- Erase
- Program
Write takes two steps


### Writing
Need to be done at **block** level
1. Backup
2. Erase
3. Change some pages in **memory**
4. Re-program from memory to SSD
Very expensive!
- May wear down cell!
- Will not write in place, due to wear balancing

## In-Memory Map
Keep memory map of logical -> physical page number
- On write, pick unused page, mark previous page free
- Repeated write will remap

**Metadata**
- Allocated
- Written
- Obsolete

100: after power failure, partially written state

Requires a lot of memory, wastes RAM in host
- Solution: store FTL map in flash itself!
**Problem**: write amplification
- Small writes to empty blocks will lead to intense fragmentation!
- Must periodically defragment

## Disk Scheduling
> No seek time for SSD

- **No op**: pass request directly to device
- **MQ-deadline**
- **Wear Level Focus**: coalesce write

## RAID
> [!info] Redundant Array of Independent Disks
> - Used as SLED (Single Large Expensive Disk) logically, but each block may parallel IO
###  Hard Drive Errors
- **Checksum error**
	- Transient
	- Permanent: catastrophic
- **Seek error**: aggressive overshoot
- **Programming error**: requesting nonexistent sector
- **Controller error**

### RAID Levels
- Level 0
	- **No** redundancy, just logical partition into **strips**
- Level 1
	- **Duplicate all data**
	- Double the cost :(
	- No write penalty (parallelized)
- Level 2
	- Data stripping (very small)
		- Parallel access
	- Use **Hamming code** for ECC ($\log(N)$)
		- Correct 1 bit, detect 2 bits
- Level 3
	- Similar to 2, but only **single** redundant disk
		- Independent of disk array size!
	- Parallel access
	- High data transfer rate, but only **one** IO at a time
- Level 4
	- Larger strips
	- Bit-by-bit parity strips, all stored in parity disk
	- Write penalty when IO
- Level 5
	- Level 4, but parity distributed across **all disks**
	- Loss of any one disk is fine
- Level 6
	- Two parity calculations, stored in separate blocks on different disks
	- Substantial write penalty
![[Pasted image 20260413210602.png]]

## Logical Volume Manager
> **Volume**: partition of hard drive

LVM allows combining physical partitions to **volume groups** logically
- IO requests directed to correct physical disk


# 19. Linux File System
## 1. Original UNIX
1. **Superblock**: sentinel (E. number of blocks, pointer to free list)
2. **Inode**: contiguous block, point to data
3. **Data**
**Problem**: slow
- Blocks too small
	- Index too large
	- Transfer rate low
- Poor clustering related objects
	- `ls` inefficient
	- Inode not local to each other

## Modern UNIX FS
> Multilevel indexed block allocation

- Designed with disk geometry (cylinder groups)

## BFS
Partition disk into multiple OSes, or multiple file systems
**Top level**
1. **Super block**: FS metadata
2. **Boot block**: place bootloader, for hardware
3. **Cylinder group partitions**: contain Inode and data blocks
	- Minimize disk seeks
Allocation goals
- Sequential blocks in adjacent sectors
- Inode the same cylinder group as file data
- Inodes in a directory in same cylinder group
**Cylinder group**
1. Metadata: super block/CG info
2. Inode bitmap
3. Block bitmap
4. Inodes (128 B each)
5. Data blocks (4 KB each)

Reserve scattered empty spaces for near allocations

### Inode
One Inode for one file, uniquely identified

**Directory**: also a file, with Inode and data blocks
- One dentry per file, with filename and Inode **pointer**

See via 
```sh
ls -i
```

Has direct data block pointers, single indirect, double indirect, ...

**Extent-based**: contiguous mapping of certain blocks on the physical disk

## Linking
## Static Linking
> aka hard link
```shell
ln orig_file new_file
ln -p orig_file new_file
```
- Two filenames pointing to the same I-node
File deleted only after all references deleted

### Symbolic Linking
Special file, data is the **name**/path to another file
- The name doesn't need to exist, since not pointing to I-node
- Symbolic link has its **own** I-node
- Extra overhead, since need to open twice
```shell
ln -s orig_file new_file
```

## Syscalls
Reading file
```c
struct stat *statbuf;     // modes, number of links, ID, ...
int stat(const char *pathname, struct stat *statbuf);
int fstat(int fd, struct stat *statbuf);
int lstat(const char *pathname, struct stat *statbuf);   // for ls
```

Reading directory
```c
struct *dirent;            // single entry information
DIR *opendir(const char *name);           // open directory, get opaque handler
struct dirent *readdir(DIR *dirp);
```

```c
DIR *dir;
struct dirent *entry;

dir = opendir("/");
while ((entry = readdir(dir)) != NULL))
	printf(" %s\n", entry->d_name);
closedir(dir);
```
For `ls -ls`, open file, and do `lstat` on that


## LFS: Log-structured FS
> Disk caching optimized, so most seeks are **writes**. LFS **optimizes writes**

**Buffer** writes within memory. Once full, write to a log (checkpoint)
- Segment write is sequential, **fast**
Read **still random**, but mostly handled by cache
- Problem: scatter I-nodes
- Need an **I-node map** pointing to I-nodes
- Map is cached, and has fixed disk location
Kernel runs a cleaner thread 
- Treat disk as a **circular buffer**
- If crash in-between, losing data
Avoid overhead
- Group old data in the same segment
- Avoid strict circular log, but a list of segments

### Segment
Inode interleaved with data
- Need store identity of I-node, block
## Crashes
Assume write happens atomically
- B: I-node bitmap update
- I: I-node added
- D: Dentry added to directory data block
### `fsck`: File System Consistency Check
Very long time
- Can't fix all senarios, such as `B'I D'`
### Block Consistency
- Consistent: either in free list or used list
- Missing block: add it back to free list
- Duplicate free blocks: fix free list
- Duplicate used blocks pointed by 2 I-nodes: make a copy
### Journaling
> Keep a log of my actions, before updating FS

If crash in the middle, **replay** the log
- Better than `fsck`
1. Commit dirty blocks to journal
2. Write commit
3. Write to actual disk
4. Free journal space

> Still expensive. Need **two** disk writes

- Data journaling: all writes, expensive
- Metadata journaling: only **metadata**
- Ordered journal: write file to FS first, then journal metadata
	- Possible inconsistency
## Virtual FS
> Various FS under UNIX

Interface: `open()`, `close()`, `read()`, etc. 
- Does not expose implementation details

### Creation
```sh
mkfs -t ext3 /dev/sda6
```
- Creates an `ext3` FS on partition `sda6`
- Will wipe out all existing data


### Mounting
```sh
mount -t type device directory
```
- Hard disk mounted to `/`
- Other FS (E. temp, network) ...

### Data Structures
`struct file`: instance of open file
- Per-process fdtable entry, allowing sharing by copying file pointer
- Flags, current position

`struct dentry`: hard link that contains link and inode number
- Break absolute path into dentries
- Expensive path resolution, need recursive find

`struct inode`
> [!info] HW7

`const struct inode_operations *i_op`
- Interface to read, write, seek, ...

`struct super_block`: descriptor of a *mounted* FS
- Journaling

Change scheduling algorithm for a particular disk device


### Special Purpose FS
- RamFS (built on RAM)

# HW6
## Device Drivers
> Interface between specific hardware from software

- Loaded through **Loadable Kernel Modules** (LKMs)
- Virtual files, can be interacted with syscalls `open()`, `read()`
	- Functions specified in `struct file_operations`
- **Device type** (from `stat <file>`): major and minor number

### E. `/dev/nullzero`
```c
static struct file_operations fops = { 
	.owner = THIS_MODULE, 
	.open = nullzero_open,
	.read = nullzero_read, 
	.write = nullzero_write, 
	.release = nullzero_release, // Called during `close()` 
	.unlocked_ioctl = nullzero_ioctl,   // called during ioctl()
};
```

```c
static int nullzero_open(struct inode *ino, struct file *fp) { return 0; }
static int nullzero_release(struct inode *ino, struct file *fp) { return 0; }
static ssize_t nullzero_read(struct file *fp, char __user *buf, 
	size_t len, loff_t *off); 
static ssize_t nullzero_write(struct file *fp, const char __user *buf, 
	size_t len, loff_t *off);
```

- `fp->private_data` is a generic `void *` to store **per-open** state information

### `ioctl()`
> **Syscall** whose behavior can be specified per device
> - Fall out of scope of `read()` and `write()`, for larger device control

```c
#define NULLZERO_IOC_SET_CHAR _IOW(NULLZERO_IOC_MAGIC, 1, char)
static long nullzero_ioctl(struct file *filep, 
						   unsigned int cmd, unsigned long arg) { 
	char new_c; 
	switch (cmd) { 
	case NULLZERO_IOC_SET_CHAR: 
		if (get_user(new_c, (char __user *)arg)) // Similar to `copy_from_user()` 
			return -EFAULT; 
		c = new_c; 
		break; 
	default: 
		return -ENOTTY; // "Not a typewriter"; for invalid `ioctl()` 
	} 
	return 0; 
}
```