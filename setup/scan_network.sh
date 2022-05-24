#!/usr/bin/env bash
tab=$'\t'
pIF=$(echo "show State:/Network/Global/IPv4" | scutil | awk -F: '/PrimaryInterface/{sub(/ /,"",$2); print $2}')
sn=$(ipconfig getifaddr $pIF | sed -En 's/^([0-9]+\.[0-9]+\.[0-9]+).*/\1/p')
for i in {1..254}; do ping -i0.1 -W100 -c1 $sn.$i | grep from; done
arp -a | grep $pIF | sed -e 's/^\?/unnamed/' -e "s/\ at\ /${tab}/g" -e "s/\ on\ /${tab}/g" -e 's/\ ifscope.*$//g' | awk 'BEGIN { FS="\t"; OFS="\t"; printf "%-17s\t%-15s\t%s\n", "MAC","INTERFACE","HOSTNAME (IP)" } { if($2!="(incomplete)") {printf "%-17s\t%-15s\t%s\n",$2,$3,$1}}'
