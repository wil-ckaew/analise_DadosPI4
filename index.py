import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# import from folders/theme changer
from app import *
from dash_bootstrap_templates import ThemeSwitchAIO


# ========== Styles ============ #
tab_card = {'height': '100%'}

main_config = {
    "hovermode": "x unified",
    "legend": {"yanchor":"top", 
                "y":0.9, 
                "xanchor":"left",
                "x":0.1,
                "title": {"text": None},
                "font" :{"color":"white"},
                "bgcolor": "rgba(0,0,0,0.5)"},
    "margin": {"l":10, "r":10, "t":10, "b":10}
}

config_graph={"displayModeBar": False, "showTips": False}

template_theme1 = "flatly"
template_theme2 = "darkly"
url_theme1 = dbc.themes.FLATLY
url_theme2 = dbc.themes.DARKLY


# ===== Reading n cleaning File ====== #
B_Dados = pd.read_csv('dengue_campinas.csv')
B_Dados_cru = B_Dados.copy()

# Meses em numeros para poupar memória
B_Dados.loc[ B_Dados['mês'] == 'Jan', 'mês'] = 1
B_Dados.loc[ B_Dados['mês'] == 'Fev', 'mês'] = 2
B_Dados.loc[ B_Dados['mês'] == 'Mar', 'mês'] = 3
B_Dados.loc[ B_Dados['mês'] == 'Abr', 'mês'] = 4
B_Dados.loc[ B_Dados['mês'] == 'Mai', 'mês'] = 5
B_Dados.loc[ B_Dados['mês'] == 'Jun', 'mês'] = 6
B_Dados.loc[ B_Dados['mês'] == 'Jul', 'mês'] = 7
B_Dados.loc[ B_Dados['mês'] == 'Ago', 'mês'] = 8
B_Dados.loc[ B_Dados['mês'] == 'Set', 'mês'] = 9
B_Dados.loc[ B_Dados['mês'] == 'Out', 'mês'] = 10
B_Dados.loc[ B_Dados['mês'] == 'Nov', 'mês'] = 11
B_Dados.loc[ B_Dados['mês'] == 'Dez', 'mês'] = 12

# Algumas limpezas
#B_Dados['Valor Pago'] = B_Dados['Valor Pago'].str.lstrip('R$ ')
#B_Dados.loc[B_Dados['Status de Pagamento'] == 'Pago', 'Status de Pagamento'] = 1
#B_Dados.loc[B_Dados['Status de Pagamento'] == 'Não pago', 'Status de Pagamento'] = 0

# Transformando em int tudo que der
B_Dados['casos-confirmados'] = B_Dados['casos-confirmados'].astype(int)
B_Dados['dia'] = B_Dados['dia'].astype(int)
B_Dados['mês'] = B_Dados['mês'].astype(int)
B_Dados['temperatura-mininima'] = B_Dados['temperatura-mininima'].astype(int)
B_Dados['temperatura-mininima'] = B_Dados['temperatura-mininima'].astype(int)


# Criando opções pros filtros que virão
options_month = [{'label': 'Ano todo', 'value': 0}]
for i, j in zip(B_Dados_cru['mês'].unique(), B_Dados['mês'].unique()):
    options_month.append({'label': i, 'value': j})
options_month = sorted(options_month, key=lambda x: x['value']) 

options_team = [{'label': 'Todos os Casos', 'value': 0}]
for i in B_Dados['casos-confirmados'].unique():
    options_team.append({'label': i, 'value': i})
# ========= Função dos Filtros ========= #
def month_filter(month):
    if month == 0:
        mask = B_Dados['mês'].isin(B_Dados['mês'].unique())
    else:
        mask = B_Dados['mês'].isin([month])
    return mask

def team_filter(team):
    if team == 0:
        mask = B_Dados['casos-confirmados'].isin(B_Dados['casos-confirmados'].unique())
    else:
        mask = B_Dados['casos-confirmados'].isin([team])
    return mask

