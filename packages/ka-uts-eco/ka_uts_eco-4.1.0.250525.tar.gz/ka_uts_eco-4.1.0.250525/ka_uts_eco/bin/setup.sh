#!/usr/bin/env bash
#
# Setup EcoVadis SRR Infrastructure
#
DIR_APP='/tmp/app/otev/bin'
DIR_DAT='/tmp/data/otev'
#
# /usr/bin/env python3 -m otev_srr \
#
# sw_mkdirs=True \
#
kautsuts \
\
cmd='setup' \
\
package="otev_srr" \
\
src_dir_app="bin" \
src_dir_dat="data/otev" \
tgt_dir_app="$DIR_APP" \
tgt_dir_dat="$DIR_DAT" \
\
log_sw_mkdirs=True \
log_type="std" \
sw_debug=False \
tenant='UMH'
