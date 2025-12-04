from dash import Dash, html, dcc, Output, Input, State, callback_context, no_update, ALL
import plotly.express as px
from pandas import to_datetime
from db import fetch_data, write_data, update_data
# db is my file which has the database connected , fetch_data, write_data, update_data are functions which do just as their name suggest

app = Dash(__name__)

rowStyle = {
    "display": "flex",
    "justifyContent": "space-between",
    "gap": "40px",
    "marginRight": "40px",
    'marginBottom':'40px',
}

cardStyle = {
    "background": "white",
    "padding": "20px",
    "borderRadius": "12px",
    "boxShadow": "0 4px 12px rgba(0,0,0,0.08)",
}


app.layout = html.Div(
    style={
        "padding": "30px",
        "display": "block",
        "width": "1300px",
        "margin": "0 auto", 
    },
    children=[

        # Row-1 for graph and live delivery
        html.Div([
            
            # bar graph for profit / sales graph
            html.Div([

                html.Div([
                        html.Button("profit", id="btn_profit", n_clicks=0, style={'width':'100px','height':'30px'}),
                        html.Button("sales", id="btn_sales", n_clicks=0, style={'width':'100px','height':'30px'}),
                    ],
                    style={'gap':'20px','display':'flex','marginLeft':'40px'}
                ),

                html.H1("Profit Graph",id='bar_graph_text', style={'textAlign':'center'}),

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
                        "top": "115px",
                        "left": "100px",
                        "zIndex": 10,
                        "display": "flex",
                        "gap": "10px",
                    }
                ),

                # Graph
                dcc.Graph(id='total_profit', style={"height": "350px","marginRight": "-40px","paddingRight": "50px"}),

            ], style={
                "position": "relative",         
                "width": "48%", 
                "height": "480px",  
                **cardStyle,                  
            }),
            
            # section for live update on delevry
            html.Div([
                html.Div([
                    html.H2(
                        "🚚 Active Deliveries",
                        style={
                            "margin": 0,
                            "flexGrow": 1,
                            "textAlign": "center"
                        }),

                    html.Button('Order More',id='btn_order',n_clicks=0,style={'height':'30px','width':'100px','marginRight':'80px'}),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "marginBottom": "15px",
                    "width": "100%",
                    'marginLeft':'30px'
                }),
                html.Div(id="live_delivery_feed",style={"overflowY": "scroll",'height':'400px','width':'500px','marginLeft':'30px'}),
            ],style={"height": "480px",'width':'48%',**cardStyle,}),
        
        ],style=rowStyle),

        # Row-2 for search bar and pi-chart
        html.Div([
            
             # searching for product
            html.Div([
                html.H1("Search Product Stock", style={"textAlign": "center"}),
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
                        "borderRadius": "5px",
                        'marginBottom':'50px'
                    },
                ),
            ],style={'width':'48%',"height": "480px",**cardStyle}),
            
            # making a pi chart
            html.Div([
                html.H1('pi-chart for vendors' , style={'textAlign':'center' }),
                dcc.Graph(id='pi-chart',style={'height':'88%'}),
            ],
            style={
                'width':'48%',
                'height':'480px',
                **cardStyle
            }),
        
        ],style=rowStyle),


        # --- Popup Overlay + Centered Modal Box ---
        html.Div(
            id="modal_overlay",
            children=[
                html.Div(
                    id="modal-box",
                    children=[
                        html.H2("Order Form", style={"marginBottom": "10px"}),

                        dcc.Dropdown(
                            id="order_product_selection",
                            options=[],
                            placeholder="Type product name to search...",
                            style={
                                "fontSize": "16px",
                                'height' : '40px',
                                'marginBottom': '20px'
                            },
                            clearable=True,
                            searchable=True,
                        ),

                        dcc.Input(
                            id="qty_input",
                            type="number",
                            placeholder="Quantity",
                            min=1,
                            max=9999,
                            step=1,
                            style={"width": "80%", "marginBottom": "40px",'height' : '40px',"fontSize": "20px",}
                        ),

                        html.Div([
                            html.Button(
                                "Submit",
                                id="btn_submit",
                                n_clicks=0,
                                style={
                                    "marginRight": "20px",
                                    'height':'35px',
                                    'width':'100px',
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "backgroundColor": "#4cf006"
                                }),

                            html.Button(
                                "Close",
                                id="btn_close",
                                n_clicks=0,
                                style={
                                    'height' : '35px',
                                    'width':'100px',
                                    "borderRadius": "10px",
                                    "cursor": "pointer",
                                    "backgroundColor": "#fa2206" 
                                }),
                        ])
                    ],
                    style={
                        "background": "white",
                        "padding": "20px",
                        "width": "400px",
                        'height': '300px',
                        "borderRadius": "12px",
                        "boxShadow": "0px 4px 25px rgba(0,0,0,0.3)",
                        "textAlign": "center",
                    }
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "background": "rgba(0,0,0,0.4)",  
                "display": "none",                
                "alignItems": "center",           
                "justifyContent": "center",       
                "zIndex": 99                   
            }
        ),

        # popup for order conformation
        html.Div(
            id="order_conformation_popup",
            children=[
                html.Div(
                    id="order_popup_box",
                    children=[
                        html.H3("Confirm Order"),
                        html.P("Are you sure you want to place this order?"),
                        html.P(id='popup_order_detail'),

                        html.Button("OK", id="popup_ok", n_clicks=0, style={'marginRight':'20px'}),
                        html.Button("Cancel", id="popup_cancel", n_clicks=0),
                    ],
                    style={
                        "background": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "300px",
                        "textAlign": "center",
                    },
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "background": "rgba(0,0,0,0.5)",
                "display": "none",
                "justifyContent": "center",
                "alignItems": "center",
                "zIndex": 999,
            },
        ),

        # for delivery details which has not yet recived
        html.Div(
            id="pop_up_delivery_detail_outer",
            children=[
                html.Div(
                    id="pop_up_delivery_detail_inner",
                    children=[
                        html.H1("Delivery Detail", style={"marginBottom": "30px",'textAlign':'center'}),

                        html.Div(id='delivery_details'),
                       
                        html.Div([
                            html.Button("Cancel Order", id="btn_cancel_detail", n_clicks=0, style={"marginRight": "15px", 'height':'32px'}),
                            html.Button("Mark As Delevered", id="btn_delivered_detail", n_clicks=0, style={"marginRight": "60px", 'height':'32px'}),
                            html.Button("Close", id="btn_close_detail", n_clicks=0,style={'height':'32px'}),
                        ])
                    ],
                    style={
                        "background": "white",
                        "padding": "20px",
                        "width": "400px",
                        'height': '380px',
                        "borderRadius": "12px",
                        "boxShadow": "0px 4px 25px rgba(0,0,0,0.3)",
                        "textAlign": "left",
                    }
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "background": "rgba(0,0,0,0.4)",  
                "display": 'none',                
                "alignItems": "center",           
                "justifyContent": "center",       
                "zIndex": 99                   
            }
        ),

        # for delivery detail operation conformation box
        html.Div(
            id="detail_conformation_popup",
            children=[
                html.Div(
                    id="detail_popup_box",
                    children=[
                        html.Div(id='detail_conform_message'),

                        html.Button("YES", id="btn_popup_yes", n_clicks=0, style={'marginRight':'20px'}),
                        html.Button("NO", id="btn_popup_no", n_clicks=0),
                    ],
                    style={
                        "background": "white",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "width": "300px",
                        "textAlign": "center",
                    },
                )
            ],
            style={
                "position": "fixed",
                "top": 0,
                "left": 0,
                "width": "100%",
                "height": "100%",
                "background": "rgba(0,0,0,0.5)",
                "display": "none",
                "justifyContent": "center",
                "alignItems": "center",
                "zIndex": 999,
            },
        ),

    ]
)

query= "SELECT product_name FROM products"
df_product=fetch_data(query)

query='SELECT product_name, product_id FROM products'
df=fetch_data(query)
name_to_id=df.set_index('product_name')['product_id'].to_dict()
id_to_name=df.set_index('product_id')['product_name'].to_dict()


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
        df = df_product.head(8)
    else:
        # Filter based on what user types
        df = df_product[df_product['product_name'].str.contains(search_value,case=False)].head(8)

    return [{"label": name, "value": name} for name in df["product_name"]]



def making_product_dict():
    product_dict={}
    query='SELECT product_sold, discount_rate FROM selling_records;'
    df= fetch_data(query)
    df['product_sold'] = df['product_sold'].str.split(';')

    def row_wise(row):
        for i in row['product_sold']:
            single_item_list= i.split(' - ')
            single_item_list[1] = int(single_item_list[1])

            try:
                x=1-(row['discount_rate']/100)
                product_dict[single_item_list[0]][0] += single_item_list[1]
                product_dict[single_item_list[0]][1] += single_item_list[1] * x

            except KeyError:
                product_dict[single_item_list[0]] = [single_item_list[1], single_item_list[1] * x]
    

    df.apply(row_wise,axis=1)  # updated a dict name product_dict which now contains each product name as key and a list as value , the list has 2 elements 1st is total product sold and 2nd is total product sold * discount if any

    # getting total sales and total profit per product
    query='SELECT p.product_name, p.selling_price, v.purchase_price FROM products p JOIN vendors v ON p.product_id = v.for_product;'
    df= fetch_data(query)
    def calculating_total_sales(row):
        cost= product_dict[row['product_name']][0] * row['purchase_price']
        income= product_dict[row['product_name']][1] * row['selling_price']
        profit= income - cost
        product_dict[row['product_name']][1] = profit
        product_dict[row['product_name']][0] *= row['selling_price']
        
    df.apply(calculating_total_sales,axis=1)

    return product_dict
product_dict=making_product_dict()

@app.callback(
    Output("search-result", "children"),
    Input("search-button", "n_clicks"),
    State("product-dropdown", "value"),
    prevent_initial_call=True
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
        html.Br(),
        html.B(f'Total Sales: {product_dict[selected_product][0]}'),
        html.Br(),
        html.Br(),
        html.B(f'Total Profit: {product_dict[selected_product][1]:.2f}'),
        html.Br(),
        html.Br(),
        html.Span(f"Stock Available: {row['stock_in_inventory']} units", style={"fontSize": "24px", "color": "#2c3e50"}),
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
            FROM products
            ORDER BY product_name;
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


show_profit=True
@app.callback(
    Output('total_profit','figure'),
    Output('month_dropdown','style'),
    Output('bar_graph_text','children'),
    [
        Input('total_profit','id'),
        Input('btn_year','n_clicks'),
        Input('btn_month','n_clicks'),
        Input('year','value'),
        Input('btn_profit','n_clicks'),
        Input('btn_sales','n_clicks'),
    ] 
)

def perodic_profit(_,__,___,year_value,____,_____):

    global show_profit

    ctx = callback_context

    if not ctx.triggered:
        # for initial loading
        triggered = 'total_profit'
    else:
        triggered = ctx.triggered[0]['prop_id'].split('.')[0]

    m=False

    if triggered == 'btn_sales':
        show_profit=False
    elif triggered == 'btn_profit' or triggered == 'total_profit':
        show_profit=True

    # for profit graph
    if show_profit:
        # for monthly profit graph
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
            m=True

        # for yearly profit graph
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
            m=False

        # making dictinary of {product_name : price} start here
        qurey= '''
                    SELECT v.purchase_price AS price, p.product_name AS product
                    FROM vendors v JOIN products p 
                    ON v.for_product = p.product_id;
                '''
        df_temp = fetch_data(qurey)
        d=dict(zip(df_temp['product'],df_temp['price']))       # till here

        # function for finding total cost of all product from a list of products
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
        
        df['profit']= df['final_bill'] - df["total_cost"]

    # for sales graph
    else:
        # for monthly sales graph
        if triggered == 'btn_month' or triggered == 'year':
            qurey= """
                    SELECT date_trunc('month',transaction_date) as month,
                        sum(bill_amount * (1 - (discount_rate / 100.0))) as total_sales 
                    FROM selling_records 
                    WHERE EXTRACT(YEAR FROM transaction_date) = :yr
                    group by month 
                    order by month;
                    """
            df = fetch_data(qurey,params={'yr':year_value})
            df['month'] = to_datetime(df['month']).dt.strftime('%b')
            m=True

        # for yearly sales graph
        else:
            qurey= """
                    SELECT 
                        to_char(transaction_date,'yyyy') as year,
                        sum(bill_amount * (1 - (discount_rate / 100.0))) as total_sales 
                    FROM selling_records 
                    group by year 
                    order by year;
                    """
            df = fetch_data(qurey)
            m=False


    fig = px.bar(
        df,
        x='month' if m else 'year',
        y='profit' if show_profit else 'total_sales',
    )
    style={'display':'block' if m else 'none'}
    text= 'Profit Graph' if show_profit else 'Sales Graph'
    return fig , style, text



@app.callback(
    Output('order_product_selection','options'),
    Input('order_product_selection','search_value'),
    Input('order_product_selection','value')
)

def order_popup_dropdown_options_update(search_value,value):

    if value and not search_value:
        # this condition make sure that the value of the dropdown is in the options of dropdown , if the value of dropdown is not in the options of dropdown then the value will be cleared from the dropdown
        df= df_product[df_product["product_name"].str.contains(value[:5],case=False)].head(5)
        return [{'label':name , 'value':name} for name in df['product_name']]

    if not search_value or len(search_value) < 1:
        df= df_product.head(5)
    else:
        df= df_product[df_product["product_name"].str.contains(search_value,case=False)].head(5)

    return [{'label':name , 'value':name} for name in df['product_name']]



@app.callback(
    Output('order_conformation_popup', 'style'),
    Output('modal_overlay','style'),
    Output('popup_order_detail','children'),
    Input('popup_ok','n_clicks'),
    Input('popup_cancel','n_clicks'),
    Input('btn_submit','n_clicks'),
    Input('btn_order','n_clicks'),
    Input('btn_close','n_clicks'),
    State('order_conformation_popup', 'style'),
    State('modal_overlay','style'),
    State('order_product_selection', 'value'),
    State('qty_input', 'value'),
)

def conform_order_popup_visibility(_,__,___,____,_____,order_conformation_style,order_page_style,product,quantity):
    ctx_id= callback_context.triggered_id

    if ctx_id == 'btn_submit':
        text=html.Div([
                        html.B(f'Product name = {product}'),
                        html.Br(),
                        html.Br(),
                        html.B(f'Quantity = {quantity}'),
                        html.Br(),
                        html.Br(),
                    ])
        order_conformation_style['display'] = 'flex'
        return order_conformation_style , no_update, text
    
    if ctx_id == 'popup_ok':
        write_data([product,quantity])
        order_page_style['display'] = 'none'
        order_conformation_style['display'] = 'none'
        return order_conformation_style, order_page_style, no_update
    
    if ctx_id == 'popup_cancel':
        order_conformation_style['display'] = 'none'
        return order_conformation_style, no_update, no_update
    
    else:
        order_page_style['display'] = 'flex' if ctx_id == 'btn_order' else 'none'
        return no_update, order_page_style, no_update



@app.callback(
    Output("live_delivery_feed", "children"),
    Input("live_delivery_feed", "id"),
)

def refresh_feed(_):

    query= "SELECT shipment_id, product_id, quantity_delivered, order_date FROM shipment_records WHERE status = 'Active' ORDER BY order_date DESC LIMIT 10"
    df = fetch_data(query)

    cards = []

    for i, row in df.iterrows():
        cards.append(
            html.Button(
                [
                    html.Div(f"Order #{row.shipment_id}", style={"fontSize": "20px", "fontWeight": "bold"}),
                    html.Div(f"Product: {row.product_id}"),
                    html.Div(f"Quantity: {row.quantity_delivered}"),
                ],
                n_clicks=0,
                id={'type':'btn_shipment_detail','index':i, 'shipment_id':row.shipment_id},
                style={
                    "padding": "15px",
                    "borderRadius": "12px",
                    "background": "white",
                    "boxShadow": "0px 4px 12px rgba(0,0,0,0.1)",
                    "marginBottom": "15px",
                    'marginRight' : '20px',
                    'width' : '95%',
                    "cursor": "pointer"
                }
            )
        )
    return cards



@app.callback(
    Output('pop_up_delivery_detail_outer','style',allow_duplicate=True),
    Output('delivery_details','children'),
    Input({'type':'btn_shipment_detail','index':ALL,'shipment_id':ALL},'n_clicks'),
    Input('btn_close_detail','n_clicks'),
    State('pop_up_delivery_detail_outer','style'),
    prevent_initial_call=True
)

def order_detail_visibility(n_clicks1,_, style1):

    ctx_id=callback_context.triggered_id

    if any(n_clicks1) and n_clicks1:

        if isinstance(ctx_id,dict):
            style1['display'] = 'flex'
            shipment_id=ctx_id['shipment_id']
            query='SELECT product_id, quantity_delivered, order_date FROM shipment_records where shipment_id = :shipment_id'
            prams={'shipment_id': shipment_id}
            df=fetch_data(query,prams).iloc[0]
            order_date= str(df["order_date"]).replace('T',"   ")
            children=html.Div(
                html.Div([
                    html.Div([
                        html.Strong("Product Name: "),
                        html.Span(id_to_name[df["product_id"]])
                    ],style={'marginBottom': '20px',"fontSize": "20px"}),
                    html.Div([
                        html.Strong("Product ID: "),
                        html.Span(df["product_id"])
                    ],style={'marginBottom': '20px',"fontSize": "20px"}),
                    html.Div([
                        html.Strong("Quantity: "),
                        html.Span(df["quantity_delivered"])
                    ],style={'marginBottom': '20px',"fontSize": "20px"}),
                    html.Div([
                        html.Strong("ID: "),
                        html.Span(shipment_id)
                    ],style={'marginBottom': '20px',"fontSize": "20px"}),
                    html.Div([
                        html.Strong("Order Date: "),
                        html.Span(order_date)
                    ],style={'marginBottom': '30px',"fontSize": "20px"}),
                ])
            )
            return style1, children

    style1['display'] = 'none'
    return style1, no_update



@app.callback(
    Output('detail_conformation_popup','style',allow_duplicate=True),
    Output('detail_conform_message','children'),
    Input('btn_cancel_detail','n_clicks'),
    Input('btn_delivered_detail','n_clicks'),
    State('detail_conformation_popup','style'),
    prevent_initial_call=True
)

def detail_conformation(_,__,style):
    ctx_id = callback_context.triggered_id
    if ctx_id == 'btn_cancel_detail':
        children= html.Div([
            html.H2('CONFIRMATION'),
            html.P('Are you sure you want to cancel this delivery ?',style={'fontSize' : '20px'})
        ])
    else:
        children= html.Div([
            html.H2('CONFIRMATION'),
            html.P('Are you sure you have recived this delivery ?',style={'fontSize' : '20px'})
        ])
    style['display'] = 'flex'
    return style, children



@app.callback(
    Output('detail_conformation_popup','style'),
    Output('pop_up_delivery_detail_outer','style'),
    Input('btn_popup_yes','n_clicks'),
    Input('btn_popup_no','n_clicks'),
    State('detail_conformation_popup','style'),
    State('pop_up_delivery_detail_outer','style'),
    State('detail_conform_message','children'),
    State('delivery_details','children'),
    prevent_initial_call=True
)

def detail_popup_work(_,__,style1,style2,children1,children2):
    ctx_id= callback_context.triggered_id

    if ctx_id == 'btn_popup_yes' :
        temp= children1['props']['children'][1]['props']['children']   # # this contains the final pop up message which comes after clicking 'cancel order' and 'mark as delevered' button
        shipment_id= children2['props']['children']['props']['children'][3]['props']['children'][1]['props']['children']  # this is shipment id
        if 'cancel' in temp :
            update_data('shipment_records','status',"'Cancled'",'shipment_id',shipment_id)
        else:
            update_data('shipment_records','status',"'Delivered'",'shipment_id',shipment_id)
            update_data('shipment_records','delivery_date','NOW()::timestamp(0)','shipment_id',shipment_id)   # need to also update in the products table but do that in the last 
            product_id= children2['props']['children']['props']['children'][1]['props']['children'][1]['props']['children']
            product_quantity= children2['props']['children']['props']['children'][2]['props']['children'][1]['props']['children']
            current_stock= fetch_data('SELECT stock_in_inventory FROM products WHERE product_id = :id',{'id':product_id}).iloc[0]['stock_in_inventory']
            final_quantity= product_quantity + current_stock
            update_data('products','stock_in_inventory',f"'{final_quantity}'",'product_id',product_id) # to update the stocks in inventory with the new delivery marked as delivered

        style2['display']= 'none'

    style1['display'] = 'none'
    return style1, style2




if __name__ == "__main__":
    app.run(debug=True)
