#!/bin/bash
cd led_matrix_application
pkill -f 'hypercorn main:app'
lsof -t -i :8000 | xargs kill -9
lsof -t -i :8888 | xargs kill -9
sleep 0.1
hypercorn main:app
