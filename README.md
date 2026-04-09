Project Overview

This project is an AI-powered targeted disease spraying robot designed for real-time plant protection.
The system uses a Raspberry Pi as the main processing unit and a Pi Camera to capture live plant images.
A trained YOLO model analyzes the video feed to detect diseased leaves and identify the exact location of infection.
After detection, the system automatically moves a pan-tilt spraying mechanism to align the nozzle with the infected region 
and activates a pump through a relay to spray treatment precisely where needed.
A live video stream is also displayed through a web browser so the user can monitor the system remotely. 
The design reduces unnecessary spraying, improves targeting accuracy, and demonstrates the integration of computer vision, 
embedded control, and mechanical actuation in a smart agricultural application.

Working Mechanism
The camera continuously captures live frames of the plants.
The YOLO model processes each frame and detects diseased areas.
The bounding box center is converted into servo movement commands.
The pan and tilt servos align the nozzle with the target spot.
The relay activates the pump for a short, controlled spray.
A cooldown timer prevents repeated spraying in quick succession.
The live annotated feed is streamed through a local web server for monitoring.
