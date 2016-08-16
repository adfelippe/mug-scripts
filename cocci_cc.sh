#! /bin/bash
#
# cocci_cc - send cover letter to all mailing lists referenced in a patch series
# intended to be used as 'git send-email --cc-cmd=cocci_cc ...'
# done by Wolfram Sang in 2012-14, version 20140204 - WTFPLv2

shopt -s extglob
cd $(git rev-parse --show-toplevel) > /dev/null

name=${1##*/}
num=${name%%-*}

if [ "$num" = "0000" ]; then
    dir=${1%/*}
    for f in $dir/!(0000*).patch; do
        scripts/get_maintainer.pl --no-m $f
    done | sort -u
else
    scripts/get_maintainer.pl $1
fi
