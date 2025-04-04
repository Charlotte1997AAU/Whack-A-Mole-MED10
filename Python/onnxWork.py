import onnx
from onnx import numpy_helper

model = onnx.load("SGD_Model.onnx")

for output in model.graph.output:
    print(output.name)