# braccio_arm
ROS stack for the braccio arm

To run the ball passing choreography, ssh into the three Arduinos and run the python script /first_tests/moving_braccio_arduino_new.py in each of them. Finally:

    - cd braccio_arduino/tests/
    - python choreography.py

To execute commands from RViz, as before ssh into the Arduinos and run the python script /first_tests/moving_braccio_arduino_new.py in each of them. Then issue the command:

    - roslaunch braccio_moveit_config moveit_planning_execution.launch

and while RViz is launching, when it says that it is waiting for an Action Server open a new Terminal and run:

    - python braccio_controller.py      # Located in /braccio_arduino/tests

Then after clicking Execute in Rviz the robot will move.




For info please contact Lorenzo Betto (lorys_23@hotmail.it) or Gerardo Aragón Camarasa (Gerardo.AragonCamarasa@glasgow.ac.uk).
