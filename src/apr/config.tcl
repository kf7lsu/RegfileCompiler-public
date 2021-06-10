
# Project and design
# ==========================================================================
set TOPLEVEL "regfile"
set PROJECT_DIR "../../"

# Source files 
# ==========================================================================
set BASE "$PROJECT_DIR/run"

set RTL_SOURCE_FILES [list \
   "regfile.v" \
   
]

set RTL_DEFINES ""

# Runtime options 
# ==========================================================================

#clock period and uncertainty
set CLK_PER 1.0
set CLK_UNCERTAINTY .1

# Multicore acceleration
if {$TOOL_NAME != "PTPX"} {
   set_host_options -max_cores 8 ;   
}

# Silence the unholy number of warnings that are known to be harmless
suppress_message "DPI-025"
suppress_message "PSYN-485"

# Check for latches in RTL
set_app_var hdlin_check_no_latch true

# Library setup
# ==========================================================================

# Design libraries 
set DESIGN_MW_LIB_NAME "regfile_lib"

   # Logic libraries 
set NODE_PATH "/node_path/digital"
set TARGETCELLLIB_PATH "$NODE_PATH/target_cell_lib"
set ADDITIONAL_SEARCH_PATHS [list \
   "$TARGETCELLLIB_PATH" \
   "$NODE_PATH/node_path/milkyway*" \
   "$synopsys_root/libraries/syn" \
   "./" \
]
set TARGET_LIBS [list \
   "targetlib1.db" \
   "targetlib2.db" \
]

set ADDITIONAL_TARGET_LIBS ""
set SYMBOL_LIB "symbol_lib.db"
set SYNOPSYS_SYNTHETIC_LIB "synthetic_lib.sldb"

   # Reference libraries 
set MW_REFERENCE_LIBS "$NODE_PATH/node_path/milkyway/fram_only"
set MW_ADDITIONAL_REFERENCE_LIBS ""

   # Worst case library
set LIB_WC_FILE   "worstcase_lib.db"
set LIB_WC_NAME   "worstcase_lib"

   # Best case library
set LIB_BC_FILE   "bestcase_lib.db"
set LIB_BC_NAME   "bestcase_lib"

   # Operating conditions
set LIB_WC_OPCON  "worst_opcon"
set LIB_BC_OPCON  "best_opcon"

   # Technology files
set MW_TECHFILE_PATH "$NODE_PATH/techfiles"
set MW_TLUPLUS_PATH "$MW_TECHFILE_PATH/tluplus"
set MAX_TLUPLUS_FILE "best.tluplus"
set MIN_TLUPLUS_FILE "worst.tluplus"


set TECH2ITF_MAP_FILE "map.map_9M"
set MW_TECHFILE "mw_techfile.tf"

# nand2 gate name for area size calculation
set NAND2_NAME    "NAND2W1"

# Clock 
# ==========================================================================
#  - Assumes a single clock

# Name of the port
set CLK_PORT   "clk"


# Timing uncertainties
set clk_critical_range 0.010
set clk_setup_uncertainty 0.050
set clk_hold_uncertainty 0.010
# set clk_hold_uncertainty 0.000

# Transition
set clk_trans 0.050

# General timing
# ==========================================================================
# - simplified timing constraints

set max_fanout 32
set max_trans 1.000

set blanket_output_delay 0.100
set blanket_input_delay 0.100

set blanket_output_drive "${LIB_WC_NAME}/INVW1/ZN"
set blanket_input_load "${LIB_WC_NAME}/INVW16/I"


# DC compile options
# ==========================================================================

# Reduce runtime
set DC_PREFER_RUNTIME 0

# Preserve design hierarchy
set DC_KEEP_HIER 1

# Register retiming
set DC_REG_RETIME 0
set DC_REG_RETIME_XFORM "multiclass"

# Logic flattening
set DC_FLATTEN 0
set DC_FLATTEN_EFFORT "medium"

# Logic structuring
set DC_STRUCTURE 0
set DC_STRUCTURE_TIMING "true"
set DC_STRUCTURE_LOGIC  "true"

set DC_GLOBAL_CLK_GATING 1

# Do an additional incremental compile for better results
set DC_COMPILE_ADDITIONAL 1

# Result generation and reporting
# ==========================================================================
set results "results"
set reports "reports"


