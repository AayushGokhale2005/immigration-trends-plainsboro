from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

external_stylesheets = [
    'https://fonts.googleapis.com/css2?family=Roboto&display=swap'
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#f0f8e0',  # Light yellowish green
    'header': '#013220',      # Dark green
    'text': '#2c2c2c'
}

# Load data
df = pd.read_csv('plainsboro_cleaned.csv')

# Citizenship Pie Chart
citizenship_df = df[(df['Group'] == 'CITIZENSHIP') & df['Label'].isin(['Naturalized citizen', 'Not a citizen'])].copy()
citizenship_df['Plainsboro_total'] = citizenship_df['Plainsboro_total'].str.replace('%', '').astype(float)

fig_pie = px.pie(
    citizenship_df,
    names='Label',
    values='Plainsboro_total',
    title='Citizenship Status of Foreign-born Population in Plainsboro'
)
fig_pie.update_layout(paper_bgcolor=colors['background'])

# Age and Gender
age_labels = ['Under 5 years','5 to 17 years','18 to 24 years','25 to 44 years','45 to 54 years','55 to 64 years','65 to 74 years','75 to 84 years','85 years and over']
gender_labels = ['Male', 'Female']

age_df = df[(df['Group']=='SEX AND AGE') & df['Label'].isin(age_labels)].copy()
df_gender = df[(df['Group']=='SEX AND AGE') & df['Label'].isin(gender_labels)].copy()

for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    age_df[col] = age_df[col].str.replace('%', '').replace('(X)', '0').astype(float)

fig_age = px.bar(
    age_df,
    x='Label',
    y=['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000'],
    title='Age Distribution by Entry Year',
    labels={'value': 'Percentage', 'Label': 'Age Group'},
)
fig_age.update_layout(barmode='stack', paper_bgcolor=colors['background'])

df_gender['Plainsboro_total'] = df_gender['Plainsboro_total'].str.replace('%', '').astype(float)

fig1 = px.bar(df_gender, x='Label', y='Plainsboro_total', title='Gender Distribution of Foreign-born Population in Plainsboro')
fig1.update_layout(paper_bgcolor=colors['background'])

# World Region of Birth
region_df = df[(df['Group'] == 'WORLD REGION OF BIRTH OF FOREIGN-BORN')].copy()
region_df = region_df[region_df['Label'].isin(['Europe', 'Asia', 'Africa', 'Oceania', 'Latin America', 'Northern America'])]
region_df['Plainsboro_total'] = region_df['Plainsboro_total'].str.replace('%', '').astype(float)

region_coords = {
    'Europe': (54.5260, 15.2551),
    'Asia': (34.0479, 100.6197),
    'Africa': (1.6508, 17.6791),
    'Oceania': (-22.7359, 140.0188),
    'Latin America': (-10.3333, -53.2000),
    'Northern America': (54.5260, -105.2551)
}
plainsboro_coords = (40.3337, -74.5858)

lines = []
for _, row in region_df.iterrows():
    region = row['Label']
    lat1, lon1 = region_coords[region]
    lat2, lon2 = plainsboro_coords
    lines.append(go.Scattergeo(
        lon=[lon1, lon2],
        lat=[lat1, lat2],
        mode='lines+markers',
        line=dict(width=2),
        marker=dict(size=8),
        name=f"{region}: {row['Plainsboro_total']}%"
    ))

fig_map = go.Figure(data=lines)
fig_map.update_layout(
    title="Birth Regions of Foreign-born Population Connected to Plainsboro, NJ",
    geo=dict(
        scope='world',
        projection_type='natural earth',
        showland=True,
        landcolor='rgb(243, 243, 243)',
        countrycolor='rgb(204, 204, 204)',
    ),
    showlegend=True,
    paper_bgcolor=colors['background']
)

# Household Type Distribution

household_labels = [
    "In married-couple family",
    "In other households"
]

household_df = df[(df['Group'] == 'HOUSEHOLD TYPE') & df['Label'].isin(household_labels)].copy()
for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    household_df[col] = household_df[col].str.replace('%', '').astype(float)

household_melted = household_df.melt(
    id_vars='Label',
    value_vars=['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000'],
    var_name='Entry Year',
    value_name='Percentage'
)

fig_household = px.bar(
    household_melted,
    x='Label',
    y='Percentage',
    color='Entry Year',
    barmode='group',
    title='Household Type Distribution by Entry Year'
)
fig_household.update_layout(paper_bgcolor=colors['background'])


