#!/bin/bash

echo "Enter the name for the new directory:"
read NEW_DIR

if [ ! -d "$NEW_DIR" ]; then
  mkdir -p "$NEW_DIR"
  echo "Directory $NEW_DIR created."
else
  echo "Directory $NEW_DIR already exists."
fi

echo "Enter the names of the files to create (space-separated):"
read FILE_NAMES

for FILE in $FILE_NAMES; do
  touch "$NEW_DIR/$FILE"
  echo "File $FILE created in $NEW_DIR."
done
