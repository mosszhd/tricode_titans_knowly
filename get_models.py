import ollama
import yaml
from ollama import delete

def check_and_pull_models(model_option=0):
  """
  This function checks for Ollama models based on the provided integer parameter.

  Args:
      model_option (int): An integer (0 or 1) indicating which models to check.
          - 0: Checks for gemma:2b, tinyllama:latest, and llava:latest.
          - 1: Checks for all models mentioned above and llama2-uncensored:latest.
  """

  models_to_check = ["gemma:2b", "tinyllama:latest", "llava:latest"]
  if model_option == 1:
    models_to_check.append()
  models = ollama.list()
  available_models = {model["name"]: model for model in models["models"]}
  model_list = list(available_models.keys())
  models_to_pull = set(models_to_check) - set(model_list) 
 
  if models_to_pull:
    print("Models to pull:")
    for model_name in models_to_pull:
      print(f"  - {model_name}")
      print(f"Initializing {model_name} pull..")
      print("Please be patient as it may take a while depending on the speed of your internet...")
      ollama.pull(model_name)
      print(f"{model_name} is ready..")
      print(f"We appreciate your patience while we get the environment ready for you.")

    print("Ollama models ready for finetuning!")
  else:
      print("All model requirements fulfilled.")
  
  create_knowly_models(models_to_check)

def create_knowly_models(models_list):
  for model in models_list:
        if "gemma" in model:
            ollama.create(model="KnowlyGemma",path="./modelfiles/gemma/Modelfile")
        elif "tiny" in model:
            ollama.create(model="KnowlyTinyLlama",path="./modelfiles/tinyllama/Modelfile")
        elif "llava" in model:
            ollama.create(model="KnowlyLlava",path="./modelfiles/llava/Modelfile")
        else:
            ollama.create(model="KnowlyLlama2",path="./modelfiles/llama2/Modelfile")
  
  print("Model finetuning complete.")
  if False:
    for model in models_list:
      delete_ollama_model(model)


def delete_ollama_model(model_name: str) -> None:
  """
  Deletes an Ollama model by name.

  Args:
      model_name (str): The name of the Ollama model to be deleted.

  Raises:
      Exception: If the model deletion fails.
  """
  try:
    delete(model_name)
    print(f"Model '{model_name}' deleted successfully.")
  except Exception as e:
    print(f"Error deleting model '{model_name}': {e}")
   

if __name__ == "__main__":
   check_and_pull_models()