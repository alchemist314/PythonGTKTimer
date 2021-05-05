#!/usr/bin/env python
# encoding: utf-8

import pygtk
pygtk.require('2.0')
import gtk
import logging
import time
from threading import Timer
import gobject
import datetime

timer_val=0
path_to_log='/home/PYTHON_BIN/timer/timer.log'
path_to_category_file='/home/PYTHON_BIN/timer/category_en.txt'
path_to_times_file='/home/PYTHON_BIN/timer/times.txt'


class PyGTKTimer(gtk.Window):
   def __init__(self):
      super(PyGTKTimer, self).__init__()
      logging.basicConfig(filename=path_to_log, level=logging.INFO)
      self.set_title("TIMER")
      self.set_resizable(False)
      self.set_default_size(350, 400)
      self.set_position(gtk.WIN_POS_CENTER)
      self.set_border_width(10)
      self.connect("destroy", gtk.main_quit)
      combobox = gtk.ComboBox()
      combobox1 = gtk.ComboBox()

      store = gtk.ListStore(str)
      store1 = gtk.ListStore(str)

      cell = gtk.CellRendererText()

      self.btn = gtk.Button("Timer Start")

      combobox.pack_start(cell)
      combobox1.pack_start(cell)

      combobox.add_attribute(cell, 'text', 0)
      combobox1.add_attribute(cell, 'text', 0)

      fixed = gtk.Fixed()

      lbl = gtk.Label("Time: ")
      fixed.put(lbl, 10,40)

      lblCat = gtk.Label("Category: ")
      fixed.put(lblCat, 140,40)

      fixed.put(combobox, 70,35)
      fixed.put(combobox1, 230,35)

      lbl3 = gtk.Label("")
      fixed.put(lbl3, 110,90)

      lbl4 = gtk.Label("")
      fixed.put(lbl4, 110,110)

      lblCounter = gtk.Label(0)
      fixed.put(lblCounter, 170,10)

      self.btn.connect("button_press_event", self.timer_start, combobox, combobox1, lbl3, lbl4, lblCounter)
      fixed.put(self.btn,125,140)

      lblEmpty = gtk.Label("")
      fixed.put(lblEmpty, 125,160)

      self.add(fixed)
      
      categoryFile = path_to_times_file
      fileName = open(categoryFile, 'r')
      for line in fileName:
	store.append ([str(line).rstrip()])

      categoryFile = path_to_category_file
      fileName = open(categoryFile, 'r')
      for line in fileName:
	store1.append ([str(line).rstrip()])

      combobox.set_model(store)
      combobox.set_active(0)

      combobox1.set_model(store1)
      combobox1.set_active(0)

      self.show_all()

      return

   def add_seconds(self, time_now, sec):
      fulldate = datetime.datetime(100, 1, 1, time_now.hour, time_now.minute, time_now.second)
      fulldate = fulldate + datetime.timedelta(seconds=sec)
      return fulldate.time()

   def timer_start(self,widget,event,combobox,combobox1,lbl3,lbl4,lblCounter):

      time_now = datetime.datetime.now().time()
      date_now = datetime.datetime.now().date()
      time_finish = self.add_seconds(time_now, (int(combobox.get_active_text())*60))

      lbl3.set_markup("<span>Start: "+str(time_now)+"</span>")
      lbl4.set_markup("<span>Stop:   "+str(time_finish)+"</span>")

      logging.info('date: '+str(date_now))
      logging.info('start: '+str(time_now))
      logging.info('stop: '+str(time_finish))
      logging.info('-----------------------')

      ReloadData(combobox, combobox1, lblCounter)


class ReloadData(object):
    def __init__(self, combobox, combobox1, lblCounter):
	self.combo=combobox1
	self.counter=lblCounter
        self.val = int(combobox.get_active_text())*60
        self.timer_id1=gobject.timeout_add(1000, self.timeout)
        self.timer_id2=gobject.timeout_add(int(combobox.get_active_text())*60000, self.show_window)

    def timeout(self):
        self.val -= 1
	self.counter.set_markup("<span>"+str(self.val)+"</span>")
        return True

    def show_window(self):
	gobject.source_remove(self.timer_id1)
	gobject.source_remove(self.timer_id2)
	widget = gtk.DrawingArea()
	widget.show()

        w = gtk.Window(gtk.WINDOW_TOPLEVEL)
	w.set_title(str(self.combo.get_active_text()))
	w.set_default_size(500, 500)
	w.set_position(gtk.WIN_POS_CENTER)

	col = gtk.gdk.Color('#0f0')
	w.present()
	widget.modify_bg(gtk.STATE_NORMAL, col)

        w.set_border_width(0)
	w.add(widget)
	w.show_all()
	w.set_keep_above(True)

if __name__ == '__main__':
    PyGTKTimer()
    gtk.main()