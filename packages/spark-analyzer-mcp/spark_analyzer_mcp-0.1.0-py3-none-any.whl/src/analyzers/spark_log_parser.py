from typing import Dict, List, Any, Optional, Union
import json
import re
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel, Field
import requests
from loguru import logger

# Pydantic models for structured log data
class SparkStageInfo(BaseModel):
    stage_id: int
    stage_name: str
    num_tasks: int
    submission_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    is_skipped: bool = False
    failure_reason: Optional[str] = None
    task_metrics: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def has_skew(self) -> bool:
        """Detect if this stage has data skew based on task metrics"""
        if not self.task_metrics or 'tasks' not in self.task_metrics:
            return False
            
        # Calculate coefficient of variation for task durations
        tasks = self.task_metrics['tasks']
        if len(tasks) < 2:
            return False
            
        durations = [t.get('duration_ms', 0) for t in tasks]
        mean_duration = sum(durations) / len(durations)
        if mean_duration == 0:
            return False
            
        std_dev = (sum((d - mean_duration) ** 2 for d in durations) / len(durations)) ** 0.5
        cv = std_dev / mean_duration
        
        # CV > 0.3 often indicates skew
        return cv > 0.3

class SparkJobInfo(BaseModel):
    job_id: int
    job_name: Optional[str] = None
    submission_time: Optional[datetime] = None
    completion_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    status: str  # RUNNING, SUCCEEDED, FAILED
    stages: List[SparkStageInfo] = Field(default_factory=list)
    stage_ids: List[int] = Field(default_factory=list) # New field to store stage IDs for this job
    num_stages: int = 0
    num_tasks: int = 0
    failure_reason: Optional[str] = None
    
    @property
    def is_bottleneck(self) -> bool:
        """Determine if this job is a bottleneck in the application"""
        if self.duration_ms is None:
            return False
        
        # A job is considered a bottleneck if it takes more than 30% of total app time
        # This is a simplified heuristic - in reality would compare to app duration
        return self.duration_ms > 60000  # 1 minute threshold as example
    
    @property
    def has_stage_skew(self) -> bool:
        """Check if any stage in this job has data skew"""
        return any(stage.has_skew for stage in self.stages)

class SparkSqlInfo(BaseModel):
    query_id: str
    description: str
    start_time_ms: Optional[int] = None # Added start time
    duration_ms: Optional[int] = None
    physical_plan: Optional[str] = None
    logical_plan: Optional[str] = None
    details: Optional[str] = None
    jobs: List[int] = Field(default_factory=list)  # Job IDs associated with this SQL query
    
    @property
    def should_optimize(self) -> bool:
        """Determine if this SQL query should be optimized"""
        if not self.physical_plan:
            return False
            
        # Look for common inefficient patterns in the plan
        inefficient_patterns = [
            r'SortMergeJoin',  # Often less efficient than broadcast joins for small tables
            r'BroadcastNestedLoopJoin',  # Very inefficient join strategy
            r'Exchange hashpartitioning',  # Indicates a shuffle which is expensive
            r'Scan parquet.*\(filter =',  # Might benefit from partitioning/bucketing
            r'Scan csv',  # CSV is inefficient format
        ]
        
        return any(re.search(pattern, self.physical_plan, re.IGNORECASE) 
                  for pattern in inefficient_patterns)

class SparkStackTrace(BaseModel):
    exception_type: str
    message: str
    full_trace: str
    source_files: List[str] = Field(default_factory=list)
    
    @property
    def is_memory_related(self) -> bool:
        """Check if stack trace is related to memory issues"""
        memory_patterns = [
            'OutOfMemoryError', 
            'MemoryLimit', 
            'SpillException',
            'not enough memory'
        ]
        return any(pattern in self.full_trace for pattern in memory_patterns)

class SparkLogData(BaseModel):
    app_id: str
    app_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration_ms: Optional[int] = None
    user: Optional[str] = None
    spark_version: Optional[str] = None
    jobs: Dict[int, SparkJobInfo] = Field(default_factory=dict)
    sql_queries: Dict[str, SparkSqlInfo] = Field(default_factory=dict)
    stack_traces: List[SparkStackTrace] = Field(default_factory=list)
    spark_conf: Dict[str, str] = Field(default_factory=dict)
    
    @property
    def bottleneck_jobs(self) -> List[SparkJobInfo]:
        """Return jobs identified as bottlenecks"""
        return [job for job in self.jobs.values() if job.is_bottleneck]
    
    @property
    def jobs_with_skew(self) -> List[SparkJobInfo]:
        """Return jobs with data skew"""
        return [job for job in self.jobs.values() if job.has_stage_skew]
    
    @property
    def sql_to_optimize(self) -> List[SparkSqlInfo]:
        """Return SQL queries that should be optimized"""
        return [sql for sql in self.sql_queries.values() if sql.should_optimize]


