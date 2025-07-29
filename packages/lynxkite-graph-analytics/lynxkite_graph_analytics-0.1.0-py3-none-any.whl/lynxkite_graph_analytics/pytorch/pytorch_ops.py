"""Boxes for defining PyTorch models."""

import enum
from lynxkite.core import ops
from lynxkite.core.ops import Parameter as P
import torch
from .pytorch_core import op, reg, ENV

reg("Input: tensor", outputs=["output"], params=[P.basic("name")], color="gray")
reg("Input: graph edges", outputs=["edges"], params=[P.basic("name")], color="gray")
reg("Input: sequential", outputs=["y"], params=[P.basic("name")], color="gray")
reg("Output", inputs=["x"], outputs=["x"], params=[P.basic("name")], color="gray")


@op("LSTM", weights=True)
def lstm(x, *, input_size=1024, hidden_size=1024, dropout=0.0):
    return torch.nn.LSTM(input_size, hidden_size, dropout=dropout)


reg(
    "Neural ODE with MLP",
    color="blue",
    inputs=["x", "y0", "t"],
    outputs=["y"],
    params=[
        P.options(
            "method",
            [
                "dopri8",
                "dopri5",
                "bosh3",
                "fehlberg2",
                "adaptive_heun",
                "euler",
                "midpoint",
                "rk4",
                "explicit_adams",
                "implicit_adams",
            ],
        ),
        P.basic("relative_tolerance"),
        P.basic("absolute_tolerance"),
        P.basic("mlp_layers"),
        P.basic("mlp_hidden_size"),
        P.options("mlp_activation", ["ReLU", "Tanh", "Sigmoid"]),
    ],
)


@op("Attention", outputs=["outputs", "weights"])
def attention(query, key, value, *, embed_dim=1024, num_heads=1, dropout=0.0):
    return torch.nn.MultiHeadAttention(embed_dim, num_heads, dropout=dropout, need_weights=True)


@op("LayerNorm", outputs=["outputs", "weights"])
def layernorm(x, *, normalized_shape=""):
    normalized_shape = [int(s.strip()) for s in normalized_shape.split(",")]
    return torch.nn.LayerNorm(normalized_shape)


@op("Dropout", outputs=["outputs", "weights"])
def dropout(x, *, p=0.0):
    return torch.nn.Dropout(p)


@op("Linear", weights=True)
def linear(x, *, output_dim=1024):
    import torch_geometric.nn as pyg_nn

    return pyg_nn.Linear(-1, output_dim)


@op("Mean pool")
def mean_pool(x):
    import torch_geometric.nn as pyg_nn

    return pyg_nn.global_mean_pool


class ActivationTypes(str, enum.Enum):
    ReLU = "ReLU"
    Leaky_ReLU = "Leaky ReLU"
    Tanh = "Tanh"
    Mish = "Mish"


@op("Activation")
def activation(x, *, type: ActivationTypes = ActivationTypes.ReLU):
    return getattr(torch.nn.functional, type.name.lower().replace(" ", "_"))


@op("MSE loss")
def mse_loss(x, y):
    return torch.nn.functional.mse_loss


@op("Constant vector")
def constant_vector(*, value=0, size=1):
    return lambda _: torch.full((size,), value)


@op("Softmax")
def softmax(x, *, dim=1):
    return torch.nn.Softmax(dim=dim)


@op("Embedding", weights=True)
def embedding(x, *, num_embeddings: int, embedding_dim: int):
    return torch.nn.Embedding(num_embeddings, embedding_dim)


@op("Concatenate")
def concatenate(a, b):
    return lambda a, b: torch.concatenate(*torch.broadcast_tensors(a, b))


reg(
    "Pick element by index",
    inputs=["x", "index"],
    outputs=["x_i"],
)
reg(
    "Pick element by constant",
    inputs=["x"],
    outputs=["x_i"],
    params=[ops.Parameter.basic("index", "0")],
)
reg(
    "Take first n",
    inputs=["x"],
    outputs=["x"],
    params=[ops.Parameter.basic("n", 1, int)],
)
reg(
    "Drop first n",
    inputs=["x"],
    outputs=["x"],
    params=[ops.Parameter.basic("n", 1, int)],
)
reg(
    "Graph conv",
    color="blue",
    inputs=["x", "edges"],
    outputs=["x"],
    params=[P.options("type", ["GCNConv", "GATConv", "GATv2Conv", "SAGEConv"])],
)
reg(
    "Heterogeneous graph conv",
    inputs=["node_embeddings", "edge_modules"],
    outputs=["x"],
    params=[
        ops.Parameter.basic("node_embeddings_order"),
        ops.Parameter.basic("edge_modules_order"),
    ],
)

reg("Triplet margin loss", inputs=["x", "x_pos", "x_neg"], outputs=["loss"])
reg("Cross-entropy loss", inputs=["x", "y"], outputs=["loss"])
reg(
    "Optimizer",
    inputs=["loss"],
    outputs=[],
    params=[
        P.options(
            "type",
            [
                "AdamW",
                "Adafactor",
                "Adagrad",
                "SGD",
                "Lion",
                "Paged AdamW",
                "Galore AdamW",
            ],
        ),
        P.basic("lr", 0.0001),
    ],
    color="green",
)

ops.register_passive_op(
    ENV,
    "Repeat",
    inputs=[ops.Input(name="input", position="top", type="tensor")],
    outputs=[ops.Output(name="output", position="bottom", type="tensor")],
    params=[
        ops.Parameter.basic("times", 1, int),
        ops.Parameter.basic("same_weights", False, bool),
    ],
)

ops.register_passive_op(
    ENV,
    "Recurrent chain",
    inputs=[ops.Input(name="input", position="top", type="tensor")],
    outputs=[ops.Output(name="output", position="bottom", type="tensor")],
    params=[],
)


def _set_handle_positions(op):
    op: ops.Op = op.__op__
    for v in op.outputs:
        v.position = ops.Position.TOP
    for v in op.inputs:
        v.position = ops.Position.BOTTOM


def _register_simple_pytorch_layer(func):
    op = ops.op(ENV, func.__name__.title())(lambda input: func)
    _set_handle_positions(op)


def _register_two_tensor_function(func):
    op = ops.op(ENV, func.__name__.title())(lambda a, b: func)
    _set_handle_positions(op)


SIMPLE_FUNCTIONS = [
    torch.sin,
    torch.cos,
    torch.log,
    torch.exp,
]
TWO_TENSOR_FUNCTIONS = [
    torch.multiply,
    torch.add,
    torch.subtract,
]


for f in SIMPLE_FUNCTIONS:
    _register_simple_pytorch_layer(f)
for f in TWO_TENSOR_FUNCTIONS:
    _register_two_tensor_function(f)
