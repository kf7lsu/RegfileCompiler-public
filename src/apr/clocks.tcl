
# ==========================================================================
# FIRST SETUP PREFERRED ROUTING DIRECTION
# ==========================================================================

#these values organize the routing layers for the process node
set MAX_ROUTING_LAYER "M0" 
set MIN_ROUTING_LAYER "M0"
set HORIZONTAL_ROUTING_LAYERS "M0 M0 M0 M0"
set VERTICAL_ROUTING_LAYERS "M0 M0 M0"
set_preferred_routing_direction \
    -layers $HORIZONTAL_ROUTING_LAYERS \
    -direction horizontal

set_preferred_routing_direction \
    -layers $VERTICAL_ROUTING_LAYERS \
    -direction vertical

if { $MAX_ROUTING_LAYER != ""} {set_ignored_layers -max_routing_layer $MAX_ROUTING_LAYER}
if { $MIN_ROUTING_LAYER != ""} {set_ignored_layers -min_routing_layer $MIN_ROUTING_LAYER}

# ==========================================================================
# CTS & CLOCK ROUTING
# ==========================================================================

# Make sure placement is good before CTS
check_legality -verbose

# Set options for compile_clock_tree (all are pretty much default, except the routing rule)
set_clock_tree_options \
   -layer_list_for_sinks {M1 M2 M3 M4 M5} \
   -layer_list {M1 M2 M3 M4 M5} \
   -use_leaf_routing_rule_for_sinks 0 \
   -max_transition 1 \
   -leaf_max_transition 1 \
   -use_leaf_max_transition_on_exceptions TRUE \
   -use_leaf_max_transition_on_macros TRUE \
   -max_capacitance 1 \
   -max_fanout 5 \
   -target_early_delay 0.000 \
   -target_skew 0.000

#Block off specific metal layers from being routed
create_metal_blockage 0

#Run the clock!
set_fix_hold [all_clocks]
clock_opt

# Fix hold violations
#psynopt -only_hold_time
verify_zrt_route

# Save current design (checkpoint)
save_mw_cel -as ${design_name}_postclk
