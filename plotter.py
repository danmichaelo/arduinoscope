#!/usr/bin/env python
"""
Plots data logged by logger.py using MatPlotLib

With my mac os x installation, realtime plotting worked best with the WXAgg backend,
but other backends may work just as well or better with other OSes or setups.

See also:
    <http://www.scipy.org/Cookbook/Matplotlib/Animations>
"""

import time
import numpy as np
import matplotlib
from math import floor
from threading import Thread
matplotlib.use('WXAgg')
#matplotlib.use('macosx')
matplotlib.rcParams['toolbar'] = 'None'
#matplotlib.rcParams['figure.facecolor'] = 'white'
#matplotlib.rcParams['figure.edgecolor'] = 'white'
#matplotlib.rcParams['axes.labelcolor'] = 'black'
#matplotlib.rcParams['axes.facecolor'] = '0.15'
#matplotlib.rcParams['axes.edgecolor'] = '0.15'
matplotlib.rcParams['axes.color_cycle'] = 'red'
#matplotlib.rcParams['xtick.color'] = 'blue'
#matplotlib.rcParams['ytick.color'] = 'blue'
matplotlib.rcParams['font.size'] = 24.0
matplotlib.rcParams['axes.linewidth'] = 1.5
matplotlib.rcParams['lines.linewidth'] = 1.5
matplotlib.rcParams['axes.grid'] = True

#axes.labelcololabelcolorr

import matplotlib.pyplot as plt

fig = plt.figure()

ax3 = fig.add_axes([ 0.08, 0.08, 0.90, 0.29 ])  # left, bottom, w, h
ax2 = fig.add_axes([ 0.08, 0.38, 0.90, 0.29 ]) 
ax1 = fig.add_axes([ 0.08, 0.68, 0.90, 0.29 ])
ax1.set_xticklabels([])
ax2.set_xticklabels([])

points = 600.       # number of data points
x_interval = 300.   # number of seconds displayed

pointlength = x_interval/points # length of each point in seconds

#ax = fig.add_subplot(111)
ax3.set_xlabel("Time")

ax1.set_ylabel(r'Voltage [V]')
ax1.axis([0,points, 0, 5])
ax1.set_yticks(np.arange(0,5,1))

ax2.set_ylabel(r'Current [mA]')
ax2.axis([0,points, 0, 90])
ax2.set_yticks(np.arange(0,80,20))

ax3.set_ylabel(r'Power [mW]')
ax3.axis([0,points, 0, 190])
ax3.set_yticks(np.arange(0,180,40))

x = np.arange(0, points, 1)
datetime = np.zeros(points)
voltage = np.zeros(points)
current = np.zeros(points)
power = np.zeros(points)
line_v, = ax1.plot(x, voltage)
line_i, = ax2.plot(x, current)
line_p, = ax3.plot(x, power)

pad = 1.0
current_pos = 0

def tt():
    print "HELLO"
    
def update(*args):
    global current_pos, pad, voltage, current, power, pltline, fig, ax1
    # Open the data file and get any new data points since
    # the last time we read from this file
    data = open("serial.log", "r")
    data.seek(current_pos)
    new_data = data.read().split("\n")

    current_pos = data.tell()
    data.close()
   
    # If we got new data then append it to the list of
    # temperatures and trim to <points> points
    for line in new_data:
        line = line.split()
        if len(line) == 4:
            if datetime[-1] == 0.:
                dt = pointlength
            else:
                dt = float(line[0]) - datetime[-1]
            npoints = int(floor(dt/pointlength))
            #print "dt: %.3f. pointlength: %.1f. Filling %d points" % (dt, pointlength, npoints)
            for i in range(npoints):
                datetime[0:-1] = datetime[1:]
                datetime[-1] = float(line[0])
                voltage[0:-1] = voltage[1:]
                voltage[-1] = float(line[1])
                current[0:-1] = current[1:]
                current[-1] = float(line[2])
                power[0:-1] = power[1:]
                power[-1] = float(line[3])

    line_v.set_ydata(voltage)
    line_i.set_ydata(current)
    line_p.set_ydata(power)
    
    if (datetime[0] > 0.):
        trange = datetime[-1] - datetime[0]
        tscale = 1./trange*points   # scaling factor from seconds to pixels
        tick_dist = 120  # tick every tick_dist seconds
        t0 = time.localtime(datetime[0])
        sec0 = t0.tm_min*60 + t0.tm_sec
        rest0 = sec0%tick_dist
        first_tick = (tick_dist - rest0) * tscale

        xt = np.arange(first_tick, points, tick_dist * tscale)
        xl = [time.strftime("%H:%M:%S",time.localtime(datetime[first_tick]+i*tick_dist)) for i in range(len(xt))]

        ax3.set_xticks(xt)
        ax3.set_xticklabels(xl)

    # Check interval
    #print (datetime[-1] - datetime[0])

    # Get the minimum and maximum temperatures these are
    # used for annotations and scaling the plot of data
    min_v = min(voltage)
    max_v = max(voltage)
   
    # Add annotations for minimum and maximum temperatures
    #a.annotate(r'Min: %0.2f$^{\circ}$F' % (min_t),
    #    xy=(temps.index(min_t), min_t),
    #    xycoords='data', xytext=(20, -20),
    #    textcoords='offset points',
    #    bbox=dict(boxstyle="round", fc="0.8"),
    #    arrowprops=dict(arrowstyle="->",
    #    shrinkA=0, shrinkB=1,
    #    connectionstyle="angle,angleA=0,angleB=90,rad=10"))

    #a.annotate(r'Max: %0.2f$^{\circ}$F' % (max_t),
    #    xy=(temps.index(max_t), max_t),
    #    xycoords='data', xytext=(20, 20),
    #    textcoords='offset points',
    #    bbox=dict(boxstyle="round", fc="0.8"),
    #    arrowprops=dict(arrowstyle="->",
    #    shrinkA=0, shrinkB=1,
    #    connectionstyle="angle,angleA=0,angleB=90,rad=10"))
   
    # Set the axis limits to make the data more readable
    #ax.axis([0,len(voltage), min_v - pad, max_v + pad])
   
    fig.canvas.draw()                 # redraw the canvas
   
    # redraw if idle
    #fig.canvas.draw_idle()




keep_going = True

class SimpleTimer(Thread):
    def run(self):
        global keep_going
        while keep_going:
            print ">sleeping"
            time.sleep(0.5)
            print ">waking"
            #hello()
            #update()
        print "ENDING"

#import signal
#def handler(s, f):
#    global keep_going
#    print "KILL"
#    keep_going = False
#signal.signal(signal.SIGINT, handler)
    
if matplotlib.get_backend() == 'WXAgg':
    import wx
    id = wx.NewId()
    actor = fig.canvas.manager.frame
    timer = wx.Timer(actor, id=id)
    timer.Start(500)
    #wx.EVT_IDLE(wx.GetApp(), update)
    wx.EVT_TIMER(actor, id, update)

elif matplotlib.get_backend() == 'GTKAgg':
    import gtk, gobject
    gobject.idle_add(update)
    gobject.timeout_add(1000, update)

elif matplotlib.get_backend() == 'MacOSX':
    #update()
    print "The MacOSX backend support is not currently functioning"
    # The code below does not work well, since the GUI completely locks the program.
    # The thread only updates whenever the GUI updates itself in some way (try moving the mouse over it)
    t = SimpleTimer()
    t.daemon = True
    t.start()
    # sleep locks up the GUI and should not be used outside a thread

else:
    print "Unsupported backend"


plt.show()
