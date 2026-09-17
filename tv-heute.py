#! /usr/bin/env python3
#
#  TV-Heute - © 2026 by Woodstock
#
###############################################################################################################

from tkinter import *
import tkinter as tk
import datetime
try:
    import requests
    NO_Requests = False
except ImportError:
    NO_Requests = True

###############################################################################################################

Vordergrund = "#FFFFCC"
Hintergrund = "#000066"

epgID = []        # EPG-ID
epgName = []      # Sendername
epgTag = 0        # 0 = heute
epgTitel = []     # Sendung
epgDesc = []      # Beschreibung

epgSender = [
        "76674, Das Erste","76627, ZDF","76740, RTL","76664, SAT.1","76762, ProSieben","438457, RTLZWEI","76792, kabel eins",
        "76704, VOX","76684, WDR","76748, NDR","76648, HR","76730, MDR","76751, RBB","76693, SWR","76712, BR","76682, 3sat",
        "76641, ARTE","76649, PHOENIX","76718, ZDF info","76739, ZDF neo","76738, ONE","76708, Tele 5","76787, NITRO","76722, RTLup",
        "76716, SAT.1 Gold","76702, ProSieben MAXX","76614, sixx","76767, SUPER RTL","76769, SAT.1 emotions","76749, ProSieben Fun",
        "76725, kabel eins CLASSICS","76796, VOXup","76619, Eurosport","76744, Eurosport 2","76659, SPORT1","76754, SPORT1+",
        "438444, ntv","76795, WELT","76696, tagesschau24","438466, ARD alpha","438462, euronews","76797, CNN International",
        "76639, Bloomberg Europe TV","182674, DF1","438440, Welt der Wunder TV","379181, DOKUSAT","438452, The HISTORY Channel",
        "438453, Prime HD","438450, Servus TV Österreich","438442, ORF 1","76616, ORF 2","76734, ORF III","76756, ORF SPORT +",
        "76784, SRF 1","76772, SRF zwei","76715, kabel eins Doku","76636, N24 Doku","76714, SPIEGEL Geschichte","76692, DMAX",
        "76628, Nat Geo HD","76638, ATV II","76699, TLC","76662, Universal Channel HD","76686, Discovery HD","76783, NAT GEO WILD",
        "76800, GEO Television","76759, Animal Planet","76700, RTL Crime","76667, Crime + Investigation","438455, DMF",
        "76804, RTL Passion","76731, RiC","76770, Kinowelt TV","76645, Warner TV Film","76806, Warner TV Serie","76679, Warner TV Comedy",
        "76745, ANIXE","76742, COMEDY CENTRAL","76736, Nicktoons ","76622, Nick Jr.","438460, 13th Street Universal","76789, TOGGO plus",
        "76763, Cartoon Network","76680, KiKA","76786, Disney Channel","438467, Fix & Foxi","76631, Silverline","76658, Star TV",
        "76776, Marco Polo TV","76675, Heimatkanal","76624, Romance TV","76732, PULS 4","76808, PULS acht","76646, Curiosity Channel",
        "76673, RTL Living","438449, Home & Garden TV","76794, Bibel TV","76805, K-TV","76688, Bergblick","76666, münchen TV","76810, ATV",
        "76701, Hamburg 1","76710, Leipzig Fernsehen","76809, DELUXE MUSIC","76803, GoldStar TV","76758, Gute Laune TV","76780, MTV",
        "76775, Fashion TV","76642, Beate-Uhse.TV","76660, Playboy TV","76685, Adult Channel","76713, Lust Pur","76765, More than Sports TV",
        "438446, Auto Motor Sport","76630, Motorvision TV","438441, sportdigital Fussball","76707, eSports1","76690, EXTREME SPORTS",
        "76661, HSE","76737, HSE Extra ","76697, QVC","76618, QVC2","76773, 123.tv","76781, sonnenklar.TV","76632, DAZN",
        "76733, Sky Sport News","10781, Sky Sport F1","464744, Sky Sport Bundesliga 1","438445, Sky Sport Premier League",
        "210645, Sky Sport Golf","10634, Sky Sport Tennis","10675, Sky Sport Top Event","438458, Sky Cinema Action HD",
        "438459, Sky Cinema Classics HD","10908, Sky Crime","438465, Sky Cinema Family HD","438461, Sky Cinema Premiere HD",
        "10620, Sky Documentaries","76663, Sky Krimi","10640, Sky Nature","10918, Sky Showcase","10635, Sky Replay" ]

