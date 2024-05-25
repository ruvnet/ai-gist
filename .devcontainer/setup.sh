#!/bin/bash

set -e

echo "Setting up the development environment..."

# Install dependencies
pip install -r requirements.txt

# Set up SQLite database
if [ ! -f data/gists.db ]; then
  echo "Creating SQLite database..."
  sqlite3 data/gists.db < .devcontainer/schema.sql
fi

# Menu for additional setup options
while true; do
  echo "Choose an option:"
  echo "1. Install additional packages"
  echo "2. Configure environment variables"
  echo "3. Optimize environment"
  echo "4. Exit"
  read -p "Enter your choice [1-4]: " choice
  case $choice in
    1)
      read -p "Enter package name: " package
      pip install $package
      ;;
    2)
      read -p "Enter environment variable name: " var_name
      read -p "Enter environment variable value: " var_value
      export $var_name=$var_value
      echo "export $var_name=$var_value" >> ~/.bashrc
      ;;
    3)
      echo "Optimizing environment..."
      # Add optimization commands here
      ;;
    4)
      break
      ;;
    *)
      echo "Invalid choice!"
      ;;
  esac
done

echo "Setup complete!"
