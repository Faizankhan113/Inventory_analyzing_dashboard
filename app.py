from dash import Dash, html, dcc, Output, Input, State, callback_context
import plotly.express as px
from pandas import to_datetime
from db import fetch_data
# db is my file which has the database connected fetch_data is a function througn which i send SQL querry and i get pandas's dataframe
app = Dash(__name__)

app.layout = html.Div(
    style={"padding": "30px", "width": "500px", "margin": "0 30px"},
    children=[

        # making a pi chart
        html.H1('pi-chart for vendors' , style={'textAlign':'center' }),
        dcc.Graph(id='pi-chart'),

        html.H2("Search Product Stock", style={"textAlign": "center"}),

        # ✅ Single searchable dropdown (type to search)
        # Container for dropdown and button side by side
        html.Div(
            style={
                "display": "flex",
                "gap": "10px",
                "marginBottom": "20px",
                "position": "relative"
            },
            children=[
                # Dropdown container with drop-up content
                html.Div(
                    style={"flex": "1", "position": "relative"},
                    children=[
                        # Drop-up content (appears above dropdown)
                        html.Div(
                            id='drop_up_content',
                            style={
                                'display': 'none',
                                'position': 'absolute',
                                'bottom': '100%',
                                'left': '0',
                                'right': '0',
                                'marginBottom': '10px',
                                'backgroundColor': 'white',
                                'border': '1px solid #ddd',
                                'borderRadius': '5px',
                                'padding': '15px',
                                'boxShadow': '0 -2px 10px rgba(0,0,0,0.1)',
                                'maxHeight': '300px',
                                'overflowY': 'auto',
                                'zIndex': '1000'
                            },
                        ),
                        # Searchable dropdown
                        dcc.Dropdown(
                            id="product-dropdown",
                            options=[],
                            placeholder="Type product name to search...",
                            style={
                                "fontSize": "16px"
                            },
                            clearable=True,
                            searchable=True,
                        ),
                    ]
                ),
                
                # See All Product button
                html.Button(
                    "See All Product",
                    id='show_product',
                    n_clicks=0,
                    style={
                        "padding": "10px 20px",
                        "fontSize": "16px",
                        "cursor": "pointer",
                        "backgroundColor": "#95a5a6",
                        "color": "white",
                        "border": "none",
                        "borderRadius": "5px",
                        "whiteSpace": "nowrap",
                        "height": "38px"
                    }
                )
            ]
        ),
        

        html.Button(
            "Search",
            id="search-button",
            n_clicks=0,
            style={
                "width": "68%",
                "padding": "10px",
                "fontSize": "18px",
                "cursor": "pointer",
                "backgroundColor": "#3498db",
                "color": "white",
                "border": "none",
                "borderRadius": "5px"
            },
        ),

        html.Div(
            id="search-result",
            style={
                "fontSize": "20px",
                "marginTop": "20px",
                "textAlign": "center",
                "padding": "15px",
                "borderRadius": "5px"
            },
        ),

        html.Div([

            html.H1('Profite Graph',style={'textAlign':'center'}),

            # Buttons positioned above the graph
            html.Div([
                html.Button("Year", id="btn_year", n_clicks=0 , style={"width": "100px", "height": "35px"}),
                html.Button("Month", id="btn_month", n_clicks=0 , style={"width": "100px", "height": "35px"}),
                html.Div(
                        id='month_dropdown',
                        children=[
                            dcc.Dropdown(
                                id='year',
                                options=[
                                    {"label": "2023", "value": 2023},
                                    {"label": "2024", "value": 2024},
                                    {"label": "2025", "value": 2025},
                                ],
                                value=2025,
                                clearable=False,
                                style={'width':'120px', 'margin':'0 auto'}
                            )],
                        style={"display": "none"}
                        ),
                ], style={
                    "position": "absolute",
                    "top": "65px",
                    "left": "100px",
                    "zIndex": 10,
                    "display": "flex",
                    "gap": "10px",
            }),



            # Graph
            dcc.Graph(id='total_profit', style={"height": "400px"}),

        ], style={
            "position": "relative",         
            "width": "600px",                     
        })

        
    ]
)

@app.callback(
    Output('pi-chart','figure'),
    Input('pi-chart','id')
)

def pi_chart_function(_):
    query="""
            SELECT v.vendor_name , p.product_name, p.stock_in_inventory
            FROM vendors v
            JOIN products p ON v.for_product = p.product_id;
        """
    df= fetch_data(query)
    grouped=(df.groupby('vendor_name').agg(total_stock = ('stock_in_inventory','sum'),
                                          products = ('product_name',list),
                                          stocks = ('stock_in_inventory',list)
                                          )
                                       .reset_index())

    grouped["details"] = grouped.apply(
        lambda row: "<br>".join([f"● {p} – {s}" for p, s in zip(row["products"], row["stocks"])]),
        axis=1
    )

    fig= px.pie(
        grouped,
        names='vendor_name',
        values='total_stock',
        hover_data=['details']
    )

    fig.update_traces(
        hovertemplate=
        "<b>%{label}</b><br>" +
        "Total Stock: %{value}<br><br>" +
        "Products:<br>%{customdata[0]}"
    )

    return fig

