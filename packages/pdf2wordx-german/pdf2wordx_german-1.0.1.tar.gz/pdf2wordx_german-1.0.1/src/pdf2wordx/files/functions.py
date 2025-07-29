from tkinter import messagebox, filedialog, Label, Button
import asyncio
from chromologger import Logger
from pdf2docx import Converter
import os

logger:Logger = Logger('./src/pdf2wordx/log.log')

class Funcs:
    def __init__(self) -> None:
        self.filedialog = filedialog
        self.file:str

        # StringVar (to output, info, directory)
        self.file_name_original:str
        self.file_name_out:str
        self.directory_out:str

    # Open File read mode
    def _askFile(self, button:Button) -> None:
        try:
            file = self.filedialog.askopenfilename(filetypes=[('PDF auswählen: ', '*.pdf')])
            self.file_name_original = self.__getFileBaseName(file)
            self.file = file
            self._activeButton(button)
        except Exception as e:
            logger.log_e(e)
            messagebox.showerror('Fehler bei der Dateiauswahl', 'Bitte stelle sicher, dass du eine korrekte Datei auswählst')

    # Ausgabeverzeichnis festlegen
    def _askDirOut(self, button:Button) -> None:
        try:
            self.directory_out = str(filedialog.askdirectory(title='Wähle den Ausgabepfad für die Datei')) + '/' + self.file_name_out
            self._activeButton(button)
        except Exception as e:
            logger.log_e(e)
            messagebox.showerror('Fehler bei der Verzeichnisauswahl', 'Bitte stelle sicher, dass du ein korrektes Verzeichnis auswählst')

    # Ausgabedateiname festlegen
    def _fileNameOut(self, txt:str) -> None:
        self.file_name_out = f'{txt}.docx'

    # Dateiname ohne Pfad extrahieren
    def __getFileBaseName(self, file:str) -> str:
        return os.path.basename(file)

    # Datei konvertieren
    async def _convertFile(self, button) -> None:
        try:
            convertFile = Converter(self.file)
            messagebox.showinfo("Information", f'Konvertiere {self.file}')
            await asyncio.sleep(1, result=convertFile.convert(self.directory_out))
            convertFile.close()
            self._disableButton(button)
            messagebox.showinfo('Konvertierung erfolgreich', f'Die Datei {self.file_name_original} wurde erfolgreich konvertiert')
        except Exception as e:
            logger.log_e(e)
            messagebox.showerror('Fehler bei der Dateikonvertierung', 'Beim Konvertieren der Datei ist ein Fehler aufgetreten, bitte versuche es erneut')
    
    # Text im Label setzen (Info)
    def _setTextLabel(self, label:Label, labelStr:str, txt:str) -> None:
        try:
            text = labelStr + txt
            print(txt)
            label.configure(text=text)
        except Exception as e:
            logger.log_e(e)
            messagebox.showerror('Fehler beim Setzen des Textes im Label', 'Es ist ein interner Fehler aufgetreten')

    # Change disabled state to normal
    def _activeButton(self, button:Button) -> None:
        button.configure(state='normal')
    
    # Disable buttons
    def _disableButton(self, button:Button | list) -> None:
        print(type(button))
        if type(button) == list:
            for item in button:
                if type(item) == Button:
                    getattr(item, 'configure')(state='disabled')
        
        if type(button) == Button:
            getattr(button, 'configure')(state='disabled')

    def msgbox(self, path: str, win_title: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as fileHelp:
                message = fileHelp.read()
                messagebox.showinfo(win_title, message)
                fileHelp.close()
        except Exception as e:
            logger.log_e(e)