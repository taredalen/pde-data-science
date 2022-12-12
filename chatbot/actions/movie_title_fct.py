



def MoviePlotCSV(plot):
    df= pd.read_csv("wiki_movie_plots_deduped.csv", sep=',')
    x = plot.split()
    print(x)
    print(df)
    df_plot=df.loc[df["plot"].str.contains('|'.join(searchfor))]
    print(df)