#!/bin/bash

cd api_server

sudo gunicorn -b 127.0.0.1:5000 --pid=app.pid tABLE_server:app