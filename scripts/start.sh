#!/bin/bash
cd led_matrix_application
pkill -f 'hypercorn main:app'
sleep 0.1
hypercorn main:app