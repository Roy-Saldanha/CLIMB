import subprocess
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

overlay_states = {
    "odom": True,
    "ut": True
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/toggle', methods=['POST'])
def toggle_overlay():
    data = request.json
    feature = data.get('feature') # 'odom' or 'ut'
    
    if feature in overlay_states:
        overlay_states[feature] = not overlay_states[feature]
        val_str = 'True' if overlay_states[feature] else 'False'
        param_name = f'show_{feature}'
        
        # Source ROS 2 setup.bash and execute the param set command together using bash
        ros_command = f"source /opt/ros/humble/setup.bash && ros2 param set /mock_cam {param_name} {val_str}"
        subprocess.run(ros_command, shell=True, executable='/bin/bash')

    return jsonify(overlay_states)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
