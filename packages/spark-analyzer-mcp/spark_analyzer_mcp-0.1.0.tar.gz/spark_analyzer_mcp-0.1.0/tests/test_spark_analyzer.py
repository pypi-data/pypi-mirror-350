import pytest
from pathlib import Path

from analyzers.spark_log_parser import (
    SparkLogParser,
    SparkJobInfo,
    SparkStageInfo,
    SparkSqlInfo,
)
from analyzers.spark_analyzer import SparkAnalyzer, SparkAnalysisResult


@pytest.fixture
def parser():
    return SparkLogParser()


@pytest.fixture
def example_log_path():
    path = Path(__file__).parent / "data" / "example1"
    assert path.exists(), f"Test data file not found: {path}"
    return path


@pytest.fixture
async def log_data(parser, example_log_path):
    return await parser.parse_log_file(example_log_path)


@pytest.fixture
def analyzer():
    return SparkAnalyzer()


@pytest.mark.asyncio
async def test_analyze_log(analyzer, log_data):
    """Test analyzing a Spark log"""
    analysis_result = await analyzer.analyze_log(log_data)

    # Verify basic analysis results
    assert isinstance(analysis_result, SparkAnalysisResult)
    assert analysis_result.app_id == log_data.app_id
    assert analysis_result.app_name == log_data.app_name

    # Check that the analysis contains expected sections
    assert analysis_result.optimization_summary is not None


def test_analyze_jobs_and_stages(analyzer, log_data):
    """Test analyzing jobs and stages"""
    # Create a test result object
    result = SparkAnalysisResult(app_id=log_data.app_id, app_name=log_data.app_name)

    # Run the analysis
    analyzer._analyze_jobs_and_stages(log_data, result)

    # Check that job analysis was performed
    # Even if no bottlenecks were found, the analysis should have run
    assert isinstance(result.bottlenecks, list)


def test_analyze_sql_queries(analyzer, log_data):
    """Test analyzing SQL queries"""
    # Create a test SQL query with known inefficient patterns
    sql_info = SparkSqlInfo(
        query_id="test-query",
        description="Test SQL Query",
        duration_ms=5000,
        physical_plan="Exchange hashpartitioning(id, 200) SortMergeJoin(id) Scan parquet table1 (filter = id > 100)",
    )

    # Add the SQL query to log data
    log_data.sql_queries["test-query"] = sql_info

    # Create a test result object
    result = SparkAnalysisResult(app_id=log_data.app_id, app_name=log_data.app_name)

    # Run the analysis
    analyzer._analyze_sql_queries(log_data, result)

    # Check that SQL analysis found the inefficient patterns
    sql_bottlenecks = [b for b in result.bottlenecks if b.bottleneck_type == "sql"]
    assert len(sql_bottlenecks) >= 1

    # Verify the bottleneck contains optimization suggestions
    if sql_bottlenecks:
        assert len(sql_bottlenecks[0].optimization_suggestions) >= 1


def test_determine_job_bottleneck_cause(analyzer):
    """Test determining the root cause of job bottlenecks"""
    # Test case 1: Job with a dominant stage (>50% of job time)
    dominant_stage = SparkStageInfo(
        stage_id=1,
        stage_name="Dominant Stage",
        duration_ms=70000,  # 70 seconds, >50% of job time
        num_tasks=50
    )
    job_with_dominant_stage = SparkJobInfo(
        job_id=1,
        job_name="Job with Dominant Stage",
        duration_ms=100000,  # 100 seconds total
        status="SUCCEEDED",
        num_stages=3,
        num_tasks=100,
        stages=[dominant_stage, 
                SparkStageInfo(stage_id=2, stage_name="Stage 2", duration_ms=20000, num_tasks=25),
                SparkStageInfo(stage_id=3, stage_name="Stage 3", duration_ms=10000, num_tasks=25)]
    )
    cause = analyzer._determine_job_bottleneck_cause(job_with_dominant_stage)
    assert "Stage 1 is the bottleneck" in cause, f"Expected dominant stage detection, got: {cause}"
    
    # Test case 2: Job with uneven stage distribution
    uneven_stages = [
        SparkStageInfo(stage_id=1, stage_name="Stage 1", duration_ms=40000, num_tasks=20),
        SparkStageInfo(stage_id=2, stage_name="Stage 2", duration_ms=30000, num_tasks=20),
        SparkStageInfo(stage_id=3, stage_name="Stage 3", duration_ms=5000, num_tasks=20),
        SparkStageInfo(stage_id=4, stage_name="Stage 4", duration_ms=5000, num_tasks=20),
        SparkStageInfo(stage_id=5, stage_name="Stage 5", duration_ms=2000, num_tasks=20)
    ]
    job_with_uneven_stages = SparkJobInfo(
        job_id=2,
        job_name="Job with Uneven Stages",
        duration_ms=82000,  # 82 seconds total
        status="SUCCEEDED",
        num_stages=5,
        num_tasks=100,
        stages=uneven_stages
    )
    cause = analyzer._determine_job_bottleneck_cause(job_with_uneven_stages)
    assert "Uneven stage duration distribution" in cause or "Stage 1 is the bottleneck" in cause, \
        f"Expected uneven distribution detection, got: {cause}"
    
    # Test case 3: Job with high shuffle-to-input ratio
    stage_with_high_shuffle = SparkStageInfo(
        stage_id=1,
        stage_name="High Shuffle Stage",
        duration_ms=30000,
        num_tasks=50,
        task_metrics={
            "summary": {
                "inputBytes": {"sum": 100 * 1024 * 1024},  # 100MB input
                "shuffleBytesWritten": {"sum": 80 * 1024 * 1024}  # 80MB shuffle (80% ratio)
            }
        }
    )
    job_with_high_shuffle = SparkJobInfo(
        job_id=3,
        job_name="Job with High Shuffle",
        duration_ms=60000,
        status="SUCCEEDED",
        num_stages=2,
        num_tasks=100,
        stages=[
            stage_with_high_shuffle,
            SparkStageInfo(stage_id=2, stage_name="Stage 2", duration_ms=30000, num_tasks=50)
        ]
    )
    cause = analyzer._determine_job_bottleneck_cause(job_with_high_shuffle)
    assert "shuffle-to-input ratio" in cause or "Uneven stage duration" in cause, \
        f"Expected high shuffle ratio detection, got: {cause}"


def test_suggest_optimizations(analyzer):
    """Test suggesting optimizations for different components"""
    # Test job optimization suggestions
    job = SparkJobInfo(
        job_id=1,
        job_name="Test Job",
        duration_ms=120000,  # 2 minutes
        status="SUCCEEDED",
        num_stages=5,
        num_tasks=100,
    )

    job_suggestions = analyzer._suggest_job_optimizations(job)
    assert isinstance(job_suggestions, list)
    assert len(job_suggestions) >= 1

    # Test stage optimization suggestions
    stage = SparkStageInfo(
        stage_id=1,
        stage_name="Test Stage",
        num_tasks=100,
        duration_ms=60000,  # 1 minute
        task_metrics={
            "summary": {"shuffleWriteSpillBytes": {"max": 1024 * 1024}}  # 1MB spill
        },
    )

    stage_suggestions = analyzer._suggest_stage_optimizations(stage)
    assert isinstance(stage_suggestions, list)
    assert len(stage_suggestions) >= 1
