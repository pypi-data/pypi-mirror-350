#!/usr/bin/env bash
#
# Map EcoVadis SRR Rating to UMH SRR Rating
#
# /usr/bin/env python3 -m otev_srr.xls \
#
otevsrr_xls \
\
cmd='evdomap' \
\
dir_dat="/data/otev" \
\
in_path_evex="EV/Exp/Eco/EVEX.eco.*.xlsx" \
\
out_path_evex="EV/Exp/Umh/EVEX.umh.\$now.xlsx" \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
