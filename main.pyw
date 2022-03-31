import matplotlib
import matplotlib.pyplot as plt
from windrose import WindroseAxes
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.ticker as tck
matplotlib.use("TkAgg")

window = Tk()
main_frame = Frame(window)
main_frame.pack(fill=BOTH, expand=1)
canvas = Canvas(main_frame)
scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)


window.state('zoomed')
window.title("Weather Station Data")
selected_file = Label(scrollable_frame, text="No file selected.", width=50)
global wind_rose, temperature_plot, pressure_plot, humidity_plot, wind_dir_plot, wind_speed_plot,\
    wind_rose_transparent, default_start, default_end, new_lines


def save_windrose():
    windrose_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                 defaultextension='.png', title="Save figure as...")
    if windrose_file:
        wind_rose.savefig(windrose_file)


def save_windrose_transparent():
    windrose_transparent_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                             defaultextension='.png', title="Save figure as...")
    if windrose_transparent_file:
        wind_rose_transparent.savefig(windrose_transparent_file, transparent=True)


def save_temperature_plot():
    temperature_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                    defaultextension='.png', title="Save figure as...")
    if temperature_file:
        temperature_plot.savefig(temperature_file)


def save_pressure_plot():
    pressure_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                 defaultextension='.png', title="Save figure as...")
    if pressure_file:
        pressure_plot.savefig(pressure_file)


def save_humidity_plot():
    humidity_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                 defaultextension='.png', title="Save figure as...")
    if humidity_file:
        humidity_plot.savefig(humidity_file)


def save_wind_dir_plot():
    winddir_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                defaultextension='.png', title="Save figure as...")
    if winddir_file:
        wind_dir_plot.savefig(winddir_file)


def save_wind_speed_plot():
    windspeed_file = filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"), ("All Files", "*.*")),
                                                  defaultextension='.png', title="Save figure as...")
    if windspeed_file:
        wind_speed_plot.savefig(windspeed_file)


def save_all():
    dest = filedialog.askdirectory()
    if dest:
        wind_rose.savefig(dest + '/wind_rose.png')
        wind_rose_transparent.savefig(dest + '/wind_rose_transparent.png', transparent=True)
        temperature_plot.savefig(dest + '/temperature_plot.png')
        humidity_plot.savefig(dest + '/humidity_plot.png')
        pressure_plot.savefig(dest + '/pressure_plot.png')
        wind_speed_plot.savefig(dest + '/wind_speed_plot.png')
        wind_dir_plot.savefig(dest + '/wind_dir_plot.png')


def draw_windrose(lines):
    ws = []
    wd = []
    for line in lines:
        ws.append(float(line[4]))
        wd.append(float(line[7]))
    global wind_rose
    wind_rose = plt.Figure(figsize=(8, 8), dpi=100)
    chart_type = FigureCanvasTkAgg(wind_rose, scrollable_frame)
    chart_type.get_tk_widget().grid(row=1, column=0, rowspan=4, columnspan=2)
    rect = [0.1, 0.1, 0.8, 0.8]
    ax = WindroseAxes(wind_rose, rect)
    wind_rose.add_axes(ax)
    ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax.legend(units='m/s', loc=(-0.1, -0.1))

    global wind_rose_transparent
    wind_rose_transparent = plt.Figure(figsize=(8, 8), dpi=100)
    ax2 = WindroseAxes(wind_rose_transparent, rect)
    wind_rose_transparent.add_axes(ax2)
    ax2.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
    ax2.set_xticklabels(["E", " ", "N-E", " ", "N", " ", "N-W", " ", "W", " ", "S-W", " ", "S", " ", "S-E", " "],
                        fontsize=14, fontweight="bold", color="white")
    for t in ax2.get_yticklabels():
        plt.setp(t, fontsize=10, color='white')
    ax2.spines['polar'].set_color('white')
    ax2.legend(units='m/s', loc=(-0.1, -0.1))


