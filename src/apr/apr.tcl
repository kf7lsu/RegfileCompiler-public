
set design_name "regfile"  ;  # Name of the design


# CONFIGURATION
# ==========================================================================
set TOOL_NAME "ICC"
# directory where tcl src is located 
set SCRIPTS_DIR "../src/apr"


# Configure design, libraries
# ==========================================================================
source ${SCRIPTS_DIR}/setup_node.tcl -echo
source ${SCRIPTS_DIR}/library.tcl -echo

# READ DESIGN
# ==========================================================================
# Read in the verilog, uniquify and save the CEL view.
import_designs $design_name.v -format verilog -top $design_name


# TIMING CONSTRAINTS
# ==========================================================================

source ${SCRIPTS_DIR}/config.tcl -echo
create_clock "clk" -period $CLK_PER
link
#set_clock_uncertainty $CLK_UNCERTAINTY

# Path groups 
# # ==============================================
group_path -name "Inputs"       -from [remove_from_collection [all_inputs] [get_ports $CLK_PORT]]
group_path -name "Outputs"      -to [all_outputs]
group_path -name "Feedthroughs" -from [remove_from_collection [all_inputs] [get_ports $CLK_PORT]] \
                                 -to [all_outputs]
group_path -name "Regs_to_Regs" -from [all_registers] -to [all_registers]

# outputs 
set_output_delay $blanket_output_delay -clock "clk" [all_outputs]
set_load [load_of $blanket_input_load] [all_outputs]

# inputs 
set_input_delay $blanket_input_delay -clock "clk" \
    [remove_from_collection [all_inputs] [get_ports $CLK_PORT]]
set_drive [drive_of $blanket_output_drive] [all_inputs]

# CUSTOM PLACEMENT
# =========================================================================
# Create TCL File to measure widths of cells
exec python ${SCRIPTS_DIR}/doWidthCheck.py

# Run Width Measurement TCL File
source ${SCRIPTS_DIR}/widthChecker.tcl

# Create TCL File to do Custom Placement
exec python ${SCRIPTS_DIR}/doCustomPlacement.py

# Run TCL File generated from custom placement to set floorplan size
source ${SCRIPTS_DIR}/floorplanSizes.tcl

# FLOORPLAN CREATION
# =========================================================================
# Create core shape and pin placement
# Edited Floorplan.TCL to not set the width and height, done in earlier TCL
source ${SCRIPTS_DIR}/floorplan.tcl -echo

# DO CUSTOM CELL PLACEMENT from File Generated in Earlier Python Script
#source python/customPlacement.tcl -echo
source ${SCRIPTS_DIR}/customPlacement.tcl -echo

# PHYSICAL POWER NETWORK
# ==========================================================================
save_mw_cel -as ${design_name}_prepns
source ${SCRIPTS_DIR}/power.tcl -echo

# PLACEMENT OPTIMIZATION
# ==========================================================================
save_mw_cel -as ${design_name}_preplaceopt
source ${SCRIPTS_DIR}/placeopt.tcl -echo

# CTS & CLOCK ROUTING
# ==========================================================================
save_mw_cel -as ${design_name}_preclock
source ${SCRIPTS_DIR}/clocks.tcl


# SIGNAL ROUTING
# ==========================================================================
save_mw_cel -as ${design_name}_preroute
source ${SCRIPTS_DIR}/route.tcl -echo
verify_lvs -ignore_floating_port

# GENERATE RESULT FILES
# ==========================================================================
save_mw_cel -as ${design_name}_finished
source ${SCRIPTS_DIR}/generate.tcl -echo

# REPORT DRCS AS POPUP WINDOW
# ==========================================================================
# AT END OF PROJECT: Potentially remove these last 3 commands? 
source ${SCRIPTS_DIR}/report_drcs.tcl -echo
report_drc -highlight -color green

start_gui