###############################################################################################################

class TT_Listbox(tk.Listbox):

    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        self.bind("<Motion>", self.Maus_Motion)
        self.bind("<Leave>", self.Maus_Leave)
        self.tFenster = None

    def Maus_Motion(self, event):
        idx = self.nearest(event.y)
        if idx >= 0:
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
        label = tk.Label(self.tFenster, text=beschreibung, font="Helvetica 11", fg="black", bg="#ffff88",
                                        padx=5, pady=5, justify="left", wraplength=350, relief="solid", borderwidth=1)
        label.pack()

###################################################################################################################

def Info_Anzeigen(event=None):

    link = "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL0Jlcmxpbg%3D%3D"
    datum = datetime.date.today() + datetime.timedelta(days=epgTag)
    datum = "&date=" + datum.strftime("%Y%m%d")

    if Sender_Liste.curselection():
        idx = Sender_Liste.curselection()[0]
        ch_id = "&channel_id=" + epgID[idx]
        URL = link + datum + ch_id           # URL zusammenbauen
        #print(URL)
        Info_Liste.delete("0", "end")
        try:
            xml_dat = requests.get(URL, timeout=10)
        except requests.exceptions.Timeout:
            Info_Liste.insert("end", "  EPG download error: timed out")
        else:
            if xml_dat.status_code != 200:
                Info_Liste.insert("end", "  EPG download error: " + str(xml_dat.status_code))
            else:
                Info_Liste.delete("0", "end")
                xml_text = str(xml_dat.text)
                x = y = z = v = w = 0
                epgTitel.clear()
                epgDesc.clear()
                while 1:  
                    x = xml_text.find('start="', x)            # Startzeit suchen
                    if x == -1:    break
                    y = xml_text.find('<title lang="', y)      # Titel-Anfang suchen
                    z = xml_text.find("</title>", y+17)        # Titel-Ende suchen (ab Textanfang)
                    v = xml_text.find("<desc", v)              # Beschreibung-Anfang suchen
                    epgTitel.append(xml_text[y+17:z])
                    if xml_text[v+6:v+8] == "/>":
                        epgDesc.append("Keine Beschreibung")
                    else:
                        w = xml_text.find("</desc>", v+6)      # Beschreibung-Ende suchen (ab Textanfang)
                        epgDesc.append(xml_text[v+6:w])
                    Info_Liste.insert("end", "  " + xml_text[x+15:x+17] + ":" + xml_text[x+17:x+19] + " - " + xml_text[y+17:z])
                    x += 50; y += 50; z += 50;v += 50; w += 50;

###################################################################################################################

def Datum_Mausklick(tag):

    global epgTag

    Datum_Buttons[epgTag+3].config(font="Consolas 9")
    epgTag = tag
    Datum_Buttons[epgTag+3].config(font="Consolas 10 bold italic")
    Info_Anzeigen()

    return "break"         # eingebaute <Pfeiltaste> in tk.Listbox verhindern

###################################################################################################################

def Datum_Pfeiltaste(tag):

    global epgTag

    if tag == 1 and epgTag < 3 or tag == -1 and epgTag > -3:
        Datum_Buttons[epgTag+3].config(font="Consolas 9")
        epgTag += tag
        Datum_Buttons[epgTag+3].config(font="Consolas 10 bold italic")
        Info_Anzeigen()

    return "break"         # eingebaute <Pfeiltaste> in tk.Listbox verhindern

