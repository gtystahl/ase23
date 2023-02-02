#!/bin/bash

val=$(cat counter.txt)
echo $(($val + 1)) > counter.txt
