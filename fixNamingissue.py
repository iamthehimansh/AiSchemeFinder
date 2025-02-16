import os
DATA_PATH = "data"
def load_documents():
    documents = []
    for filename in os.listdir(DATA_PATH):
        if "%20" in filename:
            new_filename = filename.replace("%20", " ")
            os.rename(os.path.join(DATA_PATH, filename), os.path.join(DATA_PATH, new_filename))
            filename = new_filename
    return documents


load_documents()