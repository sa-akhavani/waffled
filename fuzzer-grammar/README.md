## Prerequisites

- Python 3.6 or higher
- configatgparse (install via pip)

## T-REQS commands

After writing and customizing your grammar, you can use the following commands to generate and manage your parser:

pass your grammar file to the fuzzer using the `-c` option.

```bash
# Running the fuzzer with a single specific seed number of 64
python3 ./code/main.py -c ./grammar/multipart_simple -i -s 64 ./output

# Running the fuzzer with seed input from a file and outputting to another file
python3 ./code/main.py -c ./grammar/multipart_simple -i -f /tmp/s > ./output

# Running the fuzzer in bulk mode
python3 ./code/main.py -c ./grammar/multipart_simple

```