def convert_to_text(month):
    match month:
        case 0:
            x = 'Ano Todo'
        case 1:
            x = 'Janeiro'
        case 2:
            x = 'Fevereiro'
        case 3:
            x = 'Março'
        case 4:
            x = 'Abril'
        case 5:
            x = 'Maio'
        case 6:
            x = 'Junho'
        case 7:
            x = 'Julho'
        case 8:
            x = 'Agosto'
        case 9:
            x = 'Setembro'
        case 10:
            x = 'Outubro'
        case 11:
            x = 'Novembro'
        case 12:
            x = 'Dezembro'
    return x


# =========  Layout  =========== #
app.layout = dbc.Container(children=[
    # Armazenamento de dataset
    # dcc.Store(id='dataset', data=df_store),

    # Layout
    # Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([  
                            html.Legend("Analise de Dados")
                        ], sm=8),
                        dbc.Col([        
                            html.I(className='fa fa-eercast', style={'font-size': '300%'})
                        ], sm=4, align="center")
                    ]),
                    dbc.Row([
                        dbc.Col([
                            ThemeSwitchAIO(aio_id="theme", themes=[url_theme1, url_theme2]),
                            html.Legend("Projeto Integrador 4")
                        ])
                    ], style={'margin-top': '10px'}),
                    dbc.Row([
                        dbc.Button("Visite o Site", href="https://github.com/wil-ckaew", target="_blank")
                    ], style={'margin-top': '10px'})
                ])
            ], style=tab_card)
        ], sm=4, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col(
                            html.Legend('Total de chuvas por casos de dengue')
                        )
                    ),
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='graph1', className='dbc', config=config_graph)
                        ], sm=12, md=7),
                        dbc.Col([
                            dcc.Graph(id='graph2', className='dbc', config=config_graph)
                        ], sm=12, lg=5)
                    ])
                ])
            ], style=tab_card)
        ], sm=12, lg=7),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.Row(
                        dbc.Col([
                            html.H5('Escolha o Mês'),
                            dbc.RadioItems(
                                id="radio-month",
                                options=options_month,
                                value=0,
                                inline=True,
                                labelCheckedClassName="text-success",
                                inputCheckedClassName="border border-success bg-success",
                            ),
                            html.Div(id='month-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                        ])
                    )
                ])
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),

    # Row 2
    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph3', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph4', className='dbc', config=config_graph)
                        ])
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph5', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dcc.Graph(id='graph6', className='dbc', config=config_graph)    
                        ])
                    ], style=tab_card)
                ], sm=6)
            ], className='g-2'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        html.H4('Grafico 7 teste>>>>>>>>>>>>'),
                        dcc.Graph(id='graph7', className='dbc', config=config_graph)
                    ], style=tab_card)
                ])
            ], className='g-2 my-auto', style={'margin-top': '7px'})
        ], sm=12, lg=4),
        dbc.Col([
            dbc.Card([
                html.H4('Grafico 8 teste>>>>>>>>>>>>'),
                dcc.Graph(id='graph8', className='dbc', config=config_graph)
            ], style=tab_card)
        ], sm=12, lg=3)
    ], className='g-2 my-auto', style={'margin-top': '7px'}),
    
    # Row 3
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4('Grafico 9 Temperatura Media'),
                    dcc.Graph(id='graph9', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Grafico 10 Temperatura media por mês"),
                    dcc.Graph(id='graph10', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=5),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='graph11', className='dbc', config=config_graph)
                ])
            ], style=tab_card)
        ], sm=12, lg=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5('Escolha a Caso confirmado'),
                    dbc.RadioItems(
                        id="radio-team",
                        options=options_team,
                        value=0,
                        inline=True,
                        labelCheckedClassName="text-warning",
                        inputCheckedClassName="border border-warning bg-warning",
                    ),
                    html.Div(id='team-select', style={'text-align': 'center', 'margin-top': '30px'}, className='dbc')
                ])
            ], style=tab_card)
        ], sm=12, lg=2),
    ], className='g-2 my-auto', style={'margin-top': '7px'}),


    
], fluid=True, style={'height': '100vh'})


