from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.utils
import json
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import with error handling
try:
    from t1dsim_ai.individual_model import DigitalTwin
    DIGITAL_TWIN_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import DigitalTwin: {e}")
    DIGITAL_TWIN_AVAILABLE = False

# Import voice module with environment variable checks
VOICE_ENABLED = os.getenv('VOICE_ENABLED', 'true').lower() == 'true'
SPEECH_RECOGNITION_ENABLED = os.getenv('SPEECH_RECOGNITION_ENABLED', 'true').lower() == 'true'
TTS_ENABLED = os.getenv('TTS_ENABLED', 'false').lower() == 'true'

if VOICE_ENABLED and SPEECH_RECOGNITION_ENABLED:
    try:
        from voice_module import VoiceFoodLogger
        VOICE_MODULE_AVAILABLE = True
        voice_logger = VoiceFoodLogger()
        print("✅ Voice module loaded successfully")
    except ImportError as e:
        print(f"Warning: Could not import VoiceFoodLogger: {e}")
        VOICE_MODULE_AVAILABLE = False
        voice_logger = None
else:
    VOICE_MODULE_AVAILABLE = False
    voice_logger = None
    print("⚠️ Voice module disabled by environment variables")

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
    time_hours = np.arange(n_points) / 12  # Convert to hours
    
    # Create scenario data
    scenario_data = {
        'time': time_hours,
        'output_cgm': np.full(n_points, scenario_params['init_cgm']),
        'input_insulin': np.full(n_points, scenario_params['basal_insulin']),
        'input_meal_carbs': np.zeros(n_points),
        'heart_rate': np.full(n_points, scenario_params['heart_rate']),
        'sleep_efficiency': np.zeros(n_points),
        'is_train': np.ones(n_points),
        'feat_hour_of_day_sin': np.sin(2 * np.pi * time_hours / 24),
        'feat_hour_of_day_cos': np.cos(2 * np.pi * time_hours / 24),
        'feat_is_weekend': np.zeros(n_points),
        'heart_rate_WRTbaseline': np.zeros(n_points)
    }
    
    # Add a meal at the specified time
    meal_time_idx = int(scenario_params['meal_time'] / 5)
    if meal_time_idx < n_points:
        scenario_data['input_meal_carbs'][meal_time_idx] = scenario_params['meal_size']
    
    current_scenario = pd.DataFrame(scenario_data)
    return current_scenario

