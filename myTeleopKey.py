#!/usr/bin/env python

from tkinter.tix import TCL_WINDOW_EVENTS, TixWidget
from unittest import case

from matplotlib.pyplot import get
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi
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

def teleport(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        resp1 = teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))


def teleportPI(y, ang):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportpi = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        resp2 = teleportpi(y, ang)
        print('Teleported to ang: {}'.format(str(ang)))
    except rospy.ServiceException as e:
        print(str(e))

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


if __name__ == '__main__':
    t = 1
    while(t):
        tecla = getkey()
        check(tecla)
        if (tecla == b'x'):
            t = 0