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
from threading import Thread
#matplotlib.use('WXAgg')
matplotlib.use('macosx')
matplotlib.rcParams['toolbar'] = 'None'
matplotlib.rcParams['figure.facecolor'] = 'black'
matplotlib.rcParams['figure.edgecolor'] = 'black'
matplotlib.rcParams['axes.labelcolor'] = 'green'
matplotlib.rcParams['axes.facecolor'] = '0.15'
matplotlib.rcParams['axes.edgecolor'] = '0.15'
matplotlib.rcParams['axes.color_cycle'] = 'green'
matplotlib.rcParams['xtick.color'] = 'green'
matplotlib.rcParams['ytick.color'] = 'green'

#axes.labelcololabelcolorr

import matplotlib.pyplot as plt

fig = plt.figure()

ax3 = fig.add_axes([ 0.10, 0.08, 0.88, 0.29 ])  # left, bottom, w, h
ax2 = fig.add_axes([ 0.10, 0.38, 0.88, 0.29 ]) 
ax1 = fig.add_axes([ 0.10, 0.68, 0.88, 0.29 ])
ax1.set_xticklabels([])
ax2.set_xticklabels([])

#ax = fig.add_subplot(111)
ax1.grid(True)
ax2.grid(True)
ax3.grid(True)
ax3.set_xlabel("Time (Seconds)")
ax1.set_ylabel(r'Voltage $V$ [V]')
ax2.set_ylabel(r'Current $I$ [mA]')
ax3.set_ylabel(r'Power $P$ [mW]')
ax1.axis([0,750, 0, 5])
ax2.axis([0,750, 0, 100])
ax3.axis([0,750, 0, 100])

t = np.arange(0,750,1)
voltage = np.zeros(750)
current = np.zeros(750)
power = np.zeros(750)
line_v, = ax1.plot(t, voltage)
line_i, = ax2.plot(t, current)
line_p, = ax3.plot(t, power)

pad = 1.0
current_pos = 0

def tt():
    print "HELLO"
    
def update(*args):
    global current_pos, pad, voltage, current, power, pltline, fig, ax1
    # Open the data file and get any new data points since
    # the last time we read from this file
    print "UPDATE"
    data = open("serial.log", "r")
    data.seek(current_pos)
    new_data = data.read().split("\n")

    current_pos = data.tell()
    data.close()
   
    # If we got new data then append it to the list of
    # temperatures and trim to 750 points
    for line in new_data:
        line = line.split()
        if len(line) == 3:
            voltage[0:-1] = voltage[1:]
            voltage[-1] = float(line[0])
            current[0:-1] = current[1:]
            current[-1] = float(line[1])
            power[0:-1] = power[1:]
            power[-1] = float(line[2])

    line_v.set_ydata(voltage)
    line_i.set_ydata(current)
    line_p.set_ydata(power)
   
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
    timer.Start(1000)
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
