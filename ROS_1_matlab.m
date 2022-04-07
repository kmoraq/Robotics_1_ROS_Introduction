rosinit;%Conexión al nodo maestro
%% 
velPub=rospublisher('/turtle1/cmd_vel','geometry_msgs/Twist');%Se crea el publicador
velMsg=rosmessage(velPub);%Se crea el mensaje
%% 
velMsg.Linear.X = 1;%Valor del mensaje
velMsg.Linear.Y = 4;%Valor del mensaje
velMsg.Angular.Z = 2;%Valor del mensaje

send(velPub,velMsg);%Envío
pause(1)
%%
subP= rossubscriber('/turtle1/pose','turtlesim/Pose');%Se hace la subscripción al tópico.
%%
PoseSvcCLient=rossvcclient('/turtle1/teleport_absolute');%Se crea el servicio que permitirá enviar los valores asociados a la pose
PseMsg=rosmessage(PoseSvcCLient);
%%
PseMsg.X = 1;%Se envían los valores de posición para turtle 1
PseMsg.Y = 1;%Se envían los valores de posición para turtle 1
PseMsg.Theta = 2;%Se envían los valores de posición para turtle 1
call(PoseSvcCLient,PseMsg);
subP.LatestMessage %Se muestra el último mensaje obtenido
%%
rosshutdown %Se finaliza el nodo maestro
%%
