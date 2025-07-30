from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from loguru import logger

from analyzers.spark_log_parser import SparkLogData, SparkJobInfo, SparkStageInfo, SparkSqlInfo


class BottleneckInfo(BaseModel):
    """Information about a bottleneck in Spark execution"""
    bottleneck_type: str  # 'job', 'stage', 'sql', 'configuration'
    id: str  # Job ID, Stage ID, SQL ID, or config key
    name: Optional[str] = None
    description: str
    duration_ms: Optional[int] = None
    impact_level: str  # 'high', 'medium', 'low'
    root_cause: Optional[str] = None
    optimization_suggestions: List[str] = Field(default_factory=list)
    related_code: Optional[str] = None


class SparkAnalysisResult(BaseModel):
    """Results of Spark log analysis"""
    app_id: str
    app_name: str
    total_duration_ms: Optional[int] = None
    bottlenecks: List[BottleneckInfo] = Field(default_factory=list)
    configuration_issues: List[Dict[str, Any]] = Field(default_factory=list)
    optimization_summary: Optional[str] = None


class SparkAnalyzer:
    """Analyzer for Spark logs to identify bottlenecks and optimization opportunities"""
    
    def __init__(self):
        self.logger = logger
    
    async def analyze_log(self, log_data: SparkLogData) -> SparkAnalysisResult:
        """
        Analyze Spark log data to identify bottlenecks and optimization opportunities
        
        Args:
            log_data: Parsed SparkLogData object
            
        Returns:
            Analysis results with bottlenecks and optimization suggestions
        """
        self.logger.info("Analyzing Spark log for app: %s - %s" % (log_data.app_id, log_data.app_name))
        
        # Initialize analysis result
        result = SparkAnalysisResult(
            app_id=log_data.app_id,
            app_name=log_data.app_name,
            total_duration_ms=log_data.duration_ms
        )
        
        # Analyze jobs and stages
        self._analyze_jobs_and_stages(log_data, result)
        
        # Analyze SQL queries
        self._analyze_sql_queries(log_data, result)
        
        # Analyze Spark configuration
        self._analyze_configuration(log_data, result)
        
        # Generate optimization summary
        result.optimization_summary = self._generate_summary(result)
        
        return result
    
    def _analyze_jobs_and_stages(self, log_data: SparkLogData, result: SparkAnalysisResult) -> None:
        """Analyze jobs and stages to identify bottlenecks"""
        # Sort jobs by duration to find the longest-running jobs
        sorted_jobs = sorted(
            [job for job in log_data.jobs.values() if job.duration_ms is not None],
            key=lambda j: j.duration_ms or 0,
            reverse=True
        )
        
        # Analyze top N longest jobs
        for job in sorted_jobs[:5]:  # Focus on top 5 longest jobs
            if job.is_bottleneck:
                bottleneck = BottleneckInfo(
                    bottleneck_type="job",
                    id=str(job.job_id),
                    name=job.job_name,
                    description="Long-running job with %d stages and %d tasks" % (job.num_stages, job.num_tasks),
                    duration_ms=job.duration_ms,
                    impact_level="high" if job.duration_ms and job.duration_ms > 120000 else "medium",
                    root_cause=self._determine_job_bottleneck_cause(job)
                )
                
                # Add optimization suggestions
                bottleneck.optimization_suggestions = self._suggest_job_optimizations(job)
                
                result.bottlenecks.append(bottleneck)
            
            # Analyze stages within this job
            self._analyze_stages(job, result)
    
    def _analyze_stages(self, job: SparkJobInfo, result: SparkAnalysisResult) -> None:
        """Analyze stages within a job to identify bottlenecks"""
        # Sort stages by duration
        sorted_stages = sorted(
            [stage for stage in job.stages if stage.duration_ms is not None],
            key=lambda s: s.duration_ms or 0,
            reverse=True
        )
        
        # Analyze top N longest stages
        for stage in sorted_stages[:3]:  # Focus on top 3 longest stages per job
            # Check if stage is significantly long or has skew
            is_long_stage = stage.duration_ms and stage.duration_ms > 60000  # > 1 minute
            
            if is_long_stage or stage.has_skew:
                impact = "high" if is_long_stage and stage.has_skew else "medium"
                
                description = "Stage in job %s" % job.job_id
                if is_long_stage:
                    description += ", long duration"
                if stage.has_skew:
                    description += ", data skew detected"
                
                bottleneck = BottleneckInfo(
                    bottleneck_type="stage",
                    id="%s.%s" % (job.job_id, stage.stage_id),
                    name=stage.stage_name,
                    description=description,
                    duration_ms=stage.duration_ms,
                    impact_level=impact,
                    root_cause=self._determine_stage_bottleneck_cause(stage)
                )
                
                # Add optimization suggestions
                bottleneck.optimization_suggestions = self._suggest_stage_optimizations(stage)
                
                result.bottlenecks.append(bottleneck)
    
    def _analyze_sql_queries(self, log_data: SparkLogData, result: SparkAnalysisResult) -> None:
        """Analyze SQL queries to identify optimization opportunities"""
        # Get SQL queries that should be optimized
        sql_to_optimize = log_data.sql_to_optimize
        
        # Sort by duration
        sorted_sql = sorted(
            sql_to_optimize,
            key=lambda s: s.duration_ms or 0,
            reverse=True
        )
        
        for sql in sorted_sql:
            # Find associated jobs
            related_jobs = []
            for job_id in sql.jobs:
                if job_id in log_data.jobs:
                    related_jobs.append(log_data.jobs[job_id])
            
            # Determine impact level based on duration and related job bottlenecks
            impact = "medium"
            if sql.duration_ms and sql.duration_ms > 60000:  # > 1 minute
                impact = "high"
            elif any(job.is_bottleneck for job in related_jobs):
                impact = "high"
            
            bottleneck = BottleneckInfo(
                bottleneck_type="sql",
                id=sql.query_id,
                name=sql.description[:50] + "..." if sql.description and len(sql.description) > 50 else sql.description,
                description="SQL query with optimization opportunities",
                duration_ms=sql.duration_ms,
                impact_level=impact,
                root_cause=self._analyze_sql_plan(sql)
            )
            
            # Add optimization suggestions
            bottleneck.optimization_suggestions = self._suggest_sql_optimizations(sql)
            
            result.bottlenecks.append(bottleneck)
    
    def _analyze_configuration(self, log_data: SparkLogData, result: SparkAnalysisResult) -> None:
        """Analyze Spark configuration for potential issues"""
        # Check for common configuration issues
        config_issues = []
        
        # Memory configuration
        if 'spark.executor.memory' in log_data.spark_conf:
            executor_mem = log_data.spark_conf['spark.executor.memory']
            if executor_mem.endswith('g') or executor_mem.endswith('G'):
                mem_value = int(executor_mem[:-1])
                if mem_value < 4:  # Less than 4GB
                    config_issues.append({
                        "key": "spark.executor.memory",
                        "value": executor_mem,
                        "issue": "Low executor memory",
                        "suggestion": "Increase executor memory to at least 4g for better performance"
                    })
        
        # Parallelism
        if 'spark.default.parallelism' not in log_data.spark_conf:
            config_issues.append({
                "key": "spark.default.parallelism",
                "value": "Not set",
                "issue": "Default parallelism not explicitly set",
                "suggestion": "Set spark.default.parallelism to 2-3x the number of cores available"
            })
        
        # Shuffle partitions
        if 'spark.sql.shuffle.partitions' in log_data.spark_conf:
            shuffle_partitions = int(log_data.spark_conf['spark.sql.shuffle.partitions'])
            if shuffle_partitions == 200:  # Default value
                config_issues.append({
                    "key": "spark.sql.shuffle.partitions",
                    "value": "200 (default)",
                    "issue": "Using default shuffle partitions",
                    "suggestion": "Adjust spark.sql.shuffle.partitions based on data size and cluster resources"
                })
        
        # Dynamic allocation
        if 'spark.dynamicAllocation.enabled' not in log_data.spark_conf or \
           log_data.spark_conf.get('spark.dynamicAllocation.enabled', 'false').lower() != 'true':
            config_issues.append({
                "key": "spark.dynamicAllocation.enabled",
                "value": log_data.spark_conf.get('spark.dynamicAllocation.enabled', 'false'),
                "issue": "Dynamic allocation not enabled",
                "suggestion": "Enable dynamic allocation for better resource utilization"
            })
        
        # Add configuration issues to result
        result.configuration_issues = config_issues
        
        # Add significant configuration issues as bottlenecks
        for issue in config_issues:
            bottleneck = BottleneckInfo(
                bottleneck_type="configuration",
                id=issue["key"],
                name=issue["key"],
                description=issue["issue"],
                impact_level="medium",
                root_cause="Current value: %s" % issue['value'],
                optimization_suggestions=[issue["suggestion"]]
            )
            result.bottlenecks.append(bottleneck)
    
    def _determine_job_bottleneck_cause(self, job: SparkJobInfo) -> str:
        """Determine the root cause of a job bottleneck using relative metrics"""
        if not job.stages:
            return "Unknown - no stage information available"
        
        # Check if there's a single long-running stage
        if job.stages and len(job.stages) > 0:
            # Sort stages by duration
            sorted_stages = sorted(
                [s for s in job.stages if s.duration_ms is not None],
                key=lambda s: s.duration_ms or 0,
                reverse=True
            )
            
            if sorted_stages and len(sorted_stages) > 0:
                longest_stage = sorted_stages[0]
                # If the longest stage accounts for >50% of job time, it's the bottleneck
                if longest_stage.duration_ms and job.duration_ms and \
                   longest_stage.duration_ms > job.duration_ms * 0.5:
                    return "Stage %d is the bottleneck, taking %.1f%% of job time" % \
                           (longest_stage.stage_id, 
                            (longest_stage.duration_ms / job.duration_ms) * 100)
                
                # Check for uneven stage distribution
                total_stages_time = sum(s.duration_ms or 0 for s in job.stages)
                if total_stages_time > 0 and len(job.stages) >= 3:  # Need at least 3 stages to detect meaningful distribution
                    # Calculate measures of inequality for stage durations
                    stage_durations = [s.duration_ms or 0 for s in job.stages]
                    mean_duration = total_stages_time / len(job.stages)
                    variance = sum((d - mean_duration)**2 for d in stage_durations) / len(job.stages)
                    std_dev = variance**0.5
                    
                    # Calculate coefficient of variation (CV) - lower threshold for complex jobs
                    cv = std_dev / mean_duration if mean_duration > 0 else 0
                    
                    # Check if max duration is significantly higher than median
                    sorted_durations = sorted(stage_durations)
                    median_duration = sorted_durations[len(sorted_durations) // 2]
                    max_duration = max(stage_durations)
                    
                    # Either high CV or max/median ratio indicates uneven distribution
                    if cv > 0.7 or (median_duration > 0 and max_duration > 2.5 * median_duration):
                        return f"Uneven stage duration distribution - CV: {cv:.2f}, max/median ratio: {max_duration/median_duration if median_duration > 0 else 0:.2f}"
        
        # Check for data skew in any stage
        skewed_stages = [s for s in job.stages if s.has_skew]
        if skewed_stages:
            return "Data skew detected in %d stages" % len(skewed_stages)
        
        # For complex jobs, focus on stage interdependencies rather than just count
        if len(job.stages) > 1:
            # Check for stage dependencies and parallelism opportunities
            stage_ids = set(s.stage_id for s in job.stages)
            parent_stage_ids = set()
            for stage in job.stages:
                if hasattr(stage, 'parent_stage_ids'):
                    parent_stage_ids.update(stage.parent_stage_ids)
            
            # If many stages have dependencies, there might be optimization opportunities
            dependency_ratio = len(parent_stage_ids.intersection(stage_ids)) / len(stage_ids) if stage_ids else 0
            if dependency_ratio > 0.7:  # High dependency ratio
                return f"Complex job with high stage interdependency ({dependency_ratio:.2f}) - potential for parallelism optimization"
        
        # Check for high shuffle-to-compute ratio across the job
        total_shuffle = sum(sum(s.task_metrics.get('summary', {}).get('shuffleBytesWritten', {}).get('sum', 0) for s in job.stages) 
                          if s.task_metrics else 0 for s in job.stages)
        total_input = sum(sum(s.task_metrics.get('summary', {}).get('inputBytes', {}).get('sum', 0) for s in job.stages) 
                        if s.task_metrics else 0 for s in job.stages)
        
        if total_input > 0 and total_shuffle > 0.5 * total_input:
            return f"High shuffle-to-input ratio ({total_shuffle/total_input:.2f}x) across job - excessive data movement"
        
        return "Multiple factors contributing to long duration"
    
    def _determine_stage_bottleneck_cause(self, stage: SparkStageInfo) -> str:
        """Determine the root cause of a stage bottleneck using relative metrics"""
        if stage.has_skew:
            return "Data skew detected - some tasks taking significantly longer than others"
        
        if not stage.task_metrics:
            return "Unknown - no task metrics available"
        
        # Check task metrics for common issues
        if 'summary' in stage.task_metrics:
            summary = stage.task_metrics['summary']
            
            # Check for shuffle spill - any spill is a problem
            if summary.get('shuffleWriteSpillBytes', {}).get('max', 0) > 0:
                return "Shuffle spill detected - memory pressure during shuffle"
            
            # Check for shuffle write compared to input data
            input_bytes_max = summary.get('inputBytes', {}).get('max', 0)
            shuffle_bytes_max = summary.get('shuffleBytesWritten', {}).get('max', 0)
            
            # If shuffle write is more than 50% of input, it's significant
            if input_bytes_max > 0 and shuffle_bytes_max > 0 and shuffle_bytes_max > 0.5 * input_bytes_max:
                return f"High shuffle-to-input ratio ({shuffle_bytes_max/input_bytes_max:.2f}x) - potential for optimization"
            
            # Check for stage duration distribution
            if 'duration' in summary:
                duration_stats = summary['duration']
                if duration_stats.get('max', 0) > 3 * duration_stats.get('median', 1):
                    return "Task duration outliers detected - some tasks taking significantly longer than median"
            
            # Check for large input relative to average task input
            if 'inputBytes' in summary and summary['inputBytes'].get('max', 0) > 2 * summary['inputBytes'].get('mean', 1):
                return "Uneven input distribution - some tasks processing significantly more data"
        
        return "Long-running stage - multiple factors may contribute"
    
    def _analyze_sql_plan(self, sql: SparkSqlInfo) -> str:
        """Analyze SQL execution plan to identify issues"""
        if not sql.physical_plan:
            return "No physical plan available for analysis"
        
        # Check for common inefficient patterns
        if 'BroadcastNestedLoopJoin' in sql.physical_plan:
            return "Inefficient BroadcastNestedLoopJoin detected - consider rewriting query"
        
        if 'SortMergeJoin' in sql.physical_plan and 'Broadcast' not in sql.physical_plan:
            return "SortMergeJoin without broadcast - consider using broadcast join for small tables"
        
        if 'Exchange hashpartitioning' in sql.physical_plan:
            return "Shuffle operation detected - potential for optimization"
        
        if 'Scan parquet' in sql.physical_plan and 'filter' in sql.physical_plan.lower():
            return "Filter applied after scanning parquet - consider partition pruning or predicate pushdown"
        
        if 'Scan csv' in sql.physical_plan:
            return "Reading from CSV format - consider converting to Parquet for better performance"
        
        return "Multiple optimization opportunities in query execution plan"
    
    def _suggest_job_optimizations(self, job: SparkJobInfo) -> List[str]:
        """Suggest optimizations for a job"""
        suggestions = []
        
        if job.has_stage_skew:
            suggestions.append("Address data skew by using salting techniques or adjusting partitioning strategy")
        
        if len(job.stages) > 10:
            suggestions.append("Consider simplifying the job by reducing the number of transformations or combining operations")
        
        # Check if job has associated SQL
        if hasattr(job, 'sql_id') and job.sql_id:
            suggestions.append("Optimize the SQL query associated with this job (see SQL recommendations)")
        
        # Generic suggestions if none specific
        if not suggestions:
            suggestions.append("Profile the job to identify specific bottlenecks in stages and tasks")
            suggestions.append("Consider caching intermediate results if the job is part of an iterative algorithm")
        
        return suggestions
    
    def _suggest_stage_optimizations(self, stage: SparkStageInfo) -> List[str]:
        """Suggest optimizations for a stage based on relative metrics"""
        suggestions = []
        
        if stage.has_skew:
            suggestions.append("Use salting or custom partitioning to address data skew")
            suggestions.append("Consider using broadcast join instead of shuffle join if one table is small")
        
        if stage.task_metrics:
            summary = stage.task_metrics.get('summary', {})
            
            # Memory-related suggestions
            if summary.get('shuffleWriteSpillBytes', {}).get('max', 0) > 0:
                suggestions.append("Increase executor memory or reduce parallelism to avoid shuffle spill")
                
                # Add specific memory tuning suggestion if we have memory metrics
                if 'memoryBytesSpilled' in summary:
                    suggestions.append(f"Consider increasing spark.executor.memory or spark.memory.fraction based on spill of {summary['memoryBytesSpilled'].get('sum', 0) / (1024*1024):.2f}MB")
            
            # I/O-related suggestions based on relative metrics
            input_bytes = summary.get('inputBytes', {})
            if input_bytes:
                # If max input is significantly higher than mean, suggest better partitioning
                if input_bytes.get('max', 0) > 2 * input_bytes.get('mean', 1):
                    suggestions.append("Improve data partitioning to balance task input sizes")
                
                # If input is large relative to available memory, suggest filtering
                if input_bytes.get('sum', 0) > 0:
                    suggestions.append("Consider data filtering earlier in the pipeline to reduce processing volume")
                    suggestions.append("Use more efficient storage format (Parquet) if not already using it")
            
            # Shuffle-related suggestions based on relative metrics
            shuffle_written = summary.get('shuffleBytesWritten', {})
            if shuffle_written:
                # If shuffle write is large relative to input, suggest optimization
                input_sum = summary.get('inputBytes', {}).get('sum', 0)
                shuffle_sum = shuffle_written.get('sum', 0)
                
                if input_sum > 0 and shuffle_sum > 0.3 * input_sum:
                    suggestions.append(f"High shuffle-to-input ratio ({shuffle_sum/input_sum:.2f}x) - tune spark.sql.shuffle.partitions based on data volume")
                    suggestions.append("Consider using broadcast variables for lookup data")
                
                # If max shuffle is much higher than mean, suggest better partitioning
                if shuffle_written.get('max', 0) > 2 * shuffle_written.get('mean', 1):
                    suggestions.append("Improve shuffle partitioning strategy to balance shuffle write sizes")
            
            # Task duration distribution analysis
            duration = summary.get('duration', {})
            if duration and duration.get('max', 0) > 3 * duration.get('median', 1):
                suggestions.append("Investigate task duration outliers - some tasks taking significantly longer than median")
        
        # Generic suggestions if none specific
        if not suggestions:
            suggestions.append("Analyze task-level metrics to identify specific bottlenecks")
        
        return suggestions
    
    def _suggest_sql_optimizations(self, sql: SparkSqlInfo) -> List[str]:
        """Suggest optimizations for a SQL query"""
        suggestions = []
        
        if not sql.physical_plan:
            return ["Analyze the SQL execution plan to identify optimization opportunities"]
        
        # Join optimizations
        if 'BroadcastNestedLoopJoin' in sql.physical_plan:
            suggestions.append("Rewrite query to avoid BroadcastNestedLoopJoin, which is very inefficient")
        
        if 'SortMergeJoin' in sql.physical_plan and 'Broadcast' not in sql.physical_plan:
            suggestions.append("Use broadcast hint for small tables: SELECT /*+ BROADCAST(small_table) */ ...")
        
        # Shuffle optimizations
        if 'Exchange hashpartitioning' in sql.physical_plan:
            suggestions.append("Tune spark.sql.shuffle.partitions based on data size")
            suggestions.append("Consider using bucketing for frequently joined columns")
        
        # Storage format optimizations
        if 'Scan parquet' in sql.physical_plan and 'filter' in sql.physical_plan.lower():
            suggestions.append("Use partitioning on frequently filtered columns")
            suggestions.append("Ensure statistics are collected: ANALYZE TABLE ... COMPUTE STATISTICS")
        
        if 'Scan csv' in sql.physical_plan:
            suggestions.append("Convert CSV data to Parquet format for better performance")
        
        # Generic suggestions if none specific
        if not suggestions:
            suggestions.append("Review the full query and execution plan for optimization opportunities")
        
        return suggestions
    
    def _generate_summary(self, result: SparkAnalysisResult) -> str:
        """Generate a summary of the analysis results"""
        if not result.bottlenecks:
            return "No significant bottlenecks identified in the Spark application."
        
        # Count bottlenecks by type and impact
        bottleneck_types = {}
        high_impact = 0
        
        for b in result.bottlenecks:
            bottleneck_types[b.bottleneck_type] = bottleneck_types.get(b.bottleneck_type, 0) + 1
            if b.impact_level == "high":
                high_impact += 1
        
        summary = "Analysis identified %d potential bottlenecks in the Spark application." % len(result.bottlenecks)
        
        # Add type breakdown
        type_summary = ", ".join(["%d %s" % (count, btype) for btype, count in bottleneck_types.items()])
        summary += " Breakdown: %s." % type_summary
        
        # Add impact summary
        if high_impact > 0:
            summary += " %d issues are high-impact and should be addressed first." % high_impact
        
        # Add configuration summary if applicable
        if result.configuration_issues:
            summary += " %d Spark configuration issues were identified." % len(result.configuration_issues)
        
        return summary
