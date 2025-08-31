#!/bin/bash

# This script creates an annotated Git tag for a project milestone and pushes it to the remote repository.

# --- Functions ---

# Function to display usage information
usage() {
    echo "Usage: $0 -v <version> -m <message>"
    echo "  -v <version>  : The version for the tag (e.g., v1.0-initial-release)."
    echo "  -m <message>  : The message for the annotated tag."
    exit 1
}

# --- Main Script ---

# --- Option Parsing ---
# The while loop and getopts command is used to handle command-line options.
# 'v:' and 'm:' specify that the -v and -m options require an argument.
# The 'opt' variable will hold the option character that is currently being processed.
while getopts "v:m:" opt; do
    # The 'case' statement checks the value of the 'opt' variable and executes the corresponding code block.
    case $opt in
        v)
            # The 'OPTARG' variable contains the argument that was passed to the option.
            version="$OPTARG"
            ;;
        m)
            message="$OPTARG"
            ;;
        # The '\?' case is executed if an invalid option is specified.
        \?)
            usage
            ;;
    esac
done

# --- Argument Validation ---

# Check if the version and message were provided
if [ -z "$version" ] || [ -z "$message" ]; then
    echo "Error: Both version and message are required."
    usage
fi

# --- Git Operations ---

# Create an annotated Git tag
echo "Creating annotated tag: $version"
git tag -a "$version" -m "$message"

# Push the tag to the remote repository
echo "Pushing tag to remote..."
git push origin "$version"

echo "Milestone tag created and pushed successfully."
