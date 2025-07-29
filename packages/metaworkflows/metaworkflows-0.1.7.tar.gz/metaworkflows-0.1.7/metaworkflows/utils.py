import yaml
from typing import Dict, List, Any, Set
import jsonschema
from metaworkflows.constants import SUPPORTED_CONNECTORS, SUPPORTED_ENGINES, SUPPORTED_STEP_TYPES, SUPPORTED_FILE_FORMATS, SUPPORTED_WRITE_MODES

class JobValidator:
    """Validator for ETL job configuration files."""
    
    # Define supported engines, step types, connectors, etc.
    SUPPORTED_ENGINES = SUPPORTED_ENGINES
    SUPPORTED_STEP_TYPES = SUPPORTED_STEP_TYPES
    SUPPORTED_CONNECTORS = SUPPORTED_CONNECTORS
    SUPPORTED_FILE_FORMATS = SUPPORTED_FILE_FORMATS
    SUPPORTED_WRITE_MODES = SUPPORTED_WRITE_MODES
    
    # Schema for validation
    JOB_SCHEMA = {
        "type": "object",
        "required": ["job_name", "version", "engine", "steps"],
        "properties": {
            "job_name": {"type": "string"},
            "description": {"type": "string"},
            "version": {"type": "string"},
            "engine": {
                "type": "object",
                "required": ["type"],
                "properties": {
                    "type": {"type": "string"},
                    "config": {"type": "object"}
                }
            },
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["step_name", "type"],
                    "properties": {
                        "step_name": {"type": "string"},
                        "type": {"type": "string"},
                        "connector": {"type": "string"},
                        "connection_ref": {"type": "string"},
                        "options": {"type": "object"},
                        "output_alias": {"type": "string"},
                        "input_alias": {"type": "string"},
                        "input_aliases": {"type": "array", "items": {"type": "string"}},
                        "engine_specific": {"type": "object"}
                    }
                }
            }
        }
    }
    
    @classmethod
    def validate_job_config(cls, config: Dict[str, Any]) -> List[str]:
        """
        Validate a job configuration dictionary.
        
        Args:
            config: The job configuration dictionary
            
        Returns:
            List of validation errors, empty if valid
        """
        errors = []
        
        # Validate against schema
        try:
            jsonschema.validate(instance=config, schema=cls.JOB_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            errors.append(f"Schema validation error: {e.message}")
            return errors
        
        # Validate engine type
        engine_type = config["engine"]["type"]
        if engine_type not in cls.SUPPORTED_ENGINES:
            errors.append(f"Unsupported engine type: {engine_type}. Supported engines: {', '.join(cls.SUPPORTED_ENGINES)}")
        
        # Track defined dataframes for reference validation
        defined_dataframes = set()
        step_names = set()
        
        # Validate steps
        for i, step in enumerate(config["steps"]):
            step_num = i + 1
            step_name = step.get("step_name", f"Step {step_num}")
            
            # Check for duplicate step names
            if step_name in step_names:
                errors.append(f"Duplicate step name: {step_name}")
            step_names.add(step_name)
            
            # Validate step type
            step_type = step.get("type")
            if step_type not in cls.SUPPORTED_STEP_TYPES:
                errors.append(f"Unsupported step type in {step_name}: {step_type}")
                continue
            
            # Step-specific validation
            if step_type == "read":
                errors.extend(cls._validate_read_step(step, step_name))
                # Add output dataframe to defined set
                if "output_alias" in step:
                    defined_dataframes.add(step["output_alias"])
            
            elif step_type == "transform":
                errors.extend(cls._validate_transform_step(step, step_name, defined_dataframes, engine_type))
                # Add output dataframe to defined set
                if "output_alias" in step:
                    defined_dataframes.add(step["output_alias"])
            
            elif step_type == "write":
                errors.extend(cls._validate_write_step(step, step_name, defined_dataframes))
        
        return errors
    
    @classmethod
    def _validate_read_step(cls, step: Dict[str, Any], step_name: str) -> List[str]:
        """Validate a read step."""
        errors = []
        
        # Check required fields
        if "connector" not in step:
            errors.append(f"Missing 'connector' in read step: {step_name}")
        elif step["connector"] not in cls.SUPPORTED_CONNECTORS:
            errors.append(f"Unsupported connector in {step_name}: {step['connector']}")
        
        if "connection_ref" not in step:
            errors.append(f"Missing 'connection_ref' in read step: {step_name}")
            
        if "output_alias" not in step:
            errors.append(f"Missing 'output_alias' in read step: {step_name}")
            
        if "options" not in step:
            errors.append(f"Missing 'options' in read step: {step_name}")
        else:
            options = step["options"]
            connector = step.get("connector")
            
            # Database connector validation
            if connector == "database" and not ("query" in options or "dbtable" in options):
                errors.append(f"Database read step {step_name} must specify either 'query' or 'dbtable' in options")
                
            # File connector validation
            if connector == "file" and "path" not in options:
                errors.append(f"File read step {step_name} must specify 'path' in options")
                
            # Check file format if specified
            if "format" in options and options["format"] not in cls.SUPPORTED_FILE_FORMATS:
                errors.append(f"Unsupported file format in {step_name}: {options['format']}")
        
        return errors
    
    @classmethod
    def _validate_transform_step(cls, step: Dict[str, Any], step_name: str, 
                               defined_dataframes: Set[str], engine_type: str) -> List[str]:
        """Validate a transform step."""
        errors = []
        
        # Check required fields
        if "output_alias" not in step:
            errors.append(f"Missing 'output_alias' in transform step: {step_name}")
            
        # Check input references
        if "input_aliases" not in step and "input_alias" not in step:
            errors.append(f"Transform step {step_name} must specify either 'input_aliases' or 'input_alias'")
        
        if "input_aliases" in step:
            for df_alias in step["input_aliases"]:
                if df_alias not in defined_dataframes:
                    errors.append(f"Referenced DataFrame '{df_alias}' in {step_name} not found in previous steps")
        
        if "input_alias" in step and step["input_alias"] not in defined_dataframes:
            errors.append(f"Referenced DataFrame '{step['input_alias']}' in {step_name} not found in previous steps")
            
        # Check engine-specific configuration
        if "engine_specific" not in step:
            errors.append(f"Missing 'engine_specific' in transform step: {step_name}")
        else:
            # Validate Spark SQL configuration
            if engine_type == "spark" and "spark_sql" in step["engine_specific"]:
                spark_sql = step["engine_specific"]["spark_sql"]
                
                if "temp_views" not in spark_sql:
                    errors.append(f"Missing 'temp_views' in spark_sql config for step: {step_name}")
                elif not isinstance(spark_sql["temp_views"], list):
                    errors.append(f"'temp_views' must be a list in step: {step_name}")
                else:
                    # Validate each temp view
                    view_aliases = set()
                    for view in spark_sql["temp_views"]:
                        if "alias" not in view:
                            errors.append(f"Missing 'alias' in temp_view for step: {step_name}")
                        elif view["alias"] in view_aliases:
                            errors.append(f"Duplicate view alias '{view['alias']}' in step: {step_name}")
                        else:
                            view_aliases.add(view["alias"])
                            
                        if "dataframe" not in view:
                            errors.append(f"Missing 'dataframe' reference in temp_view for step: {step_name}")
                        elif view["dataframe"] not in defined_dataframes:
                            errors.append(f"Referenced DataFrame '{view['dataframe']}' not found for temp_view in step: {step_name}")
                
                if "query" not in spark_sql:
                    errors.append(f"Missing 'query' in spark_sql config for step: {step_name}")
        
        return errors
    
    @classmethod
    def _validate_write_step(cls, step: Dict[str, Any], step_name: str, defined_dataframes: Set[str]) -> List[str]:
        """Validate a write step."""
        errors = []
        
        # Check required fields
        if "connector" not in step:
            errors.append(f"Missing 'connector' in write step: {step_name}")
        elif step["connector"] not in cls.SUPPORTED_CONNECTORS:
            errors.append(f"Unsupported connector in {step_name}: {step['connector']}")
            
        if "connection_ref" not in step:
            errors.append(f"Missing 'connection_ref' in write step: {step_name}")
            
        if "input_alias" not in step:
            errors.append(f"Missing 'input_alias' in write step: {step_name}")
        elif step["input_alias"] not in defined_dataframes:
            errors.append(f"Referenced DataFrame '{step['input_alias']}' in {step_name} not found in previous steps")
            
        if "options" not in step:
            errors.append(f"Missing 'options' in write step: {step_name}")
        else:
            options = step["options"]
            connector = step.get("connector")
            
            # File connector validation
            if connector in ("file", "object_storage", "gcp_cloud_storage") and "path" not in options:
                errors.append(f"File/object storage write step {step_name} must specify 'path' in options")
                
            # Check file format if specified
            if "format" in options and options["format"] not in cls.SUPPORTED_FILE_FORMATS:
                errors.append(f"Unsupported file format in {step_name}: {options['format']}")
                
            # Check write mode if specified
            if "mode" in options and options["mode"] not in cls.SUPPORTED_WRITE_MODES:
                errors.append(f"Unsupported write mode in {step_name}: {options['mode']}. " +
                             f"Supported modes: {', '.join(cls.SUPPORTED_WRITE_MODES)}")
        
        return errors
    
    @classmethod
    def validate_yaml_file(cls, yaml_path: str) -> List[str]:
        """
        Validate a YAML job configuration file.
        
        Args:
            yaml_path: Path to the YAML file
            
        Returns:
            List of validation errors, empty if valid
        """
        try:
            with open(yaml_path, 'r') as f:
                config = yaml.safe_load(f)
            return cls.validate_job_config(config)
        except yaml.YAMLError as e:
            return [f"YAML parsing error: {str(e)}"]
        except Exception as e:
            return [f"Error validating YAML file: {str(e)}"]
# class Job:
#     """Job class for ETL processing."""
    
#     def __init__(self, config: Dict[str, Any]):
#         self.config = config
#         # Validate config upon initialization
#         errors = JobValidator.validate_job_config(config)
#         if errors:
#             raise ValueError("\n".join(errors))
    
#     @classmethod
#     def from_yaml(cls, yaml_path: str) -> 'Job':
#         """
#         Create a Job instance from a YAML configuration file.
        
#         Args:
#             yaml_path: Path to the YAML file
            
#         Returns:
#             Job instance
            
#         Raises:
#             ValueError: If the configuration is invalid
#         """
#         # Validate YAML file
#         errors = JobValidator.validate_yaml_file(yaml_path)
#         if errors:
#             raise ValueError("\n".join(errors))
            
#         # Load config from YAML
#         with open(yaml_path, 'r') as f:
#             config = yaml.safe_load(f)
            
#         return cls(config)