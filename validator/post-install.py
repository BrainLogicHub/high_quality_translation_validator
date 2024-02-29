from comet import download_model, load_from_checkpoint

# Download the model during post installation
# to reduce latency during the first validation
MODEL_NAME = "Unbabel/wmt22-cometkiwi-da"
try:
    # Download and load the model
    print(f"Loading the model {MODEL_NAME}...")
    model_path = download_model(MODEL_NAME)
    model = load_from_checkpoint(model_path)
except Exception as e:
    raise RuntimeError(
        f"Error while downloading the model {MODEL_NAME} "
        "from COMET: {e}.\n Please review the validator "
        "documentation for more details on the pre-requisites."
        "Ensure that you are logged into Huggingface Hub."
    ) from e
