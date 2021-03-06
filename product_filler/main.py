#!/usr/bin/env python

import sys
import os
import Tkinter as tk
from tkFileDialog import askopenfilename
import configuration
import dbConnect
import connectionWidget
import categoriesWidget
import brandsWidget
import productWidget


class Application(tk.Frame):
  def __init__(self, master=None, name='root'):
    tk.Frame.__init__(self, master, name=name)
    self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
    self.path = os.path.dirname(os.path.abspath(__file__))
    self.config = configuration.Configuration('cosmexo', 'config')
    self.createWidgets()
    self.db = None

  def createWidgets(self):
    top = self.winfo_toplevel()
    top.configure(bg='grey')
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    # database connection
    self.connectionWidget = connectionWidget.ConnectionWidget(self)
    self.connectionWidget.grid(sticky=tk.N+tk.W)
    self.categoriesWidget = \
          categoriesWidget.CategoriesWidget('CATEGORY EDITOR', self)
    self.categoriesWidget.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=0)
    self.brandsWidget = \
          brandsWidget.BrandsWidget('COMPANIES/BRANDS EDITOR', self)
    self.brandsWidget.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=1, column=1)
    self.productWidget = \
          productWidget.ProductWidget('PRODUCT EDITOR', self)
    self.productWidget.grid(sticky=tk.N+tk.S+tk.E+tk.W, row=2, columnspan=2)

    self.bind('<<Connection>>', self.onConnected)
    self.bind('<<Disconnection>>', self.onDisconnected)
    top.iconbitmap(os.path.join(self.path, 'resources', 'favicon.ico'))

  def onConnected(self, event):
    """Activates the widgets once you are connected"""
    self.db = self.connectionWidget.db
    self.awsManager = self.connectionWidget.awsManager
    self.categoriesWidget.activate(self.db)
    self.brandsWidget.activate(self.db)
    self.productWidget.activate(self.db, self.awsManager)

  def onDisconnected(self, event):
    """Deactivates the widgets once you are disconnected"""
    self.db = None
    self.categoriesWidget.deactivate()
    self.brandsWidget.deactivate()
    self.productWidget.deactivate()

if __name__=='__main__':
  app = Application()
  app.master.title('Product Filler')
  app.mainloop()
  if app.db:
    app.db.closeConnection()
  sys.exit()