def df_stats(df, descriptives=True):
    
    import pandas as pd
    from IPython.display import display
    pd.set_option("display.max_columns",200)
    pd.set_option("display.max_rows",200)
    pd.options.display.float_format = '{:,.1f}'.format

    stats = pd.DataFrame(index=list(df))
    stats['DataTypes'] = df.dtypes
    stats['MissingPct'] = df.isnull().sum()/df.shape[0]*100
    stats['NUnique'] = df.nunique().astype(int)
    if descriptives:
        
        stats = stats.merge(
            right=df.describe().T,
            how='left',
            left_index=True,
            right_index=True
        ).drop(['count'],axis=1)
    display(stats.sort_values(by='NUnique'))


def comp_dist(dataframe, feature, color_var, n_bins=50, palette=0):
    
    import plotly as py
    import plotly.figure_factory as ff
    
    # Find unique categories and their colors
    categories = dataframe[color_var].unique().tolist()    
    hist_data = [dataframe[dataframe[color_var]==x][feature].values.tolist() for x in categories]
    colors = ['Vivid_r','Vivid','Set1','D3','Pastel','Alphabet','Bold','Dark2']
    # Calculate bin_size
    min_h, max_h = min(min(hist_data)), max(max(hist_data))
    bin_size = (max_h-min_h)/n_bins
    rug = True if dataframe.shape[0] < 10000 else False

    fig = ff.create_distplot(
        hist_data=hist_data,
        group_labels=categories,
        bin_size=bin_size,
        curve_type='kde',
        colors=getattr(py.express.colors.qualitative,colors[palette]), 
        show_rug=rug
    )
    fig['layout'].update(
        title_text=feature,
        height=400, width=950,
        title=dict(x=0.5, y=0.02),
        margin=dict(l=10, r=0,b=40,t=10)
    )  
    fig.show()
    

def corr_plot(df,target):
    
    import plotly.express as px
    import pandas as pd
    for m in ['pearson','spearman']:
        fig = px.bar(
            data_frame=df.corr(method=m)[target].sort_values(),
            labels={'index':m}
        )
        fig.update_xaxes(tickangle=45,tickfont=dict(size=10))
        fig.show()