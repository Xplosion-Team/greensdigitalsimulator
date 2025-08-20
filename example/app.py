from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.utils
import json
from datetime import datetime
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import with error handling
try:
    from t1dsim_ai.individual_model import DigitalTwin
    DIGITAL_TWIN_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import DigitalTwin: {e}")
    DIGITAL_TWIN_AVAILABLE = False

app = Flask(__name__)

# Global variables
current_digital_twin = 1
current_scenario = None
animation_frame = 0
animation_data = None

# Scenario parameters
scenario_params = {
    'init_cgm': 110,
    'basal_insulin': 1.0,
    'carb_ratio': 12,
    'meal_size': 75,
    'meal_time': 60,
    'heart_rate': 70
}

def load_patient_data(digital_twin_id):
    """Load real patient data from the data files"""
    try:
        # Try to load from the data_example.csv file
        data_file = os.path.join(os.path.dirname(__file__), 'data_example', 'data_example.csv')
        print(f"Looking for data file: {data_file}")
        print(f"File exists: {os.path.exists(data_file)}")
        
        if os.path.exists(data_file):
            print(f"Loading patient data from {data_file}")
            df = pd.read_csv(data_file)
            print(f"Loaded CSV with shape: {df.shape}")
            print(f"CSV columns: {df.columns.tolist()}")
            
            # Select a 24-hour window of data
            df_subset = df.head(288)  # 24 hours * 12 data points per hour (5-minute intervals)
            
            # Ensure required columns exist
            required_columns = ['output_cgm', 'input_insulin', 'input_meal_carbs', 'heart_rate', 
                              'sleep_efficiency', 'is_train', 'feat_hour_of_day_sin', 
                              'feat_hour_of_day_cos', 'feat_is_weekend', 'heart_rate_WRTbaseline']
            
            for col in required_columns:
                if col not in df_subset.columns:
                    if col == 'output_cgm':
                        df_subset[col] = scenario_params['init_cgm']
                    elif col == 'input_insulin':
                        df_subset[col] = scenario_params['basal_insulin']
                    elif col == 'input_meal_carbs':
                        df_subset[col] = 0.0
                    elif col == 'heart_rate':
                        df_subset[col] = scenario_params['heart_rate']
                    elif col == 'sleep_efficiency':
                        df_subset[col] = 0.0
                    elif col == 'is_train':
                        df_subset[col] = 1.0
                    elif col == 'feat_hour_of_day_sin':
                        df_subset[col] = 0.0
                    elif col == 'feat_hour_of_day_cos':
                        df_subset[col] = 1.0
                    elif col == 'feat_is_weekend':
                        df_subset[col] = 0.0
                    elif col == 'heart_rate_WRTbaseline':
                        df_subset[col] = 0.0
            
            print(f"Loaded {len(df_subset)} data points with columns: {df_subset.columns.tolist()}")
            return df_subset
        else:
            print(f"Data file not found: {data_file}")
            return create_simple_scenario()
    except Exception as e:
        print(f"Error loading patient data: {e}")
        return create_simple_scenario()

