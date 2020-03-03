#!/usr/bin/env bash

# Manage a TaskLight .status file
#
# Version 1.0.0


# Function to show help info - keeps this out of the code
function showHelp {
    echo -e "\ntask 1.0.0\n"
    echo -e "Manage a TaskLight .status file\n"
    echo -e "Usage:\n    task.sh [-r value] [-g value] [-b value]\n"
    echo    "Options:"
    echo    "    -r / --red   [value]  Set the red pixel on (1) or off (0)."
    echo    "    -g / --green [value]  Set the green pixel on (1) or off (0)."
    echo    "    -b / --blue  [value]  Set the blue pixel on (1) or off (0)."
    echo    "    -o / --off            Turn all the pixels off (eg. clear notifications)."
    echo    "    -h / --help           This help screen."
    echo
}


# Initialize variables
argCount=0
argIsAValue=0
red=0
blue=0
green=0
dostop=0
statusfile="$HOME/.status"
# Get the current values
if [ -e "$statusfile" ]; then
    line=$(head -n 1 "$statusfile")
    IFS='.' read -r -a parts <<< "$line"
    red=${parts[0]}
    green=${parts[1]}
    blue=${parts[2]}
fi

# Parse the command line arguments
for arg in "$@"; do
    if [[ "$argIsAValue" -gt 0 ]]; then
        # The argument should be a value (previous argument was an option)
        if [[ ${arg:0:1} = "-" ]]; then
            # Next value is an option: ie. missing value
            echo "Error: Missing value for ${args[((argIsAValue - 1))]}"
            exit 1
        fi

        # Set the appropriate internal value
        case "$argIsAValue" in
            1)  red=$arg ;;
            2)  green=$arg ;;
            3)  blue=$arg ;;
            *)  echo "Error: Unknown argument"; exit 1 ;;
        esac
        argIsAValue=0
    else
        # Make the argument lowercase
        arg=${arg,,}

        if [[ $arg = "-r" || $arg = "--red" ]]; then
            argIsAValue=1
        elif [[ $arg = "-g" || $arg = "--green" ]]; then
            argIsAValue=2
        elif [[ $arg = "-b" || $arg = "--blue" ]]; then
            argIsAValue=3
        elif [[ $arg = "-s" || $arg = "--stop" ]]; then
            dostop=1
        elif [[ $arg = "-h" || $arg = "--help" ]]; then
            showHelp
            exit 0
        elif [[ $arg = "-o" || $arg = "--off" ]]; then
            echo "0.0.0.0." > "$statusfile"
            exit 0
        else
            echo "[ERROR] Unknown switch: $arg"
            exit 1
        fi
    fi

    ((argCount++))

    if [[ "$argCount" -eq $# && "$argIsAValue" -ne 0 ]]; then
        echo "[Error] Missing value for $arg"
        exit 1
    fi
done

echo "$red.$green.$blue.$dostop." > "$statusfile"