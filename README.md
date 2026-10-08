# ROS 2 Navigation System

A modular ROS 2 navigation project combining **mapping, localization, path planning, obstacle avoidance, and goal-based navigation** using Cartographer, AMCL, Nav2, RViz2, and TurtleBot3 simulation.

> **Learning context:** This project was developed as part of ROS 2 navigation training using **The Construct's learning environment and TurtleBot3 simulation**. The repository contains the ROS 2 code, configuration, and project organization developed while completing the practical work.

## Demo

[▶ Watch the full navigation demonstration](assets/navigation_demo.mp4)

The demonstration shows the TurtleBot3 navigating through the simulated environment and avoiding obstacles during navigation.

## Overview

The project separates the main navigation responsibilities into four ROS 2 packages:

- **Mapping** — Cartographer-based SLAM and saved map configuration
- **Localization** — AMCL-based localization on the saved map
- **Path planning** — Nav2 planner, controller, behavior, and navigation-goal configuration
- **Navigation bring-up** — Main launch file integrating the complete navigation system and RViz2

The overall workflow is:

```text
Mapping
   ↓
Save map (.pgm + .yaml)
   ↓
Map Server
   ↓
AMCL Localization
   ↓
Initial Pose
   ↓
Nav2 Planner / Controller
   ↓
Navigation Goal
   ↓
Robot Motion
```

## System Architecture

```text
                     TurtleBot3 / Gazebo Classic
                              │
              ┌───────────────┼────────────────┐
              │               │                │
            LiDAR           Odometry          TF
              │               │                │
              └───────────────┴────────────────┘
                              │
                                                     ▼
                    ┌─────────────────┐
                    │     Mapping     │
                    │   Cartographer  │
                    └────────┬────────┘
                             │
                         Saved Map
                             │
                                                   ▼
                    ┌─────────────────┐
                    │  Localization   │
                    │      AMCL       │
                    └────────┬────────┘
                             │
                       Robot Pose
                             │
                                                   ▼
                    ┌─────────────────┐
                    │    Nav2 Stack   │
                    │                 │
                    │ Planner         │
                    │ Controller      │
                    │ Behaviors       │
                    │ BT Navigator    │
                    └────────┬────────┘
                             │
                       Velocity Commands
                             │
                                                   ▼
                         TurtleBot3

                    ┌──────────────────┐
                    │      RViz2       │
                    │ Map / TF / Goal  │
                    │ Paths / Costmaps │
                    └──────────────────┘
```

### Package responsibilities

| Package | Responsibility |
|---|---|
| `project_mapping` | Cartographer mapping and saved map files |
| `project_localization` | Map Server and AMCL-based localization |
| `project_path_planning` | Nav2 planner/controller configuration and reusable navigation goals |
| `project_navigation` | Main navigation bring-up launch file and RViz2 configuration |

## Repository Structure

```text
02_ros2-navigation/
├── .gitignore
├── README.md
└── src/
    ├── project_mapping/
    │   ├── config/
    │   ├── launch/
    │   └── maps/
    │
    ├── project_localization/
    │   ├── config/
    │   └── launch/
    │
    ├── project_navigation/
    │   ├── launch/
    │   └── rviz/
    │
    └── project_path_planning/
        ├── config/
        ├── launch/
        └── project_path_planning/
```

## Prerequisites

The project was developed and tested with:

- Ubuntu/Linux
- **ROS 2 Humble**
- **Gazebo Classic**
- **TurtleBot3**
- `colcon`
- A ROS 2 Docker-based development environment

The simulation environment itself is **not included in this repository**. A compatible TurtleBot3 simulation must be started separately.

## Getting Started

Follow these steps to reproduce the project.

### 1. Prepare ROS 2 Humble

Set up a ROS 2 Humble environment with the required navigation and build dependencies. The original development setup used ROS 2 inside Docker.

### 2. Start the TurtleBot3 simulation

Start the TurtleBot3 Gazebo Classic simulation separately from this repository.

The simulation should provide the interfaces required by the navigation stack, including compatible sensor data, odometry, TF frames, velocity commands, and simulation time where applicable.

### 3. Use the included map or create a new one

The repository contains a reference map at:

```text
src/project_mapping/maps/
├── my_map.pgm
└── my_map.yaml
```

The included map was generated from the TurtleBot3 simulation/environment used during development.

If you are using a **different world, simulator, or robot**, create a new map for that environment before starting localization and navigation.

### 4. Save a newly generated map

Save the generated map into:

```text
src/project_mapping/maps/
```

The current navigation configuration expects:

```text
my_map.pgm
my_map.yaml
```

For example, using the Nav2 map saver:

```bash
ros2 run nav2_map_server map_saver_cli \
  -f /ros2/ros2_ws/src/project_mapping/maps/my_map
```

This creates:

```text
my_map.pgm
my_map.yaml
```

If you use different filenames, update the launch/configuration files that reference `my_map.yaml`.

### 5. Build the workspace

From the repository root:

```bash
colcon build
```

Then source the workspace:

```bash
source install/setup.bash
```

Verify the project packages:

```bash
ros2 pkg list | grep project_
```

Expected packages:

```text
project_localization
project_mapping
project_navigation
project_path_planning
```

### 6. Launch the navigation system

Run:

```bash
ros2 launch project_navigation project_navigation.launch.py
```

The main launch file starts:

- Map Server
- AMCL
- Nav2 Planner Server
- Nav2 Controller Server
- Nav2 Behavior Server
- Nav2 BT Navigator
- Lifecycle Manager
- RViz2

### 7. Set the initial pose

In RViz2:

