#! /usr/bin/env python3
#
#  TV-Heute-EU - © 2026 by Woodstock
#
###############################################################################################################

from tkinter import *
import tkinter as tk
from datetime import datetime
import urllib.request
import gzip
import xml.etree.ElementTree as ET

###############################################################################################################

Vordergrund = "#FFFFCC"
Hintergrund = "#000066"

Wochentag = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

xmlText = ""
epgID = []
epgName = []
epgTag = 0
epgTitel = []
epgDesc = []

epgURLs = [ "Deutschland, DE1", "Österreich, AT1", "Schweiz, CH1", "Niederlande, NL1", "Belgien, BE2", 
            "Luxemburg, LU1", "Frankeich, FR1", "Großbritannien, UK1", "Irland, IE1", "Italien, IT1", 
            "Spanien, ES1", "Portugal, PT1", "Dänemark, DK1", "Norwegen, NO1", "Schweden, SE1", "Finnland, FI1", 
            "Lettland, LV1", "Polen, PL1", "Ukraine, UA1", "Tschechien, CZ1", "Slowakei, SK1", "Ungarn, HU1",
            "Rumänien, RO1", "Bulgarien, BG1", "Serbien, RS1", "Kroatien, HR1", "Bosnien Herzegowina, BA1", 
            "Griechenland, GR1", "Malta, MT1", "United States, US2", "Brasilien, BR1", "Australien, AU1" ] 

###############################################################################################################

class TT_Listbox(tk.Listbox):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind("<Motion>", self.Maus_Motion)
        self.bind("<Leave>", self.Maus_Leave)
        self.tFenster = None

    def Maus_Motion(self, event):
        idx = self.nearest(event.y)
        if idx >= 0 and len(epgDesc) > 0:
            self.Tooltip_Anzeigen(epgDesc[idx], event.x_root, event.y_root)

    def Maus_Leave(self, event=None):
        if self.tFenster:
            self.tFenster.destroy()
            self.tFenster = None

    def Tooltip_Anzeigen(self, beschreibung, x, y):
        self.Maus_Leave()
        self.tFenster = tk.Toplevel(self)
        self.tFenster.wm_overrideredirect(True)
        self.tFenster.wm_geometry(f"+{x+20}+{y}")
        label = tk.Label(self.tFenster, text=beschreibung, font="Helvetica 11", fg="#000000", bg="#FFFF88",
                                        padx=5, pady=5, justify="left", wraplength=500, relief="solid", borderwidth=1)
        label.pack()

###################################################################################################################

def Info_Anzeigen(event=None):

    if Sender_Liste.curselection():
        idx = Sender_Liste.curselection()[0]

        Info_Liste.delete("0", "end")
        epgDesc.clear()

        for programme in root.findall("programme"):
            Sender = programme.get("channel", 'Unbekannt')

            if Sender == epgID[idx]:
                Titel = programme.find("title").text
                Start = programme.get("start", "")
                Stop = programme.get("stop", "")

                Start_str = f"{Start[0:8]}"
                Datum = datetime.strptime(Start_str, "%Y%m%d")
                Wochentag_idx = Datum.weekday()

                if len(Start) >= 8:    DatZeit = Wochentag[Wochentag_idx] + f" {Start[6:8]}.{Start[4:6]}. {Start[8:10]}:{Start[10:12]}"
                else:                  DatZeit = "Unbekannt   "
                Info_Liste.insert("end", "  " + DatZeit + " - " + f"{Titel}")

                try:
                    epgDesc.append(programme.find("desc").text)
                except:
                    epgDesc.append("Keine Beschreibung")

####################################################################################################################

