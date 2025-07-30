#!/usr/bin/env bash
#
# Create EcoVadis upload workbook with an Admin Sheet and a Delete Sheet or
# create two EcoVadis upload workbooks for the Admin- or Delete-Sheet.
#
# /usr/bin/env python3 -m otev_srr \
#
otevsrr_xls \
\
cmd='evupreg' \
\
dir_dat="/data/otev" \
\
in_path_evex="EV/Exp/Eco/EVEX.eco.*.xlsx" \
in_path_evup_tmp="EV/Upl/Tmp/EVUP.tmp.xlsx" \
in_path_otex="OT/Exp/OTEX.*.xlsx" \
\
out_path_evup_adm="EV/Upl/Dat/EVUP.adm.\$now.xlsx" \
out_path_evup_del="EV/Upl/Dat/EVUP.del.\$now.xlsx" \
out_path_evup_reg="EV/Upl/Dat/EVUP.reg.\$now.xlsx" \
out_path_otex_reg_vfy="OT/Vfy/OTEX.reg.vfy.\$now.xlsx" \
\
sw_single_wb=True \
sw_vfy_ignore_duns=False \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
