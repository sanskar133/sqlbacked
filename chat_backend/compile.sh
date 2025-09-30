#!/bin/bash

ROOT_DIR="compile"

rm -rf $ROOT_DIR
find . -name "*.pyc" -exec rm -f {} \;
find . -name "__pycache__" -exec rm -rf {} \;


folders=($(ls -d */))

# echo ${folders[@]}

# Find all files recursively starting from the ROOT_DIR
files=$(find . -type f)

# Loop through each file and replace .py with .pyc
for file in $files; do
    sed -i 's/\.py/\.pyc/g' "$file"
done

mkdir -p $ROOT_DIR
for folder in "${folders[@]}"; do
    python3.10 -m compileall $folder
    cp -r $folder $ROOT_DIR/$folder
done

files=("requirements.txt" "log_config.conf" "Dockerfile" ".env" ".dockerignore")
for file in "${files[@]}"; do
    cp $file $ROOT_DIR/$file
done

# Loop through all Python files in the current directory
for file in *.py; do
  # Compile the Python file
  python3.10 -m compileall "$file"

  # Copy the compiled bytecode to the root directory's __pycache__ folder
  cp -r __pycache__ "$ROOT_DIR"
done

find $ROOT_DIR -type f -name "*.py" ! -name '__init__.py' -delete
sudo apt install rename -f
find $ROOT_DIR -type f -exec rename 's/.cpython-310//' {} \;
# Find all .pyc files in nested __pycache__ directories and move them one directory up
find $ROOT_DIR -type d -name '__pycache__' -exec sh -c 'mv -n "$0"/*.pyc "$0"/..' {} \;
# Remove all __pycache__ directories
find $ROOT_DIR -type d -name '__pycache__' -exec rm -r {} +


# # Loop through each file and replace .py with .pyc
# for file in $files; do
#     sed -i 's/\.py/\.pyc/g' "$file"
# done

# # Replace ./local_volume with ../local_volume
# sed -i 's/\.\/local_volume/\.\.\/local_volume/g' $ROOT_DIR/docker-compose.yml

# Delete all source files
find . -maxdepth 1 ! -name $ROOT_DIR ! -name 'local_volume' -exec rm -r {} +
# Retain git data
# find . -maxdepth 1 -type d ! -name $ROOT_DIR ! -name '.git' ! -name 'local_volume' -exec rm -r {} +

# Move everything one level up.
mv $ROOT_DIR/{*,.*} .

# Clean compile folder
rm -rf $ROOT_DIR
rm -rf README.md