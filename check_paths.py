import os
print("Current Directory:", os.getcwd())
print("Files here:", os.listdir())
if os.path.exists("evaluation"):
    print("Found evaluation folder!")
    print("Inside evaluation:", os.listdir("evaluation"))