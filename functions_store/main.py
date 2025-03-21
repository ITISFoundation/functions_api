import asyncio
import importlib
import json
import logging
import os
import sys
import urllib
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

import requests
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from jsonschema import ValidationError as JSONSchemaValidationError
from jsonschema import validate
from jsonschema.validators import validator_for
from sqlalchemy.orm import Session

from . import database, models

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Swagger Functions Store - OpenAPI 3.0",
    version="0.0.1",
    openapi_tags=[
        {"name": "function", "description": "Function operations"},
        {"name": "function_job", "description": "Function job operations"},
    ],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

function_executors: Dict[str, Callable] = {}


def register_function_executor(type_name: str, executor: Callable):
    """Register an executor for a specific function type"""
    function_executors[type_name] = executor


def execute_local_python(url: str, inputs: Dict[str, Any]) -> Any:
    """Execute a local Python function"""
    if ":" not in url:
        raise ValueError("URL must be in format /path/to/file.py:function_name")

    file_path, function_name = url.rsplit(":", 1)

    func = load_function_from_path(file_path, function_name)

    try:
        return func(**inputs)
    except Exception as e:
        raise Exception(f"Error executing local Python function: {str(e)}")


def execute_remote_http(url: str, inputs: Dict[str, Any]) -> Any:
    """Execute a remote function via HTTP"""
    try:
        response = requests.post(url, json=inputs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error executing remote HTTP function: {str(e)}")


# Register default executors
register_function_executor("local.python", execute_local_python)
register_function_executor("remote.http", execute_remote_http)


def execute_function(function_type: str, url: str, inputs: Dict[str, Any]) -> Any:
    """Execute a function based on its type"""
    executor = function_executors.get(function_type)
    if not executor:
        raise ValueError(f"Unsupported function type: {function_type}")

    return executor(url, inputs)


@app.get("/generate-openapi")
async def generate_openapi():
    """Generate OpenAPI spec and save to file"""
    openapi_schema = app.openapi()
    print("OpenAPI spec generated")
    return openapi_schema


def load_function_from_path(file_path: str, function_name: str):
    """Load a Python function from a file path"""
    try:
        # Get absolute path
        abs_path = os.path.abspath(file_path)

        # Load module spec
        spec = importlib.util.spec_from_file_location("dynamic_module", abs_path)
        if spec is None:
            raise ImportError(f"Could not load spec for {abs_path}")

        # Create module
        module = importlib.util.module_from_spec(spec)
        sys.modules["dynamic_module"] = module

        # Execute module
        spec.loader.exec_module(module)

        # Get function
        if not hasattr(module, function_name):
            raise AttributeError(f"Function {function_name} not found in {abs_path}")

        return getattr(module, function_name)
    except Exception as e:
        raise Exception(f"Error loading function: {str(e)}")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/function/list",
    response_model=List[models.Function],
    operation_id="list_functions",
    tags=["function"],
)
def list_functions(db: Session = Depends(get_db)):
    """
    List all functions in the store.

    Returns:
        List of all registered functions
    """
    return db.query(database.FunctionDB).all()


@app.delete("/function/all", operation_id="delete_all_functions", tags=["function"])
def delete_all_functions(db: Session = Depends(get_db)):
    """
    Delete all functions from the store.

    Returns:
        Message confirming deletion with count of deleted functions
    """
    count = db.query(database.FunctionDB).count()
    db.query(database.FunctionDB).delete()
    db.commit()
    return {"message": f"Deleted {count} functions"}


@app.get(
    "/function/searchByName",
    response_model=List[models.Function],
    operation_id="search_functions_by_name",
    tags=["function"],
)
def search_functions_by_name(name: str, db: Session = Depends(get_db)):
    """
    Search for functions by name.

    Parameters:
        name: String to search for in function names (case-sensitive partial match)

    Returns:
        List of functions whose names contain the search string
    """
    return (
        db.query(database.FunctionDB)
        .filter(database.FunctionDB.name.like(f"%{name}%"))
        .all()
    )


