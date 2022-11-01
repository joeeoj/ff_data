#!/usr/bin/env bash

case $1 in
  download)
    python3 download.py
    ;;

  parse)
    python3 parse.py
    ;;

  createdb)
    if [ -f "football.db" ]; then
      rm "football.db"
    fi
    sqlite3 football.db < schema.sql
    ;;

  loaddb)
    python3 load.py
    ;;

  copydb)
    cp football.db ./reports/football.db
    ;;

  runall)
    python3 parse.py

    if [ -f "football.db" ]; then
      rm "football.db"
    fi
    sqlite3 football.db < schema.sql

    python3 load.py

    cp football.db ./reports/football.db
    ;;

  *)
    echo 'options: download, parse, createdb, loaddb, or runall (except download)'
    ;;
esac
