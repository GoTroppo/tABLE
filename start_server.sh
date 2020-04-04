#!/bin/bash

cd api_server

sudo gunicorn -b 0.0.0.0:5000 --pid=app.pid tABLE_server:app