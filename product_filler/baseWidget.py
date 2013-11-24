import Tkinter as tk
import tkMessageBox

class BaseWidget(tk.Frame):
  """The base class for the category and company/brand widgets"""
  HIDDEN = -1
  WAITING = 0
  EDITING = 1
  ADDING = 2
  DELETING = 3

  def __init__(self, title, master=None):
    tk.Frame.__init__(self, master, border=2, relief=tk.GROOVE)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
    self.createWidgets(title)
    self.editState = self.HIDDEN

  def createWidgets(self, title):
    """Initialize the frame's widgets"""
    # Show or not
    self.title = tk.Label(self, text=str(title))
    self.title.grid(row=0, column=0, sticky=tk.W)
    self.showButton = tk.Button(self, text='Show/Hide', command=self.showHide,
                                state=tk.DISABLED)
    self.showButton.grid(row=0, column=1, sticky=tk.E)
    self.mainFrame = tk.Frame(self)

  def activate(self, db):
    """Enables Show/Hide Button"""
    if db:
      self.db = db
      self.showButton.config(state=tk.NORMAL)
    self.createButtons()

  def deactivate(self):
    """Hides the widget and disables button"""
    self.db = None
    self.showButton.config(state=tk.DISABLED)
    self.mainFrame.grid_forget()
    self.editState = self.HIDDEN
    self.deleteMainFrame()

  def showHide(self):
    """Show/Hide the whole widget"""
    if self.editState != self.HIDDEN:
      self.mainFrame.grid_forget()
      self.editState = self.HIDDEN
    else:
      self.mainFrame.rowconfigure(0, weight=1)
      self.mainFrame.columnconfigure(0, weight=1)
      self.mainFrame.grid(columnspan=2, sticky=tk.W)
      self.editState = self.WAITING

  def createButtons(self):
    """This is where you create the buttons, throws error if not overwritten"""
    raise BaseWidgetException("createButtons needs to be overwritten")

  def updateMainFrame(self):
    """Updates the tree and the labels"""
    self.deleteMainFrame()
    self.createButtons()

  def deleteMainFrame(self):
    """Deletes the tree"""
    for child in self.mainFrame.winfo_children():
      child.destroy()


class MainWidgetException:
  """Raised when the subclass of TreeWidget is not implemented correctly"""

  def __init__(self, value):
    self.value = value

  def __str__(self):
    return repr(self.value)