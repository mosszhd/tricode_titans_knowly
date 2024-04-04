
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

ollama_check() {
  # Check if ollama command exists and get its version
  if command -v ollama &> /dev/null; then
    ollama_version=$(ollama --version 2>&1)
    echo "Ollama version: $ollama_version"

    # Determine runtime based on argument (0: low config, 1: high config)
    if [[ $1 -eq 0 ]]; then
      # Run ollama serve (assuming low configuration)
      ollama serve &
      ollama_serve_pid=$!
      echo "Ollama server started in background (PID: $ollama_serve_pid)"
    else
      # Check Ollama models (assuming high configuration)
      ollama_list=$(ollama list)

      # Check RAM size
      ram_size=$2
      if [[ $ram_size -lt 16000 ]]; then
        # If RAM is less than 16GB, install gemma:2b, tinyllama, llama2
        required_models=("gemma:2b" "tinyllama" "llama2")
      elif [[ $ram_size -ge 8000 && $3 == "available" ]]; then
        # If RAM is greater than or equal to 16GB and GPU is available, install gemma:2b, tinyllama, llama2, llava
        required_models=("gemma:2b" "tinyllama" "llama2" "llava")
      fi

        # Determine argument to pass to ollama.py based on required models
        model_arg=0  # Default argument (assuming low configuration)
        if [[ "${#required_models[@]}" -eq 4 ]]; then
            model_arg=1  # Argument for high configuration with all models
        fi

        # Call ollama.py with the appropriate argument (**assuming `ollama.py` exists and accepts this argument**)
        python ollama_model_loading.py check_and_pull_models $model_arg  # Replace with the actual call to your Python script
        
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
    run_app
}

# Execute main function
main

# Wait for user input before exiting
read -p "Environment setup complete. Please press any key to exit..."
