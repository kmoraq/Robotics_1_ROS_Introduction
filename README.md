# Robotics_1_ROS_Introduction
With the final purpose of understanding the basic concepts of ROS and use the fundamental commands, we sorted out the first assigment  of the subject of robotics.

**Table of Contents**

[TOCM]

[TOC]

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
Later for subscribe to the topic pose in turtle1 we used `rossubscriber` by defining first the name of the topic and then the type of the topic. By using the command `.LatestMessage` we can show the last message obtained:
```Matlab
  %%
  subP= rossubscriber('/turtle1/pose','turtlesim/Pose');%Se hace la subscripción al tópico.
  subP.LatestMessage %Se muestra el último mensaje obtenido
```
In order to send the values associated to the pose of turtle1 we explored the services of turtlesim for modifying the pose of the turtle, we created the serive and then the message:
```Matlab
  %%
  PoseSvcCLient=rossvcclient('/turtle1/teleport_absolute');%Se crea el servicio que permitirá enviar los valores      asociados a la pose
  PseMsg=rosmessage(PoseSvcCLient);
```
Additionally, we sent the messages for modifying the positions in the axes X, Y and the angle Theta. Next we call the service and send the message, and finally, we finalized the master node by using `rosshutdown`:
```Matlab
  %%
  PseMsg.X = 1;%Se envían los valores de posición para turtle 1
  PseMsg.Y = 1;%Se envían los valores de posición para turtle 1
  PseMsg.Theta = 2;%Se  envían los valores de posición para turtle 1
  call(PoseSvcCLient,PseMsg);%
  %%
  rosshutdown %Se finaliza el nodo maestro
```
## Management of hello_turtle with Python:
