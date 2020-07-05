import datetime
import os
import shutil
import threading
import time
import sys
from sys import exit
from time import strftime
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QDialog, QProgressBar, QPushButton, QVBoxLayout
import sys
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import time
import pkg_resources.py2_warn

###############################################################################################


# Set default app values in case the config file does not exist or contain invalid data

source_folder = "none"
destination_folder = "none"
wait_timer = 300
language = "English"
start_application_running = False
wait_timer_as_string = "00:05:00"

# Check if configuration file exist
configFileExist = os.path.exists('config.txt')

# if the configuration file exist, read the content and set variables
if configFileExist == True:
    try:
        with open("config.txt", "r") as myfile:
            config_file_variables = myfile.read().splitlines()
            source_folder_read = config_file_variables[0].split('=')
            destination_folder_read = (config_file_variables[1]).split('=')
            wait_timer_read = (config_file_variables[2]).split('=')
            language_read = (config_file_variables[3]).split('=')
            start_application_running_read = (config_file_variables[4]).split('=')

            # setting the variables
            source_folder = (source_folder_read[1])
            destination_folder = (destination_folder_read[1])
            wait_timer_as_string = (wait_timer_read[1])
            language = (language_read[1])
            if start_application_running_read[1] == "False":
                start_application_running = False
            elif start_application_running_read[1] == "True":
                start_application_running = True
            myfile.close()
    except:
        pass


# Language array - the language configuration is done here

ENGLISH = ['No', 'Yes', 'Start', 'Stop', 'STATUS', 'TIMER', 'Wait timer', 'Progress:', 'Source Folder:',
           'Destination Folder:', 'Open Log Files', 'Help', 'About', 'Save Configuration', 'Language:',
           'Start Application \n Running?', 'Apply Language', 'Time until next run:', 'Close',
           ' - SUCCESS: Moved file ', ' from folder ', ' to folder ', ' - FAILURE: Permission denied to file ',
           ' - FAILURE: File ', ' from folder ', ' was NOT MOVED to folder ',
           ' because file already exist in the destination.', 'About CDR File Organizer',
           'This is a simple software to organize Cisco CDR Files by Year, Month and day.\n', 'Apply language',
           'Save your config and restart the application to changes to take effect.', 'Error',
           'Source Folder does not exist.', 'Error', 'Source folder and Destination Folder cannot be the same.',
		   'Destination Folder does not exist.', 'Saved', 'The configuration was saved successfully.',
		   'Configuration file not saved', 'The configuration file could NOT be saved. Try running the application in another folder.',
           ' - FAILURE: Permission denied to file ', 'Some files could not be moved,\nplease check log files.', ' - FAILURE: File ',
           ' from folder ', ' was NOT MOVED to folder ', ' because file already exist in the destination.']

PORTUGUESE = ['Não', 'Sim', 'Iniciar', 'Parar', 'STATUS', 'TEMPORIZADOR', 'Tempo de \n espera', 'Progresso:',
              'Pasta de origem:', 'Pasta de destino:', 'Abrir os \n arquivos de log', 'Ajuda', 'Sobre',
              'Salvar a Configuração', 'Idioma', 'Iniciar o Aplicativo \n Rodando?', 'Aplicar Idioma',
              'Tempo até a \n próxima execução:', 'Fechar', ' - SUCCESSO: Movido o arquivo ', ' da pasta ',
              ' para a pasta ', ' - FALHA: Permissão negada no arquivo ', ' - FALHA: Arquivo ', ' da pasta ',
              ' NÃO FOI MOVIDO para a pasta ', ' porque o arquivo já existe no destino.', 'Sobre o CDR File Organizer',
              'Este é um pequeno software que organiza arquivos CDR Cisco por ano, mês e dia.\n', 'Aplicar Idioma',
              'Salve suas configurações e reinicie o aplicativo para as mudanças surtirem efeito.', 'Erro',
              'A Pasta de Origem não existe.', 'Erro', 'A pasta de origem e de destino não podem ser a mesma.',
			  'A pasta de destino não existe.', 'Salvo', 'A configuração foi salva com sucesso.',
			  'O arquivo de configuração não foi salvo.', 'O arquivo de configuração NÃO foi salvo. Tente rodar a aplicação em outra pasta.',
              ' - FALHA: permissão negada para o arquivo ', 'Alguns arquivos não puderam ser\nmovidos,por favor verifique os\narquivos de log.',
              ' - FALHA: O arquivo ', ' da pasta ', ' NÃO foi movido para a pasta ', ' porque o arquivo já existe no destino.']

