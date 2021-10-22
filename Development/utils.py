from datetime import datetime
from dateutil.relativedelta import relativedelta

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







def main():
    dates, data = generate_data()
    fig, ax = plt.subplots(figsize=(6, 10))
    calendar_heatmap(ax, dates, data)
    plt.show()

def generate_data():
    num = 100
    data = np.random.randint(0, 20, num)
    start = dt.datetime(2015, 3, 13)
    dates = [start + dt.timedelta(days=i) for i in range(num)]
    return dates, data
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


def calendar_heatmap(ax, dates, data):
    i, j, calendar = calendar_array(dates, data)
    im = ax.imshow(calendar, interpolation='none', cmap='summer')
    label_days(ax, dates, i, j, calendar)
    label_months(ax, dates, i, j, calendar)
    ax.figure.colorbar(im)

def label_days(ax, dates, i, j, calendar):
    ni, nj = calendar.shape
    day_of_month = np.nan * np.zeros((ni, 7))
    day_of_month[i, j] = [d.day for d in dates]

    for (i, j), day in np.ndenumerate(day_of_month):
        if np.isfinite(day):
            ax.text(j, i, int(day), ha='center', va='center')

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
    ax.set_yticklabels(labels, rotation=90)
