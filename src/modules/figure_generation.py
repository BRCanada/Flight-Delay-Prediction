# FIGURE GENERATION MODULE
# This module contains all functions and libraries required for data visualization and figure generation
# All generated figures will be output to the /output/figures directory

import seaborn as sns
import matplotlib.pyplot as plt


#--------2-feature Scatter--
def scatter_plot(df, xinput, yinput, hinput,):
    """
    Function returns a scatter_plot from a dataframe, based on chosen x and y inputs.
    
    df = DataFrame
    xinput = string   (X axis feature)
    yinput = string   (Y axis feature)
    hinput = string   (Hue feature)
    """
    
    x = df[xinput]
    y = df[yinput]
    hue = df[hinput]
    
    sns.scatterplot(data=df, x=xinput, y=yinput, hue=hinput)
    plt.savefig(f'/output/figures/{xinput}_{yinput}_scatter.png')
#---------------------------    

#---------Multi-Histogram---
def multi_hist(df, featurelist):
    """ This Function outputs a multi histogram of a list of chosen features in a dataframe. df = DataFrame
   featurelist = List of features (string) 
   """

                                            
    namestr = ''
    
    fig, axes = plt.subplots(1,len(featurelist), sharey=True, figsize=(10,5))
    fig.suptitle(f'Multi_histogram of {len(featurelist)} features')
    for i in range(0,len(featurelist)):         
        namestr += featurelist[i][0:3]+'_'
        axes[i].set_title(f'{featurelist[i]}')
        sns.histplot(ax=axes[i], x=df[featurelist[i]].values)
        plt.savefig(f'output/figures/{namestr}multi.png')
        
#---------------------------
#------Pie Chart------------

def make_pie(df, data, label):
    """
    This will turn any two features into a pie chart.
    
    df = DataFrame
    data = feature column label <where values are numerical>
    label = feature column label <preferrably categorical>
    """
    colors = sns.color_palette('pastel')[0:len(df[label].unique())]
    
    plt.title(f"{data} by {label}")
    plt.pie(df[data], labels=df[label].unique(), colors = colors, autopct='%.0f%%')
    
    plt.savefig(f'output/figures/{data}by{label}_pie.png')

#----------------------------
#-----Bar Plot---------------

def make_bar(df, xlabel, ylabel):
    """
    This will turn any two labels into a barplot
    
    df = DataFrame
    xlabel = x-axis feature (string)
    ylabel = y-axis feature (string)
    """
    
    sns.barplot(data=df, x=xlabel, y=ylabel).set(title=f'{xlabel} by {ylabel}')
    
    plt.savefig(f'output/figures/{xlabel}_{ylabel}_bar.png')

#------------------------------------
#---------Donut----------------------
def make_donut(df, labels, slices):
    
    """
    Function that takes a dataframe and two feature labels, turning them into a 
    donut chart with a color coded legend.
    
    df = DataFrame
    labels = feature label string (for legend)
    slices = feature label string (for chart items)
    """
    
    label = df[labels]
    sizes = df[slices]
    
    fig1, ax1 = plt.subplots(figsize=(20, 20))
    wedges, texts, autotexts = ax1.pie(sizes, autopct='%1.1f%%', startangle=90)
    
    centre_circle = plt.Circle((0,0),0.60,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    ax1.legend(wedges, label,
              title=f'labels',
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    ax1.axis('equal')         # Equal aspect ratio ensures that pie is drawn as a circle
    plt.tight_layout()
    plt.title(f"{slices} by {labels}")
    plt.show()
    plt.savefig(f'output/figures/{slices}_{labels}_donut.png')
    
#---------------------------------------------
