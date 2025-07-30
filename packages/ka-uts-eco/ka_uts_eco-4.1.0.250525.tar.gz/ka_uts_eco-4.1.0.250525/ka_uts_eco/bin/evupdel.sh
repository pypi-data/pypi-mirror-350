#!/usr/bin/env bash
#
# Create EcoVadis upload workbook with a Delete sheet and an empty Admin sheet
#
#
# /usr/bin/env python3 -m otev_srr \
#
otevsrr_xls \
\
cmd='evupdel' \
\
dir_dat="/data/otev" \
\
in_path_evex="EV/Exp/Eco/EVEX.eco.*.xlsx" \
in_path_evup_tmp="EV/Upl/Tmp/EVUP.tmp.xlsx" \
in_path_otex="OT/Exp/OTEX.*.xlsx" \
\
out_path_otex_del_vfy="OT/Vfy/OTEX.del.vfy.\$now.xlsx" \
out_path_evup_del="EV/Upl/Dat/EVUP.del.\$now.xlsx" \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