def Land_Auswahl(event=None):

    def XML_Laden(event):

        if Land_Liste.curselection():
            nr = Land_Liste.curselection()[0]
            link = "https://epgshare01.online/epgshare01/epg_ripper_" + epgURLs[nr].split(", ")[1] + ".xml.gz"
            Master.wm_title(epgURLs[nr].split(", ")[0])
            Land_Laden(link)
            Info_Anzeigen()
            Fenster.destroy()

    Fenster = tk.Toplevel(Master)
    Fenster.title("")
    Fenster.geometry("+" + str(Master.winfo_x()+20) + "+" + str(Master.winfo_y()+3)) 
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Land_VScroll = tk.Scrollbar(Fenster, width=14)
    Land_Liste = tk.Listbox(Fenster, width=19, height=16, selectborderwidth=2, yscrollcommand=Land_VScroll.set)
    Land_VScroll.config(command=Land_Liste.yview)
    Land_Liste.config(fg="#000000", bg="#FFFF88", font="Helvetica 11")
    Land_VScroll.pack(side="right", fill="y", padx=1, pady=1)
    Land_Liste.pack(fill="both", padx=3, pady=3, expand=True)

    Land_Liste.delete(0, tk.END) 
    for i in range(len(epgURLs)):
        Land_Liste.insert(tk.END, "    " + epgURLs[i].split(", ")[0])

    Land_Liste.selection_set(0)
    Land_Liste.activate(0)
    Land_Liste.see(0)
    Land_Liste.focus_set()
    Land_Liste.bind("<Return>", XML_Laden)
    Land_Liste.bind("<Double-Button-1>", XML_Laden)
    Fenster.bind("<Escape>", lambda event: Fenster.destroy())

##################################################################################################################

def Land_Laden(link):

    global root, epgID, epgName

    Anfrage = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(Anfrage, timeout=10) as Antwort:
        Gepackt = Antwort.read()
        Entpackt = gzip.decompress(Gepackt)
        xmlText = Entpackt.decode("utf-8")

    root = ET.fromstring(xmlText)

    epgID.clear()
    epgName.clear()
    if link == "https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz":    # Deutschland unsortiert
        for channel in root.findall("channel"):
            epgID.append(channel.get("id"))
            epgName.append(channel.find("display-name").text)
    else:
        for channel in sorted(root.findall("channel"), key=lambda x: x.findtext("display-name", default="").lower()):
            epgID.append(channel.get("id"))
            epgName.append(channel.find("display-name").text)

    Sender_Liste.delete(0, tk.END) 
    for i in range(len(epgName)):
        Sender_Liste.insert(tk.END, "    " + epgName[i])
    Sender_Liste.selection_set(0)
    Sender_Liste.activate(0)
    Sender_Liste.see(0)
    Sender_Liste.focus_set()

##################################################################################################################

Master = tk.Tk()
Master.title("Deutschland")
Master.geometry("+500+100") 

Menuleiste = tk.Menu(Master, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
Menuleiste.add_command(label="  Länderwahl  ", command=Land_Auswahl, underline=2)
Master.config(menu=Menuleiste)

# Sender-Liste
Sender_VScroll = tk.Scrollbar(Master, width=14)
Sender_Liste = tk.Listbox(Master, width=26, height=33, selectborderwidth=2, yscrollcommand=Sender_VScroll.set)
Sender_Liste.config(foreground=Vordergrund, background=Hintergrund, font="Helvetica 11")
Sender_VScroll.config(command=Sender_Liste.yview)
Sender_Liste.pack(side="left", fill="both", padx=3, pady=3, expand=True)
Sender_VScroll.pack(side="left", fill="y", padx=1, pady=1)
# Info-Liste
Info_VScroll = tk.Scrollbar(Master, width=14)
Info_HScroll = tk.Scrollbar(Master, width=14, orient="horizontal")
Info_Liste = TT_Listbox(Master, width=64, height=31, selectborderwidth=2, yscrollcommand=Info_VScroll.set, xscrollcommand = Info_HScroll.set)
Info_Liste.config(foreground=Vordergrund, background=Hintergrund, font="Consolas 10")
Info_VScroll.config(command=Info_Liste.yview)
Info_HScroll.config(command=Info_Liste.xview)
Info_HScroll.pack(side="bottom", fill="x", padx=1, pady=1)
Info_Liste.pack(side="left", fill="both", padx=2, pady=2, expand=True)
Info_VScroll.pack(side="left", fill="y", padx=1, pady=1)

Land_Laden("https://epgshare01.online/epgshare01/epg_ripper_DE1.xml.gz")

Sender_Liste.delete(0, tk.END) 
for i in range(len(epgName)):
    Sender_Liste.insert(tk.END, "   " + epgName[i])
Sender_Liste.selection_set(0)
Sender_Liste.activate(0)
Sender_Liste.see(0)
Sender_Liste.focus_set()

Info_Anzeigen()

Sender_Liste.bind("<Return>", Info_Anzeigen)
Sender_Liste.bind("<Double-Button-1>", Info_Anzeigen)
Sender_Liste.bind("<Alt-Key-q>", lambda event: Master.destroy())

Master.mainloop()

###############################################################################################################

