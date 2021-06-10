set results "results"
set reports "reports"

file mkdir ./$results
file mkdir ./$reports

# ICC runtime 
# ==========================================================================
# Silence the unholy number of warnings that are known to be harmless
suppress_message "DPI-025"
suppress_message "PSYN-485"

# Library setup
# ==========================================================================

set DESIGN_MW_LIB_NAME "regfile_lib"
# Logic libraries 
set NODE_PATH "/node_path/digital"
set TARGETCELLLIB_PATH "$NODE_PATH/target_cell_lib"
set ADDITIONAL_SEARCH_PATHS [list \
				 "$TARGETCELLLIB_PATH" \
				 "$NODE_PATH/milkyway/*" \
				 "$synopsys_root/libraries/syn" \
				 "./" \
				]
set TARGET_LIBS [list \
		     "target_lib.db" \
		    ]
#Used by sdc 
set ADDITIONAL_TARGET_LIBS {}
set ADDITIONAL_SYMBOL_LIBS {}
set SYMBOL_LIB "symbol_lib.db"
set SYNOPSYS_SYNTHETIC_LIB "synthetic_lib.sldb"

# Reference libraries 
set MW_REFERENCE_LIBS "$NODE_PATH/milkyway/frame_only/"
set MW_ADDITIONAL_REFERENCE_LIBS {}

# Technology files
set MW_TECHFILE_PATH "$NODE_PATH/techfiles"
set MW_TLUPLUS_PATH "$MW_TECHFILE_PATH/tluplus"
set MAX_TLUPLUS_FILE "max.tluplus"
set MIN_TLUPLUS_FILE "min.tluplus"

set TECH2ITF_MAP_FILE "map.map_9M"
set MW_TECHFILE "techfile.tf"

# POWER NETWORK CONFIG
# ==========================================================================
set MESH_FILE "mesh.tpl"
set MESH_NAME "core_mesh"
set CUSTOM_POWER_PLAN_SCRIPT "macro_power.tcl"

# FUNCTIONAL CONFIG
# ==========================================================================

set_route_zrt_common_options -global_max_layer_mode hard
if {$TOOL_NAME == "ICC"} {
    # Zroute and the common router do not respect macro blockage layers by default
    set_route_zrt_common_options \
	-read_user_metal_blockage_layer "true" \
	-wide_macro_pin_as_fat_wire "true"
}

set FILL_CELLS {FILL8 FILL4 FILL2 FILL1}

# RESULT GENERATION AND REPORTING
# ==========================================================================
set reports "reports" ; # Directory for reports
set results "results" ; # For generated design files
source ${SCRIPTS_DIR}/common_functions.tcl

