
# ASSUMING PEOPLE HAVE PYTHON ENVIRONMENT AND STUFF FIGURED OUT. ENSURE SO THAT THEY DON'T HAVE TO DO MENIAL TASKS.
# ASSUMPTIONS:
# - They have python installed.
# - They have their own environments set
# - They don't know about ollama yet. So they don't have it downloaded.
# - They don't have any of the required dependencies.


# Function to display RAM and ROM information
display_ram_and_rom() {
    # Get RAM (Memory) information
    echo "RAM (Memory) Information:"
    ram_info=$(systeminfo | grep "Total Physical Memory")
    echo "$ram_info"

    # Extract maximum RAM size
    ram_max=$(echo "$ram_info" | awk '{print $NF}')

    # Get ROM (Disk) information
    echo "ROM (Disk) Information:"
    rom_info=$(df -h . | tail -1)
    echo "$rom_info"

    # Extract maximum and current ROM (disk) sizes
    rom_max_current=$(echo "$rom_info" | awk '{print $2 " (" $3 "/" $2 ")"}')

    # Call function with RAM and ROM information
    ollama_check "$ram_max" "$rom_max_current"
}

# Function to check the version of Ollama and install required models
ollama_check() {
    # Check if ollama command exists and get its version
    if command -v ollama &> /dev/null; then
        ollama_version=$(ollama --version 2>&1)
        echo "Ollama version: $ollama_version"

        # Check if Ollama models are installed
        ollama_list=$(ollama list)
        
        # Check RAM size
        ram_size=$1
        if [[ $ram_size -lt 16000 ]]; then
            # If RAM is less than 16GB, install gemma:2b, tinyllama, llama2
            required_models=("gemma:2b" "tinyllama:latest" "llava:latest")
        elif [[ $ram_size -ge 8000 && $2 == "available" ]]; then
            # If RAM is greater than or equal to 16GB and GPU is available, install gemma:2b, tinyllama, llama2, llava
            required_models=("gemma:2b" "tinyllama:latest" "llama2-uncensored:latest" "llava:latest")
        fi

        # Check if all required models are installed
        missing_models=()
        for model in "${required_models[@]}"; do
            if ! echo "$ollama_list" | grep -q "$model"; then
                missing_models+=("$model")
            fi
        done

        if [[ ${#missing_models[@]} -gt 0 ]]; then
            echo "Downloading required Ollama models..."
            # Download required Ollama models
            for model in "${missing_models[@]}"; do
                ollama pull "$model"
            done

            # Check if all required models are installed
            ollama_list=$(ollama list)
            missing_models=()
            for model in "${required_models[@]}"; do
                if ! echo "$ollama_list" | grep -q "$model"; then
                    missing_models+=("$model")
                fi
            done

            if [[ ${#missing_models[@]} -eq 0 ]]; then
                echo "Required Ollama models installed."
                return
            else
                echo "Failed to install required Ollama models."
                exit 1
            fi
        else
            echo "Required Ollama models already installed."
            return
        fi
    else
        echo "Ollama not found. Please install Ollama from 'https://ollama.com/download'"
        exit 1
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

# Function to get Whisper model
get_whisper() {
    # Check if "./models" directory exists
    if [ ! -d "./models" ]; then
        echo "Creating './models' directory..."
        mkdir "./models"
        echo "'./models' directory created successfully."
    else
        echo "'./models' directory already exists."
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
            return
        else
            echo "'./models' directory is not empty. Skipping installation."
            return
        fi
    fi
}

# Function to run the Python application
run_app() {
    echo "Running the application..."
    # Replace `python app.py` with your command to run the Python application
    streamlit run app.py
}

# Function to install Python requirements from requirements.txt
install_requirements() {
    echo "Installing Python requirements..."
    # Install requirements.txt using pip
    pip install -r requirements.txt
    echo "Python requirements installed successfully."
}

# Main function to execute the script
main() {
    display_ram_and_rom
    create_sessions_folder
    create_checkpoints_folder
    install_requirements
    get_whisper
}

# Execute main function
main

# Wait for user input before exiting
read -p "Environment setup complete. Please press any key to exit..."
