from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from dateutil import parser
import io, urllib, base64
import matplotlib.backends.backend_agg as backend
from matplotlib.figure import Figure




def prettify_tracker_status_dict(dict):
    pretty_status = {
                    "period_progressing":"You're still working on it",
                    "period_complete": "You've already submitted this period",
                    "period_not_begun": "This period is not active yet",}
    tracker_types = {'maximize':'Count Up',
                    'minimize': 'Count Down',
                    'boolean': 'Yes or No',
                    }

    dict_status_pretty = {  "tracker type": tracker_types[dict['tracker'].metric_tracker_type],
                            "period starts": dict["next_period_start"].strftime("%d/%m/%y @ %H:%M:%S"),
                            "period ends": dict['next_period_end'].strftime("%d/%m/%y @ %H:%M:%S"),
                            "period status": pretty_status[dict['next_period_status']],
                            }
    if dict['tracker'] != "boolean":
        dict_status_pretty["logs in period"]= dict['next_period_log_counts']
        dict_status_pretty["total count"] = dict['next_period_log_total_value']
    return dict_status_pretty

def get_next_sunday():
    dt = datetime.today()
    while dt.strftime('%A') != "Sunday":
        dt += relativedelta(days=1)
    return dt

def generate_heatmap_from_df(df, vmin, vmax):
    dates = list(df['date_time'])
    data = list(df['heatmap_value'])
    data = [d if isinstance(d, float) else np.nan for d in data]
    fig = Figure(figsize=(7, 10))
    canvas = backend.FigureCanvas(fig)
    ax = fig.add_subplot(111)
    calendar_heatmap(ax, dates, data, vmin, vmax)

    buf = io.BytesIO()
    fig.savefig(buf, bbox_inches='tight',format="png", pad_inches = 0)
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
#
def calendar_array(dates, data):
    i, j = zip(*[d.isocalendar()[1:] for d in dates])
    i = np.array(i) - min(i)
    j = np.array(j) - 1
    ni = max(i) + 1
    calendar = np.nan * np.zeros((ni, 7))
    calendar[i, j] = data

    return i, j, calendar


def calendar_heatmap(ax, dates, data, count_lower, count_upper):
    i, j, calendar = calendar_array(dates, data)
    data_max = np.nanmax(data)
    im = ax.imshow(calendar, interpolation='none', cmap='Oranges', aspect="auto")
    label_days(ax, dates, i, j, calendar)
    label_months(ax, dates, i, j, calendar)
    tick_g = [0, count_upper//4, count_lower, count_upper ]
    ax.figure.colorbar(im, ticks=tick_g)
    # cbar = fig.colorbar(cax.get_children()[1],ticks=[vmin, vmax*0.25, vmax*0.5, vmax], ax=cax, orientation="horizontal")
    #cbar.ax.set_xticklabels(["Incomplete", "Minimum show", count_lower//2, count_upper//2])

def label_days(ax, dates, i, j, calendar):
    ni, nj = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 7))
    day_of_month[i, j] = [d.day for d in dates]

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j, i, int(day), ha='center', va='center', fontsize=10)

    ax.set(xticks=np.arange(7),
           xticklabels=['M', 'T', 'W', 'R', 'F', 'S', 'S'])
    ax.xaxis.tick_top()

def label_months(ax, dates, i, j, calendar):
    month_labels = np.array(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                             'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    months = np.array([d.month for d in dates])
    uniq_months = sorted(set(months))
    yticks = [i[months == m].mean() for m in uniq_months]
    labels = [month_labels[m - 1] for m in uniq_months]
    ax.set(yticks=yticks)
    ax.set_yticklabels(labels, rotation=45, fontsize=10)
