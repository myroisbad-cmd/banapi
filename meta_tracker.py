import dash
from dash import dcc, html, callback
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

# Charger les données depuis le fichier CSV - cette fonction est réutilisée du code original
def load_data():
    return pd.read_csv('/home/ubuntu/brawlapi/brawlapi-main/battlelog-csv/sets-final.csv')

# Initialiser les données
df = load_data()
all_players = pd.concat([df['P1'], df['P2'], df['P3'], df['P4'], df['P5'], df['P6']]).dropna().unique()
teams = sorted(set(df['Team1 Name'].tolist() + df['Team2 Name'].tolist()) - {'unknown'})

# Extraction des modes uniques et leurs cartes correspondantes
modes = df['mode'].dropna().unique()
mode_to_maps = {
    "Gem Grab": [
        "Hard Rock Mine", "Gem Fort", "Undermine", "Double Swoosh",
        "Minecart Madness", "Acute Angle", "Rustic Arcade", "Open Space",
        "Last Stop", "Sneaky Sneak", "Ahead Of The Curve", "Bear Trap","Crystal Arcade"
    ],
    "Heist": [
        "Kaboom Canyon", "Safe Zone", "Hot Potato", "Bridge Too Far",
        "Diamond Dome", "Secret Or Mystery","Pit Stop"
    ],
    "Hot Zone": [
        "Open Business", "Parallels Plays", "Ring of Fire",
        "Dueling Beetles", "Local Businesses", "Misty Meadows","Open Zone"
    ],
    "Bounty": [
        "Snake Prairie", "Shooting Star", "Hideout", "Canal Grande",
        "Flank Attack", "Crowd Strike","Layer Cake","Dry Season"
    ],
    "Knockout": [
        "Goldarm Gulch", "Belle's Rock", "Deep End", "Flaring Phoenix",
        "Out in the Open", "New Horizons", "Between The Rivers",
        "Four Levels", "Twilight Passage", "Hard Lane",
        "Island Hooping", "Sunset Spar"
    ],
    "Brawl Ball": [
        "Backyard Bowl", "Triple Dribble", "Sneaky Fields",
        "Super Beach", "Pinball Dreams", "Center Stage", "Beach Ball",
        "Sunny Soccer", "Penalty Kick", "Retina", "Offside Trap",
        "Back Pocket","Pinhole Punt"
    ]
}

