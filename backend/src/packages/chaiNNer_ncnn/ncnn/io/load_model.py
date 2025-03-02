from __future__ import annotations

from typing import Tuple

from nodes.group import group
from nodes.impl.ncnn.model import NcnnModel, NcnnModelWrapper
from nodes.impl.ncnn.optimizer import NcnnOptimizer
from nodes.properties.inputs import BinFileInput, ParamFileInput
from nodes.properties.outputs import DirectoryOutput, FileNameOutput, NcnnModelOutput
from nodes.utils.utils import split_file_path

from .. import io_group


@io_group.register(
    schema_id="chainner:ncnn:load_model",
    name="Load Model",
    description="Load NCNN model (.bin and .param files). Theoretically supports any NCNN Super-Resolution model that doesn't expect non-standard preprocessing.",
    icon="NCNN",
    inputs=[
        group("ncnn-file-inputs")(
            ParamFileInput(primary_input=True),
            BinFileInput(primary_input=True),
        )
    ],
    outputs=[
        NcnnModelOutput(kind="tagged"),
        DirectoryOutput("Model Directory", of_input=0).with_id(2),
        FileNameOutput("Model Name", of_input=0).with_id(1),
    ],
    see_also=[
        "chainner:ncnn:model_file_iterator",
    ],
)
def load_model_node(
    param_path: str, bin_path: str
) -> Tuple[NcnnModelWrapper, str, str]:
    model = NcnnModel.load_from_file(param_path, bin_path)
    NcnnOptimizer(model).optimize()

    model_dir, model_name, _ = split_file_path(param_path)

    return NcnnModelWrapper(model), model_dir, model_name