# FunctionJob endpoints
@app.get(
    "/functionJob/{function_job_id}",
    response_model=models.FunctionJob,
    operation_id="get_function_job",
    tags=["function_job"],
)
def get_function_job(function_job_id: int, db: Session = Depends(get_db)):
    """
    Get the details of a specific function job.

    Parameters:
        function_job_id: ID of the function job to retrieve

    Returns:
        Function job details including status, inputs, and outputs

    Raises:
        HTTPException: If job is not found (404)
    """
    job = (
        db.query(database.FunctionJobDB)
        .filter(database.FunctionJobDB.id == function_job_id)
        .first()
    )
    if not job:
        raise HTTPException(status_code=404, detail="Function job not found")
    return job


def process_single_input(
    function: database.FunctionDB, inputs: str, db: Session
) -> database.FunctionJobDB:
    """
    Process a single input for a function.
    """
    try:
        inputs_dict = json.loads(inputs)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail=f"Invalid JSON in inputs: {inputs}")

    # Create a new database session for this thread
    thread_db = database.SessionLocal()

    try:
        job = database.FunctionJobDB(
            functionID=function.id,
            status=models.JobStatus.RUNNING,
            inputs=inputs_dict,
        )
        thread_db.add(job)
        thread_db.commit()
        thread_db.refresh(job)

        try:
            url_parts = urllib.parse.urlparse(function.url)
            if url_parts.scheme != "file":
                raise ValueError("Only file:// URLs are supported")

            file_path = url_parts.path
            if ":" not in file_path:
                raise ValueError(
                    "URL must be in format file:///path/to/file.py:function_name"
                )

            file_path, function_name = file_path.rsplit(":", 1)

            func = load_function_from_path(file_path, function_name)
            result = func(**inputs_dict)

            job.outputs = {"result": result}
            job.status = models.JobStatus.COMPLETED

        except Exception as e:
            job.status = models.JobStatus.FAILED
            job.job_info = {"error": str(e)}

        thread_db.commit()
        job_id = job.id

        # Refresh the job from the database to ensure we have the latest state
        job = thread_db.query(database.FunctionJobDB).get(job_id)
        return job

    finally:
        thread_db.close()


@app.get(
    "/function/job/status",
    response_model=List[models.FunctionJob],
    operation_id="get_jobs_status",
    tags=["function_job"],
)
async def get_jobs_status(
    job_ids: List[int] = Query(..., title="Job IDs to check status for"),
    db: Session = Depends(get_db),
):
    """
    Get status of multiple jobs.

    Parameters:
        job_ids: List of job IDs to check

    Returns:
        List of job statuses
    """
    jobs = (
        db.query(database.FunctionJobDB)
        .filter(database.FunctionJobDB.id.in_(job_ids))
        .all()
    )
    return jobs


# Add configuration endpoint to update parallel processing settings
@app.post("/function/config", tags=["function"])
async def update_function_config(
    max_parallel_jobs: int = 10, db: Session = Depends(get_db)
):
    """
    Update function execution configuration settings.

    Parameters:
        max_parallel_jobs: Maximum number of parallel jobs allowed (default: 10)

    Returns:
        Updated configuration settings
    """
    # In a production environment, you might want to store these in a database
    # or configuration service instead of using global variables
    app.state.max_parallel_jobs = max_parallel_jobs

    return {"max_parallel_jobs": max_parallel_jobs}