# Dictionnaire des chemins d'images pour chaque carte au format WebP
map_images = {
    # Gem Grab
    "Hard Rock Mine": "assets/images/hard-rock-mine.webp",
    "Gem Fort": "assets/images/gem-fort.webp",
    "Undermine": "assets/images/undermine.webp",
    "Double Swoosh": "assets/images/double-swoosh.webp",
    "Minecart Madness": "assets/images/minecart-madness.webp",
    "Acute Angle": "assets/images/acute-angle.webp",
    "Rustic Arcade": "assets/images/rustic-arcade.webp",
    "Open Space": "assets/images/open-space.webp",
    "Last Stop": "assets/images/last-stop.webp",
    "Sneaky Sneak": "assets/images/sneaky-sneak.webp",
    "Ahead Of The Curve": "assets/images/ahead-of-the-curve.webp",
    "Bear Trap": "assets/images/bear-trap.webp",


    # Heist
    "Kaboom Canyon": "assets/images/kaboom-canyon.webp",
    "Safe Zone": "assets/images/safe-zone.webp",
    "Hot Potato": "assets/images/hot-potato.webp",
    "Bridge Too Far": "assets/images/bridge-too-far.webp",
    "Diamond Dome": "assets/images/diamond-dome.webp",
    "Secret Or Mystery": "assets/images/secret-or-mystery.webp",
    "Pit Stop":"assets/images/pit-stop.webp",

    # Hot Zone
    "Open Business": "assets/images/open-business.webp",
    "Parallels Plays": "assets/images/parallels-plays.webp",
    "Ring of Fire": "assets/images/ring-of-fire.webp",
    "Dueling Beetles": "assets/images/dueling-beetles.webp",
    "Local Businesses": "assets/images/local-businesses.webp",
    "Misty Meadows": "assets/images/misty-meadows.webp",
    "Open Zone":"assets/images/open-zone.webp",

    # Bounty
    "Snake Prairie": "assets/images/snake-prairie.webp",
    "Shooting Star": "assets/images/shooting-star.webp",
    "Hideout": "assets/images/hideout.webp",
    "Canal Grande": "assets/images/canal-grande.webp",
    "Flank Attack": "assets/images/flank-attack.webp",
    "Crowd Strike": "assets/images/crowd-strike.webp",
    "Layer Cake" : "assets/images/layer_cake.webp",

    # Knockout
    "Goldarm Gulch": "assets/images/goldarm-gulch.webp",
    "Belle's Rock": "assets/images/belles-rock.webp",
    "Deep End": "assets/images/deep-end.webp",
    "Flaring Phoenix": "assets/images/flaring-phoenix.webp",
    "Out in the Open": "assets/images/out-in-the-open.webp",
    "News Horizons": "assets/images/news-horizons.webp",
    "Between The Rivers": "assets/images/between-the-rivers.webp",
    "Four Levels": "assets/images/four-levels.webp",
    "Twilight Passage": "assets/images/twilight-passage.webp",
    "Hard Lane": "assets/images/hard-lane.webp",
    "Island Hooping": "assets/images/island-hooping.webp",
    "Sunset Spar": "assets/images/sunset-spar.webp",

    # Brawl Ball
    "Backyard Bowl": "assets/images/backyard-bowl.webp",
    "Triple Dribble": "assets/images/triple-dribble.webp",
    "Sneaky Fields": "assets/images/sneaky-fields.webp",
    "Super Beach": "assets/images/super-beach.webp",
    "Pinball Dreams": "assets/images/pinball-dreams.webp",
    "Center Stage": "assets/images/center-stage.webp",
    "Beach Ball": "assets/images/beach-ball.webp",
    "Sunny Soccer": "assets/images/sunny-soccer.webp",
    "Penalty Kick": "assets/images/penalty-kick.webp",
    "Retina": "assets/images/retina.webp",
    "Offside Trap": "assets/images/offside-trap.webp",
    "Back Pocket": "assets/images/back-pocket.webp",
    "Pinhole Punt" :"assets/images/pinhole-punt.webp"
}