class SparkLogParser:
    """Parser for Spark UI logs and event logs"""
    
    def __init__(self):
        self.logger = logger
    
    async def parse_log_file(self, log_path: Union[str, Path]) -> SparkLogData:
        """
        Parse a Spark event log file (JSON format)
        
        Args:
            log_path: Path to the Spark event log file
            
        Returns:
            Parsed SparkLogData object
        """
        log_path = Path(log_path)
        self.logger.info(f"Parsing Spark log file: {log_path}")
        
        if not log_path.exists():
            raise FileNotFoundError(f"Log file not found: {log_path}")
            
        # Initialize empty log data
        log_data = SparkLogData(
            app_id="unknown",
            app_name="unknown"
        )
        
        # In a real implementation, we would parse the event log line by line
        # For now, this is a simplified placeholder
        try:
            with open(log_path, 'r') as f:
                # Spark event logs are typically one JSON object per line
                for line in f:
                    try:
                        event = json.loads(line.strip())
                        self._process_event(event, log_data)
                    except json.JSONDecodeError:
                        self.logger.warning("Failed to parse JSON line in log file")
                        continue
        except Exception as e:
            self.logger.error(f"Error parsing log file: {e}")
            raise
            
        return log_data
    
    async def parse_spark_ui(self, ui_url: str) -> SparkLogData:
        """
        Parse Spark UI by scraping the web interface
        
        Args:
            ui_url: URL to the Spark UI (e.g., http://localhost:4040)
            
        Returns:
            Parsed SparkLogData object
        """
        self.logger.info(f"Parsing Spark UI from URL: {ui_url}")
        
        # Initialize empty log data
        log_data = SparkLogData(
            app_id="unknown",
            app_name="unknown"
        )
        
        try:
            # Get application info
            response = requests.get(f"{ui_url}/api/v1/applications")
            if response.status_code == 200:
                apps = response.json()
                if apps:
                    app = apps[0]  # Assume first app
                    log_data.app_id = app.get('id', 'unknown')
                    log_data.app_name = app.get('name', 'unknown')
                    
                    # Get jobs
                    self._fetch_jobs(ui_url, log_data)
                    
                    # Get SQL queries
                    self._fetch_sql(ui_url, log_data)
                    
                    # Get configuration
                    self._fetch_configuration(ui_url, log_data)
            else:
                self.logger.error(f"Failed to fetch Spark UI: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error parsing Spark UI: {e}")
            raise
            
        return log_data
    
    def _process_event(self, event: Dict[str, Any], log_data: SparkLogData) -> None:
        """Process a single event from the Spark event log"""
        event_type = event.get('Event')
        
        if event_type == 'SparkListenerLogStart': # Added handler for SparkListenerLogStart
            log_data.spark_version = event.get('Spark Version')

        elif event_type == 'SparkListenerApplicationStart':
            log_data.app_id = event.get('App ID', 'unknown')
            log_data.app_name = event.get('App Name', 'unknown')
            log_data.user = event.get('User') # Set user
            if 'Timestamp' in event:
                log_data.start_time = datetime.fromtimestamp(event['Timestamp'] / 1000)
                
        elif event_type == 'SparkListenerApplicationEnd':
            if 'Timestamp' in event:
                log_data.end_time = datetime.fromtimestamp(event['Timestamp'] / 1000)
                if log_data.start_time:
                    log_data.duration_ms = (log_data.end_time - log_data.start_time).total_seconds() * 1000
                    
        elif event_type == 'SparkListenerJobStart':
            job_id = event.get('Job ID')
            if job_id is not None:
                stage_infos = event.get('Stage Infos', [])
                job_info = SparkJobInfo(
                    job_id=job_id,
                    job_name=event.get('Job Name', f"Job {job_id}"),
                    submission_time=datetime.fromtimestamp(event.get('Submission Time', 0) / 1000),
                    status="RUNNING",
                    num_stages=len(stage_infos),
                    num_tasks=sum(stage.get('Number of Tasks', 0) for stage in stage_infos),
                    stage_ids=[s_info.get('Stage ID') for s_info in stage_infos if s_info.get('Stage ID') is not None] # Store stage IDs
                )
                log_data.jobs[job_id] = job_info
                
        elif event_type == 'SparkListenerJobEnd':
            job_id = event.get('Job ID')
            if job_id is not None and job_id in log_data.jobs:
                job = log_data.jobs[job_id]
                job.completion_time = datetime.fromtimestamp(event.get('Completion Time', 0) / 1000)
                raw_status = event.get('Job Result', {}).get('Result', 'UNKNOWN')
                # Standardize job status
                if raw_status == 'JobSucceeded':
                    job.status = 'SUCCEEDED'
                elif raw_status == 'JobFailed':
                    job.status = 'FAILED'
                else:
                    job.status = raw_status.upper() if isinstance(raw_status, str) else 'UNKNOWN'

                if job.submission_time and job.completion_time:
                    job.duration_ms = (job.completion_time - job.submission_time).total_seconds() * 1000
                    
        elif event_type == 'SparkListenerStageSubmitted':
            stage_info = event.get('Stage Info', {})
            stage_id = stage_info.get('Stage ID')
            if stage_id is not None:
                stage = SparkStageInfo(
                    stage_id=stage_id,
                    stage_name=stage_info.get('Stage Name', f"Stage {stage_id}"),
                    num_tasks=stage_info.get('Number of Tasks', 0),
                    submission_time=datetime.fromtimestamp(stage_info.get('Submission Time', 0) / 1000)
                )
                
                # Find the job this stage belongs to by checking job.stage_ids
                for job in log_data.jobs.values():
                    if stage_id in job.stage_ids:
                        # Check if stage already added to prevent duplicates if StageSubmitted is processed after JobStart's Stage Infos
                        if not any(s.stage_id == stage_id for s in job.stages):
                            job.stages.append(stage)
                        break
                        
        elif event_type == 'SparkListenerStageCompleted':
            stage_info_dict = event.get('Stage Info', {}) # Renamed to avoid conflict
            stage_id = stage_info_dict.get('Stage ID')
            if stage_id is not None:
                # Find the stage in the job it belongs to
                found_stage = None
                for job in log_data.jobs.values():
                    if stage_id in job.stage_ids:
                        for s in job.stages:
                            if s.stage_id == stage_id:
                                found_stage = s
                                break
                        if found_stage:
                            break
            
                if found_stage:
                    stage = found_stage # Use the found stage object
                    stage.completion_time = datetime.fromtimestamp(stage_info_dict.get('Completion Time', 0) / 1000)
                    stage.is_skipped = stage_info_dict.get('Failure Reason') is not None
                    stage.failure_reason = stage_info_dict.get('Failure Reason')
                    if stage.submission_time and stage.completion_time:
                        stage.duration_ms = (stage.completion_time - stage.submission_time).total_seconds() * 1000
                
                    # Add task metrics
                    task_metrics = stage_info_dict.get('Task Metrics')
                    if task_metrics:
                        stage.task_metrics = task_metrics
                else:
                    # If stage was not found via JobStart's Stage Infos (e.g. dynamic stages or partial log)
                    # We might need a fallback or log a warning. For now, let's try to add it if it's a new stage.
                    # This part might need more robust handling for edge cases.
                    self.logger.warning(f"Stage {stage_id} completed but was not found in any job's initial stage_ids. Attempting to associate.")
                    # Attempt to create and associate like in SparkListenerStageSubmitted as a fallback
                    stage_to_add = SparkStageInfo(
                        stage_id=stage_id,
                        stage_name=stage_info_dict.get('Stage Name', f"Stage {stage_id}"),
                        num_tasks=stage_info_dict.get('Number of Tasks', 0),
                        submission_time=datetime.fromtimestamp(stage_info_dict.get('Submission Time', 0) / 1000),
                        completion_time=datetime.fromtimestamp(stage_info_dict.get('Completion Time', 0) / 1000),
                        is_skipped=stage_info_dict.get('Failure Reason') is not None,
                        failure_reason=stage_info_dict.get('Failure Reason')
                    )
                    if stage_to_add.submission_time and stage_to_add.completion_time:
                        stage_to_add.duration_ms = (stage_to_add.completion_time - stage_to_add.submission_time).total_seconds() * 1000
                
                    task_metrics = stage_info_dict.get('Task Metrics')
                    if task_metrics:
                        stage_to_add.task_metrics = task_metrics

                    associated = False
                    for job in log_data.jobs.values():
                        if (stage_to_add.submission_time and job.submission_time and
                            stage_to_add.submission_time >= job.submission_time and
                            (not job.completion_time or stage_to_add.submission_time <= job.completion_time)):
                            if not any(s.stage_id == stage_id for s in job.stages):
                                 job.stages.append(stage_to_add)
                            associated = True
                            break
                    if not associated:
                        self.logger.error(f"Could not associate completed stage {stage_id} with any job.")

                        
        elif event_type in ('SparkListenerSQLExecutionStart', 'org.apache.spark.sql.execution.ui.SparkListenerSQLExecutionStart'):
            query_id = event.get('executionId') # Corrected key
            if query_id is not None:
                sql_info = SparkSqlInfo(
                    query_id=str(query_id),
                    description=event.get('description', ''),
                    physical_plan=event.get('physicalPlanDescription', ''),
                    details=event.get('details', ''), # Added details field
                    start_time_ms=event.get('time') # Store start time in ms
                )
                # Attempt to get logical plan if sparkPlanInfo exists
                spark_plan_info = event.get('sparkPlanInfo')
                if spark_plan_info and isinstance(spark_plan_info, dict):
                    sql_info.logical_plan = spark_plan_info.get('logical', '')
                else:
                    sql_info.logical_plan = '' # Default to empty string if not found

                log_data.sql_queries[str(query_id)] = sql_info
            
        elif event_type in ('SparkListenerSQLExecutionEnd', 'org.apache.spark.sql.execution.ui.SparkListenerSQLExecutionEnd'):
            query_id = event.get('executionId') # Corrected key
            if query_id is not None and str(query_id) in log_data.sql_queries:
                sql = log_data.sql_queries[str(query_id)]
                event_duration_ns = event.get('duration') # Spark often provides duration in nanoseconds
                if event_duration_ns is not None:
                    sql.duration_ms = event_duration_ns // 1_000_000 # Convert ns to ms
                elif sql.start_time_ms is not None:
                    end_time_ms = event.get('time') # This is the completion timestamp in ms
                    if end_time_ms is not None:
                        sql.duration_ms = end_time_ms - sql.start_time_ms
                    else:
                        sql.duration_ms = None # Or some default if end time is missing
                else:
                    sql.duration_ms = None # Fallback if no start time or direct duration
            
        elif event_type == 'SparkListenerEnvironmentUpdate':
            spark_properties = event.get('Spark Properties')
            if spark_properties:
                for key, value in spark_properties.items(): # Assuming Spark Properties is a dict
                    log_data.spark_conf[key] = value
                    if key == 'spark.version':
                        log_data.spark_version = value
            # Fallback if Spark Properties is a list of lists/tuples (older format?)
            elif isinstance(event.get('Spark Properties'), list):
                for item in event.get('Spark Properties', []):
                    if isinstance(item, (list, tuple)) and len(item) == 2:
                        log_data.spark_conf[item[0]] = item[1]
                        if item[0] == 'spark.version':
                            log_data.spark_version = item[1]

    def _fetch_jobs(self, ui_url: str, log_data: SparkLogData) -> None:
        """Fetch job information from Spark UI"""
        try:
            response = requests.get(f"{ui_url}/api/v1/applications/{log_data.app_id}/jobs")
            if response.status_code == 200:
                jobs_data = response.json()
                for job_data in jobs_data:
                    job_id = job_data.get('jobId')
                    if job_id is not None:
                        job_info = SparkJobInfo(
                            job_id=job_id,
                            job_name=job_data.get('name', f"Job {job_id}"),
                            status=job_data.get('status', 'UNKNOWN'),
                            num_stages=len(job_data.get('stageIds', [])),
                            num_tasks=job_data.get('numTasks', 0),
                            duration_ms=job_data.get('duration', 0) if job_data.get('status') != 'RUNNING' else None
                        )
                        log_data.jobs[job_id] = job_info
                        
                        # Fetch stages for this job
                        self._fetch_stages(ui_url, log_data, job_id)
            else:
                self.logger.error(f"Failed to fetch jobs: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error fetching jobs: {e}")
    
    def _fetch_stages(self, ui_url: str, log_data: SparkLogData, job_id: int) -> None:
        """Fetch stage information for a job from Spark UI"""
        try:
            response = requests.get(f"{ui_url}/api/v1/applications/{log_data.app_id}/jobs/{job_id}/stages")
            if response.status_code == 200:
                stages_data = response.json()
                for stage_data in stages_data:
                    stage_id = stage_data.get('stageId')
                    if stage_id is not None:
                        stage_info = SparkStageInfo(
                            stage_id=stage_id,
                            stage_name=stage_data.get('name', f"Stage {stage_id}"),
                            num_tasks=stage_data.get('numTasks', 0),
                            duration_ms=stage_data.get('duration', 0),
                            is_skipped=stage_data.get('status') == 'SKIPPED',
                            failure_reason=stage_data.get('failureReason')
                        )
                        
                        # Fetch task metrics for this stage
                        self._fetch_task_metrics(ui_url, log_data, job_id, stage_id, stage_info)
                        
                        if job_id in log_data.jobs:
                            log_data.jobs[job_id].stages.append(stage_info)
            else:
                self.logger.error(f"Failed to fetch stages for job {job_id}: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error fetching stages for job {job_id}: {e}")
    
    def _fetch_task_metrics(self, ui_url: str, log_data: SparkLogData, job_id: int, 
                           stage_id: int, stage_info: SparkStageInfo) -> None:
        """Fetch task metrics for a stage from Spark UI"""
        try:
            response = requests.get(
                f"{ui_url}/api/v1/applications/{log_data.app_id}/stages/{stage_id}/{0}/taskSummary"
            )
            if response.status_code == 200:
                metrics_data = response.json()
                stage_info.task_metrics = {
                    'summary': metrics_data.get('quantiles', {}),
                    'tasks': []
                }
                
                # Get individual task details
                task_response = requests.get(
                    f"{ui_url}/api/v1/applications/{log_data.app_id}/stages/{stage_id}/{0}/taskList"
                )
                if task_response.status_code == 200:
                    tasks_data = task_response.json()
                    stage_info.task_metrics['tasks'] = tasks_data
            else:
                self.logger.error(f"Failed to fetch task metrics for stage {stage_id}: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error fetching task metrics for stage {stage_id}: {e}")
    
    def _fetch_sql(self, ui_url: str, log_data: SparkLogData) -> None:
        """Fetch SQL query information from Spark UI"""
        try:
            response = requests.get(f"{ui_url}/api/v1/applications/{log_data.app_id}/sql")
            if response.status_code == 200:
                sql_data = response.json()
                for query_data in sql_data:
                    query_id = query_data.get('id')
                    if query_id is not None:
                        sql_info = SparkSqlInfo(
                            query_id=str(query_id),
                            description=query_data.get('description', ''),
                            duration_ms=query_data.get('duration', 0)
                        )
                        
                        # Get the execution details including the plan
                        details_response = requests.get(
                            f"{ui_url}/api/v1/applications/{log_data.app_id}/sql/{query_id}"
                        )
                        if details_response.status_code == 200:
                            details = details_response.json()
                            sql_info.physical_plan = details.get('planDescription', '')
                            sql_info.logical_plan = details.get('logicalPlan', '')
                            sql_info.jobs = details.get('jobs', [])
                            
                        log_data.sql_queries[str(query_id)] = sql_info
            else:
                self.logger.error(f"Failed to fetch SQL queries: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error fetching SQL queries: {e}")
    
    def _fetch_configuration(self, ui_url: str, log_data: SparkLogData) -> None:
        """Fetch Spark configuration from Spark UI"""
        try:
            response = requests.get(f"{ui_url}/api/v1/applications/{log_data.app_id}/environment")
            if response.status_code == 200:
                env_data = response.json()
                spark_props = env_data.get('sparkProperties', [])
                for prop in spark_props:
                    if len(prop) >= 2:
                        log_data.spark_conf[prop[0]] = prop[1]
            else:
                self.logger.error(f"Failed to fetch Spark configuration: {response.status_code}")
        except Exception as e:
            self.logger.error(f"Error fetching Spark configuration: {e}")
