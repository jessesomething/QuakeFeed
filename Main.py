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
from PIL import Image, ImageTk


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

    def clear_table(self):
        tv.destroy()

    def LoadTable(self, loc, link, mag, coord, tsunami, time_utc, date_utc):
        tv.insert('', 'end', text=loc, values=(link, mag, coord, tsunami, time_utc, date_utc))
        # children = tv.get_children()

        # for child in children:
        #     print(tv.set(child, column="#2"))

class MainGUI():
    def __init__(self):
        self.root = tk.Tk()
        self.tree = ttk.Treeview()
        self.root.title("QuakeFeed")
        self.window_height = 600
        self.window_width = 400
        self.sidebar_width = 181
        self.main_window_width = 800
        self.side_window_width = 200
        self.side_bg_color = 'white'
        self.main_bg_color = 'white'
        self.set_sidebar()
        self.main_quakes_day = ttk.Frame(self.root)
        self.show_quakes()

    def enter(self, event):
        print('Someone pressed enter')


    def set_sidebar(self):
        sidebar = tk.Frame(
            self.root, width=self.side_window_width, bg=self.side_bg_color,
            height=self.window_height, borderwidth=5)
        sidebar.pack(expand=True, fill='both', side='left', anchor='nw')

        # mag_combobox = ttk.Combobox(self.root, values=('this', 'that', 'and the other'))
        # mag_combobox.pack()
        # mag_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.03, rely=.22, )

        # get_link_button = tk.Button(self.root, text="Go to link", command=self.show_quakes)
        # get_link_button.pack()
        # get_link_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=0.3, rely=.24)

        logo_unconv = Image.open("images/usgs.jpg")
        logo = ImageTk.PhotoImage(logo_unconv)

        # refresh_button = tk.Button(self.root, text="Refresh", command=self.show_quakes)
        # refresh_button.pack()
        # refresh_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.01, rely=.013)

        logo_label = Label(self.root, image=logo)
        logo_label.image = logo
        logo_label.pack()
        logo_label.place(bordermode='outside', relx=.01, rely=.013)


        quit_button = tk.Button(self.root, text="Quit", command=quit)
        quit_button.pack()
        quit_button.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.01, rely=.90)

    def show_quakes(self):
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

        def populate_events(filter):
            for i in tv.get_children():
                tv.delete(i)
            tsunami_count = 0
            for q in quakes['features']:
                url = q['properties']['url']
                loc = q['properties']['place']
                mag = q['properties']['mag']
                coord = q['geometry']['coordinates']
                tsunami = q['properties']['tsunami']
                time_epoch = q['properties']['time']
                time_stamp = time_epoch / 1000.0
                time_readable = datetime.fromtimestamp(time_stamp).strftime('%H:%M:%S')
                date_readable = datetime.fromtimestamp(time_stamp).strftime('%d-%m-%Y')

                if tsunami == 0:
                    tsunami = 'No'
                elif tsunami == 1:
                    tsunami = 'Yes'

                loc_split = loc.split(', ')

                try:
                    if country_list.count(loc_split[1]) == 0:
                        country_list.append(loc_split[1])
                    # print(loc_split[1])
                except:
                    break

                if filter == '':
                    QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                                 time_utc=time_readable, date_utc=date_readable)

                if filter == "All Countries/States":
                    QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                                 time_utc=time_readable, date_utc=date_readable)

                if filter == "All Events":
                    QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                                 time_utc=time_readable, date_utc=date_readable)

                try:
                    try:
                        if filter == "Tsunamis Only":
                            if tsunami == 'Yes':
                                tsunami_count = tsunami_count + 1
                                QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                            time_utc=time_readable, date_utc=date_readable)
                        if filter == "Earthquakes Only":
                            if tsunami == 'No':
                                QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                            time_utc=time_readable, date_utc=date_readable)
                    except:
                        print('Something went wrong')
                except:
                    "Nothing chosen"

                try:
                    country = loc_split[1]
                    try:
                        if country == filter:
                            QuakeFrame.LoadTable(self.main_quakes_day, loc=loc, link=url, mag=mag, coord=coord, tsunami=tsunami,
                            time_utc=time_readable, date_utc=date_readable)
                    except:
                        break
                except:
                    break
            if tsunami_count == 0:
                    print('No tsunamis reported.')

        # columns = ()
            country_list.sort()
            if country_list.count('All Countries/States') == 0:
                country_list.insert(0,'All Countries/States')


        def select_location(event):
            location = loc_combobox.get()
            print(loc_combobox.get())
            populate_events(location)

        def select_event_type(event):
            event_type = event_combobox.get()
            print(event_combobox.get())
            populate_events(event_type)

        global locvar
        locvar = StringVar()
        loc_combobox = ttk.Combobox(self.root, textvariable=locvar)
        populate_events(locvar.get())
        loc_combobox.bind('<<ComboboxSelected>>', select_location)
        loc_combobox.pack()
        loc_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.01, rely=.15)
        loc_combobox['values'] = country_list
        loc_combobox.current(0)

        eventvar = StringVar()
        options = ["All Events", "Tsunamis Only", "Earthquakes Only"]
        event_combobox = ttk.Combobox(self.root, textvariable=eventvar, values=options)
        event_combobox.bind('<<ComboboxSelected>>', select_event_type)
        event_combobox.current(0)
        event_combobox.pack()
        event_combobox.place(bordermode='outside', height=50, width=self.sidebar_width, relx=.01, rely=.25)


        self.main_quakes_day.pack(expand=True, fill='both', side='right')
        self.root.mainloop()


    def select_item(self, event):
        item = tv.selection()[0]
        item_url = tv.set(item, column='#1')
        r = requests.get(item_url)
        hazards_url = "http://earthquake.usgs.gov/hazards/products/scenario/"
        r = requests.get(hazards_url)
        data = r.text

        # r = urllib.urlopen('')

        webbrowser.open(item_url)

        # Right here is where I couldn't get the data inside the page source that I wanted
        # They include div classes that it just wouldn't access for some reason.
        # I understand how it works to an extent but it wasn't clear how to get to
        # Inner classes within the html source.

        # soup = BeautifulSoup(data, "html.parser")
        # events = soup.find('a')
        # print(events)
        # soup = BeautifulSoup(urlopen(item_url))A
        # links = soup.find_all('a')
        # for link in links:
        #     print(link.get("href"))
        # print(soup)
        # text = soup.find_all('div class', 'general-text')
        # text = soup.find_all
        # for words in text:
        #     print(words.get("p"))
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