brawler_icons = {
    "8-BIT": "assets/brawler_icon/8bit_portrait.png",
    "AMBER": "assets/brawler_icon/amber_portrait.png",
    "ANGELO": "assets/brawler_icon/angelo_portrait.png",
    "BARLEY": "assets/brawler_icon/barley_portrait.png",
    "BEA": "assets/brawler_icon/bea_portrait.png",
    "ASH": "assets/brawler_icon/ash_portrait.png",
    "BELLE": "assets/brawler_icon/belle_portrait.png",
    "BERRY": "assets/brawler_icon/berry_portrait.png",
    "BIBI": "assets/brawler_icon/bibi_portrait.png",
    "BO": "assets/brawler_icon/bo_portrait.png",
    "BONNIE": "assets/brawler_icon/bonnie_portrait.png",
    "BROCK": "assets/brawler_icon/brock_portrait.png",
    "BULL": "assets/brawler_icon/bull_portrait.png",
    "BUSTER": "assets/brawler_icon/buster_portrait.png",
    "BUZZ LIGHTYEAR": "assets/brawler_icon/buzz_lightyear_portrait.png",
    "BUZZ": "assets/brawler_icon/buzz_portrait.png",
    "BYRON": "assets/brawler_icon/byron_portrait.png",
    "CARL": "assets/brawler_icon/carl_portrait.png",
    "CHARLIE": "assets/brawler_icon/charlie_portrait.png",
    "CHESTER": "assets/brawler_icon/chester_portrait.png",
    "CHUCK": "assets/brawler_icon/chuck_portrait.png",
    "CLANCY": "assets/brawler_icon/clancy_portrait.png",
    "COLETTE": "assets/brawler_icon/colette_portrait.png",
    "COLT": "assets/brawler_icon/colt_portrait.png",
    "CORDELIUS": "assets/brawler_icon/cordelius_portrait.png",
    "CROW": "assets/brawler_icon/crow_portrait.png",
    "DARRYL": "assets/brawler_icon/darryl_portrait.png",
    "DOUG": "assets/brawler_icon/doug_portrait.png",
    "DRACO": "assets/brawler_icon/draco_portrait.png",
    "DYNAMIKE": "assets/brawler_icon/dynamike_portrait.png",
    "EDGAR": "assets/brawler_icon/edgar_portrait.png",
    "EL PRIMO": "assets/brawler_icon/elprimo_portrait.png",
    "EMZ": "assets/brawler_icon/emz_portrait.png",
    "EVE": "assets/brawler_icon/eve_portrait.png",
    "FANG": "assets/brawler_icon/fang_portrait.png",
    "FINX": "assets/brawler_icon/finx_portrait.png",
    "FRANK": "assets/brawler_icon/frank_portrait.png",
    "GALE": "assets/brawler_icon/gale_portrait.png",
    "GENE": "assets/brawler_icon/gene_portrait.png",
    "GRAY": "assets/brawler_icon/gray_portrait.png",
    "GRIFF": "assets/brawler_icon/griff_portrait.png",
    "GROM": "assets/brawler_icon/grom_portrait.png",
    "GUS": "assets/brawler_icon/gus_portrait.png",
    "HANK": "assets/brawler_icon/hank_portrait.png",
    "HYPER COLT": "assets/brawler_icon/hyper_colt_portrait.png",
    "JACKY": "assets/brawler_icon/jacky_portrait.png",
    "JANET": "assets/brawler_icon/janet_portrait.png",
    "JESSIE": "assets/brawler_icon/jessie_portrait.png",
    "JUJU": "assets/brawler_icon/juju_portrait.png",
    "KENJI": "assets/brawler_icon/kenji_portrait.png",
    "KIT": "assets/brawler_icon/kit_portrait.png",
    "LARRY & LAWRIE": "assets/brawler_icon/larry&lawrie_portrait.png",
    "LEON": "assets/brawler_icon/leon_portrait.png",
    "LILY": "assets/brawler_icon/lily_portrait.png",
    "LOLA": "assets/brawler_icon/lola_portrait.png",
    "LOU": "assets/brawler_icon/lou_portrait.png",
    "LUMI": "assets/brawler_icon/lumi_portrait.png",
    "MAISIE": "assets/brawler_icon/maisie_portrait.png",
    "MANDY": "assets/brawler_icon/mandy_portrait.png",
    "MAX": "assets/brawler_icon/max_portrait.png",
    "MEEPLE": "assets/brawler_icon/meeple_portrait.png",
    "MEG": "assets/brawler_icon/meg_portrait.png",
    "MELODIE": "assets/brawler_icon/melodie_portrait.png",
    "MICO": "assets/brawler_icon/mico_portrait.png",
    "MOE": "assets/brawler_icon/moe_portrait.png",
    "MORTIS": "assets/brawler_icon/mortis_portrait.png",
    "MR. P": "assets/brawler_icon/mrp_portrait.png",
    "NANI": "assets/brawler_icon/nani_portrait.png",
    "NITA": "assets/brawler_icon/nita_portrait.png",
    "OLLIE": "assets/brawler_icon/ollie_portrait.png",
    "OTIS": "assets/brawler_icon/otis_portrait.png",
    "PAM": "assets/brawler_icon/pam_portrait.png",
    "PEARL": "assets/brawler_icon/pearl_portrait.png",
    "PENNY": "assets/brawler_icon/penny_portrait.png",
    "PIPER": "assets/brawler_icon/piper_portrait.png",
    "POCO": "assets/brawler_icon/poco_portrait.png",
    "RICO": "assets/brawler_icon/rico_portrait.png",
    "R-T": "assets/brawler_icon/rt_portrait.png",
    "ROSA": "assets/brawler_icon/rosa_portrait.png",
    "RUFFS": "assets/brawler_icon/ruffs_portrait.png",
    "SAM": "assets/brawler_icon/sam_portrait.png",
    "SANDY": "assets/brawler_icon/sandy_portrait.png",
    "SHADE": "assets/brawler_icon/shade_portrait.png",
    "SHELLY": "assets/brawler_icon/shelly_portrait.png",
    "SPIKE": "assets/brawler_icon/spike_portrait.png",
    "SPROUT": "assets/brawler_icon/sprout_portrait.png",
    "SQUEAK": "assets/brawler_icon/squeak_portrait.png",
    "STU": "assets/brawler_icon/stu_portrait.png",
    "SURGE": "assets/brawler_icon/surge_portrait.png",
    "TARA": "assets/brawler_icon/tara_portrait.png",
    "TICK": "assets/brawler_icon/tick_portrait.png",
    "WILLOW": "assets/brawler_icon/willow_portrait.png",
}

