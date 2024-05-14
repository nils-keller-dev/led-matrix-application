#!/bin/bash
./scripts/start.sh &
watchmedo shell-command --patterns="*.py;*.txt" --recursive --command='./scripts/start.sh' ./led_matrix_application