1. Select **2D Pose Estimate**.
2. Click the robot's approximate location on the map.
3. Drag to indicate the robot's orientation.
4. Allow AMCL to converge as the robot moves.

### 8. Send a navigation goal

In RViz2:

1. Select **Nav2 Goal / 2D Goal Pose**.
2. Select a valid free-space location on the map.
3. Set the desired orientation.
4. Nav2 plans and executes the path.

## Mapping Workflow

When creating a map for a new environment:

```text
Start simulation
      ↓
Start Cartographer
      ↓
Start RViz2
      ↓
Move robot around environment
      ↓
Complete map
      ↓
Save .pgm + .yaml
      ↓
Place files in project_mapping/maps/
      ↓
Build workspace
      ↓
Launch navigation
```

The included map is therefore an **environment-specific reference/test map**, not a universal map.

## Saved Navigation Goals

The `project_path_planning` package includes utilities for recording and reusing named navigation poses.

### Record a spot

The `spot_recorder` node listens to `/initialpose` and can store a pose under a user-defined name.

```bash
ros2 run project_path_planning spot_recorder
```

### Navigate to a saved spot

The `move_to_spot` node sends a saved pose to Nav2 through the `NavigateToPose` action.

Example:

```bash
ros2 run project_path_planning move_to_spot \
  --ros-args --params-file spot-list.yaml \
  -p spot_name:=corner1
```

## Navigation Architecture

The main navigation system uses:

| Component | Responsibility |
|---|---|
| Map Server | Loads and publishes the saved map |
| AMCL | Estimates the robot pose on the saved map |
| Planner Server | Calculates a path toward the goal |
| Controller Server | Follows the planned path |
| Behavior Server | Provides navigation behaviors/recovery actions |
| BT Navigator | Coordinates navigation through the Behavior Tree |
| Lifecycle Manager | Starts and manages Nav2 lifecycle nodes |
| RViz2 | Visualization, initial pose, and navigation-goal input |

Simplified flow:

```text
RViz2
 ├── 2D Pose Estimate
 │        ↓
 │      AMCL
 │        ↓
 │   Robot Localization
 │
 └── Navigation Goal
          ↓
     BT Navigator
          ↓
    Planner Server
          ↓
      Global Path
          ↓
   Controller Server
          ↓
        Robot
```

### Saved Navigation Spots

The project includes a small workflow for recording and reusing named navigation poses.

Three files are included to reflect the development of this feature:

- `spots.yaml` — stores navigation poses generated by the `spot_recorder` workflow.
- `spots.txt` — an earlier/intermediate representation of recorded navigation spots from the learning process.
- `spot-list.yaml` — the ROS 2 parameter file used by `move_to_spot` to retrieve a named pose and send the robot to that location.

The final navigation workflow uses `spot-list.yaml`:

```bash
ros2 run project_path_planning move_to_spot \
  --ros-args --params-file spot-list.yaml \
  -p spot_name:=corner1

```

## Using a Different Robot or Simulator

Cloning and building this repository does not guarantee that it will work unchanged with an arbitrary robot or simulator.

A different setup may require changes to:

- LaserScan topic
- Odometry topic
- TF frames
- Robot base frame
- `cmd_vel` interface
- Simulation-time configuration
- Robot description
- Sensor configuration
- Nav2 parameters
- Cartographer configuration
- RViz configuration

Recommended workflow:

1. Start the new simulation.
2. Verify the required sensor, odometry, TF, and command interfaces.
3. Generate a map for the new environment.
4. Save it to `src/project_mapping/maps/`.
5. Replace `my_map.pgm` and `my_map.yaml`, or update the relevant configuration if using different filenames.
6. Adjust robot/simulation-specific configuration if required.
7. Build and test the navigation system.

## Validation

The project was tested from a clean Git clone in a separate ROS 2 test workspace.

Validation included:

- Independent `colcon build`
- Package discovery after sourcing the cloned workspace
- Map loading
- AMCL localization
- Initial pose estimation
- Nav2 path planning
- Controller execution
- Obstacle avoidance
- Navigation to manually selected goals
- Navigation to saved goal locations

The simulation itself remained separate from the navigation repository.

## Known Limitations

- The included map is specific to the development simulation.
- The repository does not include the complete simulation environment.
- A different robot or simulator may require topic, TF, sensor, or controller changes.
- Saved navigation poses are specific to the included map.
- The project is a practical learning implementation rather than a production-ready navigation framework.
- Automated CI and comprehensive integration testing have not yet been added.

## What This Project Demonstrates

This project demonstrates practical experience with:

- ROS 2 package and repository organization
- ROS 2 launch files
- Cartographer-based SLAM
- Occupancy-grid map generation
- Nav2 Map Server
- AMCL localization
- TF-based robot localization
- Nav2 planning and control
- Behavior-tree-based navigation
- Lifecycle-managed ROS 2 nodes
- RViz2 navigation workflows
- ROS 2 actions
- YAML-based configuration
- Reusable navigation goals
- Reproducing a project from a clean Git clone

## Future Improvements

Possible extensions include:

- Automated tests
- GitHub Actions / CI
- Improved dependency documentation
- More generic robot/simulation parameterization
- Better separation of environment-specific configuration
- Additional navigation scenarios and validation tests
- Integration with perception and computer-vision-based navigation

## Attribution and Learning Context

This project was developed as part of ROS 2 navigation training using **The Construct's learning environment and TurtleBot3 simulation**.

The repository is intended to document the ROS 2 implementation, configuration, project structure, and practical work completed during the learning process. It does not claim that third-party course material or simulation resources were independently authored.

## License

No open-source license is currently declared for this repository.

Please check the applicable terms for any third-party course, simulation, or dependency material before redistributing those materials.
