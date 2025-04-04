import onnx
from onnx import numpy_helper

model = onnx.load("SGD_Model.onnx")
nodesToRemove = []
for node in model.graph.node:
    if node.op_type == "ZipMap":
        nodesToRemove.append(node)

for node in model.graph.node:
    if node.op_type == "ArrayFeatureExtractor":
        nodesToRemove.append(node)

for output in model.graph.output:
    if output.name == "output_label":
        output.name = "final_label"


for node in nodesToRemove:
    model.graph.node.remove(node)

onnx.save(model, "modified_sgd_model.onnx")

modified_model = onnx.load("modified_sgd_model.onnx")

for output in modified_model.graph.output:
    print(output.name)


print("Nodes:")
for node in modified_model.graph.node:
    print(node.op_type)

print("\nOutputs:")
for output in modified_model.graph.output:
    print(output.name)
