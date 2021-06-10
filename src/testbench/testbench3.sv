// Test bench for Register file
// 1 Read ports, 64 bit data, 6 bit(64 lines) addresses
`timescale 1ns/10ps

module testbench3(); 		

	parameter ClockDelay = 10000;

   logic	[5:0] 	wr_addr, rd_addr_0;
   
	logic [63:0]	wr_data;
	logic 			clk, wr_en;
   logic [63:0] 		rd_data_0;
   

	integer i;
   logic 	VDD, VSS;
   
   assign VDD = 1'b1;
   assign VSS =1'b0;
   

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
	        
			wr_addr <= i;
			wr_data <= i*64'h2408274503245853;
			@(negedge clk);
			
			wr_en <= 1;
			@(negedge clk);
		end

		// Go back and verify that the registers
		// retained the data.
		$display("%t Checking pattern.", $time);
		for (i=0; i<64; i=i+1) begin
			wr_en <= 0;
		   @(negedge clk);
		   
			rd_addr_0 <= i-1;
	        
			wr_addr <= i;
			wr_data <= i*64'h0100000000000000+i;
			@(posedge clk);
		end
		$finish;
	end
endmodule
