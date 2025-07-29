# Task 5 - Create the python package

A simple CLI application that counts characters which occur exactly once in a string.

## Features

- Accepts either a string or a file as input
- Prioritizes file input if both are provided
- Counts letters that occur only once

## Usage

Run from the command line:
python -m collection --string "aaaabccccdfg"
or
python -m collection --file path_to_file.txt

## Installation

git clone https://github.com/your-username/task-4-cli.git
cd task-4-cli
pip install -r requirements.txt

## Tests

pytest