# Marital Status 
marital_labels = [
    "Never married",
    "Now married, except separated",
    "Divorced or separated",
    "Widowed"
]

marital_df = df[(df['Group'] == 'MARITAL STATUS') & df['Label'].isin(marital_labels)].copy()
for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    marital_df[col] = marital_df[col].str.replace('%', '').astype(float)

marital_melted = marital_df.melt(
    id_vars='Label',
    value_vars=['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000'],
    var_name='Entry Year',
    value_name='Percentage'
)

fig_marital = px.bar(
    marital_melted,
    x='Label',
    y='Percentage',
    color='Entry Year',
    title='Marital Status of Foreign-born (15+ Years) by Entry Year'
)
fig_marital.update_layout(barmode='stack', paper_bgcolor=colors['background'])

# Employment
employment_labels = ['In labor force', 'Civilian labor force', 'Employed', 'Unemployed', 'Not in labor force']
employment_df = df[(df['Group'] == 'EMPLOYMENT STATUS') & df['Label'].isin(employment_labels)].copy()

for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    employment_df[col] = employment_df[col].str.replace('%', '').astype(float)

fig_employment = go.Figure()
for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    fig_employment.add_trace(go.Bar(
        x=employment_df['Label'],
        y=employment_df[col],
        name=col.replace('_', ' ')
    ))

fig_employment.update_layout(
    barmode='group',
    title='Employment Status of Foreign-born by Year of Entry',
    xaxis_title='Employment Category',
    yaxis_title='Percentage',
    legend_title='Year of Entry',
    paper_bgcolor=colors['background']
)

# Occupation Heatmap
occupation_labels = [
    'Management, business, science, and arts occupations',
    'Service occupations',
    'Sales and office occupations',
    'Natural resources, construction, and maintenance occupations',
    'Production, transportation, and material moving occupations',
]

occupation_df = df[(df['Group'] == 'OCCUPATION') & df['Label'].isin(occupation_labels)].copy()
for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    occupation_df[col] = occupation_df[col].str.replace('%', '').astype(float)

heatmap_df = occupation_df.set_index('Label')[['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']]
heatmap_df = heatmap_df.reset_index().melt(id_vars='Label', var_name='Entry Year', value_name='Percentage')

heatmap_df['Entry Year'] = heatmap_df['Entry Year'].replace({
    'Entered_2010_or_later': '2010+',
    'Entered_2000_to_2009': '2000s',
    'Entered_before_2000': 'Pre-2000'
})

fig_occupation = px.imshow(
    heatmap_df.pivot(index='Label', columns='Entry Year', values='Percentage'),
    color_continuous_scale='Blues',
    labels=dict(x="Entry Year", y="Occupation", color="Percentage"),
    title='Occupation Distribution Heatmap by Year of Entry',
    aspect='auto',
    text_auto=True
)

fig_occupation.update_layout(
    paper_bgcolor=colors['background'],
    font=dict(size=14),
    margin=dict(l=120, r=40, t=60, b=60)
)

# Industry Sunburst
industry_dict = {
    'Agriculture, forestry, fishing and hunting, and mining': 'Agriculture, Forestry, Fishing',
    'Construction': 'Construction',
    'Manufacturing': 'Manufacturing',
    'Wholesale trade': 'Wholesale Trade',
    'Retail trade': 'Retail Trade',
    'Transportation and warehousing, and utilities': 'Transport & Utilities',
    'Information': 'Information',
    'Finance and insurance, and real estate and rental and leasing': 'Finance & Real Estate',
    'Professional, scientific, and management, and administrative and waste management services': 'Professional & Mgmt',
    'Educational services, and health care and social assistance': 'Education & Healthcare',
    'Arts, entertainment, and recreation, and accommodation and food services': 'Arts & Hospitality',
    'Other services (except public administration)': 'Other Services',
    'Public administration': 'Public Admin'
}

industry_df = df[(df['Group'] == 'INDUSTRY') & df['Label'].isin(industry_dict.keys())].copy()
industry_df['Label'] = industry_df['Label'].replace(industry_dict)
for col in ['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000']:
    industry_df[col] = industry_df[col].str.replace('%', '').astype(float)

industry_melted = industry_df.melt(
    id_vars='Label',
    value_vars=['Entered_2010_or_later', 'Entered_2000_to_2009', 'Entered_before_2000'],
    var_name='Entry Year',
    value_name='Percentage'
)