def generate_plot(frame=None):
    """Generate the plot data"""
    global current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = load_patient_data(current_digital_twin)
    
    try:
        # Create DigitalTwin and run simulation
        if DIGITAL_TWIN_AVAILABLE:
            print(f"Creating DigitalTwin with n_digitalTwin={current_digital_twin}")
            myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
            print("Running simulation...")
            df_simulation = myDigitalTwin.simulate(current_scenario)
            print(f"Simulation completed. Result shape: {df_simulation.shape}")
            
            # Print available columns for debugging
            print(f"Available columns in df_simulation: {df_simulation.columns.tolist()}")
            
            # Use real patient CGM data
            cgm_actual = df_simulation.output_cgm
            print(f"Using real patient CGM data from output_cgm - range: {cgm_actual.min():.1f} to {cgm_actual.max():.1f}")
            
            # Check for required columns
            has_cgm_nnpop = 'cgm_NNPop' in df_simulation.columns
            has_cgm_nndt = 'cgm_NNDT' in df_simulation.columns
            
            print("=== COLUMN ANALYSIS ===")
            print(f"Available columns: {df_simulation.columns.tolist()}")
            print(f"Has cgm_NNPop: {has_cgm_nnpop}")
            print(f"Has cgm_NNDT: {has_cgm_nndt}")
            
            if has_cgm_nnpop:
                cgm_pop = df_simulation.cgm_NNPop
                print(f"Population Model data range: {cgm_pop.min():.1f} to {cgm_pop.max():.1f}")
                print(f"Population Model first 5 values: {cgm_pop.head().values}")
                print(f"Actual CGM first 5 values: {cgm_actual.head().values}")
                print(f"Are Population and Actual identical? {np.array_equal(cgm_pop, cgm_actual)}")
                print(f"Population vs Actual correlation: {np.corrcoef(cgm_pop, cgm_actual)[0,1]:.3f}")
            else:
                cgm_pop = cgm_actual.copy()
                print("Using actual CGM for population model (cgm_NNPop not found)")
            
            if has_cgm_nndt:
                cgm_dt = df_simulation.cgm_NNDT
                print(f"Digital Twin data range: {cgm_dt.min():.1f} to {cgm_dt.max():.1f}")
                print(f"Digital Twin first 5 values: {cgm_dt.head().values}")
            else:
                cgm_dt = cgm_actual.copy()
                print("Using actual CGM for digital twin (cgm_NNDT not found)")
        else:
            # Fallback to simple simulation
            print("DigitalTwin not available, using fallback simulation")
            cgm_actual = current_scenario['output_cgm'].values
            cgm_pop = cgm_actual.copy()
            cgm_dt = cgm_actual.copy()
        
        # Prepare data for plotting
        time_hours_plot = np.arange(len(cgm_actual)) / 12  # Convert to hours
        
        # Quick data validation
        print("=== QUICK DATA TEST ===")
        print(f"Are arrays empty?")
        print(f"  time_hours_plot empty: {len(time_hours_plot) == 0}")
        print(f"  cgm_actual_plot empty: {len(cgm_actual) == 0}")
        print(f"  cgm_pop_plot empty: {len(cgm_pop) == 0}")
        print(f"  cgm_dt_plot empty: {len(cgm_dt) == 0}")
        
        print(f"Are arrays all the same value?")
        print(f"  cgm_actual all same: {np.all(cgm_actual == cgm_actual[0])}")
        if np.all(cgm_actual == cgm_actual[0]):
            print(f"  cgm_actual value: {cgm_actual[0]}")
        else:
            print(f"  cgm_actual range: {cgm_actual.min():.1f} to {cgm_actual.max():.1f}")
            print(f"  cgm_actual first 5 values: {cgm_actual[:5]}")
        
        print(f"  cgm_pop all same: {np.all(cgm_pop == cgm_pop[0])}")
        if np.all(cgm_pop == cgm_pop[0]):
            print(f"  cgm_pop value: {cgm_pop[0]}")
        else:
            print(f"  cgm_pop range: {cgm_pop.min():.1f} to {cgm_pop.max():.1f}")
        
        print(f"  cgm_dt all same: {np.all(cgm_dt == cgm_dt[0])}")
        if np.all(cgm_dt == cgm_dt[0]):
            print(f"  cgm_dt value: {cgm_dt[0]}")
        else:
            print(f"  cgm_dt range: {cgm_dt.min():.1f} to {cgm_dt.max():.1f}")
        
        print(f"Time range: {time_hours_plot[0]:.1f} to {time_hours_plot[-1]:.1f} hours")
        print(f"Number of data points: {len(time_hours_plot)}")
        
        # Check for NaN or infinite values
        print(f"Any NaN in cgm_actual: {np.any(np.isnan(cgm_actual))}")
        print(f"Any infinite in cgm_actual: {np.any(np.isinf(cgm_actual))}")
        print(f"Any NaN in cgm_pop: {np.any(np.isnan(cgm_pop))}")
        print(f"Any infinite in cgm_pop: {np.any(np.isinf(cgm_pop))}")
        print(f"Any NaN in cgm_dt: {np.any(np.isnan(cgm_dt))}")
        print(f"Any infinite in cgm_dt: {np.any(np.isinf(cgm_dt))}")
        
        # Convert to lists for JSON serialization
        print("Creating traces with:")
        print(f"  time_hours_plot: {len(time_hours_plot)} points, type: {type(time_hours_plot)}")
        print(f"  cgm_actual_plot: {len(cgm_actual)} points, type: {type(cgm_actual)}")
        print(f"  cgm_pop_plot: {len(cgm_pop)} points, type: {type(cgm_pop)}")
        print(f"  cgm_dt_plot: {len(cgm_dt)} points, type: {type(cgm_dt)}")
        
        time_list = time_hours_plot.tolist()
        cgm_actual_list = cgm_actual.tolist()
        cgm_pop_list = cgm_pop.tolist()
        cgm_dt_list = cgm_dt.tolist()
        
        print("After conversion:")
        print(f"  time_list: {len(time_list)} points")
        print(f"  cgm_actual_list: {len(cgm_actual_list)} points")
        
        # Find meal times
        meal_mask = current_scenario['input_meal_carbs'] > 0
        meal_times = time_hours_plot[meal_mask]
        meal_carbs = current_scenario['input_meal_carbs'][meal_mask]
        
        print("=== MEAL ANALYSIS ===")
        print(f"Meal mask sum: {meal_mask.sum()} meals found")
        print(f"Meal times: {meal_times}")
        print(f"Meal carbs: {meal_carbs.values}")
        print(f"User meal time: {scenario_params['meal_time']} minutes")
        print(f"User meal size: {scenario_params['meal_size']}g carbs")
        
        # Create Plotly figure
        fig = go.Figure()
        
        # Add traces
        fig.add_trace(go.Scatter(
            x=time_list,
            y=cgm_actual_list,
            mode='lines',
            name='Actual CGM',
            line=dict(color='red', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_list,
            y=cgm_pop_list,
            mode='lines',
            name='Population Model',
            line=dict(color='blue', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=time_list,
            y=cgm_dt_list,
            mode='lines',
            name='Digital Twin',
            line=dict(color='green', width=2)
        ))
        
        # Add meal markers
        if len(meal_times) > 0:
            fig.add_trace(go.Scatter(
                x=meal_times.tolist(),
                y=[250] * len(meal_times),  # Place at top of chart
                mode='markers',
                name='Meals',
                marker=dict(color='yellow', size=10, symbol='diamond'),
                text=[f"{carbs}g carbs" for carbs in meal_carbs],
                hovertemplate='<b>Meal</b><br>%{text}<extra></extra>'
            ))
        
        # Add threshold lines
        fig.add_hline(y=180, line_dash="dash", line_color="red", annotation_text="Hyper Threshold")
        fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Hypo Threshold")
        fig.add_hline(y=250, line_dash="dash", line_color="yellow", annotation_text="High Threshold")
        
        # Add target range shading
        fig.add_hrect(y0=70, y1=180, fillcolor="lightblue", opacity=0.2, annotation_text="Target Range")
        
        # Update layout
        fig.update_layout(
            title=f"Greens Health Simulator - Patient {current_digital_twin}<br><sub>CGM={scenario_params['init_cgm']:.1f} mg/dL, Basal={scenario_params['basal_insulin']:.1f} U/h, Meal={scenario_params['meal_size']:.1f}g at {scenario_params['meal_time']:.1f}min</sub>",
            xaxis_title="Time (hours)",
            yaxis_title="CGM (mg/dL)",
            yaxis_range=[50, 350],
            xaxis_range=[0, 25],
            hovermode='x unified',
            template='plotly_white'
        )
        
        # Convert to JSON
        plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        print(f"Plot JSON length: {len(plot_json)}")
        print(f"Number of traces in JSON: {len(fig.data)}")
        
        for i, trace in enumerate(fig.data):
            print(f"Trace {i}: {trace.name} - {len(trace.x)} points")
            if hasattr(trace, 'x') and trace.x:
                print(f"  X range: {min(trace.x):.1f} to {max(trace.x):.1f}")
            if hasattr(trace, 'y') and trace.y:
                print(f"  Y range: {min(trace.y):.1f} to {max(trace.y):.1f}")
        
        print("Plot generated successfully")
        return plot_json
        
    except Exception as e:
        print(f"Error generating plot: {e}")
        import traceback
        traceback.print_exc()
        return None

@app.route('/')
def index():
    """Main page"""
    print("Index route called")
    global current_scenario, current_digital_twin
    
    if current_scenario is None:
        current_scenario = load_patient_data(current_digital_twin)
    
    plot_json = generate_plot()
    
    return render_template('index.html', 
                         plot_json=plot_json, 
                         params=scenario_params,
                         voice_enabled=VOICE_ENABLED,
                         voice_module_available=VOICE_MODULE_AVAILABLE)

@app.route('/update_scenario', methods=['POST'])
def update_scenario():
    """Update simulation parameters"""
    global current_scenario, current_digital_twin
    
    try:
        data = request.get_json()
        
        # Update parameters
        if 'digital_twin' in data:
            current_digital_twin = int(data['digital_twin'])
        if 'init_cgm' in data:
            scenario_params['init_cgm'] = float(data['init_cgm'])
        if 'basal_insulin' in data:
            scenario_params['basal_insulin'] = float(data['basal_insulin'])
        if 'meal_size' in data:
            scenario_params['meal_size'] = float(data['meal_size'])
        if 'meal_time' in data:
            scenario_params['meal_time'] = float(data['meal_time'])
        
        # Reload scenario with new parameters
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
    
    try:
        if DIGITAL_TWIN_AVAILABLE:
            myDigitalTwin = DigitalTwin(n_digitalTwin=current_digital_twin)
            df_simulation = myDigitalTwin.simulate(current_scenario)
            
            # Calculate statistics
            actual_glucose = df_simulation.output_cgm
            pop_glucose = df_simulation.cgm_NNPop if 'cgm_NNPop' in df_simulation.columns else actual_glucose
            dt_glucose = df_simulation.cgm_NNDT if 'cgm_NNDT' in df_simulation.columns else actual_glucose
        else:
            # Fallback statistics
            actual_glucose = current_scenario['output_cgm']
            pop_glucose = actual_glucose
            dt_glucose = actual_glucose
        
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
    except Exception as e:
        print(f"Error getting stats: {e}")
        return jsonify({'error': str(e)}), 500

# Voice module routes (only if voice is enabled)
if VOICE_ENABLED and VOICE_MODULE_AVAILABLE:
    @app.route('/voice_log_food', methods=['POST'])
    def voice_log_food():
        """Voice log food intake"""
        try:
            # This would typically be called from a background thread
            # For now, we'll simulate the voice input
            result = voice_logger.voice_log_food()
            
            if result:
                total_carbs = sum(food['carbs'] * food['quantity'] for food in result)
                return jsonify({
                    'success': True,
                    'foods': result,
                    'total_carbs': total_carbs,
                    'message': f'Logged {len(result)} food items with {total_carbs} grams of carbohydrates'
                })
            else:
                return jsonify({'error': 'No food detected'}), 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/get_food_log')
    def get_food_log():
        """Get recent food log entries"""
        try:
            recent_foods = voice_logger.get_recent_foods(limit=10)
            total_carbs_24h = voice_logger.get_total_carbs(hours=24)
            
            return jsonify({
                'recent_foods': recent_foods,
                'total_carbs_24h': total_carbs_24h
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/clear_food_log', methods=['POST'])
    def clear_food_log():
        """Clear the food log"""
        try:
            voice_logger.clear_food_log()
            return jsonify({'success': True, 'message': 'Food log cleared'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/manual_log_food', methods=['POST'])
    def manual_log_food():
        """Manually log food intake"""
        try:
            data = request.get_json()
            food_name = data.get('food_name', '').lower()
            quantity = float(data.get('quantity', 1))
            unit = data.get('unit', 'serving')
            
            # Find food in database
            if food_name in voice_logger.food_database:
                food_info = voice_logger.food_database[food_name]
                food_item = {
                    'name': food_name,
                    'carbs': food_info['carbs'],
                    'category': food_info['category'],
                    'quantity': quantity,
                    'unit': unit
                }
                
                logged_foods = voice_logger.log_food([food_item])
                total_carbs = sum(food['carbs'] * food['quantity'] for food in logged_foods)
                
                return jsonify({
                    'success': True,
                    'foods': logged_foods,
                    'total_carbs': total_carbs,
                    'message': f'Logged {food_name} with {total_carbs} grams of carbohydrates'
                })
            else:
                return jsonify({'error': f'Food "{food_name}" not found in database'}), 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Get port from environment variable (for Render)
    port = int(os.getenv('PORT', 8080))
    host = os.getenv('HOST', '0.0.0.0')
    
    print("Starting Greens Health Simulator...")
    print(f"Voice enabled: {VOICE_ENABLED}")
    print(f"Voice module available: {VOICE_MODULE_AVAILABLE}")
    print(f"Speech recognition enabled: {SPEECH_RECOGNITION_ENABLED}")
    print(f"TTS enabled: {TTS_ENABLED}")
    print(f"Open your browser and go to: http://localhost:{port}")
    
    app.run(debug=False, host=host, port=port)