def create_simple_scenario():
    """Create a simple scenario DataFrame"""
    global current_scenario
    
    # Create a simple scenario DataFrame
    sim_time = 5 * 60  # 5 hours
    n_points = sim_time // 5  # 5-minute intervals
    
    # Create time array
    base_date = datetime(2024, 8, 15, 8, 0, 0)  # Start at 8 AM
    time_range = pd.date_range(base_date, periods=n_points, freq='5 min')
    
    # Create scenario DataFrame
    current_scenario = pd.DataFrame()
    current_scenario['time'] = time_range
    
    # Initialize all columns to 0
    current_scenario['output_cgm'] = 0.0
    current_scenario['input_insulin'] = scenario_params['basal_insulin']
    current_scenario['input_meal_carbs'] = 0.0
    current_scenario['heart_rate'] = scenario_params['heart_rate']
    current_scenario['sleep_efficiency'] = 0.0
    current_scenario['feat_hour_of_day_cos'] = np.cos(2 * np.pi * current_scenario['time'].dt.hour / 24)
    current_scenario['feat_hour_of_day_sin'] = np.sin(2 * np.pi * current_scenario['time'].dt.hour / 24)
    current_scenario['feat_is_weekend'] = 0.0
    current_scenario['heart_rate_WRTbaseline'] = 0.0
    
    # Set initial CGM
    current_scenario.loc[0, 'output_cgm'] = scenario_params['init_cgm']
    
    # Add meal at specified time
    meal_idx = scenario_params['meal_time'] // 5
    if meal_idx < len(current_scenario):
        current_scenario.loc[meal_idx, 'input_meal_carbs'] = scenario_params['meal_size']
        # Add bolus insulin for meal
        bolus_insulin = scenario_params['meal_size'] / scenario_params['carb_ratio']
        current_scenario.loc[meal_idx, 'input_insulin'] = scenario_params['basal_insulin'] + bolus_insulin
    
    # Add sleep period (10 PM to 6 AM)
    sleep_start = 14 * 12  # 10 PM (14 hours from 8 AM)
    sleep_end = 22 * 12    # 6 AM (22 hours from 8 AM)
    if sleep_start < len(current_scenario):
        end_idx = min(sleep_end, len(current_scenario))
        current_scenario.loc[sleep_start:end_idx, 'sleep_efficiency'] = 1.0
        current_scenario.loc[sleep_start:end_idx, 'heart_rate'] = scenario_params['heart_rate'] - 10
    
    return current_scenario

