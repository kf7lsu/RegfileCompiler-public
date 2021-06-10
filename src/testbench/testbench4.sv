// Test bench for Register file
// 2 Read ports, 32 bit data, 5 bit(32 lines) addresses
`timescale 1ns/10ps

module testbench3(); 		

	parameter ClockDelay = 10000;

	logic	[4:0] 	wr_addr, rd_addr_0, rd_addr_1;
	logic [31:0]	wr_data;
	logic 			clk, wr_en;
	logic [31:0]	rd_data_0, rd_data_1;
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
		for (i=0; i<32; i=i+1) begin
			wr_en <= 0;
		   @(negedge clk);
		   
			rd_addr_0 <= i-1;
			rd_addr_1 <= i;
			wr_addr <= i;
			wr_data <= i*32'h24082745;
			@(negedge clk);
			
			wr_en <= 1;
			@(negedge clk);
		end

		// Go back and verify that the registers
		// retained the data.
		$display("%t Checking pattern.", $time);
		for (i=0; i<32; i=i+1) begin
			wr_en <= 0;
		   @(negedge clk);
		   
			rd_addr_0 <= i-1;
			rd_addr_1 <= i;
			wr_addr <= i;
			wr_data <= i*32'h01000000+i;
			@(posedge clk);
		end
		$finish;
	end
endmodule
