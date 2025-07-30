"""Form rendering functions."""

# flake8: noqa: D103
from __future__ import annotations

from typing import Any, Type, cast, get_args

import jinja2
import streamlit as st
from pydantic import BaseModel, ValidationError
from pydantic_core import PydanticUndefined
from streamlit_ace import st_ace

from datarush.core.dataflow import Operation, Tableset
from datarush.core.types import ColumnStr, ColumnStrMeta, ContentType, TableStr
from datarush.ui.state import get_dataflow
from datarush.utils.jinja2 import render_jinja2_template
from datarush.utils.type_utils import convert_to_type, is_literal, is_string_enum, types_are_equal


def operation_from_streamlit[T: Operation](
    operation_type: Type[T], tableset: Tableset | None = None, key: int | str | None = None
) -> T | None:
    """Render a streamlit form for a given operation type and return the operation instance."""
    try:
        model_dict = model_dict_from_streamlit(
            operation_type.schema(),
            tableset=tableset,
            key=key,
        )
        return operation_type(model_dict)
    except ValidationError as e:
        return None


def update_operation_from_streamlit(
    operation: Operation, tableset: Tableset | None = None, key: int | str | None = None
) -> bool:
    """Update the operation instance from a streamlit form."""
    model_dict = model_dict_from_streamlit(
        operation.schema(),
        tableset=tableset,
        key=key,
        current_model_dict=operation.model_dict,
        advanced_mode=operation.advanced_mode,
    )
    if operation.model_dict == model_dict:
        return False

    if st.button("Update", f"operation_update_button_{key}"):
        operation._model_dict = model_dict
        return True

    return False


def model_from_streamlit[T: BaseModel](
    schema: Type[T],
    tableset: Tableset | None = None,
    key: str | int | None = None,
    current_model: T | None = None,
) -> T:
    """Render a streamlit form based on a Pydantic model and return the model instance.

    Args:
        schema : The Pydantic model class.
        tableset: Optional tableset for table-related fields.
        key: Optional key for Streamlit widgets.
        current_model_dict: Optional current model dictionary to pre-fill values.
    Returns:
        T: The Pydantic model instance with the values from the Streamlit widgets.
    """
    model_dict = model_dict_from_streamlit(
        schema=schema,
        tableset=tableset,
        key=key,
        current_model_dict=current_model.model_dump() if current_model else None,
        advanced_mode=False,
    )
    return schema.model_validate(model_dict)


