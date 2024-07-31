#!/bin/bash
cd led_matrix_application &&
sudo /home/admin/.cache/pypoetry/virtualenvs/led-matrix-application-eByq54Dv-py3.9/bin/hypercorn -b 0.0.0.0:8080 main:app