async def process_single_job(
    function: database.FunctionDB,
    job: database.FunctionJobDB,
    task_db: Session,
    executor: ThreadPoolExecutor,
    loop: asyncio.AbstractEventLoop,
):
    """Process a single job and update its status."""
    job_id = job.id
    logger.info(f"Starting processing of job {job_id}")

    try:
        # Update to RUNNING
        job.status = models.JobStatus.RUNNING
        task_db.commit()
        logger.info(f"Job {job_id} marked as RUNNING")

        # Execute the function in the thread pool
        logger.info(f"Executing job {job_id} with inputs {job.inputs}")
        result = await loop.run_in_executor(
            executor,
            lambda: execute_function(function.type, function.url, job.inputs),
        )
        logger.info(f"Job {job_id} execution completed with result: {result}")

        # Update job status to COMPLETED
        job = task_db.query(database.FunctionJobDB).get(job_id)  # Refresh job from DB
        job.outputs = {"result": result}
        job.status = models.JobStatus.COMPLETED
        task_db.commit()
        logger.info(f"Job {job_id} marked as COMPLETED")

    except Exception as e:
        logger.error(f"Error processing job {job_id}: {str(e)}", exc_info=True)
        # Update job with error
        job = task_db.query(database.FunctionJobDB).get(job_id)  # Refresh job from DB
        job.status = models.JobStatus.FAILED
        job.job_info = {"error": str(e)}
        task_db.commit()

    return job_id


async def process_inputs_async(
    function: database.FunctionDB,
    jobs: List[database.FunctionJobDB],
    db: Session,
    max_workers: Optional[int] = None,
):
    """
    Process inputs asynchronously in the background.
    """
    logger.info(f"Starting background processing for {len(jobs)} jobs")

    # Create a new database session for background task
    task_db = database.SessionLocal()

    try:
        # Get the event loop
        loop = asyncio.get_running_loop()

        # Use default max_workers if none provided
        workers = max_workers if max_workers is not None else 10
        logger.info(f"Using {workers} workers for processing")

        # Create a thread pool executor for running the functions
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Process jobs concurrently using the executor
            tasks = []
            for job in jobs:
                task = asyncio.create_task(
                    process_single_job(
                        function=function,
                        job=job,
                        task_db=task_db,
                        executor=executor,
                        loop=loop,
                    )
                )
                tasks.append(task)

            # Wait for all tasks to complete
            logger.info("Waiting for all tasks to complete")
            completed_job_ids = await asyncio.gather(*tasks)
            logger.info(f"All tasks completed. Job IDs: {completed_job_ids}")

    except Exception as e:
        logger.error(f"Error in background processing: {str(e)}", exc_info=True)
        # Update all remaining jobs as failed
        for job in jobs:
            if job.status in [
                models.JobStatus.PENDING,
                models.JobStatus.RUNNING,
            ]:
                job = task_db.query(database.FunctionJobDB).get(
                    job.id
                )  # Refresh from DB
                job.status = models.JobStatus.FAILED
                job.job_info = {"error": f"Background task error: {str(e)}"}
                task_db.add(job)
        task_db.commit()

    finally:
        task_db.close()


