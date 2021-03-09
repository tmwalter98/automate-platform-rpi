#!/bin/sh
# uses the 5-minute load value
LOADVAL5=$(awk '{ print $2; }' < /proc/loadavg)
NUMCPUS=$(getconf _NPROCESSORS_ONLN)
echo "$LOADVAL5 * 100 / $NUMCPUS" | bc