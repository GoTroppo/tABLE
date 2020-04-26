#!/bin/bash
export PYTHONPATH=$(pwd)/../api_server

cd $(pwd)/api_server

sudo pdoc3 --force --html . --html-dir ../documentation/