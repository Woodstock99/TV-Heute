#!/usr/bin/env python3
#
#  TV-Heute (Qt6 Version) - © 2026 by Woodstock
#
###############################################################################################################

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QListWidgetItem, QLabel )
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import sys
import datetime
try:
    import requests
    NO_Requests = False
except ImportError:
    NO_Requests = True

###############################################################################################################

class TVHeuteQtApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TV-Heute (Qt6 Version)")
        self.resize(800, 700)

        #self.vordergrund = "#FFFFCC"    # fixes Design
        #self.hintergrund = "#000066"    # fixes Design
        
        self.wochentag = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"]
        self.wo_tag_nr = datetime.datetime.now().weekday()

        self.epg_id = []
        self.epg_name = []
        self.epg_tag = 0    # 0 = heute
        self.epg_titel = []
        self.epg_desc = []

        self.epg_sender = [
            "76674, Das Erste", "76627, ZDF", "76739, ZDF neo", "76718, ZDF info", 
            "76740, RTL", "438457, RTLZWEI", "76722, RTLup", "76767, SUPER RTL", 
            "76664, SAT.1", "76716, SAT.1 Gold", "76769, SAT.1 emotions", "76762, ProSieben", 
            "76702, ProSieben MAXX", "76749, ProSieben Fun", "76792, kabel eins", 
            "76725, kabel eins CLASSICS", "76715, kabel eins Doku", "76704, VOX", 
            "76796, VOXup", "76787, NITRO", "76708, Tele 5", "76684, WDR", 
            "76748, NDR", "76648, HR", "76730, MDR", "76751, RBB", "76693, SWR", 
            "76712, BR", "76682, 3sat", "76738, ONE", "76641, ARTE", "76649, PHOENIX", 
            "76619, Eurosport", "76744, Eurosport 2", "76773, 123.tv", 
            "438460, 13th Street Universal", "76670, 3+", "76685, Adult Channel", 
            "76759, Animal Planet", "76745, ANIXE", "438466, ARD alpha", "76810, ATV", 
            "76638, ATV II", "438446, Auto Motor Sport", "438468, AXN Black", 
            "438454, AXN White", "76642, Beate-Uhse.TV", "76688, Bergblick", 
            "76794, Bibel TV", "438469, Bon Gusto", "500397, Cartoonito", 
            "76763, Cartoon Network", "76723, Classica", "76797, CNN International", 
            "76742, COMEDY CENTRAL", "76667, Crime + Investigation", "76646, Curiosity Channel", 
            "76632, DAZN", "451928, DAZN 1", "451927, DAZN 2", "76809, DELUXE MUSIC", 
            "182674, DF1", "76686, Discovery HD", "76786, Disney Channel", "76692, DMAX", 
            "438455, DMF", "379181, DOKUSAT", "76775, Fashion TV", "438467, Fix & Foxi", 
            "76800, GEO Television", "76803, GoldStar TV", "76758, Gute Laune TV", 
            "76701, Hamburg 1", "76675, Heimatkanal", "438449, Home & Garden TV", 
            "76661, HSE", "76737, HSE Extra", "76615, Jukebox", "76680, KiKA", 
            "76770, KinoweltTV", "76805, K-TV", "76710, Leipzig Fernsehen", 
            "76713, LUST PUR", "76776, Marco Polo TV", "76765, More than Sports TV", 
            "197537, Motorvision+", "76630, Motorvision TV", "450290, MS Sport", 
            "76780, MTV", "76666, münchen.tv", "76636, N24 Doku", "76628, Nat Geo HD", 
            "76783, NAT GEO WILD", "438439, nick", "76622, Nick Jr.", "76736, Nicktoons", 
            "76694, NOW US", "438444, ntv", "100304, oe24.TV", "438442, ORF 1", 
            "76616, ORF 2", "76734, ORF III", "76756, ORF SPORT +", "76660, Playboy TV", 
            "575368, PULS 24", "76732, PULS 4", "76808, PULS acht", "76697, QVC", 
            "76618, QVC2", "76731, RiC", "535469, Rocket Beans TV", "76624, Romance TV", 
            "76700, RTL Crime", "76673, RTL Living", "76804, RTL Passion", 
            "438450, Servus TV Österreich", "76631, Silverline", "76614, sixx", 
            "76781, sonnenklar.TV", "76714, SPIEGEL Geschichte", "76659, SPORT1", 
            "76754, SPORT1+", "450294, SportDigital1+", "438441, sportdigital Fussball", 
            "76784, SRF 1", "76772, SRF zwei", "76658, STAR TV", "76696, tagesschau24", 
            "438452, The HISTORY Channel", "76699, TLC", "76789, TOGGO plus", 
            "562036, Top Serien", "568719, tv.berlin", "76726, UHD1", 
            "76662, Universal Channel HD", "76679, Warner TV Comedy", "76645, Warner TV Film", 
            "76806, Warner TV Serie", "76795, WELT", "438440, Welt der Wunder TV", 
            "76774, Sky Atlantic HD", "438458, Sky Cinema Action HD", "438459, Sky Cinema Classics HD", 
            "438465, Sky Cinema Family HD", "321554, Sky Cinema Highlights HD", 
            "438461, Sky Cinema Premiere HD", "10908, Sky Crime", "10620, Sky Documentaries", 
            "76663, Sky Krimi", "10640, Sky Nature", "401732, Sky One", 
            "562033, Sky Replay HD", "76764, Sky Sci-Fi", "10918, Sky Showcase", 
            "562035, Sky Showcase HD", "401577, Sky Sport 1", "482486, Sky Sport 2", 
            "456331, Sky Sport 3", "212838, Sky Sport 4", "212824, Sky Sport 5", 
            "480217, Sky Sport 6", "482693, Sky Sport 7", "453384, Sky Sport 8", 
            "478720, Sky Sport 9", "559683, Sky Sport 10", "438448, Sky Sport Austria", 
            "452123, Sky Sport Austria 1 HD", "452126, Sky Sport Austria 2 HD", 
            "452120, Sky Sport Austria 3 HD", "452121, Sky Sport Austria 4 HD", 
            "452122, Sky Sport Austria 5 HD", "452118, Sky Sport Austria 6 HD", 
            "452125, Sky Sport Austria 7 HD", "212821, Sky Sport Bundesliga", 
            "561726, Sky Sport Bundesliga 1", "559320, Sky Sport Bundesliga 2", 
            "558543, Sky Sport Bundesliga 3", "558272, Sky Sport Bundesliga 4", 
            "477005, Sky Sport Bundesliga 5", "446434, Sky Sport Bundesliga 6", 
            "540526, Sky Sport Bundesliga 7", "499802, Sky Sport Bundesliga 8", 
            "473829, Sky Sport Bundesliga 9", "212817, Sky Sport Bundesliga 10", 
            "562034, Sky Sport Bundesliga UHD", "10781, Sky Sport F1", "10645, Sky Sport Golf", 
            "10785, Sky Sport Mix", "76733, Sky Sport News", "438445, Sky Sport Premier League", 
            "10634, Sky Sport Tennis", "10675, Sky Sport Top Event", "452124, Sky Sport UHD", 
            "558979, Sport 1 - myTeamTV", "450501, Sport 2 - myTeamTV", "450500, Sport 3 - myTeamTV", 
            "456147, Sport 4 - myTeamTV", "450295, Sport 5 - myTeamTV", "513148, Sport 6 - myTeamTV", 
            "450303, Sport 7 - myTeamTV", "450300, Sport 8 - myTeamTV", "450502, Sport 9 - myTeamTV", 
            "450302, Sport 10 - myTeamTV", "450306, Sport 11 - myTeamTV", "450299, Sport 12 - myTeamTV", 
            "482487, Sport 13 - myTeamTV", "455988, Sport 14 - myTeamTV", "462760, Sport 15 - myTeamTV", 
            "491421, Sport 16 - myTeamTV", "456554, Sport 17 - myTeamTV", "450292, Sport 18 - myTeamTV" ]

        self.setStyleSheet("""
            QToolTip {
                border: 2px solid #CCCCCC;
                padding: 3px;
                font-family: Consolas;
                font-size: 9pt;  }  """)

        if NO_Requests:
            self.init_error_ui()
        else:
            self.init_ui()

