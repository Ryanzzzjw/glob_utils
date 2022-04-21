# from tkinter import Tk
# from tkinter.messagebox import showerror,showinfo, showwarning
# from typing import Any

# import tkinter.messagebox


# # icons
# ERROR = "error"
# INFO = "info"
# QUESTION = "question"
# WARNING = "warning"

# # types
# ABORTRETRYIGNORE = "abortretryignore"
# OK = "ok"
# OKCANCEL = "okcancel"
# RETRYCANCEL = "retrycancel"
# YESNO = "yesno"
# YESNOCANCEL = "yesnocancel"

# def create_tinker(func):
#     '''Decorator that create a tinker window for dialog'''
  
#     def wrap(*args, **kwargs)-> Any:
#         root=Tk()
#         root.withdraw()
#         answer = func(*args, **kwargs)
#         root.destroy()
#         return answer
#     return wrap

# @create_tinker
# def infoMsgBox(title:str='',message:str='') -> bool:
#     return tkinter.messagebox.showinfo(title, message)

# @create_tinker
# def warningMsgBox(title:str='',message:str='') -> bool:
#     return tkinter.messagebox.showwarning(title, message)

# @create_tinker
# def errorMsgBox(title:str='',message:str='') -> bool:
#     return tkinter.messagebox.showerror(title, message)

# @create_tinker
# def askokcancelMsgBox(title:str='',message:str='') -> bool:
#     return tkinter.messagebox.askokcancel(title, message)


# if __name__ == "__main__":
#     """"""
#     print(infoMsgBox('hurghruehgioh', 'fjijgijreg'))