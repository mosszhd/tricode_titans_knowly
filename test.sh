#!/bin/bash

# Function to check if Python Interpreter exists
check_python() {
    if command -v python3 &>/dev/null; then
        python_version=$(python --version 2>&1)
        if [[ $python_version == *"Python 3.10"* ]]; then
            echo "Python interpreter found. Version: $python_version"
            return 0 # Success
        else
            echo "Python 3.10 is not installed. This can be a problem, please visit https://www.python.org/downloads/"
            return 1
        fi
    else
        echo "Python interpreter not found. Please install Python 3.10 from https://www.python.org/downloads/"
        exit 1
    fi
    
}

# Function to install Python requirements from requirements.txt
install_requirements() {
    echo "Installing Python requirements..."
    # Install requirements.txt using pip
    pip install -r requirements.txt
    echo "Python requirements installed successfully."
}

# Function to get Whisper model
get_whisper() {
    # Check if "./models" directory exists
    if [ ! -d "./models" ]; then
        echo "Creating './models' directory..."
        mkdir "./models"
        echo "'./models' directory created successfully."
    else
        echo "'./models' directory already exists."
    fi
    
    # Check if "./models" directory is empty
    if [ -z "$(ls -A ./models)" ]; then
        echo "'./models' directory is empty."
        echo "Executing 'git lfs install'..."
        # Run git lfs install if not already installed
        git lfs install
        echo "Cloning Whisper model..."
        # Clone Whisper model repository
        git clone https://huggingface.co/openai/whisper-small ./models/whisper-small
        echo "Whisper model cloned successfully."
    else
        echo "'./models' directory is not empty. Skipping installation."
    fi
}


# Function to create 'sessions' folder in the root directory
create_sessions_folder() {
    if [ ! -d "sessions" ]; then
        echo "Creating 'sessions' folder..."
        mkdir ./sessions
        echo "'sessions' folder created successfully."
    else
        echo "'sessions' folder already exists."
    fi
}

# Function to create 'sessions' folder in the root directory
create_checkpoints_folder() {
    if [ ! -d "checkpoints" ]; then
        echo "Creating 'checkpoints' folder..."
        mkdir ./checkpoints
        echo "'checkpoints' folder created successfully."
    else
        echo "'checkpoints' folder already exists."
    fi
}

check_pc_config() {
    # Get RAM (Memory) information
    echo "RAM (Memory) Information:"
    ram_info=$(systeminfo | grep "Total Physical Memory")
    echo "$ram_info"

    # Extract maximum RAM size without units
    ram_max=$(echo "$ram_info" | awk '{print $NF}')

    # Check for GPU availability
    has_gpu=$(lspci | grep -i "vga" || lshw -c video | grep -i "product")

    # Check ROM information
    echo "ROM (Disk) Information:"
    rom_info=$(df -h . | tail -1)
    echo "$rom_info"

    # Extract available disk space
    rom_available=$(echo "$rom_info" | awk '{print $4}')

   
   # Check hard disk space requirements
    if (( rom_available < 10000000 )); then
        echo "Insufficient hard disk space. At least 10GB of free space is required."
    elif (( ram_max >= 8000000 && rom_available < 20000000 )); then  # High RAM, but less than 20GB available
        echo "Configuration mismatch. Not enough space in disk. RAM specification matched."
        ollama_check 0
    else
        # Determine PC configuration level
        if (( ram_max < 8000000 && ! "$has_gpu" )); then
            echo "PC configuration mismatch. Sorry, the program is not ideal for your device."
        elif (( ram_max < 8000000 )); then  # RAM less than 8GB, GPU available
            ollama_check 0
        elif (( ram_max >= 16000000 )); then  # RAM 16GB or more, GPU optional
            ollama_check 1
        else  # RAM 8GB or more, GPU check required
            if [ "$has_gpu" ]; then
                ollama_check 1
            else
                ollama_check 0
            fi
        fi
    fi
}




ollama_check(){
    if command -v ollama &> /dev/null; then
        ollama_version=$(ollama --version 2>&1)
        echo "Ollama version: $ollama_version"

        # Check if Ollama models are installed
        ollama_list=$(ollama list)
        
        # Check RAM size
        ram_size=$1
        if [[ $ram_size -eq 0 ]]; then
            required_models=("gemma:2b" "tinyllama:latest" "llava:latest")
            python get_models.py "${required_models[@]}"
        elif [[ $ram_size -eq 1 ]]; then
            required_models=("gemma:2b" "tinyllama:latest" "llama2-uncensored:latest" "llava:latest")
            python get_models.py "${required_models[@]}"
        fi
    else
        echo "Ollama not found. Please install Ollama from 'https://ollama.com/download'"
        exit 1
    fi
}

# Main function to execute the script
main() {
    create_sessions_folder
    create_checkpoints_folder
    check_python
    install_requirements
    check_pc_config
    get_whisper
}

# Execute main function
main

# Wait for user input before exiting
read -p "Environment setup complete. Please press any key to exit..."
