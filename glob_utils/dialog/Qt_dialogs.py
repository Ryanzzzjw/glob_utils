import sys
from typing import Any, Union
import PyQt5.QtWidgets
import PyQt5.QtGui


import logging
logger = logging.getLogger(__name__)

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

ap = PyQt5.QtWidgets.QApplication(sys.argv)
icon_w= {
    #https://www.pythonguis.com/faq/built-in-qicons-pyqt/
    'SP_ArrowBack':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowBack),
    'SP_ArrowDown':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowDown),
    'SP_ArrowForward':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowForward),
    'SP_ArrowLeft':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowLeft),
    'SP_ArrowRight':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowRight),
    'SP_ArrowUp':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ArrowUp),
    'SP_BrowserReload':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_BrowserReload),
    'SP_BrowserStop':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_BrowserStop),
    'SP_CommandLink':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_CommandLink),
    'SP_ComputerIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ComputerIcon),
    'SP_CustomBase':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_CustomBase),
    'SP_DesktopIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DesktopIcon),
    'SP_DialogApplyButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogApplyButton),
    'SP_DialogCancelButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogCancelButton),
    'SP_DialogCloseButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogCloseButton),
    'SP_DialogDiscardButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogDiscardButton),
    'SP_DialogHelpButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogHelpButton),
    'SP_DialogNoButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogNoButton),
    'SP_DialogOkButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogOkButton),
    'SP_DialogOpenButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogOpenButton),
    'SP_DialogResetButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogResetButton),
    'SP_DialogSaveButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogSaveButton),
    'SP_DialogYesButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DialogYesButton),
    'SP_DirClosedIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DirClosedIcon),
    'SP_DirHomeIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DirHomeIcon),
    'SP_DirIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DirIcon),
    'SP_DirLinkIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DirLinkIcon),
    'SP_DirOpenIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DirOpenIcon),
    'SP_DockWidgetCloseButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DockWidgetCloseButton),
    'SP_DriveCDIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DriveCDIcon),
    'SP_DriveDVDIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DriveDVDIcon),
    'SP_DriveFDIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DriveFDIcon),
    'SP_DriveHDIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DriveHDIcon),
    'SP_DriveNetIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_DriveNetIcon),
    'SP_FileDialogBack':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogBack),
    'SP_FileDialogContentsView':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogContentsView),
    'SP_FileDialogDetailedView':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogDetailedView),
    'SP_FileDialogEnd':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogEnd),
    'SP_FileDialogInfoView':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogInfoView),
    'SP_FileDialogListView':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogListView),
    'SP_FileDialogNewFolder':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogNewFolder),
    'SP_FileDialogStart':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogStart),
    'SP_FileDialogToParent':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileDialogToParent),
    'SP_FileIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileIcon),
    'SP_FileLinkIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_FileLinkIcon),
    'SP_MediaPause':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPause),
    'SP_MediaPlay':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaPlay),
    'SP_MediaSeekBackward':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaSeekBackward),
    'SP_MediaSeekForward':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaSeekForward),
    'SP_MediaSkipBackward':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaSkipBackward),
    'SP_MediaSkipForward':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaSkipForward),
    'SP_MediaStop':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaStop),
    'SP_MediaVolume':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaVolume),
    'SP_MediaVolumeMuted':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MediaVolumeMuted),
    'SP_MessageBoxCritical':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MessageBoxCritical),
    'SP_MessageBoxInformation':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MessageBoxInformation),
    'SP_MessageBoxQuestion':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MessageBoxQuestion),
    'SP_MessageBoxWarning':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_MessageBoxWarning),
    'SP_TitleBarCloseButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarCloseButton),
    'SP_TitleBarContextHelpButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarContextHelpButton),
    'SP_TitleBarMaxButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarMaxButton),
    'SP_TitleBarMenuButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarMenuButton),
    'SP_TitleBarMinButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarMinButton),
    'SP_TitleBarNormalButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarNormalButton),
    'SP_TitleBarShadeButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarShadeButton),
    'SP_TitleBarUnshadeButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TitleBarUnshadeButton),
    'SP_ToolBarHorizontalExtensionButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ToolBarHorizontalExtensionButton),
    'SP_ToolBarVerticalExtensionButton':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_ToolBarVerticalExtensionButton),
    'SP_TrashIcon':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_TrashIcon),
    'SP_VistaShield':PyQt5.QtWidgets.QWidget().style().standardIcon(PyQt5.QtWidgets.QStyle.SP_VistaShield),
    }


buttons={
    'OK':PyQt5.QtWidgets.QMessageBox.Ok,
    'Abort':PyQt5.QtWidgets.QMessageBox.Abort,
    'Cancel':PyQt5.QtWidgets.QMessageBox.Cancel
}