# Mise à jour des cartes en fonction du mode
for mode in modes:
    mode_to_maps[mode] = df[df['mode'] == mode]['map'].dropna().unique().tolist()

# Générer dynamiquement la liste des régions à partir du DataFrame
regions = ['ALL'] + sorted([r for r in df['region'].dropna().unique() if r != 'ALL'])

dash.register_page(__name__, path='/meta-tracker')

layout = html.Div([
    dcc.Store(id='auth-store', storage_type='session'),  # Store pour l'authentification
    html.Div(id='meta-tracker-content'),  # Conteneur conditionnel pour le contenu de la page
    dcc.Location(id="url"),  # Pour gérer les redirections
])

# Callback pour vérifier l'authentification et afficher ou rediriger
@callback(
    Output('meta-tracker-content', 'children'),
    Input('auth-store', 'data')
)
def update_meta_tracker_content(auth_store):
    if not auth_store or auth_store.get('is_logged_in') != "b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b":
        # Redirection si non authentifié
        return dcc.Location(pathname='/', id='redirect-to-login')
    
    # Contenu de la page si authentifié
    return html.Div([
        html.H1("Meta Tracker"),
        html.Div(className="container", children=[
            html.Div(className="selecteur", children=[
                # Sélecteur de mode de jeu
                html.Label("Choose a Game Mode"),
                dcc.Dropdown(
                    id='mode-dropdown-meta',
                    options=[{'label': mode, 'value': mode} for mode in mode_to_maps.keys()],
                    value=list(mode_to_maps.keys())[0] if mode_to_maps else None,
                    clearable=False
                ),
                # Sélecteur de carte (mis à jour en fonction du mode sélectionné)
                html.Label("Choose a Map"),
                dcc.Dropdown(
                    id='map-dropdown-meta',
                    clearable=False,
                    value=None
                ),
                # Sélecteur de région
                html.Label("Choose a Region"),
                dcc.Dropdown(
                    id='region-dropdown-meta',
                    options=[{'label': region, 'value': region} for region in regions],
                    value="ALL",
                    clearable=False
                ),
            ]),
            # Filtres supplémentaires
            html.Div(className="filters", children=[
                dcc.Checklist(
                    id='tournament-filter-meta',
                    options=[{'label': 'Tournament only', 'value': 'tournament'}],
                    value=[],
                    inline=True,
                    style={'margin-bottom': '20px'}
                ),
                dcc.Checklist(
                    id='gadget-rework-meta',
                    options=[{'label': 'After the gadget rework', 'value': '20250213'}],
                    value=[],
                    inline=True,
                    style={'margin-bottom': '20px'}
                ),
            ]),
        ]),
        
        # Conteneur pour la visualisation du méta
        html.Div(className="meta-visualization-container", children=[
            html.H2("Brawler Meta Analysis"),
            html.Div(id='meta-visualization')
        ]),
    ])

# Callback pour mettre à jour les cartes en fonction du mode sélectionné
@callback(
    Output('map-dropdown-meta', 'options'),
    [Input('mode-dropdown-meta', 'value')]
)
def update_map_dropdown_meta(selected_mode):
    if not selected_mode or selected_mode not in mode_to_maps:
        return []
    maps = mode_to_maps.get(selected_mode, [])
    return [{'label': map_name, 'value': map_name} for map_name in maps]

# Callback pour définir la valeur par défaut du dropdown de cartes
@callback(
    Output('map-dropdown-meta', 'value'),
    [Input('map-dropdown-meta', 'options')]
)
def set_default_map_meta(available_maps):
    if available_maps and len(available_maps) > 0:
        return available_maps[0]['value']
    return None