fig_industry_sunburst = px.sunburst(
    industry_melted,
    path=['Entry Year', 'Label'],
    values='Percentage',
    title='Industry Distribution of Foreign-Born Population by Year of Entry'
)
fig_industry_sunburst.update_layout(paper_bgcolor=colors['background'])
#Earnings in 2023 dollars
earnings_labels=[]
df_earnings = df[(df['Group'] == 'EARNINGS IN THE PAST 12 MONTHS (IN 2023 INFLATION-ADJUSTED DOLLARS) FOR FULL-TIME, YEAR-ROUND WORKERS') &
                 (df['Label'].isin([...]))]








# Layout
plainsboro_logo = "https://upload.wikimedia.org/wikipedia/en/thumb/b/bf/Plainsboro_Logo.png/87px-Plainsboro_Logo.png"
wicoff_logo = "https://wicoffhouseplainsboro.com/wp-content/uploads/2021/08/WH-Logo-1-e1659994830346.png"

app.layout = html.Div(style={'backgroundColor': colors['background'], 'fontFamily': 'Roboto, sans-serif', 'padding': '20px'}, children=[
    html.H1("Immigration Trends in Plainsboro, New Jersey", style={'color': colors['header'], 'textAlign': 'center'}),

    html.Div([
        html.Img(src=plainsboro_logo, style={'height': '60px', 'float': 'right'}),
        html.H2("About Plainsboro", style={'color': colors['header']}),
        html.P("Plainsboro Township, founded in 1919, grew from a rural farming area into a diverse and thriving suburban community. Historically home to the Lenape people, early Dutch and English settlers, and later the Walker-Gordon Dairy Farm, Plainsboro has prioritized open-space preservation and cultural richness. Learn more from the ",
               style={'fontSize': '16px'}),
        html.A("Plainsboro History Page", href="https://www.plainsboronj.com/317/History", target="_blank"),
        html.Span(" or the "),
        html.A("Wikipedia Article.", href="https://en.wikipedia.org/wiki/Plainsboro_Township,_New_Jersey", target="_blank")
    ], style={'marginBottom': '40px'}),

    html.H2("Citizenship Breakdown", style={'color': colors['header']}),
    dcc.Graph(figure=fig_pie),

    html.H2("Age Distribution by Entry Year", style={'color': colors['header']}),
    dcc.Graph(figure=fig_age),

    html.H2("Gender Distribution", style={'color': colors['header']}),
    dcc.Graph(figure=fig1),

    html.H2("World Region of Birth", style={'color': colors['header']}),
    dcc.Graph(figure=fig_map),

    html.Div([
    html.H2('Household Type Distribution', style={'color': colors['header']}),
    html.P("Breakdown of family and other household types among Plainsboro's foreign-born residents.",
        style={'fontSize': '14px'}),
        dcc.Graph(figure=fig_household)
        ], style={'marginBottom': '40px'}),

    html.Div([
        html.H2('Marital Status by Entry Year', style={'color': colors['header']}),
        html.P("Marriage trends of foreign-born individuals aged 15+ across immigration waves.",
            style={'fontSize': '14px'}),
        dcc.Graph(figure=fig_marital)
    ], style={'marginBottom': '40px'}),

    html.H2("Employment by Entry Year", style={'color': colors['header']}),
    dcc.Graph(figure=fig_employment),

    html.H2("Occupation Heatmap", style={'color': colors['header']}),
    dcc.Graph(figure=fig_occupation),

    html.H2("Industry Distribution", style={'color': colors['header']}),
    dcc.Graph(figure=fig_industry_sunburst),

    html.H2("Raw Data Preview", style={'color': colors['header']}),
        dash_table.DataTable(
            data=df.to_dict('records'),
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left'},
            style_header={'backgroundColor': colors['header'], 'color': 'white'},
            style_data={'backgroundColor': 'white', 'color': colors['text']}
        ),



    html.Div([
        html.H2("About This Project", style={'color': colors['header']}),
        html.Img(src=wicoff_logo, style={'height': '80px', 'display': 'block', 'margin': '10px auto'}),
        html.P("This project was developed in partnership with the Wicoff House Museum to visualize demographic trends of Plainsboro's foreign-born residents. It was created using Python, Dash, and U.S. Census ACS data.", style={'fontSize': '16px'}),
        html.P("I'm Aayush Gokhale, a Computer Science major at Rutgers University. This work combines data science with public history to illuminate how immigration has shaped the township’s present and future.", style={'fontSize': '16px'})
    ], style={'backgroundColor': 'white', 'padding': '20px', 'borderRadius': '10px', 'marginTop': '40px'}),

   
])

if __name__ == '__main__':
    app.run(debug=True)
