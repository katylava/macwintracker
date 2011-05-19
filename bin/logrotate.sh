#!/usr/bin/env bash

logdir=~/Library/Logs/com.katylavallee.wintracker
cmddir=~/Library/Application\ Support/com.katylavallee.wintracker
filedate=`date +%Y%m%d-%H%M%S`

cd "${logdir}"
"${cmddir}/jsonlogdedupe.py" --print-last -i time_end wintracker.log > wintracker.$filedate.log && :> wintracker.log
cat wintracker_err.log > wintracker_err.$filedate.log && :> wintracker_err.log

