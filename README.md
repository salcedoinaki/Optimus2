# **Optimus2 - Satellite Tasking Optimization**

## **Project Overview**

This repository contains the code and analysis for a satellite tasking optimization tool that I developed independently after a conversation with Esper Satellite Imagery. The discussion inspired me to explore satellite tasking challenges and build a tool to optimize task scheduling for Earth observation satellites. The tool leverages publicly available satellite data to determine the best tasking opportunities for a hyperspectral payload, prioritizing tasks based on mission objectives and available windows for observation.

---

## **Problem Statement**

Satellite tasking is a critical challenge for Earth observation missions. To maximize the utility of onboard sensors, operators must determine:

1. **Where the satellite can be tasked within its orbit.**
2. **Which task provides the highest value based on mission priorities.**

---

## **Solution Overview**

The tool developed in this project addresses the tasking challenge by:

1. **Analyzing public satellite data** to predict ground tracks and observation windows.
2. **Identifying potential tasking locations** based on the satellite's position and coverage.
3. **Prioritizing tasks** based on predefined criteria (e.g., maximizing coverage, minimizing cloud interference).

The code is designed to be adaptable for different satellite configurations and mission requirements.

---

## **Repository Structure**
```
Optimus2/
├── .gitattributes                # Git configuration attributes
├── main.py                       # Entry point for the application
├── orbital_simulation.py         # Functions for simulating satellite orbits
├── orbital_simulation_debug.py   # Debugging tools for orbit simulations
├── satellite.py                  # Satellite class definition and related methods
├── scheduler.py                  # Task scheduling algorithms and logic
├── target_list.py                # Management of target locations for observation
└── visualizer.py                 # Visualization tools for plotting satellite data
```

### **File Descriptions:**

- **`.gitattributes`**:  
  Contains Git configuration settings that manage repository attributes, such as line endings and file handling.

- **`main.py`**:  
  Serves as the main entry point for the application, coordinating the execution of various modules to perform satellite tasking optimization.

- **`orbital_simulation.py`**:  
  Includes functions and methods for simulating satellite orbits, calculating positions, and predicting ground tracks based on orbital parameters.

- **`orbital_simulation_debug.py`**:  
  Provides additional debugging tools and functions to test and validate orbital simulations, ensuring accuracy in calculations.

- **`satellite.py`**:  
  Defines the `Satellite` class, encapsulating properties and behaviors of a satellite, including methods for orbit propagation and state vector calculations.

- **`scheduler.py`**:  
  Implements the algorithms and logic for scheduling tasks, determining optimal observation times, and managing task priorities based on mission objectives.

- **`target_list.py`**:  
  Manages the list of target locations designated for observation, including functionalities to add, remove, and prioritize targets.

- **`visualizer.py`**:  
  Contains tools and functions for visualizing satellite data, such as plotting ground tracks, coverage areas, and other relevant graphical representations.

---

## **Code Walkthrough**

### **Main Script: `main.py`**

The core of the tasking optimization tool is implemented in `main.py`. Key functions include:

- **Integration of modules**: Combines the functionalities of different scripts to perform the overall tasking analysis.

### **Supporting Modules**

- **`orbital_simulation.py`**: Handles orbit calculations and ground track predictions.
- **`scheduler.py`**: Manages task scheduling and optimization.
- **`target_list.py`**: Maintains the list of targets for observation.
- **`visualizer.py`**: Generates visual outputs such as ground track plots and swath coverage maps.

---

## **Installation and Usage**

### **Dependencies**

To run the code, you will need:

- Python 3.8+
- `numpy`
- `matplotlib`
- `cartopy`
- `geopy`
- `skyfield`
- `datetime`

### **Installation**
Clone the repository:
```bash
git clone https://github.com/salcedoinaki/Optimus2.git
```
Navigate to the project directory:
```bash
cd Optimus2
```
Install dependencies:
```bash
pip install -r requirements.txt
```

### **Usage**
Run the main script:
```bash
python main.py
```

---

## **Results**

The tool outputs:

- **Ground Track Visualizations:**
  - Plots of the satellite’s ground track.
- **Swath Coverage Maps:**
  - Visual representations of the areas covered by the payload.
- **Optimized Tasking Schedule:**
  - A prioritized list of observation tasks with time windows and locations.

Example output:
![Ground Track Visualization](visualizations/ground_track_plot.png)

---

## **Next Steps**

Future improvements could include:

1. **Integration with real-time satellite data feeds** to enhance accuracy.
2. **Cloud cover prediction models** to improve task prioritization.
3. **User interface development** for easier interaction with the tool.

---

## **Contributions**

This project was developed by Inaki Salcedo. Feedback and suggestions for improvements are welcome. Feel free to fork the repository and submit pull requests!

---

## **Contact**

For any questions or collaboration opportunities, please reach out via email at iniaki.salcedo@gmail.com

