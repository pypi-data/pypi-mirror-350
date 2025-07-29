# metaworkflows: A Metadata-Driven ETL Framework

metaworkflows is a Python-based framework for building robust and extensible ETL pipelines.
It leverages YAML configuration files to define ETL jobs, allowing for a clear
separation of logic and configuration.

## Features

- **Metadata-Driven:** Define ETL jobs, sources, sinks, and transformations in YAML.
- **Extensible Engine Support:** Currently supports Python scripts and Apache Spark. Easily extendable to other engines (e.g., Flink).
- **Versatile I/O:** Connect to various databases (PostgreSQL, MySQL, etc.) and object storage services (Google Cloud Storage, AWS S3, etc.).
- **SOLID Design:** Built with SOLID principles in mind for maintainability and scalability.
- **Spark SQL Transformations:** Define Spark transformations using SQL.
- **Configurable Spark:** Specify Spark configurations directly in your job YAML.

## Project Structure

```
metaworkflows/
├── README.md
├── setup.py
├── .gitignore
├── requirements.txt
├── config/
│ ├── connections.yaml.example # Example connection configurations
│ ├── connections.yaml # User-specific connection configurations
│ └── logging.conf
├── metaworkflows/ # Source code directory
│ ├── **init**.py # Makes 'metaworkflows' a package
│ ├── main.py # CLI entry point
│ ├── core/
│ │ ├── **init**.py
│ │ ├── job.py
│ │ └── pipeline.py
│ ├── engines/
│ │ ├── **init**.py
│ │ ├── base.py
│ │ ├── python_engine.py
│ │ ├── spark_engine.py
│ │ └── flink_engine.py # Placeholder for Flink
│ ├── io/
│ │ ├── **init**.py
│ │ ├── base.py
│ │ ├── database.py
│ │ ├── file.py
│ │ ├── object_storage.py
│ │ ├── postgres_database.py
│ │ └── gcp_object_storage.py
│ └── transformers/
│ ├── **init**.py
│ ├── base.py
│ └── sql.py
└── tests/
├── **init**.py
├── test_config.py
├── test_engines.py
└── test_io.py
```

## Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd metaworkflows
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure connections:**
    Copy `config/connections.yaml.example` to `config/connections.yaml` and update
    with your database and storage credentials.

## Usage

To run an ETL job via the command line:

```bash
python -m metaworkflows.main run_job --job-path jobs/etl/your_job.yaml
```

Or programmatically:

```python
from metaworkflows.core.pipeline import Pipeline
from metaworkflows.core.job import Job

# Ensure your current working directory is the project root
job_definition = Job.from_yaml("jobs/etl/spark_job.yaml")
pipeline = Pipeline(job_definition)
pipeline.run()
```
