import pandas as pd
import matplotlib.pyplot as plt
import calmap
from datetime import datetime

df = pd.read_csv("31_data.csv")
df['date_time'] = pd.to_datetime(df['create_date'].astype(str) + df['create_time'].astype(str), format = '%Y-%m-%d%H:%M:%S')
print(df.info())
df = df[['date_time', 'count_value']]
df = df.set_index('date_time')

with plt.rc_context({'xtick.color': 'black','ytick.color': 'black'}):
    fig =plt.figure(figsize=(12,3))
    ax = fig.add_subplot(111, aspect="equal")
    fig.set_facecolor('white')
    ax.set_facecolor('white')
    cax = calmap.calendarplot(df['count_value'], cmap='Oranges',vmin=50, vmax=1000, fillcolor='lightgrey',daylabels=['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'],dayticks=[0, 1,2,3,4,5, 6],
                    linewidth=2, ax=ax)
    fig.colorbar(cax.get_children()[1], ax=cax, orientation="horizontal")
    plt.tight_layout()
    plt.show()
    fig.savefig('atest.png')