def model_dict_from_streamlit[T: BaseModel](
    schema: Type[T],
    tableset: Tableset | None = None,
    key: str | int | None = None,
    current_model_dict: dict[str, Any] | None = None,
    advanced_mode: bool = False,
) -> dict[str, Any]:
    """
    Render a streamlit form based on a Pydantic model and return the values as a dictionary.

    Args:
        schema : The Pydantic model class.
        tableset: Optional tableset for table-related fields.
        key: Optional key for Streamlit widgets.
        current_model_dict: Optional current model dictionary to pre-fill values.
        advanced_mode: Flag to enable advanced mode with Jinja2 template rendering.
    Returns:
        dict[str, Any]: The dictionary containing the values from the Streamlit widgets.
    """
    model_dict: dict[str, Any] = {}

    for name, field in schema.model_fields.items():
        kwargs: dict[str, Any] = {
            "label": field.title or name,
            "key": f"{schema.__name__}_{advanced_mode}_{name}_{key or ''}",
            "help": field.description,
        }
        default = field.default if field.default is not PydanticUndefined else None
        current_value = current_model_dict.get(name, None) if current_model_dict else None

        ################################
        ######### ADVANCED MODE ########
        ################################
        if advanced_mode:
            # Display the editor for jinja2 template
            st.write(f"{kwargs['label']} template")
            value = st_ace(
                str(current_value),
                language="django",
                theme="twilight",
                keybinding="vscode",
                # height=70,
                min_lines=3,
                # max_lines=1,
                show_gutter=False,
                auto_update=False,
                key=kwargs["key"] + "_ace",
            )

            # Try to render the template and display the result
            try:
                dataflow_context = get_dataflow().get_current_context()
                rendered_value = render_jinja2_template(value, context=dataflow_context)
                # validate by trying to convert
                convert_to_type(rendered_value, to_type=field.annotation)
                # Display the rendered value
                st.write(f"{kwargs['label']} value")
                st.code(rendered_value)
                st.write("___")
            except jinja2.exceptions.TemplateSyntaxError as e:
                st.error(f"Error rendering template: {e}")
            except ValueError as e:
                st.error(f"Error converting value: {e} to type {field.annotation}")

        ################################
        ############ UI MODE ###########
        ################################
        elif field.annotation is TableStr:
            if tableset:
                options = list(tableset)
                index = options.index(current_value) if current_value is not None else 0
                value = st.selectbox(options=options, index=index, **kwargs)
            else:
                value = st.selectbox(
                    options=[current_value] if current_value is not None else [], **kwargs
                )

        elif types_are_equal(field.annotation, list[TableStr]):
            if tableset:
                options = list(tableset)
                value = st.multiselect(options=options, default=current_value or None, **kwargs)
            else:
                value = st.multiselect(
                    options=current_value or [], default=current_value, **kwargs
                )

        elif field.annotation is ColumnStr or types_are_equal(field.annotation, list[ColumnStr]):
            if tableset:
                relevant_tables = []

                if field.metadata and isinstance(field.metadata[0], ColumnStrMeta):
                    column_meta = field.metadata[0]
                else:
                    column_meta = ColumnStrMeta()

                table = model_dict.get(column_meta.table_field)
                if table:
                    relevant_tables.append(table)

                tables = model_dict.get(column_meta.tables_field, []) + [
                    model_dict.get(table_field) for table_field in column_meta.table_fields or []
                ]
                if tables:
                    relevant_tables.extend(tables)

                relevant_columns = sorted(
                    {col for name in relevant_tables for col in tableset.get_df(name).columns}
                )
                if field.annotation is ColumnStr:
                    index = (
                        relevant_columns.index(current_value) if current_value is not None else 0
                    )
                    value = st.selectbox(options=relevant_columns, index=index, **kwargs)
                else:
                    value = st.multiselect(
                        options=relevant_columns, default=current_value, **kwargs
                    )
            else:
                if field.annotation is ColumnStr:
                    value = st.selectbox(
                        options=[current_value] if current_value is not None else [], **kwargs
                    )
                else:
                    value = st.multiselect(
                        options=current_value or [], default=current_value, **kwargs
                    )
        elif is_literal(field.annotation):
            options = list(get_args(field.annotation))
            value = st.selectbox(options=options, **kwargs)

        elif is_string_enum(field.annotation):
            value = st.selectbox(options=list(field.annotation), **kwargs)  # type: ignore

        elif field.annotation is bytes:
            content_type: ContentType | None = model_dict.get("content_type")
            extension = content_type.extension() if content_type else None
            file = st.file_uploader("Choose File", type=extension, key=f"local_file_file_df_{key}")
            value = file.getvalue() if file else None

        elif field.annotation is bool:
            value = st.checkbox(
                value=cast(bool, current_value if current_value is not None else default), **kwargs
            )

        elif issubclass(field.annotation, str):  # type: ignore
            value = st.text_input(
                value=current_value if current_value is not None else (default or ""), **kwargs
            )

        elif field.annotation is int:
            value = st.number_input(
                value=current_value if current_value is not None else default, step=1, **kwargs
            )

        elif field.annotation is float:
            value = st.number_input(
                value=current_value if current_value is not None else default, step=0.01, **kwargs
            )

        else:
            raise TypeError(f"Not supported type: {field.annotation}")

        if value is not None:
            model_dict[name] = value

    # values in advanced mode are jinja2 templates strings, no point in validating them
    if not advanced_mode:
        schema.model_validate(model_dict)

    return model_dict
