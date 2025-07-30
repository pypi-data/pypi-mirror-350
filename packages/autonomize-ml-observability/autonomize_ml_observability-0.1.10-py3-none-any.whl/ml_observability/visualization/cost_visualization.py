"""Cost visualization utilities for LLM observability."""

import json
import os
import tempfile
from datetime import datetime
from typing import Dict, List, Optional, Union

import matplotlib.pyplot as plt
import mlflow
import pandas as pd

from ml_observability.utils import setup_logger

logger = setup_logger(__name__)


def generate_cost_summary_charts(
        costs_data: Union[List[Dict], pd.DataFrame],
        output_dir: Optional[str] = None
) -> Dict[str, str]:
    """
    Generate cost summary charts and save them to files.

    Args:
        costs_data: List of cost entries or DataFrame
        output_dir: Directory to save the charts (default: temporary directory)

    Returns:
        Dict mapping chart names to file paths
    """
    # Convert to DataFrame if needed
    if not isinstance(costs_data, pd.DataFrame):
        df = pd.DataFrame(costs_data)
    else:
        df = costs_data

    # Create output directory if not provided
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    else:
        os.makedirs(output_dir, exist_ok=True)

    chart_paths = {}

    # Ensure we have data to visualize
    if df.empty:
        logger.warning("No cost data to visualize")
        return chart_paths

    # Convert timestamp to datetime if it's a string
    if 'timestamp' in df.columns and df['timestamp'].dtype == 'object':
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Make sure we have the required columns
    required_cols = ['model', 'input_tokens', 'output_tokens', 'total_cost']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        logger.warning("Missing required columns for visualization: %s", missing_cols)
        return chart_paths

    try:
        # 1. Costs by model
        plt.figure(figsize=(10, 6))
        model_costs = df.groupby('model')['total_cost'].sum().sort_values(ascending=False)
        model_costs.plot(kind='bar', color='royalblue')
        plt.title('Total Cost by Model')
        plt.xlabel('Model')
        plt.ylabel('Cost (USD)')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        model_cost_path = os.path.join(output_dir, 'costs_by_model.png')
        plt.savefig(model_cost_path)
        plt.close()
        chart_paths['costs_by_model'] = model_cost_path

        # 2. Costs by provider (if available)
        if 'provider' in df.columns:
            plt.figure(figsize=(10, 6))
            provider_costs = df.groupby('provider')['total_cost'].sum().sort_values(ascending=False)
            provider_costs.plot(kind='bar', color='green')
            plt.title('Total Cost by Provider')
            plt.xlabel('Provider')
            plt.ylabel('Cost (USD)')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()

            provider_cost_path = os.path.join(output_dir, 'costs_by_provider.png')
            plt.savefig(provider_cost_path)
            plt.close()
            chart_paths['costs_by_provider'] = provider_cost_path

        # 3. Token usage by model
        plt.figure(figsize=(12, 7))
        token_usage = df.groupby('model')[['input_tokens', 'output_tokens']].sum()
        token_usage.plot(kind='bar', stacked=True, color=['#4CAF50', '#2196F3'])
        plt.title('Token Usage by Model')
        plt.xlabel('Model')
        plt.ylabel('Number of Tokens')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(title='Token Type')
        plt.tight_layout()

        token_usage_path = os.path.join(output_dir, 'token_usage_by_model.png')
        plt.savefig(token_usage_path)
        plt.close()
        chart_paths['token_usage_by_model'] = token_usage_path

        # 4. Cost over time (if timestamp is available)
        if 'timestamp' in df.columns:
            try:
                plt.figure(figsize=(12, 6))
                time_series = df.set_index('timestamp')
                # Group by hour
                hourly_costs = time_series.resample('H')['total_cost'].sum().fillna(0)
                hourly_costs.plot(marker='o', linestyle='-', color='#E91E63')
                plt.title('Cost Over Time')
                plt.xlabel('Time')
                plt.ylabel('Cost (USD)')
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()

                time_series_path = os.path.join(output_dir, 'costs_over_time.png')
                plt.savefig(time_series_path)
                plt.close()
                chart_paths['costs_over_time'] = time_series_path
            except Exception as e:
                logger.warning("Error generating time series chart: %s", str(e))

        # 5. Pie chart of cost distribution
        plt.figure(figsize=(10, 10))
        model_costs.plot(kind='pie', autopct='%1.1f%%', startangle=90, shadow=False)
        plt.title('Cost Distribution by Model')
        plt.ylabel('')  # Hide the ylabel
        plt.axis('equal')  # Equal aspect ratio ensures pie is circular

        pie_chart_path = os.path.join(output_dir, 'cost_distribution_pie.png')
        plt.savefig(pie_chart_path)
        plt.close()
        chart_paths['cost_distribution_pie'] = pie_chart_path

        logger.info("Generated %d cost visualization charts", len(chart_paths))

    except Exception as e:
        logger.warning("Error generating cost charts: %s", str(e))

    return chart_paths