def analyse_clicked_buttons(ret:PyQt5.QtWidgets.QMessageBox.StandardButton)->bool:
    boolean={
        PyQt5.QtWidgets.QMessageBox.Ok:True,
        PyQt5.QtWidgets.QMessageBox.Abort:False,
        PyQt5.QtWidgets.QMessageBox.Cancel:False
    }
    return boolean[ret]

def show_msgBox(
    parent:PyQt5.QtWidgets.QWidget=None,
    icon:PyQt5.QtWidgets.QMessageBox.Icon= PyQt5.QtWidgets.QMessageBox.NoIcon,
    text:str= "MessageBox Text",
    informative_text:str= None,
    details_text:str= None,
    title: str= "MessageBox Title",
    buttons = PyQt5.QtWidgets.QMessageBox.Ok |PyQt5.QtWidgets.QMessageBox.Abort | PyQt5.QtWidgets.QMessageBox.Cancel,
    icon_w: PyQt5.QtGui.QIcon= None) -> Any :
    
    msgBox = PyQt5.QtWidgets.QMessageBox()

    msgBox.setIcon(icon)
    msgBox.setText(text)
    msgBox.setWindowTitle(title)
    msgBox.setStandardButtons(buttons)

    if parent is not None:
        msgBox.setParent(parent)

    if icon_w is not None:
        msgBox.setWindowIcon(icon_w)

    if informative_text is not None:
        msgBox.setInformativeText(informative_text)

    if details_text is not None:
        msgBox.setDetailedText(details_text)
        
    
    return msgBox.exec_()


def infoMsgBox(title:str='', message:str='') -> bool:
    ret=show_msgBox(
        icon= PyQt5.QtWidgets.QMessageBox.Information,
        text=message,
        title=title,
        buttons = PyQt5.QtWidgets.QMessageBox.Ok,
        icon_w=icon_w['SP_MessageBoxInformation']
    )
    return analyse_clicked_buttons(ret)


def warningMsgBox(title:str='', message:str='') -> bool:
    ret=show_msgBox(
        icon= PyQt5.QtWidgets.QMessageBox.Warning,
        text=message,
        title=title,
        buttons = PyQt5.QtWidgets.QMessageBox.Ok,
        icon_w=icon_w['SP_MessageBoxWarning']
    )
    return analyse_clicked_buttons(ret)


def errorMsgBox(title:str='', message:str='') -> bool:
    ret=show_msgBox(
        icon= PyQt5.QtWidgets.QMessageBox.Critical,
        text=message,
        title=title,
        buttons = PyQt5.QtWidgets.QMessageBox.Ok,
        icon_w=icon_w['SP_MessageBoxCritical']
    )
    return analyse_clicked_buttons(ret)


def askokcancelMsgBox(title:str='', message:str='') -> bool:
    ret=show_msgBox(
        icon= PyQt5.QtWidgets.QMessageBox.Question,
        text=message,
        title=title,
        buttons = PyQt5.QtWidgets.QMessageBox.Ok | PyQt5.QtWidgets.QMessageBox.Cancel,
        icon_w=icon_w['SP_MessageBoxQuestion']
    )
    return analyse_clicked_buttons(ret)


def mk_filter(filters:list[tuple[str]]=None)-> Union[str, None]:

    if filters is None:
        return None
    filters_qt=""
    for (des, ext) in filters:
        filters_qt=f"{filters_qt}{des} ({ext});;"

    return filters_qt


def openFileNameDialog(
    filters:list=None,
    directory:str=None,
    title:str=None,
    )-> Union[str, None]:

    fileName, s = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
        parent=None,
        caption=title, 
        directory=directory,
        filter=mk_filter(filters),
        )

    return fileName or None
    
def openFileNamesDialog(
    filters:list=None,
    directory:str=None,
    title:str=None,
    )-> Union[list[str], None]:

    fileNames, s = PyQt5.QtWidgets.QFileDialog.getOpenFileNames(
        parent=None,
        caption=title, 
        directory=directory,
        filter=mk_filter(filters),
        )

    return fileNames or None

def saveFileDialog(
    filters:list=None,
    directory:str=None,
    title:str=None,
    )-> Union[str, None]:

    fileName, s = PyQt5.QtWidgets.QFileDialog.getSaveFileName(
        parent=None,
        caption=title, 
        directory=directory,
        filter=mk_filter(filters),
        )

    return fileName or None

def openDirDialog(
    directory:str=None,
    title:str=None,
    )-> Union[str, None]:

    dir = PyQt5.QtWidgets.QFileDialog.getExistingDirectory(
        parent=None,
        caption=title, 
        directory=directory,
        )

    return dir or None

if __name__ == "__main__":
    """"""
    # app = PyQt5.QtWidgets.QApplication(sys.argv)
    print(openFileNameDialog())
    print(openFileNamesDialog())
    print(saveFileDialog())
    print(openDirDialog())
    # sys.exit(app.exec_())
    
