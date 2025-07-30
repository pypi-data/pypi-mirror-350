#!/usr/bin/env bash
#
# Send email to EcoVadis: upload workbook is ready
#
# /usr/bin/env python3 -m otev_srr \
#
otevsrr_xls \
\
cmd='evupmail' \
\
dir_dat="/data/otev" \
\
in_path="EV/Upl/Dat/EVUP.reg.\$now.xlsx" \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