def draw_temperature(lines):
    x = []
    y = []
    for line in lines:
        x.append(line[0][0:-3])
        y.append(float(line[1]))
    global temperature_plot
    temperature_plot = plt.Figure(figsize=(10, 4), dpi=100, tight_layout=True)
    canvas = FigureCanvasTkAgg(temperature_plot, scrollable_frame)
    fig = temperature_plot.add_subplot()
    fig.set(xlabel='Čas [hh:mm]', ylabel='Teplota', title='Teplota v °C')
    fig.set_xlim(left=0, right=len(x)-1)
    fig.tick_params(axis='x', labelrotation=90)
    fig.yaxis.set_major_locator(tck.MaxNLocator(9))
    fig.yaxis.set_minor_locator(tck.AutoMinorLocator())
    fig.xaxis.set_major_locator(tck.MaxNLocator(20))
    fig.set_axisbelow(True)
    fig.yaxis.grid(color='gray', linestyle='dashed')
    fig.xaxis.grid(color='gray', linestyle='dashed')
    fig.plot(x, y, color='red')
    canvas.get_tk_widget().grid(row=1, column=2, sticky=N, rowspan=2, columnspan=8)


def draw_pressure(lines):
    x = []
    y = []
    for line in lines:
        x.append(line[0][0:-3])
        y.append(int(line[3]))
    global pressure_plot
    pressure_plot = plt.Figure(figsize=(10, 4), dpi=100, tight_layout=True)
    canvas = FigureCanvasTkAgg(pressure_plot, scrollable_frame)
    fig = pressure_plot.add_subplot()
    fig.set(xlabel='Čas [hh:mm]', ylabel='Tlak vzduchu', title='Tlak vzduchu v HPa')
    fig.set_ylim(bottom=min(y)-1, top=max(y)+1)
    fig.set_xlim(left=0, right=len(x)-1)
    fig.tick_params(axis='x', labelrotation=90)
    fig.yaxis.set_minor_locator(tck.AutoMinorLocator())
    fig.xaxis.set_major_locator(tck.MaxNLocator(20))
    fig.set_axisbelow(True)
    fig.yaxis.grid(color='gray', linestyle='dashed')
    fig.xaxis.grid(color='gray', linestyle='dashed')
    fig.scatter(x, y, color='green')
    canvas.get_tk_widget().grid(row=3, column=2, rowspan=2, columnspan=8)


def draw_humidity(lines):
    x = []
    y = []
    for line in lines:
        x.append(line[0][0:-3])
        y.append(int(line[2]))
    global humidity_plot
    humidity_plot = plt.Figure(figsize=(10, 4), dpi=100, tight_layout=True)
    canvas = FigureCanvasTkAgg(humidity_plot, scrollable_frame)
    fig = humidity_plot.add_subplot()
    fig.set(xlabel='Čas [hh:mm]', ylabel='Relatívna vlhkosť', title='Relatívna vlhkosť vzduchu v %')
    fig.set_ylim(bottom=min(y), top=max(y)+1)
    fig.set_xlim(left=0, right=len(x)-1)
    fig.tick_params(axis='x', labelrotation=90)
    fig.yaxis.set_minor_locator(tck.AutoMinorLocator())
    fig.xaxis.set_major_locator(tck.MaxNLocator(20))
    fig.set_axisbelow(True)
    fig.yaxis.grid(color='gray', linestyle='dashed')
    fig.xaxis.grid(color='gray', linestyle='dashed')
    fig.plot(x, y)
    canvas.get_tk_widget().grid(row=5, column=2, rowspan=2, columnspan=8)


def draw_wind_dir(lines):
    x = []
    y = []
    for line in lines:
        x.append(line[0][0:-3])
        y.append(int(line[7]))
    global wind_dir_plot
    wind_dir_plot = plt.Figure(figsize=(9, 4), dpi=100, tight_layout=True)
    canvas = FigureCanvasTkAgg(wind_dir_plot, scrollable_frame)
    fig = wind_dir_plot.add_subplot()
    fig.set(xlabel='Čas [hh:mm]', ylabel='Smer vetra', title='Smer vetra v °')
    fig.set_ylim(bottom=0, top=359)
    fig.set_xlim(left=0, right=len(x)-1)
    fig.tick_params(axis='x', labelrotation=90)
    fig.yaxis.set_minor_locator(tck.AutoMinorLocator())
    fig.xaxis.set_major_locator(tck.MaxNLocator(20))
    fig.set_axisbelow(True)
    fig.yaxis.grid(color='gray', linestyle='dashed')
    fig.xaxis.grid(color='gray', linestyle='dashed')
    fig.scatter(x, y)
    canvas.get_tk_widget().grid(row=7, column=0, rowspan=2)


