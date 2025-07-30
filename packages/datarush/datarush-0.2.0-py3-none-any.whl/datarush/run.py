"""Functions for executing DataRush templates."""

import argparse
from typing import Any

from datarush.core.templates import get_template_manager, template_to_dataflow
from datarush.core.types import ParameterSpec
from datarush.utils.type_utils import convert_to_type


def run_template(name: str, version: str, parameters: dict[str, Any] | None = None) -> None:
    """Run a template by its name and version."""
    template = get_template_manager().read_template(name, version)
    dataflow = template_to_dataflow(template)
    if parameters:
        parameter_values = _parse_parameter_values_from_specs(
            parameter_specs=dataflow.parameters, parameter_values=parameters
        )
        dataflow.set_parameters_values(parameter_values)
    dataflow.run()


def run_template_from_command_line() -> None:
    """Run a template using command-line arguments."""
    argparser = argparse.ArgumentParser(description="Datarush Template Runner")

    argparser.add_argument(
        "--template", type=str, required=True, help="Name of the template to run"
    )
    argparser.add_argument(
        "--version", type=str, required=True, help="Version of the template to run"
    )

    args, _ = argparser.parse_known_args()

    template = get_template_manager().read_template(args.template, args.version)
    dataflow = template_to_dataflow(template)

    for param in dataflow.parameters:
        argparser.add_argument(
            f"--{param.name}",
            type=str,
            default=param.default or None,
            help=param.description,
            required=param.required,
        )

    args = argparser.parse_args()

    parameter_values = _parse_parameter_values_from_specs(dataflow.parameters, vars(args))
    dataflow.set_parameters_values(parameter_values)
    dataflow.run()


def _parse_parameter_values_from_specs(
    parameter_specs: list[ParameterSpec], parameter_values: dict[str, str]
) -> dict[str, Any]:
    """Convert parameter values to their specified types."""
    for spec in parameter_specs:
        if spec.name not in parameter_values and spec.required:
            raise ValueError(f"Parameter {spec.name} not found in the provided values")

    return {
        spec.name: convert_to_type(
            value=parameter_values.get(spec.name, spec.default),
            to_type=spec.type.get_type(),
        )
        for spec in parameter_specs
    }
