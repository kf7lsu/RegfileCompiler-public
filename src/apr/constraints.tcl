
# ==========================================================================
# TIMING CONSTRAINTS
# ==========================================================================

# Set setup/hold derating factors
# - 0% derate
set_timing_derate -early 1.0
set_timing_derate -late  1.0

# Ensure that no net drives multiple ports, buffer logic constants instead of duplicating
set_fix_multiple_port_nets -all -buffer_constants