###################################################################################################################

Master = tk.Tk()
Master.title("TV-Heute")

if NO_Requests:
    tk.Label(Master, text="\n   Python Modul Requests nicht installiert.   \n").pack()

else:
    epgID.clear()
    epgName.clear()

    for i in range(len(epgSender)):
        epgID.append(epgSender[i].split(", ")[0])
        epgName.append(epgSender[i].split(", ")[1])

    # Datum-Buttons
    Datum_Frame = tk.Frame(Master, bg=Hintergrund)
    Datum_Frame.pack(side="top", fill="x", padx=1, pady=1)
    Datum_But1 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(-3))
    Datum_But2 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(-2))
    Datum_But3 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(-1))
    Datum_But4 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(0))
    Datum_But5 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(1))
    Datum_But6 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(2))
    Datum_But7 = tk.Button(Datum_Frame, bd=3, command=lambda: Datum_Mausklick(3))
    Datum_Buttons = [Datum_But1,Datum_But2,Datum_But3,Datum_But4,Datum_But5,Datum_But6,Datum_But7,]
    for i in range (7):
        datum = datetime.date.today() + datetime.timedelta(days=i-3)
        Datum_Buttons[i].config(text=datum.strftime(" %a %d.%m."), font="Consolas 9")
        Datum_Buttons[i].grid(row=1, column=i+2, padx=3, pady=4)
    # Sender-Liste
    Sender_VScroll = tk.Scrollbar(Master, width=14)
    Sender_Liste = tk.Listbox(Master, width=28, height=33, selectborderwidth=2, yscrollcommand=Sender_VScroll.set)
    Sender_Liste.config(foreground=Vordergrund, background=Hintergrund, font="Helvetica 11")
    Sender_VScroll.config(command=Sender_Liste.yview)
    Sender_Liste.pack(side="left", fill="both", padx=3, pady=3, expand=True)
    Sender_VScroll.pack(side="left", fill="y", padx=1, pady=1)
    # Info-Liste
    Info_VScroll = tk.Scrollbar(Master, width=14)
    Info_HScroll = tk.Scrollbar(Master, width=14, orient="horizontal")
    Info_Liste = TT_Listbox(Master, width=60, height=31, selectborderwidth=2, yscrollcommand=Info_VScroll.set, xscrollcommand = Info_HScroll.set)
    Info_Liste.config(foreground=Vordergrund, background=Hintergrund, font="Consolas 10")
    Info_VScroll.config(command=Info_Liste.yview)
    Info_HScroll.config(command=Info_Liste.xview)
    Info_HScroll.pack(side="bottom", fill="x", padx=1, pady=1)
    Info_Liste.pack(side="left", fill="both", padx=2, pady=2, expand=True)
    Info_VScroll.pack(side="left", fill="y", padx=1, pady=1)

    Sender_Liste.delete(0, tk.END) 
    for i in range(len(epgName)):
        Sender_Liste.insert(tk.END, "   " + epgName[i])                 # Sendernamen in Liste
    Sender_Liste.selection_set(0)
    Sender_Liste.activate(0)
    Sender_Liste.see(0)
    Sender_Liste.focus_set()

    Datum_Buttons[epgTag+3].config(font="Consolas 10 bold italic")      # Button für akt. Tag
    Info_Anzeigen()                                                     # EPG für 1.Sender

    Sender_Liste.bind("<Return>", Info_Anzeigen)
    Sender_Liste.bind("<Double-Button-1>", Info_Anzeigen)
    Sender_Liste.bind("<Left>", lambda event: Datum_Pfeiltaste(-1))     # eingebaute <Links-Taste> in tk.Listbox umgehen
    Sender_Liste.bind("<Right>", lambda event: Datum_Pfeiltaste(1))     # eingebaute <Rechts-Taste> in tk.Listbox umgehen

Master.mainloop()

###############################################################################################################

