#!/bin/bash
ARGC=$#
if [ $ARGC -lt 1 ]; then
  echo "Error - Usage: $0 <treqs_output_file>"
  exit 1
fi
filename=$1

# Extract <Request-ID> and <Request-Raw> and <String-Mutations> from treqs output
awk -F "[*]{5}" '$3 ~ /success":[ ]*1/{print $1" || "$2" || "$4}' $filename > $filename"_id_and_reqs_and_mutations"

# Extract <Request-ID> and <Bypassed WAFs List> from treqs output
cat $filename | sed 's/HTTP.... [0-9]\{3\} /\n &/g' | grep -o "HTTP[^-]*.[a-z]\+\|X-Request-ID: [0-9]\+\|success.:\s*1\+" | sed -z 's/\nsuccess/ success/g' | grep "success\|Request-ID" | sed -z 's/\nHTTP/ HTTP/g'| grep success | sed 's/HTTP[^p]*parser: //g;s/success[^1]*1/,/g;s/X-Request-ID: \([0-9]\+\)/\1,/g' | sed 's/ ,/,/g;s/,$//' > $filename"_id_and_wafs_list"

python3 ./main.py $filename > $filename"_parsed.json"
rm $filename"_id_and_wafs_list"
rm $filename"_id_and_reqs_and_mutations"

