import json
import bs4
import requests
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter.ttk import *

eventList = []

url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
r = requests.get(url)
data = r.text

print(data)

quakes = json.loads(data)

# properties = quakes['features'][0]['properties']['mag']

for features in quakes['features']:
    print(features)
    for properties in features['properties']:
        for mag in properties['mag']:
            print(mag)

#
# for events in quakes:
#
#     print(events['location'] + "\nLat: " + events['latitude'] + "\nLong: " +
#           events['longitude'] + "\nMagnitude: " + events['magnitude'] + "\n")

# url = "http://earthquake-report.com/feeds/recent-eq?json"
# r = requests.get(url)
# data = r.text
#
# soup = bs4.BeautifulSoup(data, "html.parser")
# print(soup)
#
# quakes = json.loads(data)
#
#
# for events in quakes:
#
#     print(events['location'] + "\nLat: " + events['latitude'] + "\nLong: " +
#           events['longitude'] + "\nMagnitude: " + events['magnitude'] + "\n")

class Events():
    def __init__(self, name, location, lat, long, tsunami, ):
        self.name = name

class MainGUI():
    def __init__(self):

        # self._set_main().CreateTable()
        # self._set_main().LoadTable()
        # self.grid(sticky = (N,S,W,E))
        self.root = tk.Tk()
        self.root.title("QuakeFeed")
        self.window_height = 600
        self.window_width = 300
        self.sidebar_width = 200
        self.main_window_width = 500
        self.side_window_width = 200
        self.side_bg_color = 'white'
        self.main_bg_color = 'white'
        self._set_side()
        # self._set_main()
        self.main_quakes_day = tk.Frame(self.root)
        self.main_quakes_week = tk.Frame(self.root)
        self._show_quakes_week()


    def _set_side(self):
        sidebar = tk.Frame(
            self.root, width=self.side_window_width, bg=self.side_bg_color,
            height=self.window_height, borderwidth=5)
        sidebar.pack(expand=True, fill='both', side='left', anchor='nw')

        lastDay = tk.Button(self.root, text="Last Day", command=self._show_quakes_day)
        lastDay.pack()
        lastDay.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.013)

        lastWeek = tk.Button(self.root, text="Last Week", command=self._show_quakes_week)
        lastWeek.pack()
        lastWeek.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.12)

        exit = tk.Button(self.root, text="Quit", command=quit)
        exit.pack()
        exit.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.333)

    def _show_quakes_week(self):
        self.main_quakes_day.destroy()
        self.main_quakes_day.destroy()
        self.root.update()
        self.root.minsize(self.main_window_width, self.window_height)

        self.main_quakes_day = tk.Frame(self.root, bg=self.main_bg_color,
                                            width=self.main_window_width, height=self.window_height)
        self.main_quakes_day.pack(expand=True, fill='both', side='right')

        # root = Tk()
        QuakeFrame.CreateUI(self.main_quakes_day)
        QuakeFrame.LoadTable(self.main_quakes_day)
        self.root.mainloop()


        # tree.insert('', 'end', 'widgets', text='Widget Tour')
        # tree['columns'] = ('size', 'modified', 'owner')
        # tree.heading('size', width=100, anchor='center')
        #
        # self.root.mainloop()

    def _show_quakes_day(self):
        self.main_quakes_day.destroy()
        self.main_quakes_week.destroy()
        self.root.update()
        self.root.minsize(self.main_window_width, self.window_height)
        self.main_quakes_week = tk.Frame(self.root, bg=self.main_bg_color,
                                            width=self.main_window_width, height=self.window_height)
        self.main_quakes_week.pack(expand=True, fill='both', side='right')
        self.root.mainloop()


class QuakeFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(parent)
        self.CreateUI()
        self.LoadTable()
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight = 1)
        parent.grid_columnconfigure(0, weight = 1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('location', 'magnitude', 'latitude', 'longitude')
        tv.heading('#0', text='Location', anchor='w')
        tv.column('location', anchor='center', width=200)
        tv.heading('#1', text='Magnitude')
        tv.column('magnitude', anchor='center', width=50)
        tv.heading('#2', text='Latitude')
        tv.column('latitude', anchor='center', width=100)
        tv.heading('#3', text='Longitude')
        tv.column('longitude', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self):
        locText = "hello"
        self.treeview.insert('', 'end', text=locText, values=('10:00',
                             '10:10', 'Ok'))
        self.treeview.insert('', 'end', text="Second", values=('10:00',
                             '10:10', 'Ok'))



def start_gui():
    MainGUI().mainloop()

def quit():
    exit()

def main():
    start_gui()

if __name__ == '__main__':
    main()