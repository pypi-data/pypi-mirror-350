#!/usr/bin/env python3
"""
Spark Log Analyzer MCP Server using FastMCP.
Accepts a ZIP file containing Spark event logs, analyzes them, and returns insights.
"""

import zipfile
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional

from fastmcp import FastMCP
from loguru import logger

from spark_analyzer_mcp.spark_log_parser import SparkLogParser, SparkLogData
from spark_analyzer_mcp.spark_analyzer import SparkAnalyzer, SparkAnalysisResult

# Initialize FastMCP server
mcp = FastMCP("Spark Log Analyzer")


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
    logger.info(f"Received request to analyze ZIP file: {zip_file_path}")
    path = Path(zip_file_path).resolve()

    if not path.exists():
        logger.error(f"ZIP file not found: {path}")
        return {"error": f"File not found: {zip_file_path}", "exists": False}

    if not zipfile.is_zipfile(path):
        logger.error(f"File is not a valid ZIP file: {path}")
        return {"error": f"Not a valid ZIP file: {zip_file_path}"}

    temp_dir_path: Optional[Path] = None
    try:
        # Create a temporary directory to extract files
        with tempfile.TemporaryDirectory() as temp_dir_name:
            temp_dir_path = Path(temp_dir_name)
            logger.info(f"Extracting ZIP file to temporary directory: {temp_dir_path}")

            with zipfile.ZipFile(path, "r") as zip_ref:
                zip_ref.extractall(temp_dir_path)

            logger.info("ZIP file extracted successfully.")

            # Find the Spark log file within the extracted contents
            spark_log_file = _find_spark_log_file(temp_dir_path)

            if not spark_log_file:
                return {"error": "No suitable Spark log file found in the ZIP archive."}

            logger.info(f"Found Spark log file: {spark_log_file.name}")

            # Initialize parser and analyzer
            parser = SparkLogParser()
            analyzer = SparkAnalyzer()

            # Parse the log file
            logger.info(f"Parsing Spark log file: {spark_log_file}")
            parsed_log_data: SparkLogData = await parser.parse_log_file(spark_log_file)
            logger.info(f"Log parsing complete for App ID: {parsed_log_data.app_id}")

            # Analyze the parsed data
            logger.info(
                f"Analyzing parsed log data for App ID: {parsed_log_data.app_id}"
            )
            analysis_result: SparkAnalysisResult = await analyzer.analyze_log(
                parsed_log_data
            )
            logger.info(f"Log analysis complete for App ID: {parsed_log_data.app_id}")

            return analysis_result.model_dump(
                mode="json"
            )  # Ensure Pydantic models are JSON serializable

    except zipfile.BadZipFile:
        logger.exception(f"Bad ZIP file format for: {path}")
        return {"error": f"Invalid ZIP file format: {zip_file_path}"}
    except FileNotFoundError as e:
        logger.exception(f"File not found during processing: {e}")
        return {"error": f"A required file was not found: {str(e)}"}
    except Exception as e:
        logger.exception(
            f"An unexpected error occurred during Spark log analysis for {zip_file_path}"
        )
        return {
            "error": f"An unexpected error occurred: {str(e)}",
            "file_path": zip_file_path,
        }
    # No finally block needed for temp_dir_path cleanup due to 'with tempfile.TemporaryDirectory()'


if __name__ == "__main__":
    logger.info("Starting Spark Log Analyzer MCP Server...")
    # Configure logger for better output if desired
    # logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
    mcp.run()
