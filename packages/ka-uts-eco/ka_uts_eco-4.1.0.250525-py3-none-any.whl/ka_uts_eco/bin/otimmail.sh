#!/usr/bin/env bash
#
# Create EcoVadis upload workbook with an Admin Sheet and an empty Delete Sheet
#
# /usr/bin/env python3 -m otev_srr \
#
otevsrr_xls \
\
cmd='optimmail' \
\
dir_dat="/data/otev" \
\
in_path='[
"OT/Vfy/OTEX.reg.vfy.\$now.xlsx","EV/Dow/Dat/EVDO.reg.\$now.xlsx","EV/Exp/Eco/EVEX.eco.\$now.xlsx","EV/Exp/Umh/EVEX.umh.\$now.xlsx"]' \
\
sw_attach=True \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
