import json
import bs4
import requests
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import time
from datetime import datetime
import webbrowser

eventList = []


# url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
# r = requests.get(url)
# data = r.text
# quakes = json.loads(data)
#
# for q in quakes['features']:
#     QuakeFrame.LoadTable(self.main_quakes_day,lat=)
#     print(q['properties']['mag'])



# print(quakes['features'])

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

# class Events():
#     def __init__(self, name, location, lat, long, tsunami, ):
#         self.name = name


class MainGUI():
    def __init__(self):
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
        self.main_quakes_day = tk.Frame(self.root)
        self.main_quakes_week = tk.Frame(self.root)
        self._show_quakes_week()

    def _set_side(self):
        sidebar = tk.Frame(
            self.root, width=self.side_window_width, bg=self.side_bg_color,
            height=self.window_height, borderwidth=5)
        sidebar.pack(expand=True, fill='both', side='left', anchor='nw')

        last_day_button = tk.Button(self.root, text="Last Day", command=self._show_quakes_day)
        last_day_button.pack()
        last_day_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.013)

        last_week_button = tk.Button(self.root, text="Last Week", command=self._show_quakes_week)
        last_week_button.pack()
        last_week_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.12)

        mag_combobox = ttk.Combobox(self.root, values=('this', 'that', 'and the other'))
        mag_combobox.pack()
        mag_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.22,)


        # get_link_button = tk.Button(self.root, text="Go to link", command=self._show_quakes_day)
        # get_link_button.pack()
        # get_link_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=0.3, rely=.24)

        quit_button = tk.Button(self.root, text="Quit", command=quit)
        quit_button.pack()
        quit_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.333)

    def _show_quakes_week(self):
        self.main_quakes_day.destroy()
        self.main_quakes_day.destroy()
        self.root.update()
        self.root.minsize(self.main_window_width, self.window_height)

        # get_link = tk.Button(self.root, text="Get link")
        # get_link.pack()
        # get_link.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.22)

        self.main_quakes_day = tk.Frame(self.root, bg=self.main_bg_color,
                                        width=self.main_window_width, height=self.window_height)
        self.main_quakes_day.pack(expand=True, fill='both', side='right')

        get_link_button = tk.Button(self.root, text="Go to link", command=self.get_info)
        get_link_button.pack()
        get_link_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=0.3, rely=.24)

        # root = Tk()
        QuakeFrame.CreateUI(self.main_quakes_day)
        url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
        r = requests.get(url)
        data = r.text
        quakes = json.loads(data)

        for q in quakes['features']:
            print(q)
            url = q['properties']['url']
            loc = q['properties']['place']
            mag = q['properties']['mag']
            coord = q['geometry']['coordinates']
            tsunami = q['properties']['tsunami']
            time_epoch = q['properties']['time']
            time_stamp = time_epoch / 1000.0
            time_readable = datetime.fromtimestamp(time_stamp).strftime('%H:%M:%S')
            date_readable = datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y')

            print(time_readable)
            if tsunami == 0:
                tsunami = 'No'
            elif tsunami == 1:
                tsunami = 'Yes'

            QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                                 time_utc=time_readable, date_utc=date_readable)
            # print(q['properties']['mag'])





        def print_something():
            print('something')

        print_something()



        self.root.mainloop()

        # tree.insert('', 'end', 'widgets', text='Widget Tour')
        # tree['columns'] = ('size', 'modified', 'owner')
        # tree.heading('size', width=100, anchor='center')
        #
        # self.root.mainloop()

    def get_info(self):
        tv = Treeview()
        children = tv.get_children()
        for child in children:
            print(tv.set(child))

    def _show_quakes_day(self):
        self.main_quakes_day.destroy()
        self.main_quakes_week.destroy()
        self.root.update()
        self.root.minsize(self.main_window_width, self.window_height)
        self.main_quakes_week = tk.Frame(self.root, bg=self.main_bg_color,
                                         width=self.main_window_width, height=self.window_height)
        self.main_quakes_week.pack(expand=True, fill='both', side='right')
        QuakeFrame.CreateUI(self.main_quakes_day)
        # QuakeFrame.LoadTable(self.main_quakes_day)
        self.root.mainloop()


class QuakeFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(parent)
        # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
        # r = requests.get(url)
        # data = r.text
        # quakes = json.loads(data)
        #
        # for q in quakes['features']:
        #     print(q['properties']['mag'])
        self.CreateUI()
        # self.LoadTable(loc=0,mag=0,coord=0)
        self.grid(sticky=(N, S, W, E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('location', 'link', 'magnitude', 'coordinates', 'tsunami', 'time')
        tv.heading('#0', text='Location', anchor='w')
        tv.column('location', anchor='center', width=100)
        tv.heading('#1', text='Link')
        tv.column('link', anchor='center', width=75)
        tv.heading('#2', text='Magnitude')
        tv.column('magnitude', anchor='center', width=150)
        tv.heading('#3', text='Coordinates')
        tv.column('coordinates', anchor='center', width=55)
        tv.heading('#4', text='Tsunami')
        tv.column('tsunami', anchor='center', width=50)
        tv.heading('#5', text='Time')
        tv.column('time', anchor='center', width=100)
        tv.heading('#6', text='Date')
        tv.grid(sticky=(N, S, W, E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def LoadTable(self, loc, link, mag, coord, tsunami, time_utc, date_utc):
        self.treeview.insert('', 'end', text=loc, values=(link, mag, coord, tsunami, time_utc, date_utc))
        # tv = self.treeview
        # children = tv.get_children()
        # for child in children:
        #     print(tv.set(child, column="#3"))

    #
    # def get_focus(self):
    #     self.treeview.focus_get()



def start_gui():
    MainGUI().mainloop()


def quit():
    exit()


def main():
    start_gui()


if __name__ == '__main__':
    main()
