#!/usr/bin/env bash

logdir=~/Library/Logs/com.katylavallee.wintracker
filedate=`date +%Y%m%d-%H%M%S`

cd "${logdir}"
cat wintracker.log > wintracker.$filedate.log && :> wintracker.log
cat wintracker_err.log > wintracker_err.$filedate.log && :> wintracker_err.log

