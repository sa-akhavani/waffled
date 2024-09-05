grep -o "'mutation-string.*affected" $1 | sort | uniq -c | sort -rn | less

