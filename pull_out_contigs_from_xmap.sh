#!/bin/bash                                                                                                                                                                                                 
# stdin replaced with a file supplied as a first argument
# usage: program.sh list_of_molecules xmap_source
exec < $1

grep '^#' $2

while read LINE; do
	grep $"^[0-9]\+\t${LINE}\t" $2
done
