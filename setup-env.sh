#!/bin/bash

echo "Please enter values for the following keys (leave blank to skip):"

read -p "TIMEZONE: " TIMEZONE
read -p "OWM_API_KEY: " OWM_API_KEY
read -p "LOCATION: " LOCATION

read -p "SPOTIFY_USER: " SPOTIFY_USER
read -p "SPOTIFY_CLIENT_ID: " SPOTIFY_CLIENT_ID
read -p "SPOTIFY_CLIENT_SECRET: " SPOTIFY_CLIENT_SECRET
read -p "SPOTIFY_REDIRECT_URI: " SPOTIFY_REDIRECT_URI

read -p "USE_EMULATOR: " USE_EMULATOR

{
  [[ -n "$TIMEZONE" ]] && echo "TIMEZONE=$TIMEZONE"
  [[ -n "$OWM_API_KEY" ]] && echo "OWM_API_KEY=$OWM_API_KEY"
  [[ -n "$LOCATION" ]] && echo "LOCATION=$LOCATION"

  [[ -n "$SPOTIFY_USER" ]] && echo "SPOTIFY_USER=$SPOTIFY_USER"
  [[ -n "$SPOTIFY_CLIENT_ID" ]] && echo "SPOTIFY_CLIENT_ID=$SPOTIFY_CLIENT_ID"
  [[ -n "$SPOTIFY_CLIENT_SECRET" ]] && echo "SPOTIFY_CLIENT_SECRET=$SPOTIFY_CLIENT_SECRET"
  [[ -n "$SPOTIFY_REDIRECT_URI" ]] && echo "SPOTIFY_REDIRECT_URI=$SPOTIFY_REDIRECT_URI"

  [[ -n "$USE_EMULATOR" ]] && echo "USE_EMULATOR=$USE_EMULATOR"
} > .env

echo ".env file created successfully."