SPANISH = ['No', 'Si', 'Empezar', 'Detener', 'ESTADO', 'TEMPORIZADOR', 'Tiempo de\n espera', 'Progreso:', 'Carpeta de origen:',
           'Carpeta de destino:', 'Abrir archivos\nde registro', 'Ayuda', 'Acerca de', 'Guardar configuración', 'Idioma:',
           '¿Iniciar aplicación \n en ejecución?', 'Aplicar idioma', 'Tiempo hasta la\npróxima ejecución:', 'Cerrar',
           '- ÉXITO: ​​archivo movido', 'de la carpeta', 'a la carpeta', '- FALLA: Permiso denegado al archivo',
           '- FALLO: El archivo', 'de la carpeta', 'NO SE MOVIÓ a la carpeta',
           'porque el archivo ya existe en el destino', 'Acerca del organizador de archivos CDR',
           'Este es un software simple para organizar los archivos Cisco CDR por año, mes y día.\n', 'Aplicar idioma',
           'Guarde su configuración y reinicie la aplicación para que los cambios surtan efecto', 'Error',
           'La carpeta de origen no existe', 'Error', 'La carpeta de origen y la carpeta de destino no pueden ser las mismas',
		   'La carpeta de destino no existe', 'Guardado', 'La configuración se guardó correctamente',
		   'Archivo de configuración no guardado', 'El archivo de configuración NO se pudo guardar. Intenta ejecutar la aplicación en otra carpeta.',
           ' - FALLA: Permiso denegado al archivo ', 'Algunos archivos no se pudieron mover,\npor favor revise los archivos de registro.',
           ' - FALLA: El archivo ', ' de la carpeta ', ' NO SE MUDÓ a la carpeta ', ' porque el archivo ya existe en el destino.']

ITALIAN = ['No', 'Sì', 'Inizio', 'Fermare', 'STATO', 'TIMER', 'Timer di\nattesa', 'Progresso:', 'Cartella sorgente:',
           "Cartella di\ndestinazione:", "Apri file di registro", "Guida", "Informazioni", "Salva configurazione", "Lingua:",
           "Avvia applicazione\nin esecuzione?", "Applica lingua", "Tempo fino alla\nprossima esecuzione:", "Chiudi",
           '- SUCCESSO: file spostato', 'dalla cartella', 'alla cartella', '- GUASTO: Autorizzazione negata al file',
           '- GUASTO: File', 'dalla cartella', 'NON SPOSTATO nella cartella',
           "perché il file esiste già nella destinazione.", "Informazioni su CDR File Organizer",
           "Questo è un semplice software per organizzare i file Cisco CDR per anno, mese e giorno.\n", "Applica lingua",
           "Salva la configurazione e riavvia l'applicazione per rendere effettive le modifiche.", "Errore",
           "La cartella di origine non esiste.", "Errore", "La cartella di origine e la cartella di destinazione non possono essere uguali.",
            'La cartella di destinazione non esiste.', 'Salvato', 'La configurazione è stata salvata correttamente.',
            "File di configurazione non salvato", "Impossibile salvare il file di configurazione. Prova a eseguire l'applicazione in un'altra cartella. ",
           " - GUASTO: autorizzazione negata al file", "Impossibile spostare alcuni file,\nSi prega di controllare i file di registro.", " - GUASTO: File",
           ' dalla cartella ', ' NON è stato SPOSTATO nella cartella ', ' perché il file esiste già nella destinazione. ']

FRENCH = ['Non', 'Oui', 'Démarrer', 'Arrêter', 'ÉTAT', 'MINUTERIE', "Minuterie\nd'attente", "Progression:", "Dossier source:",
           'Dossier de destination:', 'Ouvrir les\nfichiers journaux', 'Aide', 'À propos', 'Enregistrer la\nconfiguration', 'Langue:',
           "Démarrer l'application \n en cours d'exécution?", 'Appliquer la langue', 'Durée avant la\nprochaine exécution:', 'Fermer',
           '- SUCCÈS: fichier déplacé', 'du dossier', 'vers le dossier', '- ÉCHEC: autorisation refusée de déposer',
           '- ÉCHEC: le fichier', 'du dossier', "n'a PAS ÉTÉ DÉPLACÉ vers le dossier",
           'car le fichier existe déjà dans la destination.', "A propos de l'organisateur de fichiers CDR",
           "Il s'agit d'un logiciel simple pour organiser les fichiers Cisco CDR par année, mois et jour. \ N", "Appliquer la langue",
           "Enregistrez votre configuration et redémarrez l'application pour que les modifications prennent effet.", 'Erreur',
           "Le dossier source n'existe pas.", 'Erreur', 'Le dossier source et le dossier de destination ne peuvent pas être identiques.',
            "Le dossier de destination n'existe pas.", 'Enregistré', 'La configuration a été enregistrée avec succès.',
            'Fichier de configuration non enregistré', "Le fichier de configuration n'a PAS pu être enregistré. Essayez d'exécuter l'application dans un autre dossier. ",
           '- ÉCHEC: autorisation refusée pour le fichier', "Certains fichiers n'ont pas pu être déplacés, \ nVeuillez vérifier les fichiers journaux.", '- ÉCHEC: Fichier ',
           ' du dossier ', " N'A PAS ÉTÉ DÉPLACÉ vers le dossier ", ' parce que le fichier existe déjà dans la destination.']

