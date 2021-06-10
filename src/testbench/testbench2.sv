// Test bench for Register file
// 2 Read ports, 16 bit data, 6 bit(64 lines) addresses
`timescale 1ns/10ps

module testbench2(); 		

	parameter ClockDelay = 10000;

	logic	[5:0] 	wr_addr, rd_addr_0, rd_addr_1;
	logic [15:0]	wr_data;
	logic 			clk, wr_en;
	logic [15:0]	rd_data_0, rd_data_1;
   logic 		VDD, VSS;
   assign VDD = 1'b1;
   assign VSS = 1'b0;
   
	integer i;

	// Your register file MUST be named "regfile".
	// Also you must make sure that the port declarations
	// match up with the module instance in this stimulus file.
	regfile dut (.*);

	// Force %t's to print in a nice format.
	initial $timeformat(-9, 2, " ns", 10);

	initial begin // Set up the clock
		clk <= 0;
		forever #(ClockDelay/2) clk <= ~clk;
	end

	initial begin
	        $sdf_annotate("./regfile.apr.sdf", dut);
	        $vcdpluson;
		// Write a value into each  register.
		$display("%t Writing pattern to all registers.", $time);
		for (i=0; i<64; i=i+1) begin
			wr_en <= 0;
		   @(negedge clk);
		   
			rd_addr_0 <= i-1;
			rd_addr_1 <= i;
			wr_addr <= i;
			wr_data <= i*16'h2408;
			@(negedge clk);
			
			wr_en <= 1;
			@(negedge clk);
		   @(negedge clk);
		end

		// Go back and verify that the registers
		// retained the data.
		$display("%t Checking pattern.", $time);
		for (i=0; i<64; i=i+1) begin
			wr_en <= 0;
		   @(negedge clk);
		   
			rd_addr_0 <= i-1;
			rd_addr_1 <= i;
			wr_addr <= i;
			wr_data <= i*16'h0100+i;
			@(posedge clk);
		end
		$finish;
	end
endmodule
