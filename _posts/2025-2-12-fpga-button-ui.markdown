---
#layout: post
title:  "FPGA Button UI"
date:   2025-2-12 22:45:30 -0500
permalink: /posts/2025/02/lab1
tags:
    - cs
    - ee
excerpt: >
 Embedded lab 1: code an FPGA to test the Collatz Conjecture over a range of numbers... with a user interface of buttons and switches
---
Embedded lab 1: code an FPGA to test the Collatz Conjecture over a range of numbers... with a user interface of buttons and switches

The computing part was simple. With the skeleton code and test cases, it can be done in around 5 hours for a first-time Verilog user like me.

Unfortunately, the UI part is not well-defined, and I have to deal with all the *physical* hassles

> Make it so that the rightmost buttons, key[0] and key[1] increment and decrement the
value of 𝑛 being displayed. Make it so holding them makes the value change about 5 times a
second, e.g., by using a 22-bit counter running off the 50 MHz clock and only changing the
value when this counter wraps around. The lowest 𝑛 should always be set by the switches;

# Hardware specs
- For simplicity only focus on one button: `KEY[0]`, that increments `n` appropriately when pressed.
- Switches are **active low**, so `~KEY[0]` indicates a press
- The clock operates at 50 MHz, so we don't want an increment for every clock edge. There must be some "slower" clock or counter.

## Long press
Long press mode alone is simple: have an internal clock counter that operates at about 5 Hz. Only increment when counter hits 0
```verilog
logic [22:0]         counter;    // 23-bit counter

always_ff @(posedge clk) begin
    counter <= (counter == 23'h7fffff) ? (23'h0) : (counter + 23'h1);
    if (counter == 0) 
        if (~KEY[0])
		    n <= n + 1;
end
```
The result is about 6 Hz (0.16 s).

## Short press
When thinking of implementing both long and short presses, I though of a state machine.

**States:** off, short, long

**Inputs:** `key[0]`, counter
- `off`: after button press --> `short`
- `short`
	- When button released --> `off`
	- When button holds and `counter == 0` --> long; increment
- `long`
	- Increment every time `counter == 0`
	- When button released --> `off`

Seems like `short` and `long` can be merged for now, but we'll need them for later cases.

```verilog
logic [22:0] counter; 
enum logic [1:0] {off, short, long, unused} state;

always_ff @(posedge clk) begin
    counter <= (counter == 23'h7fffff) ? (23'h0) : (counter + 23'h1);

	case (state)
		off:	
			if (~KEY[0]) 	state <= short;

		short:
			if (KEY[0]) begin		// short press and release
				n <= n + 12'b1;  	// increment and reset
				state <= off;
			end else if (counter == 0) begin   	
				n <= n + 12'b1;
				state <= long;
			end

		long: 
			if (KEY[0])             state <= off;   // exit long
			else if (counter == 0)  n <= n + 12'b1;

		default:  state <= off;   
	endcase
end
```
There are a few problems:
- The exact time it transitions from `short` to `long` depends on the phase of the `counter`
	- Since it's only a 6 Hz, our human user can't detect that

## A slow short press
Moreover, we want the button to detect **slow presses** (E. ~0.5 seconds of press). The logic is expected to increment **once**, without entering the 6 Hz `long` mode.
- Our current code only has a window of around 0.16 s, so my grandma probably can't increment it properly.

The logic is also simple: add another longer timer for the `short`. Since this timer is a bit longer, we can't use `counter`, which goes with the clock.

```verilog
logic [22:0] counter; 
// Timer for short/long press detection
logic [24:0] press_counter;
localparam PRESS_THRESHOLD = 25'd25_000_000; // 0.5s

enum logic [1:0] {off, short, long, unused} state0;

always_ff @(posedge clk) begin
    counter <= (counter == 23'h7fffff) ? (23'h0) : (counter + 23'h1);

	case (state0)
		off: 
			if (~KEY[0])    state <= short;

		short: begin
		    press_counter <= 0;		// only used for short mode
			if (~KEY[0]) begin  // continue to long
				if (press_counter >= PRESS_THRESHOLD)   
					state <= longR;
				else                                    
					press_counter <= press_counter + 25'h1;
			end else begin 	// reset
				state <= off;
				n <= (n == n_init+12'hff)? (n_init) : (n + 12'b1);
			end
		end

		long: begin
			if (KEY[0])           
				state0 <= off;   // Exit long press
			else if (counter == 0) 
				n <= n + 12'b1;
		end
	endcase
end
```

## Fixing Fast Press glitches with debouncer
The FPGA manuals said they switches are Schmitt-triggered, so I assume they are debounced properly.

However, when testing it with rapid sequence of short button presses, the count sometimes resets, and sometimes freezes and completely fails :(

I asked Edwards about this. The answer was brief:
> Edwards: Keybounce. We discussed this in class.  

> Me: They said the switches are Schmitt-triggered  

> Edwards: They lied.

I was still not fully convinced on why that would cause the program to crash, although this was really rare. Still, Edwards recommended me to use a debouncer as a start.

So I started implementing. Let the button inputs be `KEY_RAW[3:0]`

```verilog
logic [23:0] deb_counter;   // 24(20)-bit debounce counter, around 20 ms
localparam DEB_THRESHOLD = 24'h7fff;    // 0.6 ms

always_ff @(posedge clk) begin

	if (KEY_RAW != KEY) begin
		if (deb_counter == DEB_THRESHOLD) begin   
			KEY <= KEY_RAW; // updates prev and allows 
			deb_counter <= 0;
		end else        
			deb_counter <= deb_counter + 24'h1;
    end
end
```
The logic is follows:
- When `KEY_RAW` updates, for 0.6 ms, ignore all changes to the keys
- After 0.6 ms, pass the *current* value of `KEY_RAW` to `KEY`.

Suppose the key is originally off, and we want to briefly press it on. The logic would fail in the following condition:
1. `KEY_RAW` is still unstable from "off" to "on" after the 0.6 ms period, and it might glitch.
2. The key "bounce back" to "off" before 0.6 ms, and it might not record a button press

Setting`DEB_THRESHOLD` should trade off between 1 and 2. I initially guessed 20 ms from a web search. However, our switch is small and hard. After some trial-and-error, I found 0.6 ms to be around optimal.
- That 0.6 ms still misses some presses, but I would prefer missing a press, rather than glitching or even crashing the system.

## Multiple button presses
What if... the user goes crazy and starts randomly simultaneously pressing buttons? Our debouncer blocks out any fast button changes, so we can focus on optimizing the logic.

Fortunately, the solution is fairly simple: make the conditions *if and if only* the button is pressed. If multiple buttons are pressed at the same time, the system just holds wait for some release.

To detect an *only* `KEY[0]` press:
```verilog
if (~KEY[0] && KEY[1] && KEY[2] && KEY[3])
``` 
and to make our lives easier, we can use binary
```verilog
if (KEY == 4'b1110)
```

## Conclusion

That's it, we've accounted for all cases:
- Slow press
- Fast press
- Press and hold
- Multiple press

Of course, I only programmed one button press, but the rest should be identical in the `always_ff` block.

An immediate follow-up is to optimize the counters. Now I used three counters:
- `counter` for long press cycle
- `press_counter` for short --> long transition
- `deb_counter` for switch debouncing  
I'm pretty sure there's a way to simplify that.