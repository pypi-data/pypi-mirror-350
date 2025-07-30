import pytest
from pathlib import Path
from datetime import datetime

from analyzers.spark_log_parser import SparkLogParser, SparkLogData, SparkJobInfo, SparkStageInfo, SparkSqlInfo, SparkStackTrace


@pytest.fixture
def parser():
    return SparkLogParser()

@pytest.fixture
def example_log_path():
    path = Path(__file__).parent / "data" / "example1"
    assert path.exists(), f"Test data file not found: {path}"
    return path

@pytest.mark.asyncio
async def test_parse_log_file(parser, example_log_path):
    """Test parsing a Spark event log file"""
    log_data = await parser.parse_log_file(example_log_path)
    
    # Verify basic log data was parsed correctly
    assert isinstance(log_data, SparkLogData)
    assert log_data.app_id == "spark-19ff21b189a24541aed07fb40733f576"
    assert log_data.app_name == "app-dss-run-in-pe-16781-250"
    assert log_data.spark_version == "3.3.0"
    
    # Verify job data was parsed
    assert len(log_data.jobs) >= 1
    assert 0 in log_data.jobs  # Job ID 0 should be present
    
    # Check job details
    job = log_data.jobs.get(0)
    assert isinstance(job, SparkJobInfo)
    assert job.status == "SUCCEEDED"
    
    # Verify application start and end times
    assert log_data.start_time is not None
    assert log_data.end_time is not None
    assert log_data.duration_ms > 0
    
def test_process_event(parser):
    """Test processing individual events from the log"""
    # Create a minimal log data object
    log_data = SparkLogData(
        app_id="test-app-id",
        app_name="test-app"
    )
    
    # Test processing an application start event
    app_start_event = {
        "Event": "SparkListenerApplicationStart",
        "App Name": "test-app",
        "App ID": "test-app-id",
        "Timestamp": 1748005604335,
        "User": "test-user"
    }
    parser._process_event(app_start_event, log_data)
    assert log_data.user == "test-user"
    assert log_data.start_time == datetime.fromtimestamp(app_start_event["Timestamp"]/1000)
    
    # Test processing a job start event
    job_start_event = {
        "Event": "SparkListenerJobStart",
        "Job ID": 1,
        "Submission Time": 1748005619881,
        "Stage Infos": [
            {"Stage ID": 1, "Stage Name": "test stage", "Number of Tasks": 10}
        ]
    }
    parser._process_event(job_start_event, log_data)
    assert 1 in log_data.jobs
    assert log_data.jobs[1].job_id == 1
    assert log_data.jobs[1].num_stages == 1
    
    # Test processing a stage completed event
    stage_complete_event = {
        "Event": "SparkListenerStageCompleted",
        "Stage Info": {
            "Stage ID": 1,
            "Stage Name": "test stage",
            "Number of Tasks": 10,
            "Submission Time": 1748005619900,
            "Completion Time": 1748005621000,
            "Failure Reason": None
        }
    }
    parser._process_event(stage_complete_event, log_data)
    assert len(log_data.jobs[1].stages) == 1
    assert log_data.jobs[1].stages[0].stage_id == 1
    assert log_data.jobs[1].stages[0].duration_ms == 1100  # 1.1 seconds
    
    # Test processing a job end event
    job_end_event = {
        "Event": "SparkListenerJobEnd",
        "Job ID": 1,
        "Completion Time": 1748005622238,
        "Job Result": {"Result": "JobSucceeded"}
    }
    parser._process_event(job_end_event, log_data)
    assert log_data.jobs[1].status == "SUCCEEDED"
    assert log_data.jobs[1].completion_time == datetime.fromtimestamp(job_end_event["Completion Time"]/1000)
    
    # Test processing a SQL execution start event
    sql_start_event = {
        "Event": "org.apache.spark.sql.execution.ui.SparkListenerSQLExecutionStart",
        "executionId": 1,
        "description": "SELECT * FROM test_table",
        "details": "test details",
        "physicalPlanDescription": "Exchange hashpartitioning(id, 200)",
        "time": 1748005620000
    }
    parser._process_event(sql_start_event, log_data)
    assert "1" in log_data.sql_queries
    assert log_data.sql_queries["1"].description == "SELECT * FROM test_table"
    
    # Test processing a SQL execution end event
    sql_end_event = {
        "Event": "org.apache.spark.sql.execution.ui.SparkListenerSQLExecutionEnd",
        "executionId": 1,
        "time": 1748005621500
    }
    parser._process_event(sql_end_event, log_data)
    assert log_data.sql_queries["1"].duration_ms == 1500  # 1.5 seconds
    
