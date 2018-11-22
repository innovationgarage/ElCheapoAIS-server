#! /bin/bash

nc -k -l 0.0.0.0 1024 |
  tee >(cat >&2 ) |
  gpsdecode |
  tee >(cat >&2 ) |
  /update.py
