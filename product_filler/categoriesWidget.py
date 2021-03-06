import Tkinter as tk
from baseWidget import BaseWidget
from textEditFrame import TextEditFrame
import tkMessageBox

class CategoriesWidget(BaseWidget):
  """Handles display and creation of Categories from the database"""

  def createButtons(self):
    """Creates the labels and buttons to edit categories"""
    self.catTree = self.db.getCategoryTree()
    label = CategoryLabel(master=self.mainFrame, name='Add main\ncategory',
                          id=-1, mainWidget=self)
    label.grid(sticky=tk.N+tk.W)
    for child in self.catTree.leaves:
      self.recursiveLabelDisplay(child)
    if self.editState != self.HIDDEN:
      self.editState = self.WAITING

  def recursiveLabelDisplay(self, tree, column=0):
    """Recursive method that creates tabulated labels"""
    label = CategoryLabel(self.mainFrame, name=tree.cargo['name'],
                          id=tree.cargo['id'], mainWidget=self)
    label.grid(column=column, columnspan=2, sticky=tk.N+tk.W)
    for child in tree.leaves:
      self.recursiveLabelDisplay(child, column+1)

  def hasChildren(self, id):
    """True if category has child categories, False if not,
    ValueError if not exist"""
    queue = self.catTree.leaves[:]
    while queue:
      node = queue.pop(0)
      if node.cargo['id']==id:
        if node.leaves:
          return True
        else:
          return False
      else:
        queue += node.leaves[:]
    raise ValueError('Could not find category with this id: ' + str(id))


class CategoryLabel(tk.Frame):
  """Labels with right-click menu for editing"""

  def __init__(self, master=None, name='', id=-1, mainWidget=None):
    self.textVar = tk.StringVar()
    self.textVar.set(str(id) + ': ' + name)
    self.id = id
    tk.Frame.__init__(self, master)
    self.label = tk.Label(self, textvariable=self.textVar,
                      bg='white', bd=1, relief=tk.RAISED)
    self.label.grid(sticky=tk.N)
    # create right-click menu
    self.menu = tk.Menu(self, tearoff=0)
    if self.id!=-1: # id=-1 for buttons only
      self.menu.add_command(label='Edit', command=self.edit)
    self.menu.add_command(label='Add subcategory',
                          command=self.add_subcategory)
    if self.id!=-1:
      self.menu.add_command(label='Delete', command=self.delete)
    self.label.bind('<Button-3>', self.openMenu)
    # shortcut
    self.mainFrame = mainWidget

  def openMenu(self, event):
    """Opens the right click menu for the label"""
    if self.mainFrame.editState == self.mainFrame.WAITING:
      self.menu.post(event.x_root, event.y_root)

  def edit(self):
    """Create edition frame to edit current category name"""
    self.mainFrame.editState = self.mainFrame.EDITING
    self.label.grid_forget()
    message = 'Edit Category Name:'
    self.newName = tk.StringVar()
    self.editFrame = TextEditFrame(master=self,
                        textVar=self.newName,
                        labelText=message,
                        buttonText='Edit',
                        buttonAction=self.editCategory,
                        cancelButtonAction=self.cancelEditCategory)
    self.editFrame.grid(columnspan=2)
    self.config(bd=2, relief=tk.SUNKEN)

  def editCategory(self):
    """when the TextEditFrame.addButton is clicked"""
    res = self.mainFrame.db.updateLineFromId('category', 'name', 
                       self.newName.get().encode('utf-8'), self.id)
    if res==True:
      self.mainFrame.updateMainFrame()
      self.mainFrame.editState = self.mainFrame.WAITING
    else:
      tkMessageBox.showerror('Edit Category Error',
            'Category could not be edited\n' + str(res))

  def cancelEditCategory(self):
    """when the TextEditFrame.cancelButton is clicked"""
    self.editFrame.destroy()
    self.label.grid()
    self.mainFrame.editState = self.mainFrame.WAITING
    self.config(bd=0, relief=tk.FLAT)

  def add_subcategory(self):
    """Create edition frame to add subcategory to current one"""
    self.mainFrame.editState = self.mainFrame.ADDING
    if self.id == -1:
      message = 'New category:'
    else:
      message = 'New Subcategory:'
    self.catName = tk.StringVar()
    self.editFrame = TextEditFrame(master=self,
                        textVar=self.catName,
                        labelText=message,
                        buttonText='Add',
                        buttonAction=self.addCategory,
                        cancelButtonAction=self.cancelAddCategory)
    self.editFrame.grid(row=0, column=1, columnspan=2, rowspan=3)
    self.config(bd=2, relief=tk.SUNKEN)

  def addCategory(self):
    """when the TextEditFrame.addButton is clicked"""
    headers = ('name', 'parent_id')
    if self.id == -1:
      values = (self.catName.get().encode('utf-8'), None)
    else:
      values = (self.catName.get().encode('utf-8'), self.id)
    res = self.mainFrame.db.simpleInsert('category', headers, values)
    if res==True:
      self.mainFrame.updateMainFrame()
      self.mainFrame.editState = self.mainFrame.WAITING
    else:
      tkMessageBox.showerror('Add Category Error',
            'Category could not be created\n' + str(res))

  def cancelAddCategory(self):
    """when the TextEditFrame.cancelButton is clicked"""
    self.editFrame.destroy()
    self.mainFrame.editState = self.mainFrame.WAITING
    self.config(bd=0, relief=tk.FLAT)

  def delete(self):
    """Delete the category if user confirms"""
    self.mainFrame.editState = self.mainFrame.DELETING
    if self.mainFrame.hasChildren(self.id):
      tkMessageBox.showerror('DeleteCategory Error',
          'Can not delete ' + self.textVar.get()
          + '\nDelete subcategories first')
    elif tkMessageBox.askyesno('Delete Category Warning',
            'Warning: if you delete a category\n' +
            'it can create broken links\n' +
            'Confirm delete?',
            icon=tkMessageBox.WARNING):
      res = self.mainFrame.db.deleteLineFromId('category', self.id)
      if res==True:
        tkMessageBox.showinfo('Delete Category Success',
            'Category was successfully deleted')
        self.mainFrame.updateMainFrame()
      else:
        tkMessageBox.showerror('Delete Category Error',
            'Category could not be deleted\n' + str(res))
    self.mainFrame.editState = self.mainFrame.WAITING


if __name__=='__main__':
  app = CategoriesWidget()
  app.master.title('CategoriesWidget')
  app.mainloop()
  import sys
  sys.exit()