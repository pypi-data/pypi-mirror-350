#!/usr/bin/env python3
"""
Spark Log Analyzer MCP Server using FastMCP.
Accepts a ZIP file containing Spark event logs, analyzes them, and returns insights.
"""

import zipfile
from pathlib import Path
from typing import Dict, Any, Optional, List

from fastmcp import FastMCP
from loguru import logger

from spark_analyzer_mcp.spark_log_parser import SparkLogParser
from spark_analyzer_mcp.spark_analyzer import SparkAnalyzer, SparkAnalysisResult

# Initialize FastMCP server
mcp = FastMCP("Spark Log Analyzer")
parser = SparkLogParser()  # single parser instance with built-in caching

def _find_spark_log_file(extract_dir: Path) -> Optional[Path]:
    """Find a suitable Spark log file in the extracted directory."""
    primary_candidates = []
    secondary_candidates = []

    for item in extract_dir.rglob("*"):  # rglob for recursive search
        if item.is_file():
            if "eventlog" in item.name.lower():
                primary_candidates.append(item)
            elif item.suffix.lower() in [".log", ".txt"] or not item.suffix:
                secondary_candidates.append(item)

    if primary_candidates:
        logger.info(f"Found primary log candidate(s): {primary_candidates}")
        return primary_candidates[0]  # Take the first eventlog found
    if secondary_candidates:
        logger.info(f"Found secondary log candidate(s): {secondary_candidates}")
        return secondary_candidates[
            0
        ]  # Take the first .log, .txt or extensionless file

    logger.warning(f"No suitable Spark log file found in {extract_dir}")
    return None


@mcp.tool()
async def analyze_spark_log_zip(zip_file_path: str) -> Dict[str, Any]:
    """
    Analyze Spark event logs contained within a ZIP file.

    Args:
        zip_file_path: Absolute or relative path to the ZIP file.

    Returns:
        Dictionary containing Spark log analysis results or an error message.
    """
    # Use parser with built-in caching to load SparkLogData
    try:
        log_data = await parser.parse_event_log_zip(zip_file_path)
    except FileNotFoundError as e:
        logger.error(str(e))
        return {"error": str(e), "exists": False}
    except zipfile.BadZipFile:
        logger.error(f"Invalid ZIP file format: {zip_file_path}")
        return {"error": f"Invalid ZIP file format: {zip_file_path}"}
    analyzer = SparkAnalyzer()

    # Analyze the parsed data
    logger.info(f"Analyzing parsed log data for App ID: {log_data.app_id}")
    analysis_result: SparkAnalysisResult = await analyzer.analyze_log(log_data)
    logger.info(f"Log analysis complete for App ID: {log_data.app_id}")
    return analysis_result.model_dump(mode="json")


@mcp.tool()
async def list_jobs(zip_file_path: str) -> List[Dict[str, Any]]:
    """List all jobs with metadata."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.list_jobs()


@mcp.tool()
async def sort_jobs_by_duration(zip_file_path: str) -> List[Dict[str, Any]]:
    """Jobs sorted by duration descending."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return [job.model_dump(mode="json") for job in log_data.sort_jobs_by_duration()]


@mcp.tool()
async def identify_outlier_jobs(zip_file_path: str) -> List[Dict[str, Any]]:
    """Jobs with duration > mean+2*std."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return [job.model_dump(mode="json") for job in log_data.identify_outlier_jobs()]


@mcp.tool()
async def list_stages_for_job(zip_file_path: str, job_id: int) -> List[Dict[str, Any]]:
    """List stages by duration for a job."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return [stage.model_dump(mode="json") for stage in log_data.list_stages_for_job(job_id)]


@mcp.tool()
async def get_stage_metrics(zip_file_path: str, stage_id: int) -> Dict[str, Any]:
    """Detailed metrics for a stage."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.get_stage_metrics(stage_id)


@mcp.tool()
async def get_tasks_for_stage(zip_file_path: str, stage_id: int) -> List[Dict[str, Any]]:
    """Retrieve tasks for a stage."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.get_tasks_for_stage(stage_id)


@mcp.tool()
async def compute_task_duration_stats(zip_file_path: str, stage_id: int) -> Dict[str, Any]:
    """Task duration statistics for a stage."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.compute_task_duration_stats(stage_id)


@mcp.tool()
async def list_sql_executions(zip_file_path: str) -> List[str]:
    """List SQL execution IDs."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.list_sql_executions()


@mcp.tool()
async def get_sql_query_text(zip_file_path: str, execution_id: str) -> Optional[str]:
    """Get SQL query text by execution ID."""
    log_data = await parser.parse_event_log_zip(zip_file_path)
    return log_data.get_sql_query_text(execution_id)


if __name__ == "__main__":
    logger.info("Starting Spark Log Analyzer MCP Server...")
    # Configure logger for better output if desired
    # logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    mcp.run()