@app.post(
    "/functionJobCollection",
    response_model=models.FunctionJobCollection,
    operation_id="create_function_job_collection",
    tags=["function_job_collection"],
)
def create_function_job_collection(
    collection: models.FunctionJobCollection, db: Session = Depends(get_db)
):
    """
    Create a new function job collection.

    Parameters:
        collection: Collection details including name and optional description

    Returns:
        Created function job collection
    """
    db_collection = database.FunctionJobCollectionDB(
        name=collection.name,
        description=collection.description,
        job_ids=collection.job_ids,
        status=collection.status,
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection


@app.get(
    "/functionJobCollection/list",
    response_model=List[models.FunctionJobCollection],
    operation_id="list_function_job_collections",
    tags=["function_job_collection"],
)
def list_function_job_collections(db: Session = Depends(get_db)):
    """
    List all function job collections.

    Returns:
        List of all function job collections
    """
    return db.query(database.FunctionJobCollectionDB).all()


@app.post(
    "/function/{function_id}/batch",
    response_model=models.FunctionJobCollection,
    operation_id="batch_run_function",
    tags=["function"],
)
async def batch_run_function(
    function_id: int,
    collection_name: str,
    request_body: List[str] = Body(..., embed=False),
    max_workers: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Run a function with multiple inputs and create a job collection.

    Parameters:
        function_id: ID of the function to run
        collection_name: Name for the job collection
        request_body: List of JSON strings containing input parameters
        max_workers: Optional maximum number of parallel workers

    Returns:
        Created function job collection containing all job IDs
    """
    # First create jobs using existing map_function
    jobs = await map_function(function_id, request_body, max_workers, db)

    # Create a job collection
    db_collection = database.FunctionJobCollectionDB(
        name=collection_name,
        description=f"Batch execution of function {function_id}",
        job_ids=[job.id for job in jobs],
        status="RUNNING",
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)

    # Convert to Pydantic model
    return models.FunctionJobCollection.model_validate(db_collection)


@app.get(
    "/functionJobCollection/{collection_id}/status",
    response_model=models.FunctionJobCollection,
    operation_id="get_collection_status",
    tags=["function_job_collection"],
)
async def get_collection_status(collection_id: int, db: Session = Depends(get_db)):
    """
    Get status of a function job collection.

    Parameters:
        collection_id: ID of the collection to check

    Returns:
        Collection details including current status of all jobs
    """
    # Get collection
    collection = (
        db.query(database.FunctionJobCollectionDB)
        .filter(database.FunctionJobCollectionDB.id == collection_id)
        .first()
    )
    if not collection:
        raise HTTPException(status_code=404, detail="Function job collection not found")

    # Get status of all jobs in collection
    jobs = (
        db.query(database.FunctionJobDB)
        .filter(database.FunctionJobDB.id.in_(collection.job_ids))
        .all()
    )

    # Update collection status based on job statuses
    if all(job.status == models.JobStatus.COMPLETED for job in jobs):
        collection.status = "COMPLETED"
    elif any(job.status == models.JobStatus.FAILED for job in jobs):
        collection.status = "FAILED"
    else:
        collection.status = "RUNNING"

    db.commit()

    # Convert to Pydantic model
    return models.FunctionJobCollection.model_validate(collection)


def validate_schema(schema: Dict[str, Any]) -> None:
    """
    Validate that a schema is a valid JSON Schema.
    Raises ValidationError if the schema is invalid.
    """
    # Get the appropriate validator
    validator_cls = validator_for(schema)
    # Check schema itself is valid
    validator_cls.check_schema(schema)


def validate_against_json_schema(
    data: Dict[str, Any], schema: Dict[str, Any], context: str = "data"
) -> None:
    """
    Validate data against a JSON Schema.
    Raises HTTPException with detailed error message if validation fails.
    """
    try:
        validate(instance=data, schema=schema)
    except JSONSchemaValidationError as e:
        path = " -> ".join(str(p) for p in e.path) if e.path else "root"
        raise HTTPException(
            status_code=400,
            detail=f"{context} validation failed at {path}: {e.message}",
        )


@app.post(
    "/function",
    response_model=models.Function,
    operation_id="create_function",
    tags=["function"],
)
def create_function(function: models.Function, db: Session = Depends(get_db)):
    """
    Create a new function with optional JSON Schema definitions for input and output.
    Validates that provided schemas are valid JSON Schema.
    Supports tags for better organization and searchability.
    """
    # Validate schemas if provided
    if function.input_schema:
        try:
            validate_schema(function.input_schema)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid input schema: {str(e)}"
            )

    if function.output_schema:
        try:
            validate_schema(function.output_schema)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Invalid output schema: {str(e)}"
            )

    # Create database model from pydantic model
    db_function = database.FunctionDB(**function.dict(exclude={"id"}))
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    return db_function


@app.post(
    "/function/{function_id}/run",
    response_model=models.FunctionJob,
    operation_id="run_function",
    tags=["function"],
)
def run_function(function_id: int, inputs: str, db: Session = Depends(get_db)):
    """
    Run a function with the given inputs.
    Validates inputs and outputs against JSON Schema if defined.
    """
    function = (
        db.query(database.FunctionDB)
        .filter(database.FunctionDB.id == function_id)
        .first()
    )
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    try:
        inputs_dict = json.loads(inputs)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in inputs")

    # Validate inputs against schema if defined
    if function.input_schema:
        try:
            validate_against_json_schema(inputs_dict, function.input_schema, "Input")
        except HTTPException as e:
            # Create failed job with validation error
            job = database.FunctionJobDB(
                functionID=function_id,
                status=models.JobStatus.FAILED,
                inputs=inputs_dict,
                job_info={"error": str(e.detail)},
            )
            db.add(job)
            db.commit()
            db.refresh(job)
            return job

    # Create and start job
    job = database.FunctionJobDB(
        functionID=function_id,
        status=models.JobStatus.RUNNING,
        inputs=inputs_dict,
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    try:
        result = execute_function(function.type, function.url, inputs_dict)

        # Validate output against schema if defined
        if function.output_schema:
            try:
                output_dict = {"result": result}
                validate_against_json_schema(
                    output_dict, function.output_schema, "Output"
                )
            except HTTPException as e:
                job.status = models.JobStatus.FAILED
                job.job_info = {"error": str(e.detail)}
                db.commit()
                return job

        job.outputs = {"result": result}
        job.status = models.JobStatus.COMPLETED
        db.commit()

    except Exception as e:
        job.status = models.JobStatus.FAILED
        job.job_info = {"error": str(e)}
        db.commit()
        print(f"Error executing function: {str(e)}")

    return job


# Modify map_function to include schema validation
@app.post(
    "/function/{function_id}/map",
    response_model=List[models.FunctionJob],
    operation_id="map_function",
    tags=["function"],
)
async def map_function(
    function_id: int,
    request_body: List[str] = Body(..., embed=False),
    max_workers: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Start asynchronous processing of multiple inputs with schema validation.
    """
    function = (
        db.query(database.FunctionDB)
        .filter(database.FunctionDB.id == function_id)
        .first()
    )
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    # Create jobs for all inputs
    jobs = []
    for input_str in request_body:
        try:
            inputs_dict = json.loads(input_str)

            # Validate input against schema if defined
            if function.input_schema:
                try:
                    validate_against_json_schema(
                        inputs_dict, function.input_schema, "Input"
                    )
                except HTTPException as e:
                    # Create failed job with validation error
                    job = database.FunctionJobDB(
                        functionID=function_id,
                        status=models.JobStatus.FAILED,
                        inputs=inputs_dict,
                        job_info={"error": str(e.detail)},
                    )
                    db.add(job)
                    jobs.append(job)
                    continue

        except json.JSONDecodeError:
            raise HTTPException(
                status_code=400, detail=f"Invalid JSON in inputs: {input_str}"
            )

        # Create job in PENDING state
        job = database.FunctionJobDB(
            functionID=function_id,
            status=models.JobStatus.PENDING,
            inputs=inputs_dict,
        )
        db.add(job)
        jobs.append(job)

    # Commit all jobs to get their IDs
    db.commit()
    for job in jobs:
        db.refresh(job)

    # Start background processing only for jobs that passed validation
    pending_jobs = [job for job in jobs if job.status == models.JobStatus.PENDING]
    if pending_jobs:
        background_task = asyncio.create_task(
            process_inputs_async(function, pending_jobs, db, max_workers)
        )
        app.state.background_tasks = getattr(app.state, "background_tasks", set())
        app.state.background_tasks.add(background_task)
        background_task.add_done_callback(
            lambda t: app.state.background_tasks.remove(t)
        )

    return jobs


@app.get(
    "/functionJobs",
    response_model=List[models.FunctionJob],
    operation_id="list_function_jobs",
    tags=["function_job"],
    summary="List all function jobs with optional filtering",
)
def list_function_jobs(
    limit: Optional[int] = Query(
        None, ge=1, le=1000, description="Maximum number of jobs to return"
    ),
    offset: Optional[int] = Query(None, ge=0, description="Number of jobs to skip"),
    status: Optional[models.JobStatus] = Query(
        None, description="Filter by job status"
    ),
    function_id: Optional[int] = Query(None, description="Filter by function ID"),
    start_date: Optional[datetime] = Query(
        None, description="Filter jobs after this date"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter jobs before this date"
    ),
    db: Session = Depends(get_db),
) -> List[models.FunctionJob]:
    """
    List all function jobs with optional filtering and pagination.

    Parameters:
        limit: Maximum number of jobs to return (default: all)
        offset: Number of jobs to skip for pagination (default: 0)
        status: Filter by job status (e.g., PENDING, RUNNING, COMPLETED, FAILED)
        function_id: Filter jobs for a specific function
        start_date: Include jobs created after this date
        end_date: Include jobs created before this date

    Returns:
        List[FunctionJob]: A filtered list of function jobs
    """
    query = db.query(database.FunctionJobDB)

    # Apply filters if provided
    if status:
        query = query.filter(database.FunctionJobDB.status == status)

    if function_id:
        query = query.filter(database.FunctionJobDB.functionID == function_id)

    if start_date:
        query = query.filter(database.FunctionJobDB.created_at >= start_date)

    if end_date:
        query = query.filter(database.FunctionJobDB.created_at <= end_date)

    # Apply pagination
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    # Order by most recent first
    query = query.order_by(database.FunctionJobDB.created_at.desc())

    return query.all()


@app.get(
    "/function/{function_id}/jobs",
    response_model=List[models.FunctionJob],
    operation_id="get_function_jobs",
    tags=["function_job"],
)
async def get_function_jobs(
    function_id: int = Path(..., description="ID of the function to get jobs for"),
    limit: Optional[int] = Query(
        100, ge=1, le=1000, description="Maximum number of jobs to return"
    ),
    offset: Optional[int] = Query(0, ge=0, description="Number of jobs to skip"),
    status: Optional[models.JobStatus] = Query(
        None, description="Filter by job status"
    ),
    start_date: Optional[datetime] = Query(
        None, description="Filter jobs after this date"
    ),
    end_date: Optional[datetime] = Query(
        None, description="Filter jobs before this date"
    ),
    db: Session = Depends(get_db),
) -> List[models.FunctionJob]:
    """
    Get all jobs for a specific function with optional filtering and pagination.
    """
    # First check if function exists
    function = (
        db.query(database.FunctionDB)
        .filter(database.FunctionDB.id == function_id)
        .first()
    )
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")

    # Start building query
    query = db.query(database.FunctionJobDB).filter(
        database.FunctionJobDB.functionID == function_id
    )

    # Apply filters if provided
    if status:
        query = query.filter(database.FunctionJobDB.status == status)

    if start_date:
        query = query.filter(database.FunctionJobDB.created_at >= start_date)

    if end_date:
        query = query.filter(database.FunctionJobDB.created_at <= end_date)

    # Apply pagination
    if offset is not None:
        query = query.offset(offset)
    if limit is not None:
        query = query.limit(limit)

    return query.all()


@app.get(
    "/function/searchByTags",
    response_model=List[models.Function],
    operation_id="search_functions_by_tags",
    tags=["function"],
)
def search_functions_by_tags(
    tags: List[str] = Query(..., description="Tags to search for"),
    match_all: bool = Query(
        False,
        description="If True, functions must have all tags. If False, functions must have any of the tags.",
    ),
    db: Session = Depends(get_db),
):
    """
    Search for functions by tags.

    Parameters:
        tags: List of tags to search for
        match_all: If True, functions must have all specified tags. If False, functions must have any of the specified tags.

    Returns:
        List of functions that match the tag criteria
    """
    # Get all functions
    query = db.query(database.FunctionDB)

    # Filter functions based on tags
    if match_all:
        # Function must have all specified tags
        functions = [
            func
            for func in query.all()
            if func.tags and all(tag in func.tags for tag in tags)
        ]
    else:
        # Function must have any of the specified tags
        functions = [
            func
            for func in query.all()
            if func.tags and any(tag in func.tags for tag in tags)
        ]

    return functions
