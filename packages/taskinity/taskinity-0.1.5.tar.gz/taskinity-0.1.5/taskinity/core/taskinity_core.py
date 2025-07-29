#!/usr/bin/env python3
"""
Taskinity Core - A simple framework for defining workflows using decorators and DSL.
Allows easy connection of functions into flows and monitoring their execution.
"""
import functools
import inspect
import json
import logging
import os
import re
import time
import traceback
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Type, Union

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("taskinity")

# Directories for logs and flow data
FLOW_DIR = os.getenv("FLOW_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "flows"))
LOG_DIR = os.getenv("LOG_DIR", os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
os.makedirs(FLOW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Flow status types
class FlowStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"

# Registry of all registered functions
REGISTRY = {}

# Flow execution history
FLOW_HISTORY = []

def task(name: Optional[str] = None, 
         description: Optional[str] = None, 
         validate_input: Optional[Callable] = None,
         validate_output: Optional[Callable] = None):
    """
    Decorator for registering functions as tasks in a flow.
    
    Args:
        name: Optional task name (default: function name)
        description: Optional task description
        validate_input: Optional function for input data validation
        validate_output: Optional function for output data validation
    """
    def decorator(func):
        task_name = name or func.__name__
        task_desc = description or func.__doc__ or ""
        
        # Create task info dictionary
        task_info = {
            "name": task_name,
            "description": task_desc,
            "function": func,
            "signature": inspect.signature(func),
            "validate_input": validate_input,
            "validate_output": validate_output,
        }
        
        # Register function in the global registry
        REGISTRY[func.__name__] = task_info
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            task_id = f"{func.__name__}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            logger.info(f"Starting task: {task_name}")
            
            # Save information about task start
            execution_info = {
                "task_id": task_id,
                "name": task_name,
                "start_time": datetime.now().isoformat(),
                "status": FlowStatus.RUNNING,
                "args": str(args),
                "kwargs": str(kwargs),
            }
            
            # Input data validation
            if validate_input:
                try:
                    validate_input(*args, **kwargs)
                except Exception as e:
                    logger.error(f"Input data validation error: {str(e)}")
                    execution_info["status"] = FlowStatus.FAILED
                    execution_info["error"] = str(e)
                    execution_info["end_time"] = datetime.now().isoformat()
                    execution_info["duration"] = time.time() - start_time
                    FLOW_HISTORY.append(execution_info)
                    raise ValueError(f"Input data validation error: {str(e)}")
            
            # Execute function
            try:
                result = func(*args, **kwargs)
                
                # Output data validation
                if validate_output:
                    try:
                        validate_output(result)
                    except Exception as e:
                        logger.error(f"Output data validation error: {str(e)}")
                        execution_info["status"] = FlowStatus.FAILED
                        execution_info["error"] = str(e)
                        execution_info["end_time"] = datetime.now().isoformat()
                        execution_info["duration"] = time.time() - start_time
                        FLOW_HISTORY.append(execution_info)
                        raise ValueError(f"Output data validation error: {str(e)}")
                
                # Save information about task completion
                execution_info["status"] = FlowStatus.COMPLETED
                execution_info["end_time"] = datetime.now().isoformat()
                execution_info["duration"] = time.time() - start_time
                FLOW_HISTORY.append(execution_info)
                
                logger.info(f"Task completed: {task_name} (duration: {execution_info['duration']:.2f}s)")
                return result
            except Exception as e:
                # Save information about task failure
                execution_info["status"] = FlowStatus.FAILED
                execution_info["error"] = str(e)
                execution_info["traceback"] = traceback.format_exc()
                execution_info["end_time"] = datetime.now().isoformat()
                execution_info["duration"] = time.time() - start_time
                FLOW_HISTORY.append(execution_info)
                
                logger.error(f"Task failed: {task_name} - {str(e)}")
                raise
        
        # Add task information to the wrapper function for testing
        wrapper.__taskinity_task__ = task_info
        
        return wrapper
    
    # Handle case when decorator is used without arguments
    if callable(name):
        func = name
        name = None
        return decorator(func)
    
    return decorator

def flow(name: Optional[str] = None, description: Optional[str] = None):
    """
    Decorator for defining a flow.
    
    Args:
        name: Optional flow name (default: function name)
        description: Optional flow description
    """
    def decorator(func):
        flow_name = name or func.__name__
        flow_desc = description or func.__doc__ or ""
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            flow_id = f"{flow_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            logger.info(f"Starting flow: {flow_name}")
            
            # Save information about flow start
            flow_info = {
                "flow_id": flow_id,
                "name": flow_name,
                "description": flow_desc,
                "start_time": datetime.now().isoformat(),
                "status": FlowStatus.RUNNING,
                "args": str(args),
                "kwargs": str(kwargs),
                "tasks": []
            }
            
            try:
                # Execute flow function
                start_time = time.time()
                result = func(*args, **kwargs)
                
                # Save information about flow completion
                flow_info["status"] = FlowStatus.COMPLETED
                flow_info["end_time"] = datetime.now().isoformat()
                flow_info["duration"] = time.time() - start_time
                
                # Save flow history to file
                flow_file = os.path.join(FLOW_DIR, f"{flow_id}.json")
                with open(flow_file, "w") as f:
                    json.dump(flow_info, f, indent=2)
                
                logger.info(f"Flow completed: {flow_name} (duration: {flow_info['duration']:.2f}s)")
                return result
            except Exception as e:
                # Save information about flow failure
                flow_info["status"] = FlowStatus.FAILED
                flow_info["error"] = str(e)
                flow_info["traceback"] = traceback.format_exc()
                flow_info["end_time"] = datetime.now().isoformat()
                flow_info["duration"] = time.time() - start_time
                
                # Save flow history to file
                flow_file = os.path.join(FLOW_DIR, f"{flow_id}.json")
                with open(flow_file, "w") as f:
                    json.dump(flow_info, f, indent=2)
                
                logger.error(f"Flow failed: {flow_name} - {str(e)}")
                raise
        
        # Add flow information to the wrapper function for testing
        wrapper.__taskinity_flow__ = {
            "name": flow_name,
            "description": flow_desc
        }
        
        return wrapper
    
    # Handle case when decorator is used without arguments
    if callable(name):
        func = name
        name = None
        return decorator(func)
    
    return decorator

def parse_dsl(dsl_text: str) -> Dict[str, Any]:
    """
    Parse DSL text into a structured flow definition.
    
    Args:
        dsl_text: DSL text to parse
        
    Returns:
        Dictionary containing the parsed flow definition with tasks and connections
    """
    lines = [line.strip() for line in dsl_text.strip().split("\n") if line.strip()]
    flow_data = {"name": "UnnamedFlow", "description": "", "tasks": {}, "connections": []}
    
    if not lines:
        return flow_data
    
    # Extract flow name
    flow_match = re.match(r"flow\s+(\w+):", lines[0])
    if flow_match:
        flow_data["name"] = flow_match.group(1)
    
    # Process each line
    current_task = None
    for line in lines[1:]:
        # Skip empty lines
        if not line:
            continue
        
        # Extract flow description
        if line.startswith("description:"):
            flow_data["description"] = line.split(":", 1)[1].strip().strip('\"')
            continue
        
        # Extract task connections
        connection_match = re.match(r"(\w+)\s*->\s*(\w+)", line)
        if connection_match:
            source, target = connection_match.groups()
            flow_data["connections"].append({"source": source, "target": target})
            
            # Ensure source and target tasks exist in the tasks dict
            for task_name in [source, target]:
                if task_name not in flow_data["tasks"]:
                    flow_data["tasks"][task_name] = {
                        "name": task_name,
                        "inputs": [],
                        "outputs": []
                    }
            continue
        
        # Extract task definition (explicit task with properties)
        task_match = re.match(r"task\s+(\w+):", line)
        if task_match:
            current_task = task_match.group(1)
            if current_task not in flow_data["tasks"]:
                flow_data["tasks"][current_task] = {
                    "name": current_task,
                    "inputs": [],
                    "outputs": []
                }
            continue
        
        # Extract task properties (only if we're in a task context)
        if current_task and ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip().strip('\"')
            flow_data["tasks"][current_task][key] = value
    
    # Process connections to update task inputs/outputs
    for conn in flow_data["connections"]:
        source = conn["source"]
        target = conn["target"]
        
        if source in flow_data["tasks"] and target not in flow_data["tasks"][source].get("outputs", []):
            if "outputs" not in flow_data["tasks"][source]:
                flow_data["tasks"][source]["outputs"] = []
            flow_data["tasks"][source]["outputs"].append(target)
        
        if target in flow_data["tasks"] and source not in flow_data["tasks"][target].get("inputs", []):
            if "inputs" not in flow_data["tasks"][target]:
                flow_data["tasks"][target]["inputs"] = []
            flow_data["tasks"][target]["inputs"].append(source)
    
    return flow_data

def run_flow_from_dsl(dsl_text: str, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Run a flow defined in DSL.
    
    Args:
        dsl_text: DSL text defining the flow
        input_data: Input data for the flow (optional)
        
    Returns:
        Dictionary containing the results of each task
    """
    if input_data is None:
        input_data = {}
    
    # Parse DSL
    flow_data = parse_dsl(dsl_text)
    
    # Get task registry
    task_registry = REGISTRY
    
    # Initialize results dictionary
    results = {}
    
    # Build dependency graph
    dependencies = {task: set() for task in flow_data["tasks"]}
    for connection in flow_data["connections"]:
        source, target = connection["source"], connection["target"]
        dependencies[target].add(source)
    
    # Topologically sort tasks
    visited = set()
    temp_visited = set()
    order = []
    
    def visit(task):
        if task in temp_visited:
            raise ValueError(f"Circular dependency detected in flow: {task}")
        if task in visited:
            return
        
        temp_visited.add(task)
        for dep in dependencies[task]:
            visit(dep)
        
        temp_visited.remove(task)
        visited.add(task)
        order.append(task)
    
    for task in dependencies:
        if task not in visited:
            visit(task)
    
    # Execute tasks in order
    for task_name in order:
        # Get task function
        if task_name not in task_registry:
            raise ValueError(f"Task '{task_name}' not found in registry")
        
        task_func = task_registry[task_name]["function"]
        
        # Get task dependencies
        task_deps = dependencies[task_name]
        
        # Prepare task arguments
        task_args = {}
        
        # Get the function's parameter names
        import inspect
        sig = inspect.signature(task_func)
        param_names = list(sig.parameters.keys())
        
        # Add dependency results (matching parameter names with _result suffix)
        for dep in task_deps:
            arg_name = dep + "_result"
            if arg_name in param_names:
                task_args[arg_name] = results[dep]
        
        # Add input data (only include parameters that match input_data keys)
        for key in input_data:
            if key in param_names:
                task_args[key] = input_data[key]
        
        # Execute task
        logger.info(f"Executing task: {task_name}")
        try:
            result = task_func(**task_args)
            results[task_name] = result
            logger.info(f"Task completed: {task_name}")
        except Exception as e:
            logger.error(f"Task failed: {task_name} - {str(e)}")
            raise
    
    return results