# ======== Callbacks ========== #
# Graph 1 and 2
@app.callback(
    Output('graph1', 'figure'),
    Output('graph2', 'figure'),
    Output('month-select', 'children'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph1(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B1_Dados = B_Dados.loc[mask]

    #B1_Dados = B1_Dados.groupby(['casos-confirmados', 'mês'])['chuva'].sum()
    # B1_Dados = # analise por caso Dengue
    B1_Dados = B_Dados.groupby( by=['mês'] ).sum().reset_index()[['mês', 'casos-confirmados']].sort_values( 'casos-confirmados', ascending=False )
    #Analise_03.head()

  

    B2_Dados = B_Dados.groupby('mês')['casos-confirmados'].sum().reset_index()

    fig2 = go.Figure(go.Scatter(
        x=B2_Dados['mês'], 
        y=B2_Dados['casos-confirmados'], 
        mode='lines', fill='tonexty')
        )
    fig1 = go.Figure(go.Bar(x=B1_Dados['mês'], y=B1_Dados['casos-confirmados'], textposition='auto', text=B1_Dados['mês']))
    fig1.update_layout(main_config, height=200, template=template)
    fig2.update_layout(main_config, height=200, template=template, showlegend=False)

    select = html.H1(convert_to_text(month))

    return fig1, fig2, select

# Graph 3
@app.callback(
    Output('graph3', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph3(team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = team_filter(team)
    B3_Dados = B_Dados.loc[mask]

    B3_Dados = B3_Dados.groupby('ano')['casos-confirmados'].sum().reset_index()
    fig3 = go.Figure(go.Scatter(
    x=B3_Dados['ano'], y=B3_Dados['casos-confirmados'], mode='lines', fill='tonexty'))
    fig3.add_annotation(text='Grafico 3 Casos confirmados de Médias por Ano',
        xref="paper", yref="paper",
        font=dict(
            size=17,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig3.add_annotation(text=f"Média : {round(B3_Dados['casos-confirmados'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig3.update_layout(main_config, height=180, template=template)
    return fig3

# Graph 4
@app.callback(
    Output('graph4', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph4(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    B4_Dados = B_Dados.loc[mask]

    B4_Dados = B4_Dados.groupby('mês')['casos-confirmados'].sum().reset_index()
    fig4 = go.Figure(go.Scatter(x=B4_Dados['mês'], y=B4_Dados['casos-confirmados'], mode='lines', fill='tonexty'))

    fig4.add_annotation(text='Grafico 4 Casos confirmados Médias por Mês',
        xref="paper", yref="paper",
        font=dict(
            size=15,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.85, showarrow=False)
    fig4.add_annotation(text=f"Média : {round(B4_Dados['casos-confirmados'].mean(), 2)}",
        xref="paper", yref="paper",
        font=dict(
            size=20,
            color='gray'
            ),
        align="center", bgcolor="rgba(0,0,0,0.8)",
        x=0.05, y=0.55, showarrow=False)

    fig4.update_layout(main_config, height=180, template=template)
    return fig4

# Indicators 1 and 2 ------ Graph 5 and 6
@app.callback(
    Output('graph5', 'figure'),
    Output('graph6', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph5(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B5_Dados = B6_Dados = B_Dados.loc[mask]
    
    B5_Dados = B5_Dados.groupby(['mês', 'casos-confirmados'])['chuva'].sum()
    B5_Dados.sort_values(ascending=False, inplace=True)
    B5_Dados = B5_Dados.reset_index()
    fig5 = go.Figure()
    fig5.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span>{B5_Dados['mês'].iloc[0]} - Grafico 5 </span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = B5_Dados['chuva'].iloc[0],
        number = {'prefix': ""},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': B5_Dados['chuva'].mean()}
    ))

    B6_Dados = B6_Dados.groupby('casos-confirmados')['chuva'].sum()
    B6_Dados.sort_values(ascending=False, inplace=True)
    B6_Dados = B6_Dados.reset_index()
    fig6 = go.Figure()
    fig6.add_trace(go.Indicator(mode='number+delta',
        title = {"text": f"<span>{B6_Dados['casos-confirmados'].iloc[0]} - TGrafico 5 ou 6</span><br><span style='font-size:70%'>Em vendas - em relação a média</span><br>"},
        value = B6_Dados['chuva'].iloc[0],
        number = {'prefix': ""},
        delta = {'relative': True, 'valueformat': '.1%', 'reference': B6_Dados['chuva'].mean()}
    ))

    fig5.update_layout(main_config, height=200, template=template)
    fig6.update_layout(main_config, height=200, template=template)
    fig5.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    fig6.update_layout({"margin": {"l":0, "r":0, "t":20, "b":0}})
    return fig5, fig6

# Graph 7
@app.callback(
  Output('graph7', 'figure'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph7(toggle):
    template = template_theme1 if toggle else template_theme2

    B7_Dados = B_Dados.groupby('temperatura-mininima')['temperatura-maxima'].sum()
    #B7_Dados_group = B7_Dados.groupby('mês')['chuva'].sum().reset_index()
    
    #fig7 = px.line(B7_Dados, y="chuva", x="mês", color="casos-confirmados")
   # fig7.add_trace(go.Scatter(y=B7_Dados_group["chuva"], x=B7_Dados_group["mês"], mode='lines+markers', fill='tonexty', name='total casos grafico 7'))
    fig7 = go.Figure()
    fig7.add_trace(go.Pie(labels=['temperatura-maxima', 'temperatura-mininima'], values=B7_Dados, hole=.6))
    


    fig7.update_layout(main_config, yaxis={'title': None}, xaxis={'title': None}, height=190, template=template)
    fig7.update_layout({"legend": {"yanchor": "top", "y":0.99, "font" : {"color":"white", 'size': 10}}})
    return fig7

# Graph 8
@app.callback(
    Output('graph8', 'figure'),
    Input('radio-month', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph8(month, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B8_Dados = B_Dados.loc[mask]

    B8_Dados = B8_Dados.groupby('casos-confirmados')['chuva'].sum().reset_index()
    fig8 = go.Figure(go.Bar(
        x=B8_Dados['chuva'],
        y=B8_Dados['casos-confirmados'],
        orientation='h',
        textposition='auto',
        text=B8_Dados['chuva'],
        insidetextfont=dict(family='Times', size=12)))

    fig8.update_layout(main_config, height=360, template=template)
    return fig8

# Graph 9
@app.callback(
    Output('graph9', 'figure'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph9(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    B9_Dados = B_Dados.loc[mask]

    mask = team_filter(team)
    B9_Dados = B9_Dados.loc[mask]

    B9_Dados = B9_Dados.groupby('temperatura-media')['chuva'].sum().reset_index()

    fig9 = go.Figure()
    fig9.add_trace(go.Pie(labels=B9_Dados['temperatura-media'], values=B9_Dados['chuva'], hole=.7))

    fig9.update_layout(main_config, height=450, template=template, showlegend=False)
    return fig9

# Graph 10
@app.callback(
    Output('graph10', 'figure'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph10(team, toggle):
    template = template_theme1 if toggle else template_theme2
    
    mask = team_filter(team)
    df_10 = B_Dados.loc[mask]

    df10 = df_10.groupby(['temperatura-media', 'mês'])['chuva'].sum().reset_index()
    fig10 = px.line(df10, y="chuva", x="mês", color="temperatura-media")

    fig10.update_layout(main_config, height=400, template=template, showlegend=False)
    return fig10

# Graph 11
@app.callback(
    Output('graph11', 'figure'),
    Output('team-select', 'children'),
    Input('radio-month', 'value'),
    Input('radio-team', 'value'),
    Input(ThemeSwitchAIO.ids.switch("theme"), "value")
)
def graph11(month, team, toggle):
    template = template_theme1 if toggle else template_theme2

    mask = month_filter(month)
    df_11 = B_Dados.loc[mask]

    mask = team_filter(team)
    df_11 = df_11.loc[mask]

    fig11 = go.Figure()
    fig11.add_trace(go.Indicator(mode='number',
        title = {"text": f"<span style='font-size:150%'>Chuva Total</span><br><span style='font-size:70%'>Em Numeros</span><br>"},
        value = df_11['chuva'].sum(),
        number = {'prefix': "Total :"}
    ))

    fig11.update_layout(main_config, height=300, template=template)
    select = html.H1("Todos chuvas confirmados") if team == 0 else html.H1(team)

    return fig11, select

# Run server
if __name__ == '__main__':
    app.run_server(debug=False)
