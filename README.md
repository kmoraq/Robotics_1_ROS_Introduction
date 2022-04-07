# Robotics_1_ROS_Introduction
With the final purpose of understanding the basic concepts of ROS and use the fundamental commands, we sorted out the first assigment  of the subject of robotics.

**Table of Contents**
## Conection of ROS with Matlab:
After inicialitzating the master node and the turtlesim simulator. started the master node but this time on Matlab, then we created the publicator and the message to publish. 
```Matlab
  rosinit;%Conexión al nodo maestro
  %% 
  velPub=rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist'); %Se crea el publicador
  velMsg=rosmessage(velPub); %Se crea el mensaje
```
Then we give the value of the message suggested by the guide and we add two more for a linear movement in the Y axis and an angular movement in Z axis. Next we send the message to the publisher previously created and with the values stated before:
```Matlab
  %% 
  velMsg.Linear.X = 1;%Valor del mensaje
  velMsg.Linear.Y = 4;%Valor del mensaje
  velMsg.Angular.Z = 2;%Valor del mensaje

  send(velPub,velMsg);%Envío
  pause(1)
```
## Management of hello_turtle with Python:
