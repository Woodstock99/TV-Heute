#! /usr/bin/env python3
#
#  TV-Heute-XXX - © 2026 by Woodstock
#
###############################################################################################################

from tkinter import *
import tkinter as tk
from datetime import datetime, timedelta
import urllib.request
import gzip
import xml.etree.ElementTree as ET

###############################################################################################################

Vordergrund = "#FFFFCC"
Hintergrund = "#000066"

Wochentag = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]

xmlText = ""
epgID = []        # EPG-ID
epgName = []      # Sendername
epgTag = 0        # 0 = heute
epgTitel = []     # Sendung
epgDesc = []      # Beschreibung

epgSender = [ "babes-tv", "barely-legal", "barely-legal-ua", "blue-hustler", "blue-hustler-24",
              "brazzers-tv-europe", "brazzers-tv-europe-ru", "dorcel", "dorcel-xxx", "erox", "erox-ua",
              "eroxxxhd", "extasy4k", "extasytv", "hustler-hd", "hustler-tv", "penthouse-gold",
              "penthouse-hd", "penthouse-passion-ua", "penthouse-quickies", "playboy-tv", "playboy-tv-uk",
              "private-spice", "private-tv", "redlight-hd", "redlips", "super-one", "vivid-red",
              "vivid-touch","vivid-tv", "xxl-xxx" ]

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
        self.tFenster.wm_overrideredirect(True)      # Rahmenloses Fenster
        self.tFenster.wm_geometry(f"+{x+20}+{y}")    # 20 Pixel rechts vom Mauszeiger
        label = tk.Label(self.tFenster, text=beschreibung, font="Helvetica 11", fg="#000000", bg="#FFFF88",
                                        padx=5, pady=5, justify="left", wraplength=500, relief="solid", borderwidth=1)
        label.pack()

###################################################################################################################

def Info_Anzeigen(event=None):

    if Sender_Liste.curselection():
        idx = Sender_Liste.curselection()[0]

        Master.title(epgName[idx])
        Info_Liste.delete("0", "end")
        epgDesc.clear()

        for programme in root.findall("programme"):
            Sender = programme.get("channel", 'Unbekannt')

            if Sender == epgID[idx]:
                Titel = programme.find("title").text
                Start = programme.get("start", "")
                Stop = programme.get("stop", "")

                Start_str = f"{Start[0:8]} {Start[8:12]}"
                Start_neu = datetime.strptime(Start_str, "%Y%m%d %H%M") + timedelta(hours=-2)
                Wochentag_idx = Start_neu.weekday()

                if len(Start) >= 8:    DatZeit = Wochentag[Wochentag_idx] + Start_neu.strftime(" %d.%m. %H:%M")
                else:                  DatZeit = "Unbekannt   "
                Info_Liste.insert("end", "  " + DatZeit + " - " + f"{Titel}")

                try:
                    epgDesc.append(programme.find("desc").text)
                except:
                    epgDesc.append("Keine Beschreibung")

##################################################################################################################

def Sender_Laden(link):

    global root, epgID, epgName

    Anfrage = urllib.request.Request(link, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(Anfrage, timeout=10) as Antwort:
        Gepackt = Antwort.read()
        Entpackt = gzip.decompress(Gepackt)
        xmlText = Entpackt.decode("utf-8")

    root = ET.fromstring(xmlText)

    epgID.clear()
    epgName.clear()
    #for channel in root.findall("channel"):    # unsortiert
    for channel in sorted(root.findall("channel"), key=lambda x: x.findtext("display-name", default="").lower()):
        if channel.get("id") in epgSender:
            epgID.append(channel.get("id"))
            epgName.append(channel.find("display-name").text)

    Sender_Liste.delete(0, tk.END) 
    for i in range(len(epgName)):
        Sender_Liste.insert(tk.END, "    " + epgName[i])
    Sender_Liste.selection_set(0)
    Sender_Liste.activate(0)
    Sender_Liste.see(0)
    Sender_Liste.focus_set()

####################################################################################################################

print("Einen Moment bitte ...")

Master = tk.Tk()
Master.title("TV-Heute-XXX")
Master.geometry("+500+100") 

Menuleiste = tk.Menu(Master, activebackground=Hintergrund, activeforeground=Vordergrund, font="Helvetica 11")
#Menuleiste.add_command(label="  Länderwahl  ", command=Land_Auswahl, underline=2)
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

Sender_Laden("https://iptvx.one/EPG_LITE/epg_lite.xml.gz")

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

