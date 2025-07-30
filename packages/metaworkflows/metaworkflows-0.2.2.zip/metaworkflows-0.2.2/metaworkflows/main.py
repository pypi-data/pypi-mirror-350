import argparse
import logging
from metaworkflows.core.job import Job
from metaworkflows.core.pipeline import Pipeline
from metaworkflows import PROJECT_ROOT # To make it available if needed by other parts

logger = logging.getLogger(__name__)

def run_job(args):
    logger.info(f"Attempting to load job from: {args.job_path}")
    try:
        job_definition = Job.from_yaml(args.job_path)
        pipeline = Pipeline(job_definition)
        pipeline.run()
        logger.info(f"Job '{job_definition.job_name}' finished.")
    except FileNotFoundError:
        logger.error(f"Job configuration file not found at {args.job_path}. Ensure the path is correct.")
    except ValueError as ve:
        logger.error(f"Configuration error in job '{args.job_path}': {ve}")
    except Exception as e:
        logger.error(f"An unexpected error occurred while running job from {args.job_path}: {e}", exc_info=True)

def main():
    parser = argparse.ArgumentParser(description="metaworkflows Command Line Interface.")
    subparsers = parser.add_subparsers(title="commands", dest="command", help="Available commands")
    subparsers.required = True # Make subparser command mandatory

    # 'run_job' command
    parser_run_job = subparsers.add_parser("run_job", help="Run an ETL job from a YAML definition file.")
    parser_run_job.add_argument(
        "--job-path",
        required=True,
        type=str,
        help="Path to the ETL job YAML definition file (e.g., jobs/etl/my_job.yaml)."
    )
    parser_run_job.set_defaults(func=run_job)

    # Add other commands here if needed (e.g., validate_job, list_jobs)

    args = parser.parse_args()
    
    # Ensure PROJECT_ROOT is easily accessible if jobs use relative paths from project root
    # and I/O handlers need it. The init.py for metaworkflows package already defines it.
    logger.debug(f"Project root directory: {PROJECT_ROOT}")


    args.func(args)

if __name__ == "__main__":
    # This allows running `python -m metaworkflows.main ...`
    main()