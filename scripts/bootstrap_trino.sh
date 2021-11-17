#!/bin/bash

trino --server localhost:8080 --execute 'show catalogs;'
