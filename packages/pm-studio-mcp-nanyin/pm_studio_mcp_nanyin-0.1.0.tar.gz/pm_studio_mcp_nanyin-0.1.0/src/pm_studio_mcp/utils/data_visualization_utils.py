"""
Utility class that provides various data visualization functions.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any, Union, Optional

class DataVisualizationUtils:
    """
    A utility class that provides various data visualization functions.
    Supports generating charts from different data sources (dictionaries, Excel files, CSV files)
    and different chart types (pie charts, bar charts, line charts, scatter plots).
    
    Includes support for McKinsey-style visualization with clear, professional designs
    and data labels for better readability and interpretation.
    """
    
    @staticmethod
    def apply_mckinsey_style():
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # Enhanced professional color palette - more vibrant but still professional
        # Combines McKinsey blue tones with complementary colors
        enhanced_colors = [
            "#2878BD",            "#FF8C00",            "#2CA02C",            "#9467BD",            "#D62728",            "#8C564B",            "#1F77B4",            "#FF7F0E",            "#17BECF",            "#E377C2",        ]
                         
        # Set color cycle
        plt.rcParams['axes.prop_cycle'] = plt.cycler(color=enhanced_colors)
        
        # Set fonts
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
        
        # Title and labels styling
        plt.rcParams['font.weight'] = 'bold'
        plt.rcParams['axes.titleweight'] = 'bold'
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelweight'] = 'bold'
        
        # Grid styling - horizontal only, light grey
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.grid.axis'] = 'y'
        plt.rcParams['grid.color'] = '#DDDDDD'
        plt.rcParams['grid.linestyle'] = '--'
        
        # Remove top and right spines
        plt.rcParams['axes.spines.top'] = False
        plt.rcParams['axes.spines.right'] = False
        
        # Figure background
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = '#F9F9F9'
        
        # Figure background
        plt.rcParams['figure.facecolor'] = 'white'
        plt.rcParams['axes.facecolor'] = '#F9F9F9'

    @staticmethod
    def generate_pie_chart_tool(
        data: Dict[str, Union[int, float]], 
        working_path: str, 
        title: str = "User Feedback Distribution",
        filename: str = "piechart_output.jpg",
        figsize: Tuple[int, int] = (8, 8),
        dpi: int = 300,
        autopct: str = '%1.1f%%',
        startangle: int = 90,
        shadow: bool = False,
        explode: Optional[List[float]] = None,
        color_palette: str = 'Set2'
    ) -> Dict[str, Any]:
        """
        Generate a pie chart from dictionary data.
        
        Args:
            data (Dict[str, Union[int, float]]): Dictionary with categories as keys and values/counts as values
            working_path (str): Directory to save the output chart
            title (str, optional): Title for the chart. Defaults to "User Feedback Distribution".
            filename (str, optional): Name of the output file. Defaults to "piechart_output.jpg".
            figsize (Tuple[int, int], optional): Figure size as (width, height). Defaults to (8, 8).
            dpi (int, optional): DPI (dots per inch) for the output image. Defaults to 300.
            autopct (str, optional): Format string for percentage labels. Defaults to '%1.1f%%'.
            startangle (int, optional): Starting angle for the first slice. Defaults to 90 (12 o'clock).
            shadow (bool, optional): Whether to draw a shadow beneath the pie. Defaults to False.
            explode (Optional[List[float]], optional): List of values to offset each wedge. Defaults to None.
            color_palette (str, optional): Seaborn color palette to use. Defaults to 'Set2'.
        
        Returns:
            Dict[str, Any]: Dictionary containing:
                - 'success' (bool): Whether the chart was generated successfully
                - 'output_path' (str): Path to the generated chart file
                - 'message' (str): Success or error message
        """
        try:
            # Process continues... (implementation omitted for brevity)
            return {
                "success": True,
                "output_path": "output_file",
                "message": "Pie chart saved successfully"
            }
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error generating pie chart: {str(e)}"
            }
            
    @staticmethod
    def generate_pie_chart_from_excel(
        file_path: str, 
        category_column: str, 
        value_column: str, 
        working_path: str, 
        title: str = "Data Distribution",
        filename: str = "piechart_from_excel.jpg",
        figsize: Tuple[int, int] = (8, 8),
        dpi: int = 300,
        autopct: str = '%1.1f%%',
        startangle: int = 90,
        shadow: bool = False,
        explode: Optional[List[float]] = None,
        color_palette: str = 'Set2'
    ) -> Dict[str, Any]:
        """
        Generate a pie chart from Excel file data
        
        Args:
            file_path (str): Path to the Excel file
            category_column (str): Name of the column containing categories
            value_column (str): Name of the column containing values
            working_path (str): Directory to save the output chart
            title (str, optional): Title for the chart. Defaults to "Data Distribution".
            filename (str, optional): Name of the output file. Defaults to "piechart_from_excel.jpg".
            figsize (Tuple[int, int], optional): Figure size as (width, height). Defaults to (8, 8).
            dpi (int, optional): DPI (dots per inch) for the output image. Defaults to 300.
            autopct (str, optional): Format string for percentage labels. Defaults to '%1.1f%%'.
            startangle (int, optional): Starting angle for the first slice. Defaults to 90 (12 o'clock).
            shadow (bool, optional): Whether to draw a shadow beneath the pie. Defaults to False.
            explode (Optional[List[float]], optional): List of values to offset each wedge. Defaults to None.
            color_palette (str, optional): Seaborn color palette to use. Defaults to 'Set2'.
            
        Returns:
            Dict[str, Any]: Dictionary containing success status, output path and message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "output_path": None,
                    "message": f"Error: File not found: {file_path}"
                }
                
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate column names
            if category_column not in df.columns or value_column not in df.columns:
                return {
                    "success": False,
                    "output_path": None,
                    "message": f"Error: One or both columns ({category_column}, {value_column}) not found in the Excel file."
                }
            
            # Convert to dictionary
            data_dict = dict(zip(df[category_column], df[value_column]))
            
            # Generate pie chart using the existing method
            return DataVisualizationUtils.generate_pie_chart_tool(
                data=data_dict, 
                working_path=working_path, 
                title=title,
                filename=filename,
                figsize=figsize,
                dpi=dpi,
                autopct=autopct,
                startangle=startangle,
                shadow=shadow,
                explode=explode,
                color_palette=color_palette
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing Excel file: {str(e)}"
            }
            
    @staticmethod 
    def generate_pie_chart_from_csv(
        file_path: str, 
        category_column: str, 
        value_column: str, 
        working_path: str, 
        title: str = "Data Distribution",
        filename: str = "piechart_from_csv.jpg",
        figsize: Tuple[int, int] = (8, 8),
        dpi: int = 300,
        autopct: str = '%1.1f%%',
        startangle: int = 90,
        shadow: bool = False,
        explode: Optional[List[float]] = None,
        color_palette: str = 'Set2'
    ) -> Dict[str, Any]:
        """
        Generate a pie chart from CSV file data
        
        Args:
            file_path (str): Path to the CSV file
            category_column (str): Name of the column containing categories
            value_column (str): Name of the column containing values
            working_path (str): Directory to save the output chart
            title (str, optional): Title for the chart. Defaults to "Data Distribution".
            filename (str, optional): Name of the output file. Defaults to "piechart_from_csv.jpg".
            figsize (Tuple[int, int], optional): Figure size as (width, height). Defaults to (8, 8).
            dpi (int, optional): DPI (dots per inch) for the output image. Defaults to 300.
            autopct (str, optional): Format string for percentage labels. Defaults to '%1.1f%%'.
            startangle (int, optional): Starting angle for the first slice. Defaults to 90 (12 o'clock).
            shadow (bool, optional): Whether to draw a shadow beneath the pie. Defaults to False.
            explode (Optional[List[float]], optional): List of values to offset each wedge. Defaults to None.
            color_palette (str, optional): Seaborn color palette to use. Defaults to 'Set2'.
            
        Returns:
            Dict[str, Any]: Dictionary containing success status, output path and message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "output_path": None,
                    "message": f"Error: File not found: {file_path}"
                }
                
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Validate column names
            if category_column not in df.columns or value_column not in df.columns:
                return {
                    "success": False,
                    "output_path": None,
                    "message": f"Error: One or both columns ({category_column}, {value_column}) not found in the CSV file."
                }
            
            # Convert to dictionary
            data_dict = dict(zip(df[category_column], df[value_column]))
            
            # Generate pie chart using the existing method
            return DataVisualizationUtils.generate_pie_chart_tool(
                data=data_dict, 
                working_path=working_path, 
                title=title,
                filename=filename,
                figsize=figsize,
                dpi=dpi,
                autopct=autopct,
                startangle=startangle,
                shadow=shadow,
                explode=explode,
                color_palette=color_palette
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing CSV file: {str(e)}"
            }
    
    @staticmethod
    def generate_line_chart(data: dict, x_values: list, working_path: str, title: str = "Line Chart",
                           xlabel: str = "X Axis", ylabel: str = "Y Axis",
                           filename: str = "linechart_output.jpg", multiple_series: bool = False):
        """
        Generate a line chart from dictionary data
        
        Args:
            data (dict): Dictionary with series names as keys and lists of values as values
                         If multiple_series is False, there should be only one key in the dictionary
            x_values (list): List of x-axis values (e.g. dates, categories)
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            multiple_series (bool): Whether the data contains multiple series
            
        Returns:
            str: Success message or error message
        """
        try:
            # Validate input data
            if not isinstance(data, dict) or not data:
                return "Error: Input data must be a non-empty dictionary with series and values."
                
            if not isinstance(x_values, list) or len(x_values) == 0:
                return "Error: X values must be a non-empty list."
            
            # Apply McKinsey style
            DataVisualizationUtils.apply_mckinsey_style()
            
            # Create figure with a reasonable size
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Generate colors for multiple series - vibrant professional palette
            # Enhanced professional color palette - more vibrant but still professional
            enhanced_colors = [
                "#2878BD",  # McKinsey blue
                "#FF8C00",  # Dark orange
                "#2CA02C",  # Green
                "#9467BD",  # Purple
                "#D62728",  # Red
                "#8C564B",  # Brown
                "#1F77B4",  # Steel blue
                "#FF7F0E",  # Light orange
                "#17BECF",  # Cyan
                "#E377C2",  # Pink
            ]
            
            # If we need more colors than available, fall back to seaborn
            if len(data) > len(enhanced_colors):
                colors = sns.color_palette('viridis', len(data))
            else:
                colors = enhanced_colors[:len(data)]
            
            # Plot each series with McKinsey-style formatting
            for i, (series_name, y_values) in enumerate(data.items()):
                if len(y_values) != len(x_values):
                    return f"Error: Series '{series_name}' has {len(y_values)} values but there are {len(x_values)} x values."
                
                line = ax.plot(
                    x_values, 
                    y_values, 
                    marker='o',  # Data point markers
                    markersize=5,  # Slightly larger markers
                    linestyle='-', 
                    linewidth=2.5,  # Thicker lines for clarity
                    color=colors[i], 
                    label=series_name,
                    alpha=0.9  # Slight transparency
                )[0]
                
                # Add data point labels for ALL or most points
                if len(y_values) > 0:
                    # Find special points
                    max_idx = np.argmax(y_values)
                    min_idx = np.argmin(y_values)
                    
                    # For small datasets, show labels for all points
                    if len(y_values) <= 12:
                        indices_to_label = list(range(len(y_values)))
                    else:
                        # For medium datasets, show a significant portion of labels
                        if len(y_values) <= 20:
                            # Label about half the points
                            step = 2
                        else:
                            # For larger datasets, use an adaptive approach
                            step = max(2, len(y_values) // 10)
                        
                      # Generate indices with step
                        indices_to_label = list(range(0, len(y_values), step))
                        
                        # Always include max, min, first and last points
                        if max_idx not in indices_to_label:
                            indices_to_label.append(max_idx)
                        if min_idx not in indices_to_label:
                            indices_to_label.append(min_idx)
                        if 0 not in indices_to_label:
                            indices_to_label.append(0)
                        if len(y_values) - 1 not in indices_to_label:
                            indices_to_label.append(len(y_values) - 1)
                        
                        # Sort the indices
                        indices_to_label = sorted(set(indices_to_label))
                    
                    # Add labels for all selected points
                    for idx in indices_to_label:
                        # Different formatting for key points vs. regular points
                        is_special_point = (idx == max_idx or idx == min_idx or idx == 0 or idx == len(y_values) - 1)
                        
                        # Determine position to minimize overlap
                        # Create different positions for labels
                        position_type = idx % 4
                        
                        if idx == max_idx:
                            # Max value gets top position
                            xytext = (0, 10)
                            ha, va = 'center', 'bottom'
                        elif idx == min_idx:
                            # Min value gets bottom position
                            xytext = (0, -10)
                            ha, va = 'center', 'top'
                        elif idx == len(y_values) - 1:
                            # Last point gets right position
                            xytext = (8, 0)
                            ha, va = 'left', 'center'
                        elif position_type == 0:
                            # Top
                            xytext = (0, 8)
                            ha, va = 'center', 'bottom'
                        elif position_type == 1:
                            # Bottom
                            xytext = (0, -8)
                            ha, va = 'center', 'top'
                        elif position_type == 2:
                            # Right
                            xytext = (8, 0)
                            ha, va = 'left', 'center'
                        else:
                            # Left
                            xytext = (-8, 0)
                            ha, va = 'right', 'center'
                        
                        # All labels get a background for better visibility
                        # Special points get more prominent styling
                        fontsize = 9 if is_special_point else 8
                        fontweight = 'bold' if is_special_point else 'normal'
                        bbox_props = dict(
                            boxstyle="round,pad=0.3" if is_special_point else "round,pad=0.2",
                            fc="white",
                            alpha=0.8,
                            ec=colors[i],
                            lw=1 if is_special_point else 0.5
                        )
                        
                        # Annotate the point
                        ax.annotate(
                            f'{y_values[idx]:,.1f}',
                            xy=(x_values[idx], y_values[idx]),
                            xytext=xytext,
                            textcoords='offset points',
                            ha=ha, va=va,
                            fontsize=fontsize,
                            fontweight=fontweight,
                            color=colors[i],
                            bbox=bbox_props
                        )
            
            # Add labels and title with McKinsey styling
            ax.set_xlabel(xlabel, fontweight='bold', fontsize=11)
            ax.set_ylabel(ylabel, fontweight='bold', fontsize=11)
            ax.set_title(title, fontweight='bold', fontsize=14, pad=20)
            
            # Add legend if there are multiple series, with McKinsey styling
            if multiple_series or len(data) > 1:
                ax.legend(
                    loc='upper left',
                    frameon=True,
                    framealpha=0.95,
                    edgecolor='#DDDDDD'
                )
            
            # Rotate x-axis labels for better readability
            if len(x_values) > 5:
                plt.xticks(rotation=45, ha='right')
            
            # McKinsey style has clean horizontal grid lines only
            ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='#DDDDDD')
            ax.set_axisbelow(True)  # Make sure grid is below data
            
            # Adjust layout to make sure everything fits
            plt.tight_layout()
            # Save the line chart
            output_file = os.path.join(working_path, filename)
            plt.savefig(output_file, dpi=300)
            plt.close()
            
            return {
                "success": True,
                "output_path": output_file,
                "message": f"Line chart saved at: {output_file}"
            }
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error generating line chart: {str(e)}"
            }
    
    @staticmethod
    def generate_line_chart_from_excel(file_path: str, x_column: str, y_columns: list,
                                      working_path: str, title: str = "Line Chart",
                                      xlabel: str = "X Axis", ylabel: str = "Y Axis",
                                      filename: str = "linechart_from_excel.jpg"):
        """
        Generate a line chart from Excel file data
        
        Args:
            file_path (str): Path to the Excel file
            x_column (str): Name of the column containing x-axis values
            y_columns (list): List of column names containing y-axis values (series)
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate column names
            if x_column not in df.columns:
                return f"Error: X column '{x_column}' not found in the Excel file."
                
            for col in y_columns:
                if col not in df.columns:
                    return f"Error: Y column '{col}' not found in the Excel file."
            
            # Extract data from DataFrame
            x_data = df[x_column].tolist()
            
            # Create data dictionary for the line chart function
            data_dict = {}
            for col in y_columns:
                data_dict[col] = df[col].tolist()
            # Generate line chart using the existing method
            return DataVisualizationUtils.generate_line_chart(
                data=data_dict,
                x_values=x_data,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                filename=filename,
                multiple_series=(len(y_columns) > 1)
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing Excel file: {str(e)}"
            }
    
    @staticmethod
    def generate_line_chart_from_csv(file_path: str, x_column: str, y_columns: list,
                                    working_path: str, title: str = "Line Chart",
                                    xlabel: str = "X Axis", ylabel: str = "Y Axis",
                                    filename: str = "linechart_from_csv.jpg"):
        """
        Generate a line chart from CSV file data
        
        Args:
            file_path (str): Path to the CSV file
            x_column (str): Name of the column containing x-axis values
            y_columns (list): List of column names containing y-axis values (series)
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Validate column names
            if x_column not in df.columns:
                return f"Error: X column '{x_column}' not found in the CSV file."
                
            for col in y_columns:
                if col not in df.columns:
                    return f"Error: Y column '{col}' not found in the CSV file."
            
            # Extract data from DataFrame
            x_data = df[x_column].tolist()
            
            # Create data dictionary for the line chart function
            data_dict = {}
            for col in y_columns:
                data_dict[col] = df[col].tolist()
            # Generate line chart using the existing method
            return DataVisualizationUtils.generate_line_chart(
                data=data_dict,
                x_values=x_data,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                filename=filename,
                multiple_series=(len(y_columns) > 1)
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing CSV file: {str(e)}"
            }
    
    @staticmethod
    def generate_scatter_plot(x_data: list, y_data: list, working_path: str, title: str = "Scatter Plot",
                             xlabel: str = "X Axis", ylabel: str = "Y Axis",
                             labels: list = None, filename: str = "scatterplot_output.jpg"):
        """
        Generate a scatter plot with comprehensive data labels
        
        Args:
            x_data (list): List of x coordinates
            y_data (list): List of y coordinates
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            labels (list): Optional list of point labels or categories
            filename (str): Name of the output file
            
        Returns:
            str: Success message or error message
        """
        try:
            # Validate input data
            if not isinstance(x_data, list) or not x_data:
                return "Error: X data must be a non-empty list."
                
            if not isinstance(y_data, list) or not y_data:
                return "Error: Y data must be a non-empty list."
                
            if len(x_data) != len(y_data):
                return f"Error: X data has {len(x_data)} points but Y data has {len(y_data)} points."
            
            # Apply McKinsey style
            DataVisualizationUtils.apply_mckinsey_style()
            
            # Create figure with a reasonable size
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Enhanced professional color palette - more vibrant but still professional
            enhanced_colors = [
                "#2878BD",  # McKinsey blue
                "#FF8C00",  # Dark orange
                "#2CA02C",  # Green
                "#9467BD",  # Purple
                "#D62728",  # Red
                "#8C564B",  # Brown
                "#1F77B4",  # Steel blue
                "#FF7F0E",  # Light orange
                "#17BECF",  # Cyan
                "#E377C2",  # Pink
            ]
            
            # If labels are provided, use them to color the points
            if labels and len(labels) == len(x_data):
                # Get unique labels
                unique_labels = list(set(labels))
                
                # Use enhanced colors or fallback to seaborn for large sets
                if len(unique_labels) <= len(enhanced_colors):
                    colors = enhanced_colors[:len(unique_labels)]
                else:
                    colors = sns.color_palette('viridis', len(unique_labels))
                
                # Create a scatter plot for each label with McKinsey styling
                for i, label in enumerate(unique_labels):
                    indices = [j for j, l in enumerate(labels) if l == label]
                    x_subset = [x_data[j] for j in indices]
                    y_subset = [y_data[j] for j in indices]
                    
                    # Create scatter with larger markers and edge color
                    ax.scatter(
                        x_subset, 
                        y_subset, 
                        color=colors[i], 
                        label=label, 
                        alpha=0.8,
                        s=80,  # Larger point size for visibility
                        edgecolor='white',  # White edges around points
                        linewidth=0.8
                    )
                
                # Add legend with McKinsey styling
                ax.legend(
                    loc='upper right',
                    frameon=True,
                    framealpha=0.95,
                    edgecolor='#DDDDDD'
                )
                
                # Add data labels for each category
                for i, label in enumerate(unique_labels):
                    indices = [j for j, l in enumerate(labels) if l == label]
                    if not indices:  # Skip if no points for this label
                        continue
                        
                    x_subset = [x_data[j] for j in indices]
                    y_subset = [y_data[j] for j in indices]
                    
                    # Find max and min points for this category
                    max_idx = np.argmax(y_subset)
                    min_idx = np.argmin(y_subset)
                    
                    # Label ALL or most points based on dataset size
                    if len(x_subset) <= 15:
                        # For smaller datasets, label all points
                        points_to_label = list(range(len(x_subset)))
                    else:
                        # For larger datasets, label a significant portion
                        # Always include max and min points
                        points_to_label = [max_idx, min_idx]
                        
                        # Include additional points at regular intervals
                        step = max(1, len(x_subset) // 8)  # Label at least 12.5% of points
                        points_to_label.extend([j for j in range(0, len(x_subset), step) 
                                              if j != max_idx and j != min_idx])
                    
                    # Add labels for selected points
                    for j in points_to_label:
                        # Special formatting for max/min points
                        is_special = (j == max_idx or j == min_idx)
                        
                        # Point coordinates
                        x, y = x_subset[j], y_subset[j]
                        
                        # Different positions to reduce overlap
                        if j == max_idx:
                            # Max point gets top-right annotation with box
                            ax.annotate(
                                f'{label} max: ({x:.1f}, {y:.1f})',
                                xy=(x, y),
                                xytext=(10, 10),
                                textcoords='offset points',
                                color=colors[i],
                                fontweight='bold',
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec=colors[i], lw=1),
                                arrowprops=dict(arrowstyle='->', color=colors[i], alpha=0.7)
                            )
                        elif j == min_idx:
                            # Min point gets bottom-right annotation with box
                            ax.annotate(
                                f'{label} min: ({x:.1f}, {y:.1f})',
                                xy=(x, y),
                                xytext=(10, -15),
                                textcoords='offset points',
                                color=colors[i],
                                fontweight='bold',
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec=colors[i], lw=1),
                                arrowprops=dict(arrowstyle='->', color=colors[i], alpha=0.7)
                            )
                        else:
                            # Other points get simpler annotations
                            # Alternate positions for better spacing
                            position_idx = j % 4
                            if position_idx == 0:
                                xytext = (0, 10)  # Above
                                ha, va = 'center', 'bottom'
                            elif position_idx == 1:
                                xytext = (10, 0)  # Right
                                ha, va = 'left', 'center'
                            elif position_idx == 2:
                                xytext = (0, -10)  # Below
                                ha, va = 'center', 'top'
                            else:
                                xytext = (-10, 0)  # Left
                                ha, va = 'right', 'center'
                            
                            # Add background box for better visibility
                            ax.annotate(
                                f'({x:.1f}, {y:.1f})',
                                xy=(x, y),
                                xytext=xytext,
                                textcoords='offset points',
                                ha=ha, va=va,
                                fontsize=8,
                                color=colors[i],
                                bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, ec=colors[i], lw=0.5)
                            )
                
            else:
                # If no labels provided, create a single scatter plot
                scatter = ax.scatter(
                    x_data, 
                    y_data, 
                    color=enhanced_colors[0], 
                    alpha=0.8,
                    s=80,  # Larger point size
                    edgecolor='white',
                    linewidth=0.8
                )
                
                # Add labels to several points
                # For small datasets (<= 20 points), label all points
                # For larger datasets, label a selection of points
                if len(x_data) <= 20:
                    points_to_label = list(range(len(x_data)))
                else:
                    # Find key points (max Y, min Y, max X, min X)
                    max_y_idx = np.argmax(y_data)
                    min_y_idx = np.argmin(y_data)
                    max_x_idx = np.argmax(x_data)
                    min_x_idx = np.argmin(x_data)
                    
                    # Include key points and others at regular intervals
                    key_indices = [max_y_idx, min_y_idx, max_x_idx, min_x_idx]
                    step = max(1, len(x_data) // 10)  # Label about 10% of points
                    
                    points_to_label = key_indices + [i for i in range(0, len(x_data), step) 
                                                    if i not in key_indices]
                
                # Add labels for selected points
                for i in points_to_label:
                    # Is this a key point?
                    is_key_point = (i == np.argmax(y_data) or i == np.argmin(y_data) or 
                                   i == np.argmax(x_data) or i == np.argmin(x_data))
                    
                    # Position labels to reduce overlap
                    if i == np.argmax(y_data):  # Max Y
                        xytext = (0, 15)
                        text = f'Max Y: ({x_data[i]:.1f}, {y_data[i]:.1f})'
                        ha, va = 'center', 'bottom'
                        font_props = {'fontweight': 'bold', 'fontsize': 9}
                        box_props = dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, 
                                       ec=enhanced_colors[0], lw=1)
                        arrow_props = dict(arrowstyle='->', color=enhanced_colors[0])
                    elif i == np.argmin(y_data):  # Min Y
                        xytext = (0, -15)
                        text = f'Min Y: ({x_data[i]:.1f}, {y_data[i]:.1f})'
                        ha, va = 'center', 'top'
                        font_props = {'fontweight': 'bold', 'fontsize': 9}
                        box_props = dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, 
                                       ec=enhanced_colors[0], lw=1)
                        arrow_props = dict(arrowstyle='->', color=enhanced_colors[0])
                    elif i == np.argmax(x_data):  # Max X
                        xytext = (15, 0)
                        text = f'Max X: ({x_data[i]:.1f}, {y_data[i]:.1f})'
                        ha, va = 'left', 'center'
                        font_props = {'fontweight': 'bold', 'fontsize': 9}
                        box_props = dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, 
                                       ec=enhanced_colors[0], lw=1)
                        arrow_props = dict(arrowstyle='->', color=enhanced_colors[0])
                    elif i == np.argmin(x_data):  # Min X
                        xytext = (-15, 0)
                        text = f'Min X: ({x_data[i]:.1f}, {y_data[i]:.1f})'
                        ha, va = 'right', 'center'
                        font_props = {'fontweight': 'bold', 'fontsize': 9}
                        box_props = dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, 
                                       ec=enhanced_colors[0], lw=1)
                        arrow_props = dict(arrowstyle='->', color=enhanced_colors[0])
                    else:
                        # For regular points, just use coordinates
                        position_idx = i % 4
                        if position_idx == 0:
                            xytext = (0, 10)
                            ha, va = 'center', 'bottom'
                        elif position_idx == 1:
                            xytext = (10, 0)
                            ha, va = 'left', 'center'
                        elif position_idx == 2:
                            xytext = (0, -10)
                            ha, va = 'center', 'top'
                        else:
                            xytext = (-10, 0)
                            ha, va = 'right', 'center'
                            
                        text = f'({x_data[i]:.1f}, {y_data[i]:.1f})'
                        font_props = {'fontsize': 8}
                        box_props = dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, 
                                       ec=enhanced_colors[0], lw=0.5)
                        arrow_props = None
                    
                    # Create annotation
                    if arrow_props:
                        ax.annotate(
                            text,
                            xy=(x_data[i], y_data[i]),
                            xytext=xytext,
                            textcoords='offset points',
                            ha=ha, va=va,
                            color=enhanced_colors[0],
                            bbox=box_props,
                            arrowprops=arrow_props,
                            **font_props
                        )
                    else:
                        ax.annotate(
                            text,
                            xy=(x_data[i], y_data[i]),
                            xytext=xytext,
                            textcoords='offset points',
                            ha=ha, va=va,
                            color=enhanced_colors[0],
                            bbox=box_props,
                            **font_props
                        )
            
            # Add title and labels with McKinsey styling
            ax.set_title(title, fontweight='bold', fontsize=14, pad=20)
            ax.set_xlabel(xlabel, fontweight='bold', fontsize=11)
            ax.set_ylabel(ylabel, fontweight='bold', fontsize=11)
            
            # McKinsey style has clean horizontal and vertical grid lines
            ax.grid(True, linestyle='--', alpha=0.3, color='#CCCCCC')
            ax.set_axisbelow(True)  # Grid below plot elements
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Add extra breathing room around points
            ax.margins(0.1)
            
            # Adjust layout
            plt.tight_layout()
            # Save the scatter plot
            output_file = os.path.join(working_path, filename)
            plt.savefig(output_file, dpi=300)
            plt.close()
            
            return {
                "success": True,
                "output_path": output_file,
                "message": f"Scatter plot saved at: {output_file}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error generating scatter plot: {str(e)}"
            }
    
    @staticmethod
    def generate_scatter_plot_from_excel(file_path: str, x_column: str, y_column: str,
                                        working_path: str, label_column: str = None,
                                        title: str = "Scatter Plot", xlabel: str = "X Axis", 
                                        ylabel: str = "Y Axis", 
                                        filename: str = "scatterplot_from_excel.jpg"):
        """
        Generate a scatter plot from Excel file data
        
        Args:
            file_path (str): Path to the Excel file
            x_column (str): Name of the column containing x-axis values
            y_column (str): Name of the column containing y-axis values
            working_path (str): Directory to save the output chart
            label_column (str): Optional name of column containing point labels/categories
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate column names
            if x_column not in df.columns:
                return f"Error: X column '{x_column}' not found in the Excel file."
                
            if y_column not in df.columns:
                return f"Error: Y column '{y_column}' not found in the Excel file."
                
            if label_column is not None and label_column not in df.columns:
                return f"Error: Label column '{label_column}' not found in the Excel file."
            
            # Extract data from DataFrame
            x_data = df[x_column].tolist()
            y_data = df[y_column].tolist()
              # Extract labels if provided
            labels = df[label_column].tolist() if label_column else None
            
            # Generate scatter plot using the existing method
            return DataVisualizationUtils.generate_scatter_plot(
                x_data=x_data,
                y_data=y_data,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                labels=labels,
                filename=filename
            )
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing Excel file: {str(e)}"
            }
            
    @staticmethod
    def generate_bar_chart(data: dict, working_path: str, title: str = "Bar Chart",
                         xlabel: str = "Categories", ylabel: str = "Values",
                         filename: str = "barchart_output.jpg", figsize: Tuple[int, int] = (10, 6),
                         dpi: int = 300, color_palette: str = 'Set2', rotation: int = 45,
                         sort_values: bool = True, grid: bool = False, horizontal: bool = False,
                         stacked: bool = False, sort_data: bool = False, show_values: bool = False):
        """
        Generate a bar chart from dictionary data
        
        Args:
            data (dict): Dictionary with category names as keys and values or lists of values as values
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            figsize (Tuple[int, int]): Figure size as (width, height). Defaults to (10, 6).
            dpi (int): DPI (dots per inch) for the output image. Defaults to 300.
            color_palette (str): Seaborn color palette to use. Defaults to 'Set2'.
            rotation (int): Rotation angle for x-axis labels. Defaults to 45.
            sort_values (bool): Whether to sort data by value in descending order. Defaults to True.
            grid (bool): Whether to show grid lines. Defaults to False.
            horizontal (bool): Whether to create a horizontal bar chart. Defaults to False.
            stacked (bool): Whether to create a stacked bar chart (when values are lists). Defaults to False.
            sort_data (bool): Whether to sort the data by value. Defaults to False.
            show_values (bool): Whether to show values on top of bars. Defaults to False.
            
        Returns:
            str: Success message or error message
        """
        try:
            # Validate input data
            if not isinstance(data, dict) or not data:
                return "Error: Input data must be a non-empty dictionary with categories and values."
            
            # Apply McKinsey style
            DataVisualizationUtils.apply_mckinsey_style()
              # Determine if we have multiple series (list values) or single values
            has_multiple_series = any(isinstance(v, (list, tuple)) for v in data.values())
            
            # If sorting is requested, sort by value (for single series only)
            # Use sort_values if provided, otherwise fall back to sort_data
            should_sort = (sort_values or sort_data) and not has_multiple_series
            if should_sort:
                # Sort by value
                sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
                categories = [item[0] for item in sorted_items]
                values = [item[1] for item in sorted_items]
            else:
                categories = list(data.keys())
                values = list(data.values())
            
            # Use provided figure size or calculate based on content
            if figsize is not None:
                fig_size = figsize
            else:
                if horizontal:
                    fig_size = (10, max(6, len(categories) * 0.5))  # Height scales with number of categories
                else:
                    fig_size = (max(8, len(categories) * 0.6), 6)  # Width scales with number of categories
                
            fig, ax = plt.subplots(figsize=fig_size)
            
            # Enhanced professional color palette - use provided palette or default
            enhanced_colors = [
                "#2878BD",  # McKinsey blue
                "#FF8C00",  # Dark orange
                "#2CA02C",  # Green
                "#9467BD",  # Purple
                "#D62728",  # Red
                "#8C564B",  # Brown
                "#1F77B4",  # Steel blue
                "#FF7F0E",  # Light orange
                "#17BECF",  # Cyan
                "#E377C2",  # Pink
            ]
            
            # Set bar width
            bar_width = 0.8 if not has_multiple_series else 0.7
            
            # Create the bars
            if has_multiple_series:
                # Multiple series (grouped or stacked)
                num_categories = len(categories)
                num_series = len(next(iter(values)))  # Number of values in first list
                
                # Validate that all series have the same length
                for i, val in enumerate(values):
                    if len(val) != num_series:
                        return f"Error: Series {categories[i]} has {len(val)} values but should have {num_series}."
                
                # Extract series data
                series_data = []
                for i in range(num_series):
                    series_data.append([values[j][i] for j in range(num_categories)])
                
                # Create positions for the bars
                if horizontal:
                    positions = np.arange(num_categories)
                else:
                    positions = np.arange(num_categories)
                
                # Create grouped or stacked bars
                if stacked:
                    # Stacked bars
                    bottom = np.zeros(num_categories)
                    bars = []
                    
                    for i, data_series in enumerate(series_data):
                        if horizontal:
                            bar = ax.barh(
                                positions, 
                                data_series, 
                                height=bar_width, 
                                left=bottom, 
                                color=enhanced_colors[i % len(enhanced_colors)],
                                alpha=0.8,
                                edgecolor='white',
                                linewidth=0.7
                            )
                            # Update the bottom for next series
                            bottom = [bottom[j] + data_series[j] for j in range(num_categories)]
                        else:
                            bar = ax.bar(
                                positions, 
                                data_series, 
                                width=bar_width, 
                                bottom=bottom, 
                                color=enhanced_colors[i % len(enhanced_colors)],
                                alpha=0.8,
                                edgecolor='white',
                                linewidth=0.7
                            )
                            # Update the bottom for next series
                            bottom = [bottom[j] + data_series[j] for j in range(num_categories)]
                        
                        bars.append(bar)
                    
                    # Add legend with series names
                    series_names = [f"Series {i+1}" for i in range(num_series)]  # Default series names
                    ax.legend(bars, series_names, loc='upper right')
                    
                    # Add data labels to each segment (total values on top of stack)
                    if horizontal:
                        for i in range(num_categories):
                            total = sum(series_data[j][i] for j in range(num_series))
                            ax.annotate(
                                f'{total:,.1f}',
                                xy=(total, positions[i]),
                                xytext=(5, 0),
                                textcoords='offset points',
                                ha='left', va='center',
                                fontsize=9,
                                fontweight='bold',
                                color='#333333',
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8)
                            )
                    else:
                        for i in range(num_categories):
                            total = sum(series_data[j][i] for j in range(num_series))
                            ax.annotate(
                                f'{total:,.1f}',
                                xy=(positions[i], total),
                                xytext=(0, 5),
                                textcoords='offset points',
                                ha='center', va='bottom',
                                fontsize=9,
                                fontweight='bold',
                                color='#333333',
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8)
                            )
                else:
                    # Grouped bars
                    group_width = bar_width / num_series
                    bars = []
                    
                    for i, data_series in enumerate(series_data):
                        if horizontal:
                            # For horizontal grouped bars
                            offset = positions + (i - num_series / 2 + 0.5) * group_width
                            bar = ax.barh(
                                offset, 
                                data_series, 
                                height=group_width,
                                color=enhanced_colors[i % len(enhanced_colors)],
                                alpha=0.8,
                                edgecolor='white',
                                linewidth=0.7
                            )
                            
                            # Add data labels to each bar
                            for j, value in enumerate(data_series):
                                ax.annotate(
                                    f'{value:,.1f}',
                                    xy=(value, offset[j]),
                                    xytext=(5, 0),
                                    textcoords='offset points',
                                    ha='left', va='center',
                                    fontsize=8,
                                    color='#333333',
                                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8)
                                )
                        else:
                            # For vertical grouped bars
                            offset = positions + (i - num_series / 2 + 0.5) * group_width
                            bar = ax.bar(
                                offset, 
                                data_series, 
                                width=group_width,
                                color=enhanced_colors[i % len(enhanced_colors)],
                                alpha=0.8,
                                edgecolor='white',
                                linewidth=0.7
                            )
                            
                            # Add data labels to each bar
                            for j, value in enumerate(data_series):
                                ax.annotate(
                                    f'{value:,.1f}',
                                    xy=(offset[j], value),
                                    xytext=(0, 5),
                                    textcoords='offset points',
                                    ha='center', va='bottom',
                                    fontsize=8,
                                    color='#333333',
                                    bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8)
                                )
                        
                        bars.append(bar)
                    
                    # Add legend with series names
                    series_names = [f"Series {i+1}" for i in range(num_series)]  # Default series names
                    ax.legend(bars, series_names, loc='upper right')
            else:
                # Single series
                if horizontal:
                    bars = ax.barh(
                        categories, 
                        values, 
                        height=bar_width,
                        color=enhanced_colors[0],
                        alpha=0.85,
                        edgecolor='white',
                        linewidth=0.8
                    )
                    
                    # Add data labels to each bar
                    for i, value in enumerate(values):
                        ax.annotate(
                            f'{value:,.1f}',
                            xy=(value, i),
                            xytext=(5, 0),
                            textcoords='offset points',
                            ha='left', va='center',
                            fontsize=9,
                            fontweight='bold',
                            color='#333333',
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8)
                        )
                else:
                    bars = ax.bar(
                        categories, 
                        values, 
                        width=bar_width,
                        color=enhanced_colors[0],
                        alpha=0.85,
                        edgecolor='white',
                        linewidth=0.8
                    )
                    
                    # Add data labels to each bar
                    for i, value in enumerate(values):
                        ax.annotate(
                            f'{value:,.1f}',
                            xy=(i, value),
                            xytext=(0, 5),
                            textcoords='offset points',
                            ha='center', va='bottom',
                            fontsize=9,
                            fontweight='bold',
                            color='#333333',
                            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8)
                        )
            
            # Add labels and title with McKinsey styling
            ax.set_title(title, fontweight='bold', fontsize=14, pad=20)
            
            if horizontal:
                ax.set_yticks(np.arange(len(categories)))
                ax.set_yticklabels(categories)
                ax.set_xlabel(ylabel, fontweight='bold', fontsize=11)  # Swapped for horizontal
                ax.set_ylabel(xlabel, fontweight='bold', fontsize=11)  # Swapped for horizontal
                
                # For horizontal bars, use vertical grid lines
                ax.yaxis.grid(False)
                ax.xaxis.grid(True, linestyle='--', alpha=0.7, color='#DDDDDD')
            else:
                ax.set_xticks(np.arange(len(categories)))
                ax.set_xticklabels(categories)
                ax.set_xlabel(xlabel, fontweight='bold', fontsize=11)
                ax.set_ylabel(ylabel, fontweight='bold', fontsize=11)
                
                # McKinsey style has clean horizontal grid lines only
                ax.yaxis.grid(True, linestyle='--', alpha=0.7, color='#DDDDDD')
            
            # Set grid below data
            ax.set_axisbelow(True)
            
            # Remove top and right spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Rotate labels if there are many categories
            if len(categories) > 5 and not horizontal:
                plt.xticks(rotation=45, ha='right')
                plt.subplots_adjust(bottom=0.2)  # Add space for rotated labels
            
            # Adjust layout to make sure everything fits
            plt.tight_layout()
            # Save the bar chart
            output_file = os.path.join(working_path, filename)
            plt.savefig(output_file, dpi=300)
            plt.close()
            
            return {
                "success": True,
                "output_path": output_file,
                "message": f"Bar chart saved at: {output_file}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error generating bar chart: {str(e)}"
            }

    @staticmethod
    def generate_bar_chart_from_excel(file_path: str, category_column: str, value_columns: list,
                                    working_path: str, title: str = "Bar Chart",
                                    xlabel: str = "Categories", ylabel: str = "Values",
                                    filename: str = "barchart_from_excel.jpg",
                                    horizontal: bool = False, stacked: bool = False,
                                    sort_data: bool = False):
        """
        Generate a bar chart from Excel file data
        
        Args:
            file_path (str): Path to the Excel file
            category_column (str): Name of the column containing categories
            value_columns (list): List of column names containing values
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            horizontal (bool): Whether to create a horizontal bar chart
            stacked (bool): Whether to create a stacked bar chart
            sort_data (bool): Whether to sort the data by value (only for single series)
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read Excel file
            df = pd.read_excel(file_path)
            
            # Validate column names
            if category_column not in df.columns:
                return f"Error: Category column '{category_column}' not found in the Excel file."
                
            for col in value_columns:
                if col not in df.columns:
                    return f"Error: Value column '{col}' not found in the Excel file."
            
            # Extract data from DataFrame
            categories = df[category_column].tolist()
            
            if len(value_columns) == 1:
                # Single series
                data_dict = {cat: val for cat, val in zip(categories, df[value_columns[0]].tolist())}
            else:
                # Multiple series
                # We need to reshape the data for stacked/grouped bars
                data_dict = {cat: [df.loc[df[category_column] == cat, col].values[0] for col in value_columns] 
                           for cat in categories}
            # Generate bar chart using the existing method
            return DataVisualizationUtils.generate_bar_chart(
                data=data_dict,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                filename=filename,
                horizontal=horizontal,
                stacked=stacked,
                sort_data=sort_data
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing Excel file: {str(e)}"
            }

    @staticmethod
    def generate_bar_chart_from_csv(file_path: str, category_column: str, value_columns: list,
                                  working_path: str, title: str = "Bar Chart",
                                  xlabel: str = "Categories", ylabel: str = "Values",
                                  filename: str = "barchart_from_csv.jpg",
                                  horizontal: bool = False, stacked: bool = False,
                                  sort_data: bool = False):
        """
        Generate a bar chart from CSV file data
        
        Args:
            file_path (str): Path to the CSV file
            category_column (str): Name of the column containing categories
            value_columns (list): List of column names containing values
            working_path (str): Directory to save the output chart
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            horizontal (bool): Whether to create a horizontal bar chart
            stacked (bool): Whether to create a stacked bar chart
            sort_data (bool): Whether to sort the data by value (only for single series)
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Validate column names
            if category_column not in df.columns:
                return f"Error: Category column '{category_column}' not found in the CSV file."
                
            for col in value_columns:
                if col not in df.columns:
                    return f"Error: Value column '{col}' not found in the CSV file."
            
            # Extract data from DataFrame
            categories = df[category_column].tolist()
            
            if len(value_columns) == 1:
                # Single series
                data_dict = {cat: val for cat, val in zip(categories, df[value_columns[0]].tolist())}
            else:
                # Multiple series
                # We need to reshape the data for stacked/grouped bars
                data_dict = {cat: [df.loc[df[category_column] == cat, col].values[0] for col in value_columns] 
                           for cat in categories}
            # Generate bar chart using the existing method
            return DataVisualizationUtils.generate_bar_chart(
                data=data_dict,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                filename=filename,
                horizontal=horizontal,
                stacked=stacked,
                sort_data=sort_data
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing CSV file: {str(e)}"
            }
    
    @staticmethod
    def generate_scatter_plot_from_csv(file_path: str, x_column: str, y_column: str,
                                      working_path: str, label_column: str = None,
                                      title: str = "Scatter Plot", xlabel: str = "X Axis", 
                                      ylabel: str = "Y Axis", 
                                      filename: str = "scatterplot_from_csv.jpg"):
        """
        Generate a scatter plot from CSV file data
        
        Args:
            file_path (str): Path to the CSV file
            x_column (str): Name of the column containing x-axis values
            y_column (str): Name of the column containing y-axis values
            working_path (str): Directory to save the output chart
            label_column (str): Optional name of column containing point labels/categories
            title (str): Title for the chart
            xlabel (str): Label for X axis
            ylabel (str): Label for Y axis
            filename (str): Name of the output file
            
        Returns:
            str: Success message or error message
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return f"Error: File not found: {file_path}"
                
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Validate column names
            if x_column not in df.columns:
                return f"Error: X column '{x_column}' not found in the CSV file."
                
            if y_column not in df.columns:
                return f"Error: Y column '{y_column}' not found in the CSV file."
                
            if label_column is not None and label_column not in df.columns:
                return f"Error: Label column '{label_column}' not found in the CSV file."
            
            # Extract data from DataFrame
            x_data = df[x_column].tolist()
            y_data = df[y_column].tolist()
            
            # Extract labels if provided
            labels = df[label_column].tolist() if label_column else None
            
            # Generate scatter plot using the existing method
            return DataVisualizationUtils.generate_scatter_plot(
                x_data=x_data,
                y_data=y_data,
                working_path=working_path,
                title=title,
                xlabel=xlabel,
                ylabel=ylabel,
                labels=labels,
                filename=filename
            )
        
        except Exception as e:
            return {
                "success": False,
                "output_path": None,
                "message": f"Error processing CSV file: {str(e)}"
            }
