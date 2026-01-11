---
title: ALD Lab Notes
permalink: /courses/ald
date: 2025-10-20
---

{% include toc %}

# 1. MATLAB

```matlab
% Behavior model for LFSR1
% Producing 256 16b outputs
% MS 7/2015

clear;

reg=zeros(16,1);
reg=[0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1];
fb=zeros(16,1);
fb=[1 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1];

bw=length(fb);
n_cycle=256;
out_file = fopen('./lfsr1.results','w');

z(1) = sum(reg.*2.^(numel(reg)-1:-1:0));
for i=1:n_cycle
   fb_sum_out=0;
   xor_out=0;
   for j=1:bw
      if fb(j)==1 
         fb_sum_out=fb_sum_out+reg(j);
      end
   end
   xor_out = mod(fb_sum_out, 2);
   reg = [reg(2:bw) xor_out];
   z(i+1) = sum(reg.*2.^(numel(reg)-1:-1:0));
   fprintf(out_file,'%d\n',z(i));
end   

%finishing
fclose(out_file);
exit;
```

# 2. Verilog and ModelSim
## Design

```verilog
`timescale 1ns/1ps
module lfsr1 (clk, resetn, seed, lfsr_out);
    input clk, resetn;
    input [15:0] seed;
    output [15:0] lfsr_out;
    reg [15:0] lfsr_out;
	wire [15:0] lfsr_next;

    always @(posedge clk) begin
        if (~resetn) begin
            lfsr_out <= #0.1 seed;
        end
        else begin
            lfsr_out <= #0.1 lfsr_next;
        end
    end

assign lfsr_next = {lfsr_out[14:0],lfsr_out[15]^lfsr_out[12]^lfsr_out[5]^lfsr_out[0]};
endmodule
```

- `timescale` specifies `scale/precision`
	- `#0.1` is artificial delay (0.1 ns), **ignored** in logic synthesis
- `wire` with `assign`, `reg` with `always` block

## Testbench
instantiation **DUT** (Device Under Test)

```verilog
`timescale 1ns/1ps
`define SD #0.010

module testbench();
	reg clk;                 // inputs declared as reg
	reg resetn;
	reg [15:0] seed;
	wire [15:0] lfsr_out;    // outputs: wire

	lfsr1 lfsr_0 ( .clk(clk), .resetn(resetn), .seed(seed), .lfsr_out(lfsr_out) );
```

CLK Generator: toggle `clk` after every half clock period

```verilog
`define HALF_CLOCK_PERIOD #0.90
	always begin
		`HALF_CLOCK_PERIOD;
		clk = ~clk;        // full period is 1.8 ns
	end
```

**File IO**

