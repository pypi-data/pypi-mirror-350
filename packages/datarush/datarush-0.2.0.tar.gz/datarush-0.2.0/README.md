# DataRush

No-Code Data Pipelines

## Installation
```bash
pip install datarush
```

## Settings

Before running the application, ensure the following environment variables are configured. The use of a `.env` file is supported.

| Name                             | Description                                                        | Default Value |
| -------------------------------- | ------------------------------------------------------------------ | ------------- |
| `TEMPLATE_STORE_TYPE`            | Specifies the template store type: `S3` or `FILESYSTEM`.           |               |
| `TEMPLATE_STORE_S3_BUCKET`       | The S3 bucket to store templates when using the S3 store type.     |               |
| `TEMPLATE_STORE_S3_PREFIX`       | The S3 prefix for templates when using the S3 store type.          | `datarush`    |
| `TEMPLATE_STORE_FILESYSTEM_PATH` | The filesystem path for templates when using the filesystem store. | `.`           |
| `S3_ENDPOINT`                    | The endpoint URL for the S3 service.                               |               |
| `S3_ACCESS_KEY`                  | The access key for the S3 service.                                 |               |
| `S3_SECRET_KEY`                  | The secret key for the S3 service.                                 |               |
| `S3_DEFAULT_BUCKET`              | The default bucket suggested in the operations UI.                 |               |

## Running UI
To launch the DataRush user interface, follow these steps:

1. Create a `run_ui.py` file to serve as the entry point for the Streamlit application:
    ```python
    from datarush import run_ui

    if __name__ == "__main__":
        run_ui()
    ```

2. Start the application using the Streamlit command:
    ```bash
    streamlit run run_ui.py
    ```

## Running Templates
To execute a DataRush template, use the following commands:

- For a template named `foo` with version `0.0.1`:
    ```bash
    python -m datarush --template "foo" --version "0.0.1"
    ```

- To pass additional input arguments supported by the template:
    ```bash
    python -m datarush --template "foo" --version "0.0.1" --other_argument "value"
    ```