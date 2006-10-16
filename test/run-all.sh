#!/usr/bin/env bash

TESTS=$(ls *.py)

echo "Tests:"
for file in $TESTS
do
  echo "running test: $file"
  mpiexec -l -n 4 python $file
  sleep 10
done