# Fonction pour analyser les méta-données des brawlers sur une carte spécifique
# Remplacer le filtrage par region_teams par un filtrage direct sur la colonne 'region'
def analyze_meta_data(df, selected_map, selected_region, tournament_filter, gadget_filter):
    filtered_df = df.copy()
    
    # Appliquer les filtres
    if tournament_filter and 'tournament' in tournament_filter:
        filtered_df = filtered_df[filtered_df['Type'] == 'tournament']
    
    if gadget_filter and '20250213' in gadget_filter:
        filtered_df['day_numeric'] = pd.to_numeric(filtered_df['day'], errors='coerce')
        filtered_df = filtered_df[filtered_df['day_numeric'] >= 20250213]
    
    # Filtrer par carte
    if selected_map:
        filtered_df = filtered_df[filtered_df['map'] == selected_map]
    
    # Nouveau filtrage par région
    if selected_region != "ALL":
        filtered_df = filtered_df[filtered_df['region'] == selected_region]
    
    if filtered_df.empty:
        return pd.DataFrame()
    
    # Collecter les données des brawlers
    brawler_data = []
    
    for idx, row in filtered_df.iterrows():
        # Traiter team1
        for i in range(1, 4):  # Brawlers 1 à 3
            brawler = row[f'brawler{i}']
            if pd.notna(brawler):
                result = row['team1 result']
                brawler_data.append({'Brawler': brawler, 'Result': result})
        
        # Traiter team2
        for i in range(4, 7):  # Brawlers 4 à 6
            brawler = row[f'brawler{i}']
            if pd.notna(brawler):
                # Inverser le résultat pour team2
                result = 'victory' if row['team1 result'] == 'defeat' else 'defeat'
                brawler_data.append({'Brawler': brawler, 'Result': result})
    
    # Convertir les données récoltées en DataFrame
    brawler_df = pd.DataFrame(brawler_data)
    
    if brawler_df.empty:
        return pd.DataFrame()
    
    # Calculer les statistiques pour chaque brawler
    brawler_counts = brawler_df['Brawler'].value_counts().reset_index()
    brawler_counts.columns = ['Brawler', 'Total Matches']
    
    victory_counts = brawler_df[brawler_df['Result'] == 'victory']['Brawler'].value_counts().reset_index()
    victory_counts.columns = ['Brawler', 'Victory Count']
    
    merged_df = pd.merge(brawler_counts, victory_counts, on='Brawler', how='left')
    merged_df['Victory Count'] = merged_df['Victory Count'].fillna(0)
    merged_df['Victory Rate (%)'] = (merged_df['Victory Count'] / merged_df['Total Matches']) * 100
    
    # Arrondir les colonnes numériques
    merged_df['Victory Count'] = merged_df['Victory Count'].astype(int)
    merged_df['Victory Rate (%)'] = merged_df['Victory Rate (%)'].round(2)
    
    # Ajouter le taux d'utilisation (Pick Rate)
    total_matches = brawler_df.shape[0] / 6  # Car il y a 6 brawlers par match
    merged_df['Pick Rate (%)'] = (merged_df['Total Matches'] / (total_matches * 2)) * 100  # *2 pour les 2 équipes
    merged_df['Pick Rate (%)'] = merged_df['Pick Rate (%)'].round(2)
    
    # Trier par nombre total de matchs (décroissant)
    merged_df = merged_df.sort_values('Total Matches', ascending=False)
    
    return merged_df

