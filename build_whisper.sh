#!/bin/bash

# Resolve the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")
WHISPER_DIR=$1
if [ $# -eq 0 ]; then
    echo "No whisper.cpp dir provided! Searching in same directory ..."
    WHISPER_DIR="$(dirname "$(realpath "$0")")/whisper.cpp"
fi

# Change to the whisper.cpp directory
cd "$WHISPER_DIR" || exit

# Build the project
make

# Download and make all specified models
#MODELS=("tiny" "base" "small" "medium" "large-v3")
#MODELS=("small")

#for MODEL in "${MODELS[@]}"; do
#    bash ./models/download-ggml-model.sh $MODEL
#done

# Move the downloaded models to the models directory
mv ggml*.bin models/

# Go back to the script directory
cd "$SCRIPT_DIR" || exit

# Create the config.json file with the correct paths
CONFIG_FILE="$SCRIPT_DIR/config.json"

MODELS_PATH="$WHISPER_DIR/models"

cat <<EOL > $CONFIG_FILE
{
    "main_command": "$WHISPER_DIR",
    "models_path": "$MODELS_PATH"
}
EOL

echo "Config file created at $CONFIG_FILE"
