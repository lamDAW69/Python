import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar y limpiar los datos
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
q_low = df['value'].quantile(0.025)
q_high = df['value'].quantile(0.975)
df = df[(df['value'] >= q_low) & (df['value'] <= q_high)]

def draw_line_plot():
    df_copy = df.copy()
    plt.figure(figsize=(12, 6))
    plt.plot(df_copy.index, df_copy['value'], color='steelblue', linewidth=1.5)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.savefig('line_plot.png')
    plt.show()

def draw_bar_plot():
    df_copy = df.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month
    monthly_avg = df_copy.groupby(['year', 'month'])['value'].mean().unstack()
    plt.figure(figsize=(12, 6))
    monthly_avg.plot(kind='bar', ax=plt.gca())
    plt.title('Average Daily Page Views per Month')
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months', labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.savefig('bar_plot.png')
    plt.show()

def draw_box_plot():
    df_copy = df.copy()
    df_copy['year'] = df_copy.index.year
    df_copy['month'] = df_copy.index.month
    plt.figure(figsize=(14, 6))
    plt.subplot(1, 2, 1)
    sns.boxplot(x='year', y='value', data=df_copy)
    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')
    plt.subplot(1, 2, 2)
    sns.boxplot(x='month', y='value', data=df_copy)
    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    plt.xticks(ticks=range(12), labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.tight_layout()
    plt.savefig('box_plot.png')
    plt.show()
