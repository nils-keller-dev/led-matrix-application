#!/bin/bash
cd /home/admin/led-matrix-application/led_matrix_application &&
sudo $(poetry env info --path)/bin/hypercorn -b 0.0.0.0:8080 main:app