GERMAN = ['Nein', 'Ja', 'Starten', 'Halt', 'DER STATUS', 'DER TIMER', 'Wartezeit', 'Fortschritt:', 'Quellordner:',
           'Zielordner:', 'Protokolldateien\nöffnen', 'Hilfe', 'Info', 'Konfiguration\nspeichern', 'Sprache:',
           'Anwendung starten\nausgeführt?', 'Sprache anwenden', 'Zeit bis zur\nnächsten Ausführung:', 'Schließen',
           '- ERFOLG: Datei verschoben', 'aus Ordner', 'in Ordner', '- FEHLER: Berechtigung für Datei verweigert',
           '- FEHLER: Datei', 'aus Ordner', 'wurde NICHT in Ordner verschoben',
           'weil die Datei bereits im Ziel vorhanden ist.', 'Über CDR File Organizer',
           'Dies ist eine einfache Software zum Organisieren von Cisco CDR-Dateien nach Jahr, Monat und Tag.\n', 'Sprache anwenden',
           'Speichern Sie Ihre Konfiguration und starten Sie die Anwendung neu, damit die Änderungen wirksam werden.', 'Fehler',
           'Quellordner existiert nicht.', 'Fehler', 'Quellordner und Zielordner können nicht identisch sein.',
		   'Zielordner existiert nicht.', 'Gespeichert', 'Die Konfiguration wurde erfolgreich gespeichert.',
		   'Konfigurationsdatei nicht gespeichert', 'Die Konfigurationsdatei konnte NICHT gespeichert werden. Versuchen Sie, die Anwendung in einem anderen Ordner auszuführen.',
          ' - FEHLER: Berechtigung für Datei verweigert', 'Einige Dateien konnten nicht verschoben werden,\nBitte überprüfen Sie die Protokolldateien.',
          ' - FEHLER: Datei ', ' aus Ordner ', ' wurde NICHT in Ordner verschoben ', ' weil Datei bereits vorhanden ist im Ziel existieren.']

# set the system language

# if any problem happens, set the language to default English
LANGUAGE = ENGLISH

# read the variable 'language' from configuration file

if language == "English":
    LANGUAGE = ENGLISH

elif language == "Português":
    LANGUAGE = PORTUGUESE

elif language == "Español":
    LANGUAGE = SPANISH

elif language == "Italiano":
    LANGUAGE = ITALIAN

elif language == "Française":
    LANGUAGE = FRENCH

elif language == "Deutsche":
    LANGUAGE = GERMAN


###############################################################################################

STOP = True
print("###############################################################################################")
log_time = time.ctime()
print((log_time) + " - Application has started.")