def generate_cost_dashboard(
        costs_data: Union[List[Dict], pd.DataFrame],
        output_dir: Optional[str] = None,
        filename: str = "cost_dashboard.html"
) -> str:
    """
    Generate an HTML dashboard for cost data.

    Args:
        costs_data: List of cost entries or DataFrame
        output_dir: Directory to save the dashboard (default: temporary directory)
        filename: Name of the HTML file

    Returns:
        Path to the generated HTML file
    """
    # Convert to DataFrame if needed
    if not isinstance(costs_data, pd.DataFrame):
        df = pd.DataFrame(costs_data)
    else:
        df = costs_data

    # Create output directory if not provided
    if output_dir is None:
        output_dir = tempfile.mkdtemp()
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Ensure we have data
    if df.empty:
        logger.warning("No cost data for dashboard")
        return ""

    # Generate charts
    chart_paths = generate_cost_summary_charts(df, output_dir)

    # Calculate summary statistics
    total_cost = df['total_cost'].sum()
    total_tokens = df['input_tokens'].sum() + df['output_tokens'].sum()
    total_requests = len(df)

    # Get model costs
    model_costs = df.groupby('model')['total_cost'].sum().to_dict()

    # Get provider costs (if available)
    provider_costs = {}
    if 'provider' in df.columns:
        provider_costs = df.groupby('provider')['total_cost'].sum().to_dict()

    # Create HTML content
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LLM Cost Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f7f7f7; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            .dashboard-header {{ background-color: #2962FF; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
            .summary-box {{ background-color: white; border-radius: 5px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .metric-container {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
            .metric-box {{ background-color: white; border-radius: 5px; padding: 15px; margin-bottom: 15px; width: 30%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .metric-value {{ font-size: 24px; font-weight: bold; color: #2962FF; }}
            .metric-label {{ font-size: 14px; color: #666; margin-top: 5px; }}
            .charts-container {{ display: flex; flex-wrap: wrap; justify-content: space-between; }}
            .chart-box {{ background-color: white; border-radius: 5px; padding: 15px; margin-bottom: 20px; width: 48%; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .chart-title {{ font-size: 16px; font-weight: bold; margin-bottom: 10px; }}
            .chart-img {{ width: 100%; height: auto; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 10px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            tr:nth-child(even) {{ background-color: #f9f9f9; }}
            @media (max-width: 768px) {{
                .metric-box, .chart-box {{ width: 100%; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="dashboard-header">
                <h1>LLM Cost Dashboard</h1>
                <p>Generated on {timestamp}</p>
            </div>

            <div class="summary-box">
                <h2>Summary Statistics</h2>
                <div class="metric-container">
                    <div class="metric-box">
                        <div class="metric-value">${total_cost:.2f}</div>
                        <div class="metric-label">Total Cost</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{total_requests}</div>
                        <div class="metric-label">Total Requests</div>
                    </div>
                    <div class="metric-box">
                        <div class="metric-value">{total_tokens:,}</div>
                        <div class="metric-label">Total Tokens</div>
                    </div>
                </div>
            </div>

            <div class="charts-container">
    """

    # Add charts to the HTML
    for chart_name, chart_path in chart_paths.items():
        # Convert to relative path for HTML
        relative_path = os.path.basename(chart_path)
        title = chart_name.replace('_', ' ').title()

        html_content += f"""
                <div class="chart-box">
                    <div class="chart-title">{title}</div>
                    <img class="chart-img" src="{relative_path}" alt="{title}">
                </div>
        """

    # Add model cost table
    html_content += f"""
            </div>

            <div class="summary-box">
                <h2>Model Cost Breakdown</h2>
                <table>
                    <tr>
                        <th>Model</th>
                        <th>Total Cost</th>
                        <th>Percentage</th>
                    </tr>
    """

    for model, cost in sorted(model_costs.items(), key=lambda x: x[1], reverse=True):
        percentage = (cost / total_cost) * 100 if total_cost > 0 else 0
        html_content += f"""
                    <tr>
                        <td>{model}</td>
                        <td>${cost:.2f}</td>
                        <td>{percentage:.1f}%</td>
                    </tr>
        """

    html_content += """
                </table>
            </div>
    """

    # Add provider cost table if available
    if provider_costs:
        html_content += f"""
            <div class="summary-box">
                <h2>Provider Cost Breakdown</h2>
                <table>
                    <tr>
                        <th>Provider</th>
                        <th>Total Cost</th>
                        <th>Percentage</th>
                    </tr>
        """

        for provider, cost in sorted(provider_costs.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_cost) * 100 if total_cost > 0 else 0
            html_content += f"""
                        <tr>
                            <td>{provider}</td>
                            <td>${cost:.2f}</td>
                            <td>{percentage:.1f}%</td>
                        </tr>
            """

        html_content += """
                </table>
            </div>
        """

    html_content += """
        </div>
    </body>
    </html>
    """

    # Write the HTML file
    dashboard_path = os.path.join(output_dir, filename)
    with open(dashboard_path, 'w') as f:
        f.write(html_content)

    logger.info("Generated cost dashboard at %s", dashboard_path)
    return dashboard_path


def log_cost_visualizations_to_mlflow(
        costs_data: Union[List[Dict], pd.DataFrame],
        run_id: Optional[str] = None,
        artifact_path: str = "cost_tracking"
) -> bool:
    """
    Generate cost visualizations and log them to MLflow.

    Args:
        costs_data: List of cost entries or DataFrame
        run_id: MLflow run ID (uses active run if None)
        artifact_path: Path within MLflow artifacts

    Returns:
        True if successful, False otherwise
    """
    try:
        # Create temporary directory for artifacts
        with tempfile.TemporaryDirectory() as temp_dir:
            # Generate charts
            chart_paths = generate_cost_summary_charts(costs_data, temp_dir)

            # Generate dashboard
            dashboard_path = generate_cost_dashboard(costs_data, temp_dir)

            # Log to MLflow
            for chart_name, chart_path in chart_paths.items():
                mlflow.log_artifact(chart_path, artifact_path)

            if dashboard_path:
                mlflow.log_artifact(dashboard_path, artifact_path)

            logger.info("Logged cost visualizations to MLflow")
            return True

    except Exception as e:
        logger.warning("Failed to log cost visualizations to MLflow: %s", str(e))
        return False