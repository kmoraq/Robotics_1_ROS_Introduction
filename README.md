# Robotics_1_ROS_Introduction
With the final purpose of understanding the basic concepts of ROS and use the fundamental commands, we sorted out the first assigment  of the subject of robotics.

**Table of Contents**

[TOCM]

[TOC]

## Conection of ROS with Matlab:
After inicialitzating the master node and the turtlesim simulator started the master node but this time on Matlab, then we created the publicator and the message to publish. 
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
Our turtle moved the values given on the message. Here you can see it:
[![1.png](https://i.postimg.cc/bv8ShQrn/1.png)](https://postimg.cc/RWsZ1JcC)

Later for subscribe to the topic pose in turtle1 we used `rossubscriber` by defining first the name of the topic and then the type of the topic:
```Matlab
  %%
  subP= rossubscriber('/turtle1/pose','turtlesim/Pose');%Se hace la subscripción al tópico.
```
In order to send the values associated to the pose of turtle1 we explored the services of turtlesim for modifying the pose of the turtle, we created the serive and then the message:
```Matlab
  %%
  PoseSvcCLient=rossvcclient('/turtle1/teleport_absolute');%Se crea el servicio que permitirá enviar los valores      asociados a la pose
  PseMsg=rosmessage(PoseSvcCLient);
```
Additionally, we sent the messages for modifying the positions in the axes X, Y and the angle Theta. Next we call the service and send the message, and by using the command `.LatestMessage` we can show the last message obtaine, finally, we finalized the master node by using `rosshutdown`:
```Matlab
  %%
  PseMsg.X = 1;%Se envían los valores de posición para turtle 1
  PseMsg.Y = 1;%Se envían los valores de posición para turtle 1
  PseMsg.Theta = 2;%Se  envían los valores de posición para turtle 1
  call(PoseSvcCLient,PseMsg);%
  subP.LatestMessage %Se muestra el último mensaje obtenido
  %%
  rosshutdown %Se finaliza el nodo maestro
```
After sending the values of position the turtle moves to the position stated:
[![2.png](https://i.postimg.cc/V6kSSmjL/2.png)](https://postimg.cc/Z9XY2k71)

and we show the last message obtained:
[![pose.png](https://i.postimg.cc/fbKtTJSr/pose.png)](https://postimg.cc/Z9WKwYc8)

## Management of hello_turtle with Python:
**Inclusion de librerías**

La librería rospy es la que contiene todas la funciones necesarias para implementar ROS en python.

Adicionalmente se agregan librerías especiales que permiten trabajar los objetos de tipo ROSservice, ROStopics y sus menajes.

En este caso se utiliza la clase Twist que permite publicar mensajes para el tópico correspondiente a la velocidad de la tortuga.

Se utilizaron dos servicios en esta implemnetación, el servicio /turtle1/teleport_absolute y el servicio /turtle1/teleport_relative, por lo que se hace necesario importar las clases correspondientes al tipo de dato que estos servicios operan. Se importan entonces las clases TeleporAbsolute y TeleportRelative desde la librería especial para el entorno de simulación de turtle.

Las demás librerías son propias para el funcionamiento de python al imprimir en consola y capturar eventos del teclado.

```python
from tkinter.tix import TCL_WINDOW_EVENTS, TixWidget
from unittest import case

from matplotlib.pyplot import get
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi
```

**Funciones para acceder a los servicios**

La función teleport se encarga de esperar a que el servicio /turtle1/teleport_absolute esté disponible, crea un objeto con los métodos necesarios para llamar al servicio y pasarle los parámetros necesarios para cambiar la orientación y el origen del marco de referencia de la tortuga. Esta función recibe como parámetros el angulo ang de la orientación y las coordenadas x,y del origen. Se utiliza la estructura try exept para capturar e identificar posibles errores en tiempo de ejecución.

En particular el método serviceProxy se encarga de crear al objeto capaz de interacutar con el servicio, esta recibe como parámetros el servicio y el tipo de dato que le corresponde.

En esta funciónel tipo de dato correspondiente es TeleporAbsolute y debe ser importado desde turtlesim.srv.

```python
def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))
```

Esta función se define del mismo modo que la anterior, la diferencia fundamental es el servicio y el tipo de dato que se deben indicar en el método rospy.ServiceProxy(). En este caso el servicio utilizado es /turtle1/teleport_relative y el tipo de dato correspondiente es TeleportRelative. Adicionalmente, la llamada de este servicio solo recibe 2 argumentos, un cambio de posición lineal y un cambio de posición angular relativos a la pose actual de la tortuga

```python
def teleportPI(y, ang):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportpi = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp2 = teleportpi(y, ang)
        print('Teleported to ang: {}'.format(str(ang)))
    except rospy.ServiceException as e:
        print(str(e))
```

**Función para publicar desde un nodo hacia el tópico /turtle1/cmd_vel**

Esta función recibe como parámetros las velocidades lineales relativas al marco de refrencia de la tortuga en el eje x, y, la velocidad angular alrededor del eje z, y el tiempo durante el que se aplican estos parámetros.

El método Publisher() crea el tipo de dato capaz de publicar la información en el topico.

El método init_node() inicia un nodo con nombre velPub.

Se crea un objeto tipo Twist que almacena los atributos necesarios para definir la velocidad lineal y angular de la tortuga.

```python
def pubVel(vel_x, vel_y, omg_z, exe_time):
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('velPub', anonymous=True)
    vel = Twist()
    vel.linear.x = vel_x
    vel.linear.y = vel_y
    vel.angular.z = omg_z
    endTime = rospy.Time.now() + rospy.Duration(exe_time)
    while rospy.Time.now() <= endTime:
        pub.publish(vel)
```

Función check() se encarga de mutiplexar el evento capturado desde el tecaldo hacia una de las acciones prederminadas en los requerimientos del ejercicios.

```python
def check(tecla):
    if(tecla == b'w'):
        pubVel(1,0,0,0.01)

    if(tecla == b's'):
        pubVel(-1,0,0,0.01)

    if(tecla == b'a'):
        pubVel(0,0,1,0.01)

    if(tecla == b'd'):
        pubVel(0,0,-1,0.01)

    if(tecla == b' '):
        teleportPI(0,-pi)

    if(tecla == b'r'):
        teleport(0,0,0)
```

```python
if __name__ == '__main__':
    t = 1
    while(t):
        tecla = getkey()
        check(tecla)
        if (tecla == b'x'):
            t = 0
```

Esta función es tomada desde el enlace propuesto en la guía para capturar los eventos del teclado.

```python
TERMIOS = termios
def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c
```