class Worker(QThread):
    # Create the worker thread and collect signals

    signal_change_progress_bar = pyqtSignal(int)
    signal_change_lcd_value = pyqtSignal(int)


    def run(self):
        # This variable RUNNING is set to avoid problems when the user
        # press the start button more than 1 time
        global RUNNING

        # if the app_start is already running, return this function
        try:
            if RUNNING == True:
                return 0
        except:
            pass

        # set the RUNNING variable to True
        RUNNING = True

        # Keep running until the variable STOP is not set to False
        global STOP
        while STOP == False:
            # Waiting time
            global wait_timer
            #print(wait_timer)
            wait_timer_original = wait_timer
            print()
            print("Waiting to execute...")
            print()

            while not wait_timer == 0 and STOP == False:
                # Decrease the wait timer by 1 second and sleep 1 second
                wait_timer -= 1
                time.sleep(1)
                self.signal_change_lcd_value.emit(wait_timer)
                #print(wait_timer)

                # Check if the main thread is still running - if not, call function app_stop and close thread
                #app_is_main_thread_still_running_test = self.app_is_main_thread_still_running()
                #if app_is_main_thread_still_running_test == False:
                #    self.app_stop()
                #    exit(1)

            # Check if log folders exist; if not, create it
            dir_path = os.path.dirname(os.path.realpath(__file__))
            logs_folder = (dir_path + '/' + 'logs')
            if not os.path.exists(logs_folder):
                os.makedirs(logs_folder)

            # Create or set the log file - 1 file per day
            day = (strftime('%Y.%m.%d'))
            #print(day)
            logs_folder = 'logs'
            #print(logs_folder)
            log_time = time.ctime()
            #print(log_time)
            f = open(logs_folder + '/' + day + '.log', 'a')



            #print("after if not os.path.exists(logs_folder):")

            # check how many files exist in directory source folder
            cdrs_available = os.listdir(source_folder)
            # global number_of_cdrs_available
            number_of_cdrs_available = len(cdrs_available)

            if number_of_cdrs_available == 0:
                wait_timer = wait_timer_original
                print()
                print("No files to process, sleeping...")
                print()

            try:
                progress_bar_increment = (100 / number_of_cdrs_available)
                pass
            except:
                pass

            progress_bar_status = 0

            print("Number of CDRs available is: " + str(number_of_cdrs_available))

            # Thread signal to change the Progress Bar
            signal_change_progress_bar = pyqtSignal(int)

            for cdr in cdrs_available:
                try:
                    if STOP == True:
                        return
                except:
                    pass

                log_time = time.ctime()
                print((log_time) + " - Processing CDR " + cdr)
                # Increment the progress bar
                status_bar = (int(progress_bar_status))
                progress_bar_status += progress_bar_increment
                self.signal_change_progress_bar.emit(progress_bar_status)

                cdr_name = (cdr.split('_')[3])
                folder_year = (cdr_name[0:4])
                folder_month = (cdr_name[4:6])
                folder_day = (cdr_name[6:8])
                folder_path = (folder_year + '/' + folder_month + '/' + folder_day)
                new_folder = (destination_folder + '/' + folder_path)

                if not os.path.exists(new_folder):
                    os.makedirs(new_folder)

                try:
                    shutil.move(source_folder + '/' + cdr, new_folder)
                    f = open(logs_folder + '/' + day + '.log', 'a')
                    f.write(log_time + LANGUAGE[19] + cdr + LANGUAGE[20] + source_folder + LANGUAGE[21] + new_folder + "." + "\n")
                    f.close()
                    wait_timer = wait_timer_original

                except Exception as ex:
                    string_ex = str(ex)
                    if "Permission denied:" in string_ex:
                        print("Permission denied")
                        print(string_ex)
                        if not os.path.exists(logs_folder + '/' + day + '.log'):
                            f = open(logs_folder + '/' + day + '.log', 'w+')
                            f.close()
                        with open((logs_folder + '/' + day + '.log'), "r") as myfile:
                            if cdr in myfile.read():
                                # if cdr log information exist int the log file, does nothing
                                wait_timer = wait_timer_original
                            else:
                                # if cdr log information does not exist int the log file, write it there
                                f = open(logs_folder + '/' + day + '.log', 'a')
                                f.write(log_time + LANGUAGE[40] + source_folder + '/' + cdr + "\n")
                                f.close()
                                wait_timer = wait_timer_original

                    elif "exists" in string_ex:
                        with open((logs_folder + '/' + day + '.log'), "r") as myfile:
                                if (LANGUAGE[42]) + cdr in myfile.read():
                                    print("File already exist")
                                    # if cdr log information exist int the log file, does nothing
                                    wait_timer = wait_timer_original
                                else:
                                    # if cdr log information does not exist int the log file, write it there
                                    f = open(logs_folder + '/' + day + '.log', 'a')
                                    f.write(log_time + LANGUAGE[42] + cdr + LANGUAGE[43] + source_folder + LANGUAGE[44] + new_folder + LANGUAGE[45] + "\n")
                                    f.close()

                wait_timer = wait_timer_original
                continue


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(839, 624)
        MainWindow.setFixedSize(839, 624)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        MainWindow.setWindowIcon(icon)


        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.button_start = QtWidgets.QPushButton(self.centralwidget)
        self.button_start.setGeometry(QtCore.QRect(60, 190, 75, 23))
        self.button_start.setObjectName("button_start")
        self.button_start.clicked.connect(self.app_start_thread)

        self.button_stop = QtWidgets.QPushButton(self.centralwidget)
        self.button_stop.setGeometry(QtCore.QRect(160, 190, 75, 23))
        self.button_stop.setObjectName("button_stop")
        self.button_stop.clicked.connect(self.app_stop)

        self.picture_status = QtWidgets.QLabel(self.centralwidget)
        self.picture_status.setGeometry(QtCore.QRect(60, 110, 171, 41))
        self.picture_status.setText("")
        self.picture_status.setPixmap(QtGui.QPixmap("imgs/stop.png"))
        self.picture_status.setScaledContents(True)
        self.picture_status.setObjectName("picture_status")

        self.text_status = QtWidgets.QLabel(self.centralwidget)
        self.text_status.setGeometry(QtCore.QRect(0, 20, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.text_status.setFont(font)
        self.text_status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_status.setAlignment(QtCore.Qt.AlignCenter)
        self.text_status.setObjectName("text_status")

        self.text_msg_alert = QtWidgets.QLabel(self.centralwidget)
        self.text_msg_alert.setGeometry(QtCore.QRect(500, 250, 290, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_msg_alert.setFont(font)
        self.text_msg_alert.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_msg_alert.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_msg_alert.setObjectName("text_msg_alert")



        self.line_horizontal = QtWidgets.QFrame(self.centralwidget)
        self.line_horizontal.setGeometry(QtCore.QRect(-13, 270, 311, 20))
        self.line_horizontal.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_horizontal.setObjectName("line_horizontal")

        self.line_vertical = QtWidgets.QFrame(self.centralwidget)
        self.line_vertical.setGeometry(QtCore.QRect(290, 0, 20, 631))
        self.line_vertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_vertical.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_vertical.setObjectName("line_vertical")

        self.text_timer = QtWidgets.QLabel(self.centralwidget)
        self.text_timer.setGeometry(QtCore.QRect(0, 300, 301, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.text_timer.setFont(font)
        self.text_timer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_timer.setAlignment(QtCore.Qt.AlignCenter)
        self.text_timer.setObjectName("text_timer")

        self.box_wait_timer = QtWidgets.QTimeEdit(self.centralwidget)
        self.box_wait_timer.setGeometry(QtCore.QRect(140, 380, 118, 22))
        # self.box_wait_timer.setCurrentSection(QtWidgets.QDateTimeEdit.MinuteSection)
        self.box_wait_timer.setCurrentSection(QtWidgets.QDateTimeEdit.HourSection)
        self.box_wait_timer.setCurrentSectionIndex(0)
        self.box_wait_timer.setTime(QtCore.QTime(0, 5, 0))
        self.box_wait_timer.setObjectName("box_wait_timer")

        self.text_wait_timer = QtWidgets.QLabel(self.centralwidget)
        self.text_wait_timer.setGeometry(QtCore.QRect(40, 360, 81, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_wait_timer.setFont(font)
        self.text_wait_timer.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_wait_timer.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_wait_timer.setObjectName("text_wait_timer")

        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setGeometry(QtCore.QRect(40, 490, 211, 111))
        self.lcdNumber.setObjectName("lcdNumber")
        # self.lcdNumber.setProperty('value', 130)

        self.box_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.box_progressBar.setGeometry(QtCore.QRect(460, 220, 351, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.box_progressBar.setFont(font)
        # To edit the progress bar, edit the value below, example:
        # self.box_progressBar.setProperty("value", 24)
        self.box_progressBar.setProperty("value", 0)
        self.box_progressBar.setObjectName("box_progressBar")

        self.text_progress = QtWidgets.QLabel(self.centralwidget)
        self.text_progress.setGeometry(QtCore.QRect(310, 200, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_progress.setFont(font)
        self.text_progress.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_progress.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_progress.setObjectName("text_progress")

        self.lineEdit_source_folder = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_source_folder.setGeometry(QtCore.QRect(500, 40, 321, 20))
        self.lineEdit_source_folder.setObjectName("lineEdit_source_folder")

        self.lineEdit_destination_folder = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_destination_folder.setGeometry(QtCore.QRect(500, 100, 321, 20))
        self.lineEdit_destination_folder.setObjectName("lineEdit_destination_folder")

        self.text_source_folder = QtWidgets.QLabel(self.centralwidget)
        self.text_source_folder.setGeometry(QtCore.QRect(360, 20, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_source_folder.setFont(font)
        self.text_source_folder.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_source_folder.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_source_folder.setObjectName("text_source_folder")

        self.text_destionation_folder = QtWidgets.QLabel(self.centralwidget)
        self.text_destionation_folder.setGeometry(QtCore.QRect(330, 80, 161, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_destionation_folder.setFont(font)
        self.text_destionation_folder.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_destionation_folder.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_destionation_folder.setObjectName("text_destionation_folder")

        self.button_open_log_files = QtWidgets.QPushButton(self.centralwidget)
        self.button_open_log_files.setGeometry(QtCore.QRect(330, 410, 121, 41))
        self.button_open_log_files.setObjectName("button_open_log_files")
        self.button_open_log_files.clicked.connect(self.app_open_log_files)

        self.button_help = QtWidgets.QPushButton(self.centralwidget)
        self.button_help.setGeometry(QtCore.QRect(330, 530, 101, 23))
        self.button_help.setObjectName("button_help")
        self.button_help.clicked.connect(self.app_help)

        self.button_about = QtWidgets.QPushButton(self.centralwidget)
        self.button_about.setGeometry(QtCore.QRect(330, 570, 101, 23))
        self.button_about.setObjectName("button_about")
        self.button_about.clicked.connect(self.app_about)

        self.button_save_configuration = QtWidgets.QPushButton(self.centralwidget)
        self.button_save_configuration.setGeometry(QtCore.QRect(330, 350, 121, 41))
        self.button_save_configuration.setObjectName("button_save_configuration")
        self.button_save_configuration.clicked.connect(self.app_save_configuration)

        self.button_source_folder_tool = QtWidgets.QPushButton(self.centralwidget)
        self.button_source_folder_tool.setGeometry(QtCore.QRect(800, 40, 21, 20))
        self.button_source_folder_tool.setObjectName("button_source_folder_tool")
        self.button_source_folder_tool.clicked.connect(self.app_button_source_folder)

        self.button_destination_folder_tool = QtWidgets.QToolButton(self.centralwidget)
        self.button_destination_folder_tool.setGeometry(QtCore.QRect(800, 100, 21, 20))
        self.button_destination_folder_tool.setObjectName("button_destination_folder_tool")
        self.button_destination_folder_tool.clicked.connect(self.app_button_destination_folder)

        self.text_language = QtWidgets.QLabel(self.centralwidget)
        self.text_language.setGeometry(QtCore.QRect(440, 450, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_language.setFont(font)
        self.text_language.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_language.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_language.setObjectName("text_language")

        self.text_start_application_running = QtWidgets.QLabel(self.centralwidget)
        self.text_start_application_running.setGeometry(QtCore.QRect(550, 340, 151, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_start_application_running.setFont(font)
        self.text_start_application_running.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_start_application_running.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.text_start_application_running.setObjectName("text_start_application_running")

        self.button_apply_language = QtWidgets.QPushButton(self.centralwidget)
        self.button_apply_language.setGeometry(QtCore.QRect(720, 470, 101, 23))
        self.button_apply_language.setObjectName("button_apply_language")
        self.button_apply_language.clicked.connect(self.app_apply_language)

        self.text_time_until_next_run = QtWidgets.QLabel(self.centralwidget)
        self.text_time_until_next_run.setGeometry(QtCore.QRect(40, 440, 211, 61))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.text_time_until_next_run.setFont(font)
        self.text_time_until_next_run.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.text_time_until_next_run.setAlignment(QtCore.Qt.AlignCenter)
        self.text_time_until_next_run.setObjectName("text_time_until_next_run")

        self.button_close = QtWidgets.QPushButton(self.centralwidget)
        self.button_close.setGeometry(QtCore.QRect(720, 570, 101, 23))
        self.button_close.setObjectName("button_close")
        self.button_close.clicked.connect(self.app_close)

        self.box_start_application_running = QtWidgets.QComboBox(self.centralwidget)
        self.box_start_application_running.setGeometry(QtCore.QRect(708, 360, 111, 22))
        self.box_start_application_running.setObjectName("box_start_application_running")
        self.box_start_application_running.addItem("")
        # self.box_start_application_running.setItemText(0, "No")
        self.box_start_application_running.setItemText(0, LANGUAGE[0])
        self.box_start_application_running.addItem("")
        # self.box_start_application_running.setItemText(1, "Yes")
        self.box_start_application_running.setItemText(1, LANGUAGE[1])

        if start_application_running == False:
            self.box_start_application_running.setCurrentIndex(0)
        elif start_application_running == True:
            self.box_start_application_running.setCurrentIndex(1)

        self.box_language = QtWidgets.QComboBox(self.centralwidget)
        self.box_language.setGeometry(QtCore.QRect(590, 470, 111, 22))
        self.box_language.setObjectName("box_language")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/usa.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon, "")
        self.box_language.setItemText(0, "English")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("imgs/por.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon1, "")
        self.box_language.setItemText(1, "Português")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("imgs/spa.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon2, "")
        self.box_language.setItemText(2, "Español")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("imgs/ita.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon3, "")
        self.box_language.setItemText(3, "Italiano")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("imgs/fra.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon4, "")
        self.box_language.setItemText(4, "Française")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("imgs/ger.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.box_language.addItem(icon5, "")
        self.box_language.setItemText(5, "Deutsche")

        if language == "English":
            self.box_language.setCurrentIndex(0)
        elif language == "Português":
            self.box_language.setCurrentIndex(1)
        elif language == "Español":
            self.box_language.setCurrentIndex(2)
        elif language == "Italiano":
            self.box_language.setCurrentIndex(3)
        elif language == "Française":
            self.box_language.setCurrentIndex(4)
        elif language == "Deutsche":
            self.box_language.setCurrentIndex(5)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ###############################################################################################
        # Here are some code that must start automatically

        # Check the configured wait time
        # nessa parte eu transformei o wait_timer_as_string em segundos e integer
        global wait_timer_as_string
        date_time = datetime.datetime.strptime(wait_timer_as_string, "%H:%M:%S")
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        seconds_from_datetime = int(a_timedelta.total_seconds())
        global wait_timer
        wait_timer = seconds_from_datetime

        wait_timer_as_string_hour = (int(wait_timer_as_string.split(':')[0]))
        wait_timer_as_string_minute = (int(wait_timer_as_string.split(':')[1]))
        wait_timer_as_string_second = (int(wait_timer_as_string.split(':')[2]))

        configure_self_box_wait_timer_setTime = ("self.box_wait_timer.setTime(QtCore.QTime(" + str(wait_timer_as_string_hour) + ", " + str(
                wait_timer_as_string_minute) + ", " + str(wait_timer_as_string_second) + "))")
        exec(configure_self_box_wait_timer_setTime)

        configure_self_lcdNumber_setProperty = ("self.lcdNumber.setProperty('value', " + str(wait_timer) + ")")
        exec(configure_self_lcdNumber_setProperty)

        #### Check if application is configured to start running
        if start_application_running == True:
            self.app_start_thread()

        ###############################################################################################

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CDR Files Organizer"))
        self.button_start.setText(_translate("MainWindow", LANGUAGE[2]))
        self.button_stop.setText(_translate("MainWindow", LANGUAGE[3]))
        self.text_status.setText(_translate("MainWindow", LANGUAGE[4]))
        self.text_timer.setText(_translate("MainWindow", LANGUAGE[5]))
        self.box_wait_timer.setDisplayFormat(_translate("MainWindow", "hh:mm:ss"))
        self.text_wait_timer.setText(_translate("MainWindow", LANGUAGE[6]))
        self.text_progress.setText(_translate("MainWindow", LANGUAGE[7]))
        self.lineEdit_source_folder.setText(_translate("MainWindow", source_folder))
        self.lineEdit_destination_folder.setText(_translate("MainWindow", destination_folder))
        self.text_source_folder.setText(_translate("MainWindow", LANGUAGE[8]))
        self.text_destionation_folder.setText(_translate("MainWindow", LANGUAGE[9]))
        self.button_open_log_files.setText(_translate("MainWindow", LANGUAGE[10]))
        self.button_help.setText(_translate("MainWindow", LANGUAGE[11]))
        self.button_about.setText(_translate("MainWindow", LANGUAGE[12]))
        self.button_save_configuration.setText(_translate("MainWindow", LANGUAGE[13]))
        self.button_source_folder_tool.setText(_translate("MainWindow", "..."))
        self.button_destination_folder_tool.setText(_translate("MainWindow", "..."))
        self.text_language.setText(_translate("MainWindow", LANGUAGE[14]))
        self.text_start_application_running.setText(_translate("MainWindow", LANGUAGE[15]))
        self.button_apply_language.setText(_translate("MainWindow", LANGUAGE[16]))
        self.text_time_until_next_run.setText(_translate("MainWindow", LANGUAGE[17]))
        self.button_close.setText(_translate("MainWindow", LANGUAGE[18]))


        # Old code before translation - clean up at the end
        # self.text_msg_alert.setText(_translate("MainWindow", "Some files could not be moved,\n please check log files."))
        # self.button_start.setText(_translate("MainWindow", "Start"))
        # self.button_stop.setText(_translate("MainWindow", "Stop"))
        # self.text_status.setText(_translate("MainWindow", "STATUS"))
        # self.text_timer.setText(_translate("MainWindow", "TIMER"))
        # self.text_wait_timer.setText(_translate("MainWindow", "Wait timer:"))
        # self.text_progress.setText(_translate("MainWindow", "Progress:"))
        # self.text_source_folder.setText(_translate("MainWindow", "Source Folder:"))
        # self.text_destionation_folder.setText(_translate("MainWindow", "Destination Folder:"))
        # self.button_open_log_files.setText(_translate("MainWindow", "Open Log Files"))
        # self.button_help.setText(_translate("MainWindow", "Help"))
        # self.button_about.setText(_translate("MainWindow", "About"))
        # self.button_save_configuration.setText(_translate("MainWindow", "Save Configuration"))
        # self.text_language.setText(_translate("MainWindow", "Language:"))
        # self.text_start_application_running.setText(_translate("MainWindow", "Start Application Running?"))
        # self.button_apply_language.setText(_translate("MainWindow", "Apply Language"))
        # self.text_time_until_next_run.setText(_translate("MainWindow", "Time until next run:"))
        # self.button_close.setText(_translate("MainWindow", "Close"))

    def app_start_thread(self):
        # Set variable STOP to False
        global STOP
        STOP = False

        # Check if source and destination folder exist
        folders_validation_test = self.folders_validation()
        if folders_validation_test == False:
            return

        ### set time information to LCD display
        self.read_timer_information()

        # Start a secondary thread to run the app_start function
        # this is necessary because, if not, the app_start function will
        # consume all resources from the main thread and the application
        # interface will freeze

        self.thread = Worker()
        self.thread.signal_change_progress_bar.connect(self.setProgressVal)
        self.thread.signal_change_lcd_value.connect(self.setCounterVal)
        self.thread.start()


        # change picture to running
        self.picture_status.setPixmap(QtGui.QPixmap("imgs/start.png"))

    def setProgressVal(self, val):
        # self.progressbar.setValue(val)
        self.box_progressBar.setProperty("value", int(np.ceil(val + 1)))

    def setCounterVal(self, val):
        # self.progressbar.setValue(val)
        configure_self_lcdNumber_setProperty = ("self.lcdNumber.setProperty('value', " + str(val) + ")")
        exec(configure_self_lcdNumber_setProperty)

    def app_stop(self):

        # Set variable STOP to true
        global STOP
        STOP = True

        global RUNNING
        RUNNING = False

        # Change the status image
        self.picture_status.setPixmap(QtGui.QPixmap("imgs/stop.png"))

        log_time = time.ctime()
        print((log_time) + " - Application has stopped due to user request.")

    def app_open_log_files(self):
        os.system("start logs")

    def app_help(self):
        os.system("start help.html")

    def app_close(self):
        self.app_stop()
        sys.exit()

    def app_about(self):
        msg = QMessageBox()
        msg.setWindowTitle(LANGUAGE[27])
        msg.setText("CDR File Organizer\n"
                    "\n"
                    "" + LANGUAGE[28] + ""
                                        "\n"
                                        "Vinicius Buscacio - vinicius@buscacio.net\n"
                                        "\n"
                                        "https://github.com/viniciusbuscacio\n"
                                        "\n"
                                        "https://www.linkedin.com/in/viniciusbuscacio/\n"
                                        "\n"
                    )
        msg.setIcon(QMessageBox.Information)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        x = msg.exec_()

        ### read the time information and write to the LCD display
    def read_timer_information(self):
        wait_timer_as_string = self.box_wait_timer.text()
        date_time = datetime.datetime.strptime(wait_timer_as_string, "%H:%M:%S")
        a_timedelta = date_time - datetime.datetime(1900, 1, 1)
        seconds_from_datetime = int(a_timedelta.total_seconds())
        global wait_timer
        wait_timer = seconds_from_datetime
        configure_self_lcdNumber_setProperty = ("self.lcdNumber.setProperty('value', " + str(wait_timer) + ")")
        exec(configure_self_lcdNumber_setProperty)



    def app_save_configuration(self):
        # call the function to test the folders - if result is 1, return
        folders_validation_test = self.folders_validation()
        if folders_validation_test == False:
            return

        global source_folder
        global destination_folder
        global wait_timer
        global start_application_running
        global language

        read_start_application_running = self.box_start_application_running.currentIndex()
        if read_start_application_running == 0:
            start_application_running = False
        elif read_start_application_running == 1:
            start_application_running = True


        ### set time information to LCD display
        self.read_timer_information()


        try:
            f = open("config.txt", "w")
            f.write("source_folder=" + source_folder + "\n")
            f.write("destination_folder=" + destination_folder + "\n")
            f.write("wait_timer=" + wait_timer_as_string + "\n")
            f.write("language=" + language + "\n")
            f.write("start_application_running=" + str(start_application_running) + "\n")
            f.close()
            msg = QMessageBox()
            msg.setWindowTitle(LANGUAGE[36])
            msg.setText(LANGUAGE[37])
            msg.setIcon(QMessageBox.Information)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            x = msg.exec_()
        except:
            msg = QMessageBox()
            msg.setWindowTitle(LANGUAGE[38])
            msg.setText(LANGUAGE[39])
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()

    def app_button_source_folder(self):
        global source_folder
        source_folder = QFileDialog.getExistingDirectory()
        self.lineEdit_source_folder.setText(source_folder)

    def app_button_destination_folder(self):
        global destination_folder
        destination_folder = QFileDialog.getExistingDirectory()
        self.lineEdit_destination_folder.setText(destination_folder)

    def app_apply_language(self):
        msg = QMessageBox()
        msg.setWindowTitle(LANGUAGE[29])
        msg.setText(LANGUAGE[30])
        msg.setIcon(QMessageBox.Information)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        msg.setWindowIcon(icon)
        x = msg.exec_()
        apply_selected_language = self.box_language.currentText()
        global language
        language = apply_selected_language

    def folders_validation(self):
        # Read the content of the field lineEdit_source_folder
        source_folder = self.lineEdit_source_folder.text()

        # Check if the source_folder exist
        if os.path.exists(source_folder):
            pass
        else:
            msg = QMessageBox()
            # msg.setWindowTitle("Error")
            msg.setWindowTitle(LANGUAGE[31])
            # msg.setText("Source Folder does not exist.")
            msg.setText(LANGUAGE[32])
            msg.setIcon(QMessageBox.Warning)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            x = msg.exec_()
            return False

        # Read the content of the field lineEdit_destination_folder
        destination_folder = self.lineEdit_destination_folder.text()

        if source_folder == destination_folder:
            msg = QMessageBox()
            msg.setWindowTitle(LANGUAGE[33])
            msg.setText(LANGUAGE[34])
            msg.setIcon(QMessageBox.Warning)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            x = msg.exec_()
            return False

        if os.path.exists(destination_folder):
            return True
        else:
            msg = QMessageBox()
            msg.setWindowTitle(LANGUAGE[33])
            msg.setText(LANGUAGE[35])
            msg.setIcon(QMessageBox.Warning)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("imgs/cdr.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
            msg.setWindowIcon(icon)
            x = msg.exec_()
            return False



###############################################################################################

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())