###############################################################################################################

    def init_error_ui(self):
        central_widget = QWidget(self)
        layout = QVBoxLayout(central_widget)
        label = QLabel("Python Modul Requests nicht installiert.")
        layout.addWidget(label)
        self.setCentralWidget(central_widget)

###############################################################################################################

    def init_ui(self):
        for item in self.epg_sender:
            self.epg_id.append(item.split(", ")[0])
            self.epg_name.append(item.split(", ")[1])

        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)

        # Buttons Layout
        self.datum_layout = QHBoxLayout()
        self.datum_buttons = []

        for i in range(7):
            btn = QPushButton()
            tag_offset = i - 3
            btn.clicked.connect(lambda checked, t=tag_offset: self.datum_mausklick(t))
            self.datum_buttons.append(btn)
            self.datum_layout.addWidget(btn)

        main_layout.addLayout(self.datum_layout)
        self.update_datum_buttons()

        # Listen Layout (Senderliste + Programminfos)
        lists_layout = QHBoxLayout()

        self.sender_liste = QListWidget()
        self.sender_liste.setStyleSheet(
            #f"background-color: {self.hintergrund}; color: {self.vordergrund}; "    # fixes Design
            "background-color: palette(base); color: palette(text); "
           "font-family: Helvetica; font-size: 11pt;" )

        for name in self.epg_name:
            self.sender_liste.addItem(f"    {name}")
        self.sender_liste.currentRowChanged.connect(self.info_anzeigen)
        lists_layout.addWidget(self.sender_liste, 1)

        self.info_liste = QListWidget()
        self.info_liste.setStyleSheet(
            #f"background-color: {self.hintergrund}; color: {self.vordergrund}; "    # fixes Design
            "background-color: palette(base); color: palette(text); "
            "font-family: Consolas; font-size: 10pt;" )

        lists_layout.addWidget(self.info_liste, 2)

        main_layout.addLayout(lists_layout)
        self.setCentralWidget(central_widget)

        # Auswahl auf ersten Sender
        if self.sender_liste.count() > 0:
            self.sender_liste.setCurrentRow(0)

