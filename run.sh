#!/usr/bin/env bash

case $1 in

  download)
    echo 'downloading data'
    python3 download.py
    ;;

  parse)
    echo 'parsing data'
    python3 parse.py
    ;;

  runall)
    echo 'running all'
    python3 download.py
    python3 parse.py
    ;;

  *)
    echo 'options: download, parse, or runall'
    ;;
esac
