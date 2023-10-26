from fastai.learner import load_learner
import pathlib

temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath


model_path = r"D:/Flask_project/project/trained_model"  # Use forward slashes for paths in Windows

learn = load_learner(model_path)

print("model is successfully loaded")
