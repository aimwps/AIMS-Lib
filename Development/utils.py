from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from dateutil import parser
import io, urllib, base64
def prettify_tracker_log_dict(dict):

    pretty_status = {
                    "count_showup":"You showed up!",
                    "count_value":"Still working on it..",
                    "boolean_showup": "You showed up!",
                    "boolean_success": "Great success!!",
                    "fail_or_no_submit":"Did not complete",}

    if dict['tracker'].metric_tracker_type == "boolean":
        if dict['boolean_status'] != None:
            status = pretty_status[dict['boolean_status']]
        else:
            status = "awaiting progress"
        dict_status_pretty = {  "tracker type": "Yes or no",
                                "period starts": dict["period_log_start"],
                                "period ends": dict['period_log_end'],
                                "period status": status,
                                }
    else:
        if dict["tracker"].metric_tracker_type == "maximize":
            tracker_type = "counting up"
        else:
            tracker_type = "counting down"

        if dict['count_status'] != None:
            status = pretty_status[dict['count_status']]
        else:
            status = "awaiting progress"
        dict_status_pretty = {  "tracker type": tracker_type,
                                "period starts": dict["period_log_start"],
                                "period ends": dict['period_log_end'],
                                "period status": status,
                                "logs in period": dict['count_quantity'],
                                "total count": dict['count_status'],
                                }

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

    fig, ax = plt.subplots(figsize=(8, 14))
    calendar_heatmap(ax, dates, data, vmin, vmax)
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)

    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri
#
# def generate_data():
#     df = pd.read_csv("testing_data.csv")
#     dates = [parser.parse(date) for date in list(df['date_time'])]
#     data = list(df['heatmap_value'])
#     return dates, data
### Create an array of the last 6 months days
###
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
    im = ax.imshow(calendar, interpolation='none', cmap='Oranges')
    label_days(ax, dates, i, j, calendar)
    label_months(ax, dates, i, j, calendar)
    ax.figure.colorbar(im, ticks=[0, count_upper//4, count_lower, count_upper ])
    # cbar = fig.colorbar(cax.get_children()[1],ticks=[vmin, vmax*0.25, vmax*0.5, vmax], ax=cax, orientation="horizontal")
    #cbar.ax.set_xticklabels(["Incomplete", "Minimum show", count_lower//2, count_upper//2])

def label_days(ax, dates, i, j, calendar):
    ni, nj = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 7))
    day_of_month[i, j] = [d.day for d in dates]

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j, i, int(day), ha='center', va='center', fontsize=7)

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
    ax.set_yticklabels(labels, rotation=45, fontsize=7)