###############################################################################################################

    def update_datum_buttons(self):
        for i in range(7):
            tag_offset = i - 3
            datum = datetime.date.today() + datetime.timedelta(days=tag_offset)
            wochentag_text = self.wochentag[(self.wo_tag_nr + tag_offset) % 7]
            text = datum.strftime(f" {wochentag_text} %d.%m.")
            btn = self.datum_buttons[i]
            btn.setText(text)
            
            font = QFont("Consolas", 9)
            if tag_offset == self.epg_tag:
                font.setBold(True)
                font.setItalic(True)
                font.setPointSize(10)
            btn.setFont(font)

###############################################################################################################

    def datum_mausklick(self, tag):
        self.epg_tag = tag
        self.update_datum_buttons()
        self.info_anzeigen()

###############################################################################################################

    def info_anzeigen(self):
        link = "https://epg.pw/api/epg.xml?lang=en&timezone=RXVyb3BlL0Jlcmxpbg%3D%3D"
        datum = datetime.date.today() + datetime.timedelta(days=self.epg_tag)
        datum_str = "&date=" + datum.strftime("%Y%m%d")

        row = self.sender_liste.currentRow()
        if row >= 0:
            ch_id = "&channel_id=" + self.epg_id[row]
            url = link + datum_str + ch_id

            self.info_liste.clear()
            try:
                xml_dat = requests.get(url, timeout=7)
            except requests.exceptions.Timeout:
                self.info_liste.addItem("  Sorry, der EPG-Server antwortet nicht.")
                self.info_liste.addItem("  Bitte versuche es später noch einmal...")
            else:
                if xml_dat.status_code != 200:
                    self.info_liste.addItem(f"  EPG download error: {xml_dat.status_code}")
                    self.info_liste.addItem("  Bitte versuche es später noch einmal...")
                else:
                    xml_text = str(xml_dat.text)
                    x = y = z = v = w = 0
                    self.epg_titel.clear()
                    self.epg_desc.clear()

                    while True:
                        x = xml_text.find('start="', x)
                        if x == -1:
                            break
                        y = xml_text.find('<title lang="', y)
                        z = xml_text.find("</title>", y + 17)
                        v = xml_text.find("<desc", v)
                        
                        titel = xml_text[y + 17 : z]
                        self.epg_titel.append(titel)
                        
                        if xml_text[v + 6 : v + 8] == "/>":
                            desc = "Keine Beschreibung"
                        else:
                            w = xml_text.find("</desc>", v + 6)
                            desc = xml_text[v + 6 : w]
                        
                        self.epg_desc.append(desc)

                        start_time = xml_text[x + 15 : x + 17] + ":" + xml_text[x + 17 : x + 19]
                        item_text = f"  {start_time} - {titel}"
                        
                        # Tooltip mit HTML-Zeilenumbruch
                        item = QListWidgetItem(item_text)
                        formatted_desc = desc.replace("\n", "<br>")
                        tooltip_html = f"<html><body><p style='width: 300px;'>{formatted_desc}</p></body></html>"
                        item.setToolTip(tooltip_html)
                        
                        self.info_liste.addItem(item)

                        x += 50; y += 50; z += 50; v += 50;  w += 50

###############################################################################################################

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TVHeuteQtApp()
    window.show()
    sys.exit(app.exec())

###############################################################################################################
