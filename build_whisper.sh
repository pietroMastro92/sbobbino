#!/bin/bash

# Resolve the script directory
SCRIPT_DIR=$(dirname "$(realpath "$0")")

# Change to the whisper.cpp directory
cd "$SCRIPT_DIR/whisper.cpp" || exit

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

MAIN_COMMAND_PATH="$SCRIPT_DIR/whisper.cpp"
MODELS_PATH="$SCRIPT_DIR/whisper.cpp/models"

cat <<EOL > $CONFIG_FILE
{
    "main_command": "$MAIN_COMMAND_PATH",
    "models_path": "$MODELS_PATH"
}
EOL

echo "Config file created at $CONFIG_FILE"