def generate_plot(frame=None):
    """Generate the simulation plot with Plotly"""
    global current_scenario, current_digital_twin, animation_data
    
    try:
        if current_scenario is None:
            current_scenario = load_patient_data(current_digital_twin)
        
        if not DIGITAL_TWIN_AVAILABLE:
            print("ERROR: DigitalTwin not available - cannot generate real simulation data")
            # Return error plot
            fig = go.Figure()
            fig.add_annotation(text='DigitalTwin not available - please check installation', 
                             xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(size=16))
            fig.update_layout(title='Error: DigitalTwin Not Available', height=400)
            plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return plot_json
            
        else:
            # Use real DigitalTwin
            print(f"Creating DigitalTwin with n_digitalTwin={current_digital_twin}")
            myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
            print(f"Running simulation...")
            df_simulation = myDigitalTwin.simulate(current_scenario)
            print(f"Simulation completed. Result shape: {df_simulation.shape}")
            
            # Debug: Print available columns and check Actual CGM data
            print(f"Available columns in df_simulation: {df_simulation.columns.tolist()}")
            print(f"df_simulation shape: {df_simulation.shape}")
            
            # Use real patient CGM data
            if 'output_cgm' in df_simulation.columns:
                cgm_actual_data = df_simulation.output_cgm.values
                print(f"Using real patient CGM data from output_cgm - range: {cgm_actual_data.min():.1f} to {cgm_actual_data.max():.1f}")
            elif 'cgm_Actual' in df_simulation.columns:
                cgm_actual_data = df_simulation.cgm_Actual.values
                print(f"Using cgm_Actual column - range: {cgm_actual_data.min():.1f} to {cgm_actual_data.max():.1f}")
            else:
                print("WARNING: No CGM data found, using fallback data")
                cgm_actual_data = np.full(len(df_simulation), scenario_params['init_cgm'])
            
            # Debug: Check what columns are available and their data
            print(f"=== COLUMN ANALYSIS ===")
            print(f"Available columns: {df_simulation.columns.tolist()}")
            
            # Check if the AI model columns exist
            has_cgm_nnpop = 'cgm_NNPop' in df_simulation.columns
            has_cgm_nndt = 'cgm_NNDT' in df_simulation.columns
            print(f"Has cgm_NNPop: {has_cgm_nnpop}")
            print(f"Has cgm_NNDT: {has_cgm_nndt}")
            
            if has_cgm_nnpop:
                pop_data = df_simulation.cgm_NNPop.values
                actual_data = df_simulation.output_cgm.values
                print(f"Population Model data range: {pop_data.min():.1f} to {pop_data.max():.1f}")
                print(f"Population Model first 5 values: {pop_data[:5]}")
                print(f"Actual CGM first 5 values: {actual_data[:5]}")
                print(f"Are Population and Actual identical? {np.array_equal(pop_data, actual_data)}")
                print(f"Population vs Actual correlation: {np.corrcoef(pop_data, actual_data)[0,1]:.3f}")
            else:
                print("WARNING: cgm_NNPop column not found - using fallback")
                
            if has_cgm_nndt:
                dt_data = df_simulation.cgm_NNDT.values
                print(f"Digital Twin data range: {dt_data.min():.1f} to {dt_data.max():.1f}")
                print(f"Digital Twin first 5 values: {dt_data[:5]}")
            else:
                print("WARNING: cgm_NNDT column not found - using fallback")
            
            # Store animation data for frame-by-frame access
            animation_data = {
                'time_hours': np.arange(len(df_simulation)) / 12,
                'cgm_actual': cgm_actual_data,
                'cgm_pop': df_simulation.cgm_NNPop.values if 'cgm_NNPop' in df_simulation.columns else np.full(len(df_simulation), scenario_params['init_cgm']),
                'cgm_dt': df_simulation.cgm_NNDT.values if 'cgm_NNDT' in df_simulation.columns else np.full(len(df_simulation), scenario_params['init_cgm']),
                'insulin': df_simulation.input_insulin.values if 'input_insulin' in df_simulation.columns else np.full(len(df_simulation), scenario_params['basal_insulin']),
                'meal_mask': df_simulation.input_meal_carbs != 0 if 'input_meal_carbs' in df_simulation.columns else np.zeros(len(df_simulation), dtype=bool)
            }
            
            # Determine data range for animation
            time_hours = animation_data['time_hours']
            if frame is not None and frame < len(time_hours):
                end_idx = frame + 1
                time_hours_plot = time_hours[:end_idx]
                cgm_actual_plot = animation_data['cgm_actual'][:end_idx]
                cgm_pop_plot = animation_data['cgm_pop'][:end_idx]
                cgm_dt_plot = animation_data['cgm_dt'][:end_idx]
                insulin_plot = animation_data['insulin'][:end_idx]
                meal_mask_plot = animation_data['meal_mask'][:end_idx]
            else:
                time_hours_plot = time_hours
                cgm_actual_plot = animation_data['cgm_actual']
                cgm_pop_plot = animation_data['cgm_pop']
                cgm_dt_plot = animation_data['cgm_dt']
                insulin_plot = animation_data['insulin']
                meal_mask_plot = animation_data['meal_mask']
            
            # Add debugging
            print(f"=== QUICK DATA TEST ===")
            print(f"Are arrays empty?")
            print(f"  time_hours_plot empty: {len(time_hours_plot) == 0}")
            print(f"  cgm_actual_plot empty: {len(cgm_actual_plot) == 0}")
            print(f"  cgm_pop_plot empty: {len(cgm_pop_plot) == 0}")
            print(f"  cgm_dt_plot empty: {len(cgm_dt_plot) == 0}")

            print(f"Are arrays all the same value?")
            if len(cgm_actual_plot) > 0:
                print(f"  cgm_actual all same: {np.all(cgm_actual_plot == cgm_actual_plot[0])}")
                print(f"  cgm_actual value: {cgm_actual_plot[0]}")
                print(f"  cgm_actual range: {cgm_actual_plot.min():.1f} to {cgm_actual_plot.max():.1f}")
                print(f"  cgm_actual first 5 values: {cgm_actual_plot[:5]}")
            if len(cgm_pop_plot) > 0:
                print(f"  cgm_pop all same: {np.all(cgm_pop_plot == cgm_pop_plot[0])}")
                print(f"  cgm_pop value: {cgm_pop_plot[0]}")
                print(f"  cgm_pop range: {cgm_pop_plot.min():.1f} to {cgm_pop_plot.max():.1f}")
            if len(cgm_dt_plot) > 0:
                print(f"  cgm_dt all same: {np.all(cgm_dt_plot == cgm_dt_plot[0])}")
                print(f"  cgm_dt value: {cgm_dt_plot[0]}")
                print(f"  cgm_dt range: {cgm_dt_plot.min():.1f} to {cgm_dt_plot.max():.1f}")
            
            print(f"Time range: {time_hours_plot.min():.1f} to {time_hours_plot.max():.1f} hours")
            print(f"Number of data points: {len(time_hours_plot)}")
            
            # Check for NaN or infinite values
            print(f"Any NaN in cgm_actual: {np.any(np.isnan(cgm_actual_plot))}")
            print(f"Any infinite in cgm_actual: {np.any(np.isinf(cgm_actual_plot))}")
            print(f"Any NaN in cgm_pop: {np.any(np.isnan(cgm_pop_plot))}")
            print(f"Any infinite in cgm_pop: {np.any(np.isinf(cgm_pop_plot))}")
            print(f"Any NaN in cgm_dt: {np.any(np.isnan(cgm_dt_plot))}")
            print(f"Any infinite in cgm_dt: {np.any(np.isinf(cgm_dt_plot))}")

            # Create Plotly figure
            fig = go.Figure()
            
            # Debug: Check data before creating traces
            print(f"Creating traces with:")
            print(f"  time_hours_plot: {len(time_hours_plot)} points, type: {type(time_hours_plot)}")
            print(f"  cgm_actual_plot: {len(cgm_actual_plot)} points, type: {type(cgm_actual_plot)}")
            print(f"  cgm_pop_plot: {len(cgm_pop_plot)} points, type: {type(cgm_pop_plot)}")
            print(f"  cgm_dt_plot: {len(cgm_dt_plot)} points, type: {type(cgm_dt_plot)}")
            
            # Convert numpy arrays to lists for Plotly
            time_list = time_hours_plot.tolist() if hasattr(time_hours_plot, 'tolist') else list(time_hours_plot)
            cgm_actual_list = cgm_actual_plot.tolist() if hasattr(cgm_actual_plot, 'tolist') else list(cgm_actual_plot)
            cgm_pop_list = cgm_pop_plot.tolist() if hasattr(cgm_pop_plot, 'tolist') else list(cgm_pop_plot)
            cgm_dt_list = cgm_dt_plot.tolist() if hasattr(cgm_dt_plot, 'tolist') else list(cgm_dt_plot)
            
            print(f"After conversion:")
            print(f"  time_list: {len(time_list)} points")
            print(f"  cgm_actual_list: {len(cgm_actual_list)} points")
            
            # Add CGM traces with thicker, more visible lines and different styles
            fig.add_trace(go.Scatter(x=time_list, y=cgm_actual_list, mode='lines+markers', 
                                   name='Actual CGM', line=dict(color='#FF0000', width=5),
                                   marker=dict(size=3, color='#FF0000')))
            fig.add_trace(go.Scatter(x=time_list, y=cgm_pop_list, mode='lines+markers', 
                                   name='Population Model', line=dict(color='#0000FF', width=4),
                                   marker=dict(size=2, color='#0000FF')))
            fig.add_trace(go.Scatter(x=time_list, y=cgm_dt_list, mode='lines+markers', 
                                   name='Digital Twin', line=dict(color='#00FF00', width=4),
                                   marker=dict(size=2, color='#00FF00')))
            
            # Test line removed - real CGM data is working!
            
            # Debug meal information
            print(f"=== MEAL ANALYSIS ===")
            print(f"Meal mask sum: {np.sum(meal_mask_plot)} meals found")
            meal_times = time_hours_plot[meal_mask_plot]
            print(f"Meal times: {meal_times}")
            if np.sum(meal_mask_plot) > 0:
                meal_carbs_debug = df_simulation.input_meal_carbs[meal_mask_plot].values
                print(f"Meal carbs: {meal_carbs_debug}")
            else:
                print("Meal carbs: No meals")
            print(f"User meal time: {scenario_params['meal_time']} minutes")
            print(f"User meal size: {scenario_params['meal_size']}g carbs")
            
            # Add meal markers
            if len(meal_times) > 0:
                meal_carbs = df_simulation.input_meal_carbs.iloc[:len(meal_mask_plot)][meal_mask_plot]
                fig.add_trace(go.Scatter(x=meal_times, y=[250] * len(meal_times), mode='markers',
                                       name='Meals', marker=dict(color='#F0E68C', size=10, symbol='diamond')))
            else:
                print("WARNING: No meals found in the data!")
            
            # Add target range
            fig.add_hrect(y0=70, y1=180, fillcolor="lightblue", opacity=0.2, 
                         annotation_text="Target Range", annotation_position="top left")
            
            # Add threshold lines
            fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Hypo Threshold")
            fig.add_hline(y=180, line_dash="dash", line_color="red", annotation_text="Hyper Threshold")
            fig.add_hline(y=250, line_dash="dash", line_color="orange", annotation_text="High Threshold")
            
            # Update layout
            scenario_text = f'CGM={scenario_params["init_cgm"]} mg/dL, Basal={scenario_params["basal_insulin"]} U/h, Meal={scenario_params["meal_size"]}g at {scenario_params["meal_time"]}min'
            fig.update_layout(
                title=f'Greens Health Simulator - Patient {current_digital_twin}<br>{scenario_text}',
                xaxis_title='Time (hours)',
                yaxis_title='CGM (mg/dL)',
                yaxis_range=[40, 380],
                height=600,
                showlegend=True,
                template='plotly_white'
            )
            
            # Convert to JSON
            plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            print(f"Plot JSON length: {len(plot_json)}")
            
            # Debug: Check what's in the JSON
            try:
                plot_data = json.loads(plot_json)
                print(f"Number of traces in JSON: {len(plot_data.get('data', []))}")
                for i, trace in enumerate(plot_data.get('data', [])):
                    print(f"Trace {i}: {trace.get('name', 'unnamed')} - {len(trace.get('x', []))} points")
                    if trace.get('x') and trace.get('y'):
                        x_vals = trace['x']
                        y_vals = trace['y']
                        if isinstance(x_vals, list) and len(x_vals) > 0:
                            print(f"  X range: {min(x_vals):.1f} to {max(x_vals):.1f}")
                        if isinstance(y_vals, list) and len(y_vals) > 0:
                            print(f"  Y range: {min(y_vals):.1f} to {max(y_vals):.1f}")
            except Exception as e:
                print(f"Error parsing JSON: {e}")
            
            return plot_json
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        import traceback
        traceback.print_exc()
        
        # Return a simple error plot
        try:
            fig = go.Figure()
            fig.add_annotation(text=f'Error: {str(e)}', xref="paper", yref="paper",
                             x=0.5, y=0.5, showarrow=False, font=dict(size=16))
            fig.update_layout(title='Error Loading Plot', height=400)
            plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            return plot_json
        except Exception as fallback_error:
            print(f"Fallback plot also failed: {fallback_error}")
            return '{"error": "Plot generation failed"}'
        insulin_plot = animation_data['insulin'][:end_idx]
        meal_mask_plot = animation_data['meal_mask'][:end_idx]
    else:
        time_hours_plot = time_hours
        cgm_actual_plot = animation_data['cgm_actual']
        cgm_pop_plot = animation_data['cgm_pop']
        cgm_dt_plot = animation_data['cgm_dt']
        insulin_plot = animation_data['insulin']
        meal_mask_plot = animation_data['meal_mask']
    
    # Plot glucose data
    ax1.plot(time_hours_plot, cgm_actual_plot, 'o-', color=color_actual, ms=3, lw=1, label='Actual CGM')
    ax1.plot(time_hours_plot, cgm_pop_plot, 'o-', color=color_pop, ms=2, lw=1, label='Population Model')
    ax1.plot(time_hours_plot, cgm_dt_plot, 'o-', color=color_dt, ms=2, lw=1, label='Digital Twin')
    
    # Add meal markers
    if meal_mask_plot.any():
        meal_times = time_hours_plot[meal_mask_plot]
        # Get meal carbs for the current window only
        meal_carbs = df_simulation.input_meal_carbs.iloc[:len(meal_mask_plot)][meal_mask_plot]
        ax1.scatter(meal_times, [350] * len(meal_times), c=color_carbs, s=100, marker='^', label='Meals')
        for i, (t, carbs) in enumerate(zip(meal_times, meal_carbs)):
            ax1.annotate(f'{carbs}g', (t, 350), xytext=(0, 10), textcoords='offset points', 
                        ha='center', fontsize=8, fontweight='bold')
    
    # Setup glucose plot
    ax1.set_ylim(40, 380)
    ax1.set_ylabel('CGM [mg/dL]', fontweight='bold')
    ax1.grid(True, alpha=0.3, color='#E0E0E0')  # Light gray grid
    ax1.axhspan(70, 180, facecolor='#20B2AA', alpha=0.2, label='Target Range')  # Teal target range
    ax1.axhline(y=70, color='#FF6347', alpha=0.7, linestyle='--', lw=2)  # Orange-red warning line
    ax1.axhline(y=180, color='#FF6347', alpha=0.7, linestyle='--', lw=2)  # Orange-red warning line
    ax1.axhline(y=250, color='#F0E68C', alpha=0.7, linestyle='--', lw=2)  # Cream high line
    ax1.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax1.set_facecolor('#FAFAFA')  # Light gray background
    
    # Plot insulin data
    ax2.plot(time_hours_plot, insulin_plot, color=color_insulin, lw=2, label='Insulin [U/h]')
    ax2.set_ylabel('Insulin [U/h]', fontweight='bold')
    ax2.set_xlabel('Time [hours]', fontweight='bold')
    ax2.grid(True, alpha=0.3, color='#E0E0E0')  # Light gray grid
    ax2.legend()
    ax2.set_facecolor('#FAFAFA')  # Light gray background
    
    # Add scenario info
    scenario_text = f'Scenario: CGM={scenario_params["init_cgm"]} mg/dL, Basal={scenario_params["basal_insulin"]} U/h, Meal={scenario_params["meal_size"]}g at {scenario_params["meal_time"]}min'
    fig.suptitle(f'Greens Health Simulator - Patient {current_digital_twin}\n{scenario_text}', 
                 fontsize=14, fontweight='bold', color='#8B4513')  # Dark Reddish Brown title
    
    # Set figure background
    fig.patch.set_facecolor('#FAFAFA')  # Light gray background
    
    plt.tight_layout()
    
    # Convert plot to base64 string
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=150, bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return plot_url

