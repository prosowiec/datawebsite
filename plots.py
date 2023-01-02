import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import base64
from io import BytesIO

def to_html(fig):    
    tmpfile = BytesIO()
    fig.savefig(tmpfile, format='png')
    encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')
    html = '<img class="ui centered image"  src=\'data:image/png;base64,{}\'>'.format(encoded)
    return html

def price_bar(x_year,y_avg_price):
    fig, ax = plt.subplots(figsize=(14,5))
    resct = plt.bar(x_year, y_avg_price)
    ax.set_xlabel('Production year')
    ax.set_ylabel('Price (PLN)')
    ax.set_title('Average price by year')
    ax.set_axisbelow(True)
    plt.grid()
    fig.autofmt_xdate(ha = "center")
    plt.ioff()
    html = to_html(fig)
    return html   

def volume_bar(x_year,volume):
    fig, ax = plt.subplots(figsize=(14,5))
    resct = plt.bar(x_year, volume)
    ax.set_xlabel('Production year')
    ax.set_ylabel('Volume')
    ax.set_title('Volume by production year')
    ax.set_axisbelow(True)

    max_y = volume.max()

    ax.set_ylim([0, max_y + max_y*0.1])
    plt.bar_label(resct,labels=volume, label_type='edge')
    plt.ylim(bottom=0)
    plt.grid()
    fig.autofmt_xdate(ha = "center")
    plt.ioff()
    html = to_html(fig)
    return html   

def mileage_bar(x_year,y_avg_mileage):
    fig, ax = plt.subplots(figsize=(14,5))
    resct = plt.bar(x_year, y_avg_mileage)
    ax.set_xlabel('Production year')
    ax.set_ylabel('Price (PLN)')
    ax.set_title('Average mileage by year')
    ax.set_axisbelow(True)
    plt.grid()
    plt.ioff()
    fig.autofmt_xdate(ha = "center")
    html = to_html(fig)
    return html

def price_and_mileage_bar(x_year,y_avg_price,y_avg_mileage):
    fig, ax = plt.subplots(figsize=(14,5))
    width = 0.35
    x = np.arange(len(x_year))
    ax2=ax.twinx()

    rects1 = ax.bar(x - width/2, y_avg_mileage, width, label='Mileage', color = 'tab:blue')
    rects2 = ax2.bar(x + width/2, y_avg_price, width, label='Price',color="orange")

    ax.set_title('Average price and mileage')
    ax.set_xticks(x, x_year)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(True)
    ax.set_axisbelow(True)
    fig.autofmt_xdate(ha = "center") 
    plt.ioff()
    html = to_html(fig)
    return html

def legend_without_duplicate_labels(ax,loc_):
    handles, labels = ax.get_legend_handles_labels()
    unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
    ax.legend(*zip(*unique),loc = loc_,bbox_to_anchor=(0, 1.0, 1, 0.1))

def price_and_mileage_plot(x_year,y_avg_price,y_avg_mileage):
    fig, ax = plt.subplots(figsize=(14,5))
    x = np.arange(len(x_year))
    width = 0.35
    ax2=ax.twinx()

    line1 = ax.plot(x , y_avg_mileage,'o-', width, label='Mileage',color="tab:blue")
    line2 = ax2.plot(x , y_avg_price,'o-', width, label='Price' ,color="orange")

    ax.set_title('Average price and mileage')
    ax.set_xticks(x, x_year)
    legend_without_duplicate_labels(ax,'upper left')
    legend_without_duplicate_labels(ax2,'upper right')
    plt.grid()
    fig.tight_layout()
    plt.ioff()
    fig.autofmt_xdate(ha = "center")   
    html = to_html(fig)
    return html

def price_and_mileage_plot(x_year,y_avg_price,y_avg_mileage):
    fig, ax = plt.subplots(figsize=(14,5))
    x = np.arange(len(x_year))
    width = 0.35
    ax2=ax.twinx()

    line1 = ax.plot(x , y_avg_mileage,'o-', width, label='Mileage',color="tab:blue")
    line2 = ax2.plot(x , y_avg_price,'o-', width, label='Price' ,color="orange")

    ax.set_title('Average price and mileage')
    ax.set_xticks(x, x_year)
    legend_without_duplicate_labels(ax,'upper left')
    legend_without_duplicate_labels(ax2,'upper right')
    plt.grid()
    fig.tight_layout()
    plt.ioff()
    fig.autofmt_xdate(ha = "center")   
    html = to_html(fig)
    return html



def compare_price(oto_x_year,auto_x_year,oto_y_avg_price,auto_y_avg_price):
    fig, ax = plt.subplots(figsize=(14,5), sharex=True, sharey=True)
    x_oto = np.arange(len(oto_x_year))
    x_auto = np.arange(len(auto_x_year))
    width = 0.35
    ax2=ax.twinx()
    y_max = max(oto_y_avg_price.max(),auto_y_avg_price.max())


    line1 = ax.plot(x_oto , oto_y_avg_price,'o-', width, label='OTOMOTO',color="tab:blue")
    line2 = ax2.plot(x_auto , auto_y_avg_price,'o-', width, label='AUTOSCOUT' ,color="orange")

    ax.set_title('Average price')
    ax.set_ylabel('Price (PLN)')
    ax.set_xticks(x_auto, auto_x_year)

    ax.set_ylim([0, y_max + 0.1*y_max])
    ax2.set_ylim([0, y_max + 0.1*y_max])

    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    legend_without_duplicate_labels(ax,'upper left')
    legend_without_duplicate_labels(ax2,'upper right')
    plt.grid()
    fig.tight_layout()
    plt.ioff()
    fig.autofmt_xdate(ha = "center")   
    html = to_html(fig)
    return html




def compare_mileage(oto_x_year,auto_x_year,oto_y_avg_mileage,auto_y_avg_mileage):
    fig, ax = plt.subplots(figsize=(14,5), sharex=True, sharey=True)
    x_oto = np.arange(len(oto_x_year))
    x_auto = np.arange(len(auto_x_year))
    width = 0.35
    ax2=ax.twinx()
    y_max = max(auto_y_avg_mileage.max(),oto_y_avg_mileage.max())

    line1 = ax.plot(x_oto , oto_y_avg_mileage,'o-', width, label='OTOMOTO',color="tab:blue")
    line2 = ax2.plot(x_auto , auto_y_avg_mileage,'o-', width, label='AUTOSCOUT' ,color="orange")

    ax.set_title('Average mileage')
    ax.set_ylabel('Mileage (km)')
    ax.set_xticks(x_auto, auto_x_year)

    ax.set_ylim([0, y_max + 0.1*y_max])
    ax2.set_ylim([0, y_max + 0.1*y_max])

    plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
    legend_without_duplicate_labels(ax,'upper left')
    legend_without_duplicate_labels(ax2,'upper right')
    plt.grid()
    fig.tight_layout()
    plt.ioff()
    fig.autofmt_xdate(ha = "center")   
    html = to_html(fig)
    return html