def test_bottleneck_jobs():
    """Test identifying bottleneck jobs"""
    log_data = SparkLogData(
        app_id="test-app-id",
        app_name="test-app"
    )
    
    # Add a non-bottleneck job
    log_data.jobs[1] = SparkJobInfo(
        job_id=1,
        job_name="Fast Job",
        duration_ms=5000,  # 5 seconds
        status="SUCCEEDED"
    )
    
    # Add a bottleneck job
    log_data.jobs[2] = SparkJobInfo(
        job_id=2,
        job_name="Slow Job",
        duration_ms=120000,  # 2 minutes
        status="SUCCEEDED"
    )
    
    bottlenecks = log_data.bottleneck_jobs
    assert len(bottlenecks) == 1
    assert bottlenecks[0].job_id == 2

def test_job_is_bottleneck():
    """Test identifying bottleneck jobs via SparkJobInfo.is_bottleneck property"""
    # Create a non-bottleneck job
    fast_job = SparkJobInfo(
        job_id=1,
        job_name="Fast Job",
        duration_ms=5000,  # 5 seconds
        status="SUCCEEDED"
    )
    assert not fast_job.is_bottleneck
    
    # Create a bottleneck job
    slow_job = SparkJobInfo(
        job_id=2,
        job_name="Slow Job",
        duration_ms=120000,  # 2 minutes
        status="SUCCEEDED"
    )
    assert slow_job.is_bottleneck

def test_stage_has_skew():
    """Test detecting data skew in stages"""
    # Create a stage with no skew
    no_skew_stage = SparkStageInfo(
        stage_id=1,
        stage_name="No Skew Stage",
        num_tasks=5,
        task_metrics={
            "tasks": [
                {"duration_ms": 100},
                {"duration_ms": 105},
                {"duration_ms": 95},
                {"duration_ms": 110},
                {"duration_ms": 90}
            ]
        }
    )
    assert not no_skew_stage.has_skew
    
    # Create a stage with significant skew
    skew_stage = SparkStageInfo(
        stage_id=2,
        stage_name="Skewed Stage",
        num_tasks=5,
        task_metrics={
            "tasks": [
                {"duration_ms": 100},
                {"duration_ms": 90},
                {"duration_ms": 500},  # Outlier
                {"duration_ms": 110},
                {"duration_ms": 95}
            ]
        }
    )
    assert skew_stage.has_skew

def test_sql_should_optimize():
    """Test identifying SQL queries that should be optimized"""
    # Create a SQL query with inefficient patterns
    inefficient_sql = SparkSqlInfo(
        query_id="1",
        description="SELECT * FROM large_table JOIN small_table ON large_table.id = small_table.id",
        physical_plan="SortMergeJoin(id) Scan parquet large_table Scan parquet small_table"
    )
    assert inefficient_sql.should_optimize
    
    # Create a SQL query without inefficient patterns
    efficient_sql = SparkSqlInfo(
        query_id="2",
        description="SELECT * FROM small_table",
        physical_plan="Scan parquet small_table"
    )
    assert not efficient_sql.should_optimize

def test_stack_trace_memory_related():
    """Test identifying memory-related stack traces"""
    # Create a memory-related stack trace
    memory_trace = SparkStackTrace(
        exception_type="java.lang.OutOfMemoryError",
        message="Java heap space",
        full_trace="java.lang.OutOfMemoryError: Java heap space\n  at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:347)"
    )
    assert memory_trace.is_memory_related
    
    # Create a non-memory-related stack trace
    other_trace = SparkStackTrace(
        exception_type="java.lang.NullPointerException",
        message="Object is null",
        full_trace="java.lang.NullPointerException: Object is null\n  at com.example.MyClass.process(MyClass.java:42)"
    )
    assert not other_trace.is_memory_related
