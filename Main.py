import json
import bs4
import urllib3 as urllib
import requests
import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from datetime import datetime
import webbrowser
from bs4 import BeautifulSoup


class QuakeFrame(Frame):
    def __init__(self, parent):
        Frame.__init__(parent)
        self.root = tk.Tk()
        self.tree = ttk.Treeview()
        self.tree.pack()
        self.CreateUI()
        self.grid(sticky=(N, S, W, E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def CreateUI(self):
        global tv
        tv = ttk.Treeview(self)
        tv['columns'] = ('location', 'link', 'magnitude', 'coordinates', 'tsunami', 'time')
        tv.heading('#0', text='Location', anchor='w')
        tv.column('location', anchor='center', width=100)
        tv.heading('#1', text='Link')
        tv.column('link', anchor='center', width=75)
        tv.heading('#2', text='Magnitude')
        tv.column('magnitude', anchor='center', width=100)
        tv.heading('#3', text='Coordinates')
        tv.column('coordinates', anchor='center', width=55)
        tv.heading('#4', text='Tsunami')
        tv.column('tsunami', anchor='center', width=50)
        tv.heading('#5', text='Time')
        tv.column('time', anchor='center', width=100)
        tv.heading('#6', text='Date')
        tv.grid(sticky=(N, S, W, E))
        # self.tv = tv
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def LoadTable(self, loc, link, mag, coord, tsunami, time_utc, date_utc):
        tv.insert('', 'end', text=loc, values=(link, mag, coord, tsunami, time_utc, date_utc))
        children = tv.get_children()

        # for child in children:
        #     print(tv.set(child, column="#2"))

    def on_click(self, event):
        item = self.tree.selection()[0]
        print("you clicked on ", self.tree.item(item, "text"))

class MainGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.tree = ttk.Treeview()
        self.root.title("QuakeFeed")
        self.window_height = 600
        self.window_width = 400
        self.sidebar_width = 200
        self.main_window_width = 1000
        self.side_window_width = 200
        self.side_bg_color = 'white'
        self.main_bg_color = 'white'
        self._set_side()
        self.main_quakes_day = ttk.Frame(self.root)
        self.main_quakes_week = tk.Frame(self.root)
        self._show_quakes_week()

    def enter(self, event):
        print('Someone pressed enter')

    def motion(self, event):
        print('Mouse is at: %s %s' % (event.x, event.y))
        #
        # def OnClick(self, event):
        #     item = self.main_quakes_day.identify('item', event.y)
        #     print('you clicked on', self.main_quakes_day.item(item, 'text'))
        children = tv.get_children()

        for child in children:
            print(tv.set(child, column="#0"))

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

        # mag_combobox = ttk.Combobox(self.root, values=('this', 'that', 'and the other'))
        # mag_combobox.pack()
        # mag_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.22, )

        # get_link_button = tk.Button(self.root, text="Go to link", command=self._show_quakes_day)
        # get_link_button.pack()
        # get_link_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=0.3, rely=.24)

        quit_button = tk.Button(self.root, text="Quit", command=quit)
        quit_button.pack()
        quit_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.333)

    def select_location(self, event):
        print()

    def _show_quakes_week(self):
        self.main_quakes_week.destroy()
        self.main_quakes_day.destroy()
        self.root.update()
        self.root.bind('<Double-Button-1>', self.select_item)
        self.root.minsize(self.main_window_width, self.window_height)
        self.main_quakes_day = tk.Frame(self.root, bg=self.main_bg_color,
                                        width=self.main_window_width, height=self.window_height)


        QuakeFrame.CreateUI(self.main_quakes_day)
        url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        # url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

        r = requests.get(url)
        data = r.text
        quakes = json.loads(data)

        global country_list
        country_list = []
        # country_list.append('Choose a country/state')

        for q in quakes['features']:
            # print(q)
            url = q['properties']['url']
            loc = q['properties']['place']
            mag = q['properties']['mag']
            coord = q['geometry']['coordinates']
            tsunami = q['properties']['tsunami']
            time_epoch = q['properties']['time']
            time_stamp = time_epoch / 1000.0
            time_readable = datetime.fromtimestamp(time_stamp).strftime('%H:%M:%S')
            date_readable = datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y')

            locStr = loc
            # print(loc)
            loc_split = loc.split(', ')
            try:
                if country_list.count(loc_split[1]) == 0:
                    country_list.append(loc_split[1])
                # print(loc_split[1])
            except:
                print('no more here')
            # print(loc_split)
            # country_state = loc_split[', ']
            # print(country_state)
            # country_list.append(country_state)
            if tsunami == 0:
                tsunami = 'No'
            elif tsunami == 1:
                tsunami = 'Yes'



            QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                                 time_utc=time_readable, date_utc=date_readable)

        for country in country_list:
            print(country)

        country_list.sort()

        print(country_list)

        country_list.insert(0,'Choose a Country/State')

        locvar = StringVar()
        global locvar
        loc_combobox = ttk.Combobox(self.root, textvariable=locvar)
        loc_combobox.bind('<<ComboboxSelected>>', print(locvar))
        loc_combobox.pack()
        loc_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.22)
        loc_combobox['values'] = country_list




        # print(loc_combobox.current(2))
        loc_combobox.current(0)

        self.main_quakes_day.pack(expand=True, fill='both', side='right')

        self.root.mainloop()



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

    def select_item(self, event):
        item = tv.selection()[0]
        item_url = tv.set(item, column='#1')
        r = requests.get(item_url)
        data = r.text

        # r = urllib.urlopen('')

        # webbrowser.open(item_url)
        soup = BeautifulSoup(data, "html.parser")
        # events = soup.find('a')
        # print(events)
        # soup = BeautifulSoup(urlopen(item_url))A
        # links = soup.find_all('a')
        # for link in links:
        #     print(link.get("href"))
        # print(soup)
        # tables = soup.find_all('footer class', class_='site-commonav')
        # print(tables)
        # print(soup.prettify()[0:5000])



        # for child in children:
        #     print(tv.set(child, column="#2"))
        print('You clicked on', tv.item(item, 'text'))


def start_gui():
    MainGUI().mainloop()


def quit():
    exit()


def main():
    start_gui()


if __name__ == '__main__':
    main()