@app.callback(
    Output("product-dropdown", "options"),
    Input("product-dropdown", "search_value"),
    State("product-dropdown", "value")
)
def update_dropdown_options(search_value, current_value):
    """Update dropdown options as user types"""

    # If something is already selected, don't change options
    if current_value and not search_value :
        query = """
            SELECT product_name
            FROM products
            WHERE LOWER(product_name) LIKE LOWER(:search_term)
            ORDER BY product_name
            LIMIT 8;
        """
        sliced= current_value[:5]
        df = fetch_data(query,params={'search_term':f'%{sliced}%'})
        return [{"label": name, "value": name} for name in df["product_name"]]

    # If user is typing (but hasn't selected yet)
    if not search_value or len(search_value) < 1:
        # Show top 8 products initially
        query = """
            SELECT product_name 
            FROM products 
            ORDER BY product_name
            LIMIT 8;
        """
        df = fetch_data(query)
    else:
        # Filter based on what user types
        query = """
            SELECT product_name 
            FROM products 
            WHERE LOWER(product_name) LIKE LOWER(:search_term)
            ORDER BY product_name
            LIMIT 8;
        """
        df = fetch_data(query, params={"search_term": f"%{search_value}%"})

    return [{"label": name, "value": name} for name in df["product_name"]]


@app.callback(
    Output("search-result", "children"),
    Input("search-button", "n_clicks"),
    State("product-dropdown", "value")
)
def search_product(n_clicks, selected_product):
    """Display stock info when search button is clicked"""
    if n_clicks == 0:
        return ""

    if not selected_product:
        return "❗ Please select a product from the dropdown."

    # Get stock information
    query = """
        SELECT product_name, stock_in_inventory
        FROM products
        WHERE LOWER(product_name) = LOWER(:product_name);
    """

    df = fetch_data(query, params={"product_name": selected_product})

    if df.empty:
        return "❌ No matching product found."

    row = df.iloc[0]

    return html.Div([
        html.B(f"✅ {row['product_name']}", style={"color": "#27ae60"}),
        html.Br(),
        html.Span(f"Stock: {row['stock_in_inventory']} units", style={"fontSize": "24px", "color": "#2c3e50"})
    ])


@app.callback(
    Output('drop_up_content', 'children'),
    Output('drop_up_content', 'style'),
    Input('show_product', 'n_clicks'),
    State('drop_up_content', 'style')
)

def drop_up_content_update(n_click,style):
    if n_click % 2 == 1 :
        query="""
            SELECT product_name
            FROM products;
        """
        df = fetch_data(query)
        items=df['product_name'].to_list()

        content= html.Div(
            [
                html.H2('Product name',style ={'textAlign' : 'center'}),
                html.Ul(
                    [html.Li(item) for item in items]
                )
            ]
        )
        
        style['display'] = 'block'

    else:
        content=''
        style['display'] = 'none'

    return content , style



@app.callback(
    Output('total_profit','figure'),
    Output('month_dropdown','style'),
    [
        Input('total_profit','id'),
        Input('btn_year','n_clicks'),
        Input('btn_month','n_clicks'),
        Input('year','value')
    ] 
)

def perodic_profit(_,__,___,year_value):

    ctx = callback_context
    triggered = ctx.triggered[0]['prop_id'].split('.')[0]
    m=0

    if triggered == 'btn_month' or triggered == 'year':
        qurey= """
                SELECT date_trunc('month',transaction_date) as month,
                    sum(bill_amount * (1 - (discount_rate / 100.0))) as final_bill,
                    array_agg(product_sold) as product_list 
                FROM selling_records 
                WHERE EXTRACT(YEAR FROM transaction_date) = :yr
                group by month 
                order by month;
                """
        df = fetch_data(qurey,params={'yr':year_value})
        df['month'] = to_datetime(df['month']).dt.strftime('%b')
        m=1

    else:    
        qurey= """
                SELECT 
                    to_char(transaction_date,'yyyy') as year,
                    sum(bill_amount * (1 - (discount_rate / 100.0))) as final_bill,
                    array_agg(product_sold) as product_list 
                FROM selling_records 
                group by year 
                order by year;
                """
        df = fetch_data(qurey)
        m=0

    qurey= '''
                SELECT v.purchase_price AS price, p.product_name AS product
                FROM vendors v JOIN products p 
                ON v.for_product = p.product_id;
            '''
    df_temp = fetch_data(qurey)
    d=dict(zip(df_temp['product'],df_temp['price']))

    def use_this(x):
        total=0

        for i in x:
            if ';' in i:
                a=i.split(';')
                for j in a :
                    temp_a, temp_b = j.split('- ')
                    temp_a=temp_a.strip()
                    total += (d[temp_a] * int(temp_b))
            else:
                temp_a, temp_b = i.split('- ')
                temp_a=temp_a.strip()
                total += (d[temp_a] * int(temp_b))

        return total
    
    df['total_cost'] = df['product_list'].apply(use_this)
    
    df['profite']= df['final_bill'] - df["total_cost"]

    if m:
        fig = px.bar(
            df,
            x='month',
            y='profite',
        )
        style={'display':'block'}
        return fig , style


    fig = px.bar(
        df,
        x='year',
        y='profite',
    )
    style={'display':'none'}
    return fig, style



if __name__ == "__main__":
    app.run(debug=True)










#   to add :-
# 1- make the vendor delevery dataset
# 2- make a chart of total profit per day / month / week and also for per product
# for profit showing i will show bar graph for every year and for every month in a year (will give options for selecting which year the data will show)