@app.route('/')
def index():
    """Main page"""
    try:
        print("Index route called")
        plot_json = generate_plot()
        print(f"Plot generated successfully")
        return render_template('index.html', plot_json=plot_json, params=scenario_params, digital_twin=current_digital_twin)
    except Exception as e:
        print(f"Error in index route: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 500

@app.route('/update_scenario', methods=['POST'])
def update_scenario():
    """Update scenario parameters and regenerate plot"""
    global current_scenario
    
    try:
        data = request.get_json()
        
        # Update scenario parameters
        if 'init_cgm' in data:
            scenario_params['init_cgm'] = float(data['init_cgm'])
        if 'basal_insulin' in data:
            scenario_params['basal_insulin'] = float(data['basal_insulin'])
        if 'carb_ratio' in data:
            scenario_params['carb_ratio'] = float(data['carb_ratio'])
        if 'meal_size' in data:
            scenario_params['meal_size'] = float(data['meal_size'])
        if 'meal_time' in data:
            scenario_params['meal_time'] = float(data['meal_time'])
        if 'digital_twin' in data:
            global current_digital_twin
            new_digital_twin = int(data['digital_twin'])
            if new_digital_twin != current_digital_twin:
                current_digital_twin = new_digital_twin
                # Reload patient data for new digital twin
                current_scenario = load_patient_data(current_digital_twin)
        
        # Create new scenario if needed
        if current_scenario is None:
            current_scenario = load_patient_data(current_digital_twin)
        plot_json = generate_plot()
        
        return jsonify({
            'plot_json': plot_json,
            'params': scenario_params,
            'digital_twin': current_digital_twin
        })
    except Exception as e:
        print(f"Error in update_scenario: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_stats')
def get_stats():
    """Get simulation statistics"""
    global current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = load_patient_data(current_digital_twin)
    
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Calculate statistics
    actual_glucose = df_simulation.cgm_Actual
    pop_glucose = df_simulation.cgm_NNPop
    dt_glucose = df_simulation.cgm_NNDT
    
    stats = {
        'actual': {
            'mean': float(round(actual_glucose.mean(), 1)),
            'max': float(round(actual_glucose.max(), 1)),
            'min': float(round(actual_glucose.min(), 1)),
            'time_in_range': float(round(((actual_glucose >= 70) & (actual_glucose <= 180)).sum() / len(actual_glucose) * 100, 1))
        },
        'population': {
            'mean': float(round(pop_glucose.mean(), 1)),
            'max': float(round(pop_glucose.max(), 1)),
            'min': float(round(pop_glucose.min(), 1)),
            'time_in_range': float(round(((pop_glucose >= 70) & (pop_glucose <= 180)).sum() / len(pop_glucose) * 100, 1))
        },
        'digital_twin': {
            'mean': float(round(dt_glucose.mean(), 1)),
            'max': float(round(dt_glucose.max(), 1)),
            'min': float(round(dt_glucose.min(), 1)),
            'time_in_range': float(round(((dt_glucose >= 70) & (dt_glucose <= 180)).sum() / len(dt_glucose) * 100, 1))
        }
    }
    
    return jsonify(stats)

@app.route('/get_animation_frame/<int:frame>')
def get_animation_frame(frame):
    """Get animation frame"""
    global animation_frame
    animation_frame = frame
    plot_url = generate_plot(frame)
    return jsonify({'plot_url': plot_url, 'frame': frame})

@app.route('/start_animation')
def start_animation():
    """Start animation sequence"""
    global animation_frame
    animation_frame = 0
    return jsonify({'status': 'started', 'frame': animation_frame})

@app.route('/get_animation_data')
def get_animation_data():
    """Get animation data for client-side animation"""
    global animation_data, current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = load_patient_data(current_digital_twin)
    
    myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
    df_simulation = myDigitalTwin.simulate(current_scenario)
    
    # Prepare data for client-side animation
    time_hours = np.arange(len(df_simulation)) / 12
    animation_data = {
        'time_hours': time_hours.tolist(),
        'cgm_actual': df_simulation.cgm_Actual.tolist(),
        'cgm_pop': df_simulation.cgm_NNPop.tolist(),
        'cgm_dt': df_simulation.cgm_NNDT.tolist(),
        'insulin': df_simulation.input_insulin.tolist(),
        'meal_times': time_hours[df_simulation.input_meal_carbs != 0].tolist(),
        'meal_carbs': df_simulation.input_meal_carbs[df_simulation.input_meal_carbs != 0].tolist(),
        'total_frames': len(time_hours)
    }
    
    return jsonify(animation_data)

if __name__ == '__main__':
    print("Starting Greens Health Simulator...")
    print("Open your browser and go to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 