# Callback pour mettre à jour la visualisation du méta
@callback(
    Output('meta-visualization', 'children'),
    [Input('map-dropdown-meta', 'value'),
     Input('region-dropdown-meta', 'value'),
     Input('tournament-filter-meta', 'value'),
     Input('gadget-rework-meta', 'value')]
)
def update_meta_visualization(selected_map, selected_region, tournament_filter, gadget_filter):
    if not selected_map:
        return html.Div("Please select a map")
    
    stats_df = analyze_meta_data(load_data(), selected_map, selected_region, tournament_filter, gadget_filter)
    
    if stats_df.empty:
        return html.Div(f"No data available for {selected_map} in {selected_region} region")
    
    # Créer 3 tables HTML avec des icônes de brawlers
    # Déterminer les indices pour diviser le DataFrame en 3 parties
    total_rows = len(stats_df)
    first_cutoff = min(20, total_rows)
    second_cutoff = min(40, total_rows)
    
    # Créer les 3 tables
    tables = []
    
    for col_idx, (start_idx, end_idx) in enumerate([
        (0, first_cutoff),
        (first_cutoff, second_cutoff),
        (second_cutoff, total_rows)
    ]):
        # Ne créer une table que s'il y a des données pour cette plage
        if start_idx < end_idx:
            table_header = [
                html.Thead(html.Tr([
                    html.Th("Rank"), 
                    html.Th("Brawler"), 
                    html.Th("Icon"), 
                    html.Th("Total Matches"), 
                    html.Th("Pick Rate (%)"), 
                    html.Th("Victory Count"), 
                    html.Th("Victory Rate (%)")
                ]))
            ]
            
            rows = []
            for i, row in stats_df.iloc[start_idx:end_idx].iterrows():
                brawler_name = row['Brawler']
                rank = stats_df.index.get_loc(i) + 1  # Pour conserver le rang original
                
                # Vérifier si le brawler existe dans le dictionnaire brawler_icons
                icon_img = html.Img(
                    src=brawler_icons.get(brawler_name, ""), 
                    style={'height': '40px', 'width': '40px'},
                    alt=brawler_name
                ) if brawler_name in brawler_icons else html.Span(brawler_name[0].upper())
                
                # Créer la ligne du tableau avec rang
                table_row = html.Tr([
                    html.Td(rank),  # Rang
                    html.Td(brawler_name),
                    html.Td(icon_img),
                    html.Td(row['Total Matches']),
                    html.Td(f"{row['Pick Rate (%)']}%"),
                    html.Td(row['Victory Count']),
                    html.Td(f"{row['Victory Rate (%)']}%")
                ])
                
                rows.append(table_row)
            
            table_body = [html.Tbody(rows)]
            
            # Créer le tableau
            table = html.Table(
                table_header + table_body,
                style={
                    'width': '100%',
                    'borderCollapse': 'collapse',
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white',
                    'border': '1px solid #444',
                    'marginBottom': '20px'
                }
            )
            
            # Ajouter un titre pour chaque table
            if col_idx == 0:
                title = html.H4("Top Tier (1-20)")
            elif col_idx == 1:
                title = html.H4("Mid Tier (21-40)")
            else:
                title = html.H4(f"Lower Tier ({second_cutoff+1}-{total_rows})")
                
            tables.append(html.Div(
    [title, table],
    style={
        'flexGrow': '1',
        'flexBasis': '0',
        'minWidth': '30%',  # Assure une largeur minimale pour la lisibilité
        'maxWidth': '32%'   # Empêche les tableaux de devenir trop larges
    }
))
    
    # Créer un conteneur pour les 3 tables
    tables_container = html.Div(
        tables,
        style={
            'display': 'flex',
            'flexDirection': 'row',  # Changé de 'column' à 'row'
            'justifyContent': 'space-between',  # Répartit l'espace uniformément
            'width': '100%',
            'gap': '15px',  # Espace entre les tableaux
            'flexWrap': 'wrap'  # Pour qu'ils passent à la ligne sur les petits écrans
        }
    )
    
    # Ajouter des informations sur le méta
    total_picks = stats_df['Total Matches'].sum()
    total_brawlers = len(stats_df)
    top_10_picks = stats_df.head(10)['Total Matches'].sum()
    top_10_percentage = (top_10_picks / total_picks) * 100 if total_picks > 0 else 0
    
    meta_info = html.Div([
        html.H3(f"Meta Statistics for {selected_map} - {selected_region} Region"),
        html.P(f"Total unique brawlers: {total_brawlers}"),
        html.P(f"Top 10 brawlers make up {top_10_percentage:.2f}% of all picks"),
    ])
    
    return html.Div([
        meta_info,
        html.Div([
            tables_container
        ], style={'overflowX': 'auto'})
    ])