```verilog
`define QSIM_OUT_FN "./qsim.out"
`define MATLAB_OUT_FN "../../matlab/lfsr1/lfsr1.results"
	integer i;
	integer qsim_out_file;
	integer matlab_out_file;
	
	initial begin 
		qsim_out_file = $fopen(`QSIM_OUT_FN,"w");         // open for write
		matlab_out_file = $fopen(`MATLAB_OUT_FN,"r");     // open for read
```

Initialize

```verilog
		// register setup
		clk = 0;
		resetn = 0;
		seed = 16'd1;
		@(posedge clk);

		@(negedge clk);   // release resetn
		resetn = 1;      

		@(posedge clk);   // start the first cycle
```

Loop

```verilog
		integer lfsr_out_matlab;
		integer lfsr_out_qsim;
		integer ret_write;
		integer ret_read;
		integer error_count = 0;
		
		for (i=0 ; i<256; i=i+1) begin 
			// compare w/ the results from Matlab sim
			ret_read = $fscanf(matlab_out_file, "%d", lfsr_out_matlab);
			lfsr_out_qsim = lfsr_out;    // circuit output
			$fwrite(qsim_out_file, "%0d\n", lfsr_out_qsim);
			
			if (lfsr_out_qsim != lfsr_out_matlab)
				error_count = error_count + 1;

			@(posedge clk);  // next cycle
		end
		
```

Check error:

```verilog
		if (error_count > 0) 
			$display("The results DO NOT match with those from Matlab :( ");
		else 
			$display("The results DO match with those from Matlab :) ");
 
		$fclose(qsim_out_file);
		$fclose(matlab_out_file);
		$finish;
	end   // initial
endmodule // testbench
```

`initial` block
- Only run once
- Begin at time 0
- Execute sequentially
- Not synthesized to HW

## Scripts

```shell
vsim -do "runsim.do"
```

- `vsim` invoke VSIM simulator
- `-do` lets VSIM execute the commands specified in "runsim.do"

### `runsim.do`

```tcl
vlib work
vmap work work

# Include Netlist and Testbench
vlog +acc -incr ../../rtl/lfsr1/lfsr1.v 
vlog +acc -incr test_lfsr.v 

# Run Simulator 
vsim +acc -t ps -lib work testbench 
do waveformat.do   
run -all
```

- `vlib` creates a design library "work"
- `vmap` maps **logical library** `work` to the directory "work"
- `vlog` **compiles** Verilog source into working library
	- `-incr`: incremental compile
- `vsim [-args] [lib_name.design_unit]`
	- `-t ps`: time resolution in ps
	- `-lib work`: default working library
	- `testbench`: library name
- `do`: executes `waveform.do` macro file
- `run`: advance simulation

### `waveformat.do`

{% raw %}
```tcl
onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /testbench/clk
# ...
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {3 ns} 0}
quietly wave cursor active 1
configure wave -namecolwidth 223
# ...
configure wave -timelineunits ps
update
```
{% endraw %}


- `TreeUpdate`: refresh waveforms
- `WaveRestoreCursors`: restore any cursor from original simulation
- `configure wave`: used in saved wave format files

# 3. Synthesis
## Design Compiler
- Translate .v (RTL) code into .nl.v (gate-level netlist)
Input:
- RTL code of the design
- Standard cell library (E. `common.tcl`)
- Timing constraints: `timing.tcl`
- Synthesis flow commands and setup: `lfsr1.tcl`
Output:
- Gate level netlist (`.nl.v`)
- Timing information (`.sdf`)
- Synthesis report (`.rpt`)
Set design constraints
- Timing, Loading, Max fanout
Compile and report

## Verilog Tips
Three types with predictable results
- Combinatorial `assign`
- Combinatorial `always`
- Sequential `always` and `<=`

- Keep **related combinatorial logic** together
	- Better for logical optimization
	- Resource sharing can happen if they are in the same `always` block or VHDL process
- **Register** block outputs
	- Improves simulation speed and simplify time estimate
- Partition by design goal
	- Do not mix timing critical blocks and area critical blocks

![[workflow.png]]

## Library Files

```tcl
# path to search for unresolved reference
set search_path [list "." "/tools4/syn2007.12/libraries/syn/"]

# DesignWare library
set synthetic_library [list "dw_foundation.sldb"]

# DC uses this to resolve cell references
set link_library [list "*" \                      "/courses/ee6321/share/ibm13rflpvt/synopsys/scx3_cmos8rf_lpvt_tt_1p2v_25c.db" \
"dw_foundation.sldb"]

# techonology that design maps to
# add here for any standard cell *.db file
set target_library "/courses/ee6321/share/ibm13rflpvt/synopsys/scx3_cmos8rf_lpvt_tt_1p2v_25c.db"
```

### `lfsr1.tcl`
1. Read design and library

```tcl
set top_level lfsr1
read_verilog "../../rtl/$top_level/$top_level.v"

source -verbose "../common_script/common.tcl"    # read common.tcl AND your design
set set_fix_multiple_port_nets "true"
list_designs
```

2. Set design constraints
{: start="2" }

```tcl
current_design $top_level
link
check_design
source -verbose "./timing.tcl"         # read timing constraints

# design rule constraint
set_max_capacitance 0.005 [all_inputs]
set_max_fanout 4 $top_level
set_max_fanout 4 [all_inputs]

# optimization constraint
set_max_area 0                         # set to 0 for smallest area
set_fix_multiple_port_nets -all -buffer_constants
```

3. Compile
{: start="3" }

``` tcl
check_design                      # check for errors and warnings
#uniquify
current_design $top_level
link
compile_ultra                     # compile
```

4. Write output
{: start="4" }

```tcl
source -verbose "../common_script/namingrules.tcl"
set verilogout_no_tri TRUE       # avoid writing tristates

# generate outputs
write -hierarchy -format verilog -output "${top_level}.nl.v"  # gate level net
write_sdc "${top_level}.syn.sdc" -version 1.7         # timing info
write_sdf "${top_level}.syn.sdf"

# Generate report file
set maxpaths 20
set rpt_file "${top_level}.dc.rpt"                    # DC report
check_design > $rpt_file
report_area  >> ${rpt_file}
report_power -hier -analysis_effort medium >> ${rpt_file}

# ...
```

## Output Files
- Gate netlist `.nv.v`
- Design constraints `.syn.sdc`
	- An elaborate version of the constrains in `lfsr1.tcl`
- Timing info `.syn.sdf`
- Design compiler report `.rpt`
	- Area (just estimate, without interconnect or floor plan)
	- Timing: individual contribution to path delay
		- Negative **slack** indicates constraints violation
	- Power
		- For normal  VDD (1.2V), not information about inputs

# 4. Timing and Power Analysis
- QuestaSim: **post-synthesis** *dynamic* timing verification
	- Compare with RTL verification
- PrimeTime: **post-synthesis** *static* timing verification and power analysis
	- Worst case delay path
	- Power consumption with detailed switching activities
	- Setup/hold time violations

## ModelSim

```tcl
#Include Netlist and Testbench
 vlog +acc -suppress 12110 -incr /courses/ee6321/share/ibm13rflpvt/verilog/ibm13rflpvt.v     # std verilog lib
 vlog +acc -suppress 12110 -incr ../../dc/lfsr1/lfsr1.nl.v  # gate level netlist
 vlog +acc -suppress 12110 -incr test_lfsr.v 

#Run Simulator 
#SDF from DC is annotated for the timing check 
vsim -voptargs=+acc -t ps -lib work -sdftyp lfsr_0=../../dc/lfsr1/lfsr1.syn.sdf testbench    
 do waveformat.do   
 run -all
```

In the new waveform, you will see actual delays
In the testbench, when `$dumpfile("./lfsr1.vcd")`, `.vcd` file used to obtain an estimate of power using PrimeTime

## Static Timing/Power Verification
`lfsr1.tcl`

```tcl
## Global
set sh_enable_page_mode true                   # set env var
set power_enable_analysis true

## Setting files/paths
# set library and design
set verilog_files "../../dc/lfsr1/lfsr1.nl.v"
set my_toplevel lfsr1
set search_path ". /courses/ee6321/share/ibm13rflpvt/synopsys/"
set link_path "* scx3_cmos8rf_lpvt_tt_1p2v_25c.db" 

## Read design
read_db "scx3_cmos8rf_lpvt_tt_1p2v_25c.db"
read_verilog $verilog_files
link_design $my_toplevel

## Timing Constraints
source ./timing.tcl                         # same format as DC
```

Run STA:  
```tcl
set rpt_file "./lfsr1_pt.rpt"
check_timing
report_design >> ${rpt_file}
report_reference >> ${rpt_file}
report_constraint >> ${rpt_file}
report_constraint -all_violators -significant_digits 4 >> ${rpt_file}
report_timing -significant_digits 4 -delay_type min_max >> ${rpt_file}
# mention delay type

## Power analysis
set power_analysis_mode "time_based"'
# read vcd file
read_vcd "../../qsim_dc/lfsr1/lfsr1.vcd" -strip_path "testbench/lfsr_0"
report_switching_activity >> ${rpt_file}
report_switching_activity -list_not_annotated >> ${rpt_file}
update_power                          # update power estimates
report_power >> ${rpt_file}           # report power
report_power -hierarchy  >> ${rpt_file}

write_sdf -context verilog "./lfsr1.sdf"
```

### `timing.tcl`
Need `clk_period`be **same** as the Verilog TB

Report file will contain the min path, max path, and power consumption