def draw_wind_speed(lines):
    x = []
    y = []
    for line in lines:
        x.append(line[0][0:-3])
        y.append(float(line[4]))
    global wind_speed_plot
    wind_speed_plot = plt.Figure(figsize=(9, 4), dpi=100, tight_layout=True)
    canvas = FigureCanvasTkAgg(wind_speed_plot, scrollable_frame)
    fig = wind_speed_plot.add_subplot()
    fig.set(xlabel='Čas [hh:mm]', ylabel='Rýchlosť vetra', title='Rýchlosť vetra v m/s')
    fig.set_ylim(bottom=min(y), top=max(y)+1)
    fig.set_xlim(left=0, right=len(x)-1)
    fig.tick_params(axis='x', labelrotation=90)
    fig.yaxis.set_minor_locator(tck.AutoMinorLocator())
    fig.xaxis.set_major_locator(tck.MaxNLocator(20))
    fig.set_axisbelow(True)
    fig.yaxis.grid(color='gray', linestyle='dashed')
    fig.xaxis.grid(color='gray', linestyle='dashed')
    fig.plot(x, y, color='purple')
    canvas.get_tk_widget().grid(row=5, column=0, rowspan=2)


def draw_graphs():
    start = default_start.get()
    end = default_end.get()
    for i in range(len(new_lines)):
        if start in new_lines[i][0]:
            start_index = i
        if end in new_lines[i][0]:
            if i == len(new_lines):
                end_index = None
            else:
                end_index = i+1
    draw_windrose(new_lines[start_index:end_index])
    draw_temperature(new_lines[start_index:end_index])
    draw_pressure(new_lines[start_index:end_index])
    draw_humidity(new_lines[start_index:end_index])
    draw_wind_speed(new_lines[start_index:end_index])
    draw_wind_dir(new_lines[start_index:end_index])


def select_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select a file...",
                                          filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    selected_file.configure(text="Selected file: "+filename)
    file = open(filename, 'r')
    lines = file.readlines()
    lines.pop(0)
    global new_lines
    new_lines = []
    times = []
    for line in lines:
        new_line = line.replace(',', '.').split('\t')
        new_line[0] = new_line[0][-8:]
        new_lines.append(new_line)
    for line in new_lines:
        times.append(line[0])
    Label(scrollable_frame, text='Start:').grid(row=0, column=2)
    global default_start
    default_start = StringVar(scrollable_frame)
    default_start.set(times[0])
    global default_end
    default_end = StringVar(scrollable_frame)
    default_end.set(times[-1])
    start_selection = ttk.Combobox(scrollable_frame, textvariable=default_start, values=times)
    start_selection.grid(row=0, column=3)
    Label(scrollable_frame, text='End:').grid(row=0, column=4)
    end_selection = ttk.Combobox(scrollable_frame, textvariable=default_end, values=times)
    end_selection.grid(row=0, column=5)
    Button(scrollable_frame, text="Confirm", command=draw_graphs).grid(row=0, column=6)
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def _on_mouse_wheel(event):
        canvas.yview_scroll(-1 * int((event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))


menu = Menu(window)
window.config(menu=menu, width=60)
file_menu = Menu(menu)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open...', command=select_file)
file_menu.add_command(label='Save WindRose', command=save_windrose)
file_menu.add_command(label='Save WindRose (transparent)', command=save_windrose_transparent)
file_menu.add_command(label='Save Temperature graph', command=save_temperature_plot)
file_menu.add_command(label='Save Pressure graph', command=save_pressure_plot)
file_menu.add_command(label='Save Humidity graph', command=save_humidity_plot)
file_menu.add_command(label='Save Wind Direction graph', command=save_wind_dir_plot)
file_menu.add_command(label='Save Wind Speed graph', command=save_wind_speed_plot)
file_menu.add_command(label='Save all', command=save_all)

# file_menu.add_command(label='Save .xlsx', command=save_xlsx)
# Add option to save a .xlsx file with all graphs and tables

selected_file.grid(row=0, column=0, sticky=NW)
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

window.mainloop()
