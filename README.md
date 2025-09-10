# Pointer Activity Monitoring Service

**Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia**

A comprehensive Python service that monitors mouse pointer activity and provides beautiful heatmap visualizations of pointer movement across single or multiple screens.

## Features

- 🖱️ **Real-time Mouse Tracking**: Continuously monitors mouse coordinates with high precision
- 🖥️ **Multi-Screen Support**: Automatically detects and supports multiple monitor setups
- 📊 **Interactive Heatmap Visualization**: Generates beautiful heatmaps showing pointer activity density
- 💾 **Data Persistence**: Saves tracking data in JSON format for later analysis
- 🎛️ **Compact UI**: Small, always-on-top control panel positioned in screen corner
- 👁️ **Easy Visualization**: One-click heatmap generation with statistical information
- 💾 **Export Capabilities**: Save heatmaps as high-resolution PNG images

## Quick Start

For immediate usage:

```bash
# Clone the repository
cd pointer-activity-monitoring

# Install dependencies
pip install -r requirements.txt

# Test installation
python test_installation.py

# Run the application
python run.py
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project**:
   ```bash
   cd pointer-activity-monitoring
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Platform-Specific Notes

#### macOS
You may need to grant accessibility permissions to your terminal or Python application:
1. Go to System Preferences → Security & Privacy → Privacy → Accessibility
2. Add Terminal or your Python interpreter to the list of allowed applications

#### Linux
Install tkinter if not already available:
```bash
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install tkinter         # CentOS/RHEL
```

#### Windows
All dependencies should work out of the box. No additional setup required.

## Usage

### Starting the Application

```bash
python pointer_monitor.py
```

### User Interface

The application opens a small control panel in the top-right corner of your screen with three buttons:

- **Start**: Begin monitoring mouse pointer activity
- **Stop**: Stop monitoring and save collected data
- **👁 Visualize**: Generate and display heatmap visualization

### Workflow

1. **Start Monitoring**: Click the "Start" button to begin tracking mouse movements
2. **Use Your Computer Normally**: The service runs in the background, collecting pointer coordinates
3. **Stop Monitoring**: Click "Stop" when you want to end the current session
4. **Visualize Data**: Click "👁 Visualize" to see the heatmap of your pointer activity

### Data Management

- **Automatic Saving**: Data is automatically saved to `pointer_data.json` when you stop monitoring
- **Persistent Storage**: Previous sessions are loaded when you restart the application
- **Clear Data**: Use the "Clear Data" button in the visualization window to reset all collected data

## Technical Details

### Architecture

- **Frontend**: Tkinter-based GUI with modern styling
- **Backend**: pynput for mouse event capture
- **Visualization**: matplotlib and seaborn for heatmap generation
- **Data Storage**: JSON format for cross-platform compatibility

### Data Structure

Each mouse movement is recorded as:
```json
{
  "x": 1234,
  "y": 567,
  "timestamp": 1694123456.789,
  "session": "2023-09-08T10:30:45.123456"
}
```

### Performance

- **Low CPU Usage**: Efficient event-driven architecture
- **Memory Efficient**: Minimal memory footprint for data storage
- **High Precision**: Captures all mouse movements with timestamp accuracy

## Visualization Features

### Heatmap Generation

- **High Resolution**: 100x100 bin resolution for detailed analysis
- **Color Mapping**: Hot colormap for intuitive density representation
- **Gaussian Interpolation**: Smooth visualization of activity patterns
- **Multi-Screen Boundaries**: Visual indicators for multiple monitor setups

### Statistical Information

- Total data points collected
- Screen resolution information
- Number of detected screens
- Session timestamps

### Export Options

- **High-Quality PNG**: 300 DPI resolution for presentations
- **Timestamped Files**: Automatic filename generation with date/time
- **Publication Ready**: Professional formatting suitable for research

## File Structure

```
pointer-activity-monitoring/
├── pointer_monitor.py    # Main application file
├── requirements.txt      # Python dependencies
├── README.md            # This documentation
├── pointer_data.json    # Data file (created after first use)
├── myenv/              # Virtual environment (optional)
└── *.png               # Generated heatmap images
```

## Configuration

### Screen Detection

The application automatically detects:
- Screen resolution
- Multiple monitor configurations
- Screen positioning and offsets

### Customization Options

You can modify the following parameters in `pointer_monitor.py`:

- **Heatmap Resolution**: Change `x_bins` and `y_bins` in `create_heatmap()`
- **UI Position**: Modify window geometry in `setup_ui()`
- **Color Scheme**: Change colormap in `create_heatmap()` (e.g., 'viridis', 'plasma', 'cool')
- **Data File Location**: Modify `self.data_file` in `__init__()`

## Research Applications

This tool is particularly useful for:

- **User Experience Research**: Understanding how users interact with interfaces
- **Ergonomic Studies**: Analyzing mouse movement patterns for workplace optimization
- **Accessibility Research**: Studying pointer behavior for assistive technology development
- **Gaming Analysis**: Understanding player interaction patterns
- **Productivity Studies**: Analyzing workflow efficiency through pointer movement

## Troubleshooting

### Common Issues

1. **Permission Denied (macOS)**:
   - Grant accessibility permissions in System Preferences
   - Run with `sudo` if necessary (not recommended for regular use)

2. **Module Not Found**:
   - Ensure virtual environment is activated
   - Reinstall requirements: `pip install -r requirements.txt`

3. **UI Not Appearing**:
   - Check if window is hidden behind other applications
   - Verify screen resolution detection

4. **No Data Collected**:
   - Ensure mouse movements are within monitored screens
   - Check if monitoring was properly started

### Debug Mode

To enable debug output, run:
```bash
python pointer_monitor.py --debug
```

## Contributing

This project is created and maintained by Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia.

For bug reports or feature requests, please ensure you include:
- Operating system and version
- Python version
- Complete error messages
- Steps to reproduce the issue

## License

© 2024 Prof. Shahab Anbarjafari, 3S Holding OÜ, Tartu Estonia. All rights reserved.

## Version History

- **v1.0.0**: Initial release with core functionality
  - Mouse tracking with pynput
  - Tkinter-based UI
  - Matplotlib heatmap visualization
  - Multi-screen support
  - Data persistence

## Academic Citation

If you use this tool in academic research, please cite:

```
Anbarjafari, S. (2024). Pointer Activity Monitoring Service. 
3S Holding OÜ, Tartu, Estonia.
```

---

**Contact**: Prof. Shahab Anbarjafari, 3S Holding OÜ, Tartu Estonia