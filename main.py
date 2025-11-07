# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

DATABASE = 'sandwichs.db'

# Initialisation de la base de données
def init_db():
    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA encoding = "UTF-8"')
    c = conn.cursor()

    # Table des sandwichs
    c.execute('''CREATE TABLE IF NOT EXISTS sandwichs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        ingredients TEXT NOT NULL,
        prix REAL NOT NULL,
        categorie TEXT DEFAULT 'Nos classiques'
    )''')

    # Table des responsables
    c.execute('''CREATE TABLE IF NOT EXISTS responsables (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL UNIQUE
    )''')

    # Table des commandes
    c.execute('''CREATE TABLE IF NOT EXISTS commandes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        personne TEXT NOT NULL,
        sandwich_id INTEGER NOT NULL,
        commentaire TEXT,
        paye INTEGER DEFAULT 0,
        responsable_id INTEGER,
        FOREIGN KEY (sandwich_id) REFERENCES sandwichs (id),
        FOREIGN KEY (responsable_id) REFERENCES responsables (id)
    )''')

    # Vérifier si des sandwichs existent déjà
    c.execute('SELECT COUNT(*) FROM sandwichs')
    if c.fetchone()[0] == 0:
        # Insérer des sandwichs par défaut (liste du restaurant)
        sandwichs_default = [
            # Nos classiques (simples)
            ('Jambon', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Fromage', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Poulet andalouse/curry/mayo', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Thon mayonnaise/cocktail/piquant', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Pain de viande', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Salade de pitta', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Salami', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Chorizo', 'Garnis avec salade, tomates, carottes à la demande', 3.00, 'Nos classiques'),
            ('Américain', 'Garnis avec salade, tomates, carottes à la demande', 3.20, 'Nos classiques'),
            ('Rôti de porc', 'Garnis avec salade, tomates, carottes à la demande', 3.20, 'Nos classiques'),
            ('Chèvre', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Brie', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Provolone', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Mozzarella fraîche', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Jambon de Parme/Ardenne', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Thon pêche', 'Garnis avec salade, tomates, carottes à la demande', 3.50, 'Nos classiques'),
            ('Salade de crabe', 'Garnis avec salade, tomates, carottes à la demande', 3.70, 'Nos classiques'),
            ('Boulette', 'Garnis avec salade, tomates, carottes à la demande', 4.00, 'Nos classiques'),
            ('Merguez', 'Garnis avec salade, tomates, carottes à la demande', 4.00, 'Nos classiques'),
            ('Poulet pané', 'Garnis avec salade, tomates, carottes à la demande', 4.00, 'Nos classiques'),
            ('Poulet grillé', 'Garnis avec salade, tomates, carottes à la demande', 4.00, 'Nos classiques'),
            ('Scampis à l\'ail', 'Garnis avec salade, tomates, carottes à la demande', 4.50, 'Nos classiques'),

            # Nos tentations
            ('DAGOBERT', 'Mayonnaise, jambon, fromage, oeufs, concombre, tomates, salade', 3.90, 'Nos tentations'),
            ('ANGLAIS', 'Ketchup, pain de viande, oeufs, oignons, salade', 3.50, 'Nos tentations'),
            ('VÉGÉTARIEN', 'Olives, aubergine, cornichons, tomates, concombre, carottes, salade, mayonnaise', 3.90, 'Nos tentations'),
            ('Feta', 'Fêta, sauce ail, oignons frais, concombre, tomates, salade', 3.90, 'Nos tentations'),
            ('MAYA', 'Brie, noix, salade, miel', 4.20, 'Nos tentations'),
            ('BRUGEOIS', 'Jambon, oeufs, asperges, salade, mayonnaise', 4.20, 'Nos tentations'),
            ('FERMIER', 'Andalouse, rôti, jambon, oeufs, tomates, carottes', 4.50, 'Nos tentations'),
            ('ARLEQUIN', 'Jambon d\'Ardennes, fromage, oeufs, tomates, salade', 4.50, 'Nos tentations'),
            ('EXOTIQUE', 'Jambon, fromage, ananas, pêches, mayonnaise', 4.50, 'Nos tentations'),
            ('SONO', 'Jambon d\'Ardennes, brie, salade, tomates', 4.50, 'Nos tentations'),
            ('DIET', 'Poulet grillé, fromage blanc, roquette, tomates', 4.50, 'Nos tentations'),
            ('GILLOU', 'Sauce piquante, américain, anchois, oeufs, tomates, salade', 4.70, 'Nos tentations'),
            ('MARTINO', 'Américain, sauce martino, anchois, oignons, cornichons', 4.70, 'Nos tentations'),
            ('ARDENNAIS', 'Sauce piquante, jambon d\'Ardennes, pain de viande, oeufs, tomates, salade', 4.90, 'Nos tentations'),

            # Nos paninis
            ('CAMARGUE', 'Huile d\'olive, jambon d\'Ardennes, mozzarella, tomates, oignons frais', 4.50, 'Nos paninis'),
            ('CORSE', 'Brie, gouda, mozzarella, fromage blanc, tomates', 4.50, 'Nos paninis'),
            ('MAISON', 'Jambon, mozzarella, tomates, poivrons, huile d\'olive, origan', 4.50, 'Nos paninis'),
            ('FAGNE', 'Jambon, mozzarella, fromage blanc, tomates', 4.50, 'Nos paninis'),
            ('POIVRE', 'Sauce au poivre, rôti, mozzarella, oignons, tomates', 4.50, 'Nos paninis'),
            ('DEK', 'Sauce martino, boulette, mozzarella, oignons frais', 4.50, 'Nos paninis'),
            ('TROPICAL', 'Jambon, gouda, ananas', 4.50, 'Nos paninis'),
            ('VENISE', 'Jambon de Parme, mozzarella, tomates, roquette', 5.00, 'Nos paninis'),
            ('LE CHÈVRE CHAUD', 'Fromage de chèvre, jambon d\'Ardennes, miel, raisins secs', 5.00, 'Nos paninis'),
            ('L\'AUTHENTIQUE', 'Gorgonzola, jambon de Parme, mozzarella, tomates, origan', 5.50, 'Nos paninis'),
            ('SAVEUR', 'Poulet pané, aubergine, mozzarella, huile d\'olives', 6.00, 'Nos paninis'),
            ('FUJI', 'Saumon, fromage blanc, tomates, roquette, oignons frais', 6.00, 'Nos paninis'),
            ('CATALAN', 'Poulet grillé, cheddar, chorizo, oignons sec, andalouse', 6.00, 'Nos paninis'),
            ('ELITE', 'Poulet pané, mozzarella, pomme de terre rôti, oignons frais, tomate, sauce poivre', 6.00, 'Nos paninis'),

            # Nos piadina
            ('CLASSICA', 'Mozzarella, jambon de Parme, roquette, tomates fraîches', 6.00, 'Nos piadina'),
            ('ANNA', 'Poulet pané, olives, tomates fraîches, mozzarella, sauce salsa diabla', 6.00, 'Nos piadina'),
            ('CORA', 'Pain de viande, mozzarella, fêta, olives, tomates, oignons frais, sauce poivre', 6.00, 'Nos piadina'),
            ('MIRELA', 'Mozzarella, aubergine, jambon de Parme, tomates fraîches', 6.00, 'Nos piadina'),
            ('VICTORIA', 'Jambon de Parme, mozzarella, gorgonzola, tomates fraîches', 6.00, 'Nos piadina'),
            ('PESCA', 'Saumon, mozzarella, fromage blanc, tomates, roquette, oignons frais', 6.00, 'Nos piadina'),
            ('CAPO', 'Mozzarella, fêta, jambon de Parme, roquette, tomates fraîches', 6.00, 'Nos piadina'),
            ('OLIVIA', 'Mozzarella, jambon de parme, tomates séchées, olives', 6.00, 'Nos piadina'),

            # Nos tendances
            ('NEW-YORKAIS', 'Américain, sauce martino, oignons secs, oignons frais, tomates, salade', 3.70, 'Nos tendances'),
            ('TOTO', 'Jambon de Parme, roquette, copeaux de parmesan, jus de citron, huile d\'olive', 4.20, 'Nos tendances'),
            ('DADDY', 'Poulet pané, miel, moutarde, oignons frais, salade', 4.50, 'Nos tendances'),
            ('DELY', 'Pain de viande, mozzarella, sauce barbecue, tomates, salade', 4.50, 'Nos tendances'),
            ('ITALIANO', 'Mozzarella fraîche, jambon de Parme, tomates, huile d\'olive, origan', 4.50, 'Nos tendances'),
            ('KOLOS', 'Pain de viande, feta, sauce à l\'ail, oignons, tomates', 4.50, 'Nos tendances'),
            ('USA-GRECO', 'Américain, feta, tomates, salade, oignons frais', 4.50, 'Nos tendances'),
            ('SAVOYARD', 'Chèvre, jambon d\'Ardennes, miel, salade', 4.80, 'Nos tendances'),
            ('PARMIGIANA', 'Aubergine, jambon de Parme, sauce bolognaise, parmesan râpé', 4.80, 'Nos tendances'),
            ('SPÉCIAL', 'Sauce piquante, chorizo, mozzarella, maïs, tomates, poivrons', 5.00, 'Nos tendances'),
            ('MATADOR', 'Sauce piquante, chorizo, feta, olives, tomates, salade', 5.00, 'Nos tendances'),
            ('TAHITI', 'Poulet pané, ananas, maïs, carottes, sauce brazil', 5.00, 'Nos tendances'),
            ('GENOVESE', 'Pesto vert, tomates séchées, jambon de Parme, aubergine', 5.20, 'Nos tendances'),
            ('NORVÉGIEN', 'Saumon, fromage blanc, oignons frais, salade, tomates', 5.20, 'Nos tendances'),
            ('NAPOLI', 'Mozza fraîche, câpres, olives, tomates, roquette, huile d\'olive, origan', 5.20, 'Nos tendances'),
            ('MIGUELITO', 'Poulet grillé, cheddar, pomme de terre, tomate, andalouse', 5.50, 'Nos tendances'),
            ('SICILIEN', 'Mozzarella, aubergine, anchois, tomates, copeaux de parmesan', 5.50, 'Nos tendances'),
            ('BRÉSILIEN', 'Sauce piquante, rôti, salami, fromage, ananas, maïs', 6.00, 'Nos tendances'),
            ('DOLCE', 'Poulet pané, aubergine, mozzarella, huile d\'olive, origan', 6.00, 'Nos tendances'),
            ('ROMA', 'Pané, provolone, olives, aubergines', 6.00, 'Nos tendances'),
            ('MONTAGNARD', 'Poulet pané, chèvre, miel/moutarde, oignons secs, oignons frais, roquette', 6.20, 'Nos tendances'),
            ('CORDON BLEU', 'Poulet pané, cheddar, jambon, salade, tomate, mayonnaise', 6.50, 'Nos tendances'),

            # Nos croques
            ('Croque-Monsieur', 'Jambon, fromage', 5.50, 'Nos croques'),
            ('Croqu\'Hawaïen', 'Jambon, fromage, ananas', 6.00, 'Nos croques'),
            ('Croqu\'ital', 'Jambon de Parme, tomates, mozzarella', 6.50, 'Nos croques'),
            ('Croqu\' blanc', 'Fromage, mozza, brie, tomates', 6.50, 'Nos croques'),

            # Nos salades
            ('GRECO', 'Fêta, jambon de Parme, tomates, concombre, oignons, olives, sauce pitta', 9.00, 'Nos salades'),
            ('L\'ARDENNAISE', 'Jambon d\'Ardennes, asperges, tomates, maïs, oeufs, vinaigrette à la ciboulette', 9.00, 'Nos salades'),
            ('LA GITANE', 'Boulette, oignons, œufs, cornichons, tomates, sauce au choix', 9.00, 'Nos salades'),
            ('L\'AUDACIEUSE', 'Poulet grillé, tomates, poivrons, maïs, oignons secs, sauce salsa', 9.00, 'Nos salades'),
            ('L\'IDÉAL', 'Poulet grillé, maïs, tomates, oeufs, mayo', 9.00, 'Nos salades'),
            ('LA TYPIQUE', 'Chèvre, jambon d\'Ardennes, raisins secs, noix, balsamique', 9.00, 'Nos salades'),
            ('LA SLAVE', 'Saumon, roquette, oignons frais, tomates, citron, poivre, sauce tartare', 9.00, 'Nos salades'),
            ('LA PAYSANNE', 'Jambon de Parme, aubergine, copeaux de parmesan, tomates, huile d\'olive, origan', 9.00, 'Nos salades'),
            ('LA JARDINIÈRE', 'Aubergine, tomates, concombre, oignons, vinaigre, cornichons, croûtons, huile balsamique', 9.00, 'Nos salades'),
            ('LA TOUNA', 'Thon à l\'huile d\'olive et citron, maïs, olives, tomates, balsamique', 9.00, 'Nos salades'),
            ('L\'ORIGINALE', 'Thon mayo, pêches, maïs, œufs, carottes, concombre', 9.00, 'Nos salades'),

            # Nos très spéciaux
            ('N°1', 'Poulet grillé, chorizo grillé, andalouse, fêta, oignons secs', 6.00, 'Nos très spéciaux'),
            ('N°2', 'Jambon de Parme, sauce 4 fromages, roquette, ananas, copeaux de parmesan', 6.00, 'Nos très spéciaux'),
            ('N°3', 'Boulette chaude, aubergine, sauce bolo, copeaux de parmesan', 6.00, 'Nos très spéciaux'),
            ('N°4', 'Pain de viande, aubergine, fêta, oignons frais, sauce poivre', 6.00, 'Nos très spéciaux'),
            ('N°5', 'Poulet pané, pesto vert, roquette, tomates séchées', 6.00, 'Nos très spéciaux'),

            # Nos Tentaburgers
            ('Hamburger', '', 3.00, 'Nos Tentaburgers'),
            ('DoubleBurger', '', 5.00, 'Nos Tentaburgers'),
            ('Mexicanos', '', 3.50, 'Nos Tentaburgers'),
            ('CheeseBurger', 'Fromage, oignons secs, salade', 4.50, 'Nos Tentaburgers'),
            ('CroustyBurger', '', 4.50, 'Nos Tentaburgers'),
            ('Bori Burger', 'Burger, cheddar, pomme de terre rôties, sauce burger', 5.50, 'Nos Tentaburgers'),
            ('Maxi Tentaburger', 'Mexicanos, burger, cheddar, sauce salsa diabla, oignons secs', 6.00, 'Nos Tentaburgers'),
            ('TentaBurger', 'Lard, fromage, sauce poivre', 6.00, 'Nos Tentaburgers'),
            ('Kebab poulet', '', 5.50, 'Nos Tentaburgers'),

            # Nos Pasta's
            ('BOLOGNAISE', 'Viande hachée porc/bœuf, sauce tomate', 6.50, 'Nos Pasta\'s'),
            ('4 FROMAGES', 'Gorgonzola, mozzarella, gruyère, parmesan', 6.50, 'Nos Pasta\'s'),
            ('ARRABIATTA', 'Sauce tomate, olives, basilic, harissa', 6.50, 'Nos Pasta\'s'),
            ('CARBONARA', 'Crème, lardons, oignons', 6.50, 'Nos Pasta\'s'),
            ('PESTO', 'Pesto verde', 6.50, 'Nos Pasta\'s'),
            ('FROMA\'VERDE', 'Sauce 4 fromages, pesto vert', 6.50, 'Nos Pasta\'s'),
            ('PARMIGIANA', 'Sauce bolo, aubergine', 7.50, 'Nos Pasta\'s'),

            # Propo
            ('Propo du chef', 'Proposition du jour', 7.00, 'Propo'),
            ('Soupe de la semaine', 'Soupe du jour', 2.80, 'Propo'),

            # Boissons
            ('Coca normal 33cl', '', 1.80, 'Boissons'),
            ('Coca zéro 33cl', '', 1.80, 'Boissons'),
            ('Fanta orange 33cl', '', 1.80, 'Boissons'),
            ('Eau plate 50cl', '', 1.80, 'Boissons'),
            ('Eau pétillante 50cl', '', 1.80, 'Boissons'),
            ('Ice Tea pétillant 33cl', '', 2.00, 'Boissons'),
            ('Jupiler 33cl', '', 2.50, 'Boissons'),
            ('Tropico 33cl', '', 2.00, 'Boissons'),
            ('Ice Tea pêche 33cl', '', 2.00, 'Boissons')
        ]
        c.executemany('INSERT INTO sandwichs (nom, ingredients, prix, categorie) VALUES (?, ?, ?, ?)', sandwichs_default)

    # Vérifier si des responsables existent déjà
    c.execute('SELECT COUNT(*) FROM responsables')
    if c.fetchone()[0] == 0:
        # Insérer les responsables par défaut (ordre alphabétique)
        responsables_default = [
            ('Adriano',),
            ('Anne',),
            ('Blaise',),
            ('Boris',),
            ('Cédric',),
            ('Charlynne',),
            ('Chris',),
            ('Christelle',),
            ('Christophe',),
            ('Claude',),
            ('Elodie',),
            ('Emilie',),
            ('Etienne',),
            ('Garance',),
            ('Géraldine',),
            ('Houria',),
            ('Ingrid',),
            ('Jean',),
            ('Johanna',),
            ('Justine',),
            ('Laurence',),
            ('Léa',),
            ('Manon',),
            ('Manuel',),
            ('Michaël',),
            ('Monalisa',),
            ('Nathalie',),
            ('Olivier',),
            ('Oscar',),
            ('Patricia',),
            ('Rachel',),
            ('Romina',),
            ('Sabrina',),
            ('Sarah',),
            ('Séverine',),
            ('Talissa',),
            ('Thibaud',),
            ('Yannick',)
        ]
        c.executemany('INSERT INTO responsables (nom) VALUES (?)', responsables_default)

    conn.commit()
    conn.close()

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# API: Obtenir tous les sandwichs
@app.route('/api/sandwichs', methods=['GET'])
def get_sandwichs():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM sandwichs')
    sandwichs = []
    for row in c.fetchall():
        sandwichs.append({
            'id': row[0],
            'nom': row[1],
            'ingredients': row[2],
            'prix': row[3],
            'categorie': row[4] if len(row) > 4 else 'Nos classiques'
        })
    conn.close()
    return jsonify(sandwichs)

# API: Ajouter une commande
@app.route('/api/commandes', methods=['POST'])
def add_commande():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    date = data.get('date', datetime.now().strftime('%Y-%m-%d'))
    personne = data['personne']
    sandwich_id = data['sandwich_id']
    commentaire = data.get('commentaire', '')
    paye = data.get('paye', 0)
    responsable_id = data.get('responsable_id', None)

    c.execute('INSERT INTO commandes (date, personne, sandwich_id, commentaire, paye, responsable_id) VALUES (?, ?, ?, ?, ?, ?)',
              (date, personne, sandwich_id, commentaire, paye, responsable_id))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Commande ajoutée avec succès'})

# API: Obtenir l'historique des commandes (15 derniers jours)
@app.route('/api/commandes', methods=['GET'])
def get_commandes():
    date_limite = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        SELECT c.id, c.date, c.personne, s.nom, s.prix, c.commentaire, c.paye, r.nom
        FROM commandes c
        JOIN sandwichs s ON c.sandwich_id = s.id
        LEFT JOIN responsables r ON c.responsable_id = r.id
        WHERE c.date >= ?
        ORDER BY c.date DESC, c.id DESC
    ''', (date_limite,))

    commandes = []
    for row in c.fetchall():
        commandes.append({
            'id': row[0],
            'date': row[1],
            'personne': row[2],
            'sandwich': row[3],
            'prix': row[4],
            'commentaire': row[5],
            'paye': row[6],
            'responsable': row[7]
        })

    conn.close()
    return jsonify(commandes)

# API: Marquer une commande comme pay�e
@app.route('/api/commandes/<int:id>/payer', methods=['PUT'])
def marquer_paye(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE commandes SET paye = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Commande marquée comme payée'})

# API: Marquer une commande comme non payée
@app.route('/api/commandes/<int:id>/non-payer', methods=['PUT'])
def marquer_non_paye(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE commandes SET paye = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Commande marquée comme non payée'})

# API: Modifier une commande
@app.route('/api/commandes/<int:id>', methods=['PUT'])
def update_commande(id):
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    personne = data['personne']
    commentaire = data.get('commentaire', '')
    paye = data.get('paye', 0)

    c.execute('UPDATE commandes SET personne = ?, commentaire = ?, paye = ? WHERE id = ?',
              (personne, commentaire, paye, id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Commande modifiée avec succès'})

# API: Supprimer une commande
@app.route('/api/commandes/<int:id>', methods=['DELETE'])
def delete_commande(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM commandes WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Commande supprimée'})

# API: Ajouter un sandwich
@app.route('/api/sandwichs', methods=['POST'])
def add_sandwich():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    nom = data['nom']
    ingredients = data['ingredients']
    prix = data['prix']
    categorie = data.get('categorie', 'Nos classiques')

    c.execute('INSERT INTO sandwichs (nom, ingredients, prix, categorie) VALUES (?, ?, ?, ?)',
              (nom, ingredients, prix, categorie))

    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Sandwich ajouté avec succès'})

# API: Modifier un sandwich
@app.route('/api/sandwichs/<int:id>', methods=['PUT'])
def update_sandwich(id):
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    nom = data['nom']
    ingredients = data['ingredients']
    prix = data['prix']
    categorie = data.get('categorie', 'Nos classiques')

    c.execute('UPDATE sandwichs SET nom = ?, ingredients = ?, prix = ?, categorie = ? WHERE id = ?',
              (nom, ingredients, prix, categorie, id))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Sandwich modifié avec succès'})

# API: Supprimer un sandwich
@app.route('/api/sandwichs/<int:id>', methods=['DELETE'])
def delete_sandwich(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM sandwichs WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Sandwich supprimé'})

# API: Obtenir tous les responsables
@app.route('/api/responsables', methods=['GET'])
def get_responsables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM responsables ORDER BY nom')
    responsables = []
    for row in c.fetchall():
        responsables.append({
            'id': row[0],
            'nom': row[1]
        })
    conn.close()
    return jsonify(responsables)

# API: Ajouter un responsable
@app.route('/api/responsables', methods=['POST'])
def add_responsable():
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    nom = data['nom']

    try:
        c.execute('INSERT INTO responsables (nom) VALUES (?)', (nom,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Responsable ajouté avec succès'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Ce responsable existe déjà'}), 400

# API: Modifier un responsable
@app.route('/api/responsables/<int:id>', methods=['PUT'])
def update_responsable(id):
    data = request.json
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    nom = data['nom']

    try:
        c.execute('UPDATE responsables SET nom = ? WHERE id = ?', (nom, id))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Responsable modifié avec succès'})
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'success': False, 'message': 'Ce nom existe déjà'}), 400

# API: Supprimer un responsable
@app.route('/api/responsables/<int:id>', methods=['DELETE'])
def delete_responsable(id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM responsables WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return jsonify({'success': True, 'message': 'Responsable supprimé'})

# API: Obtenir les statistiques
@app.route('/api/stats', methods=['GET'])
def get_stats():
    date_limite = (datetime.now() - timedelta(days=15)).strftime('%Y-%m-%d')

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    # Total des commandes non payées
    c.execute('''
        SELECT SUM(s.prix)
        FROM commandes c
        JOIN sandwichs s ON c.sandwich_id = s.id
        WHERE c.paye = 0 AND c.date >= ?
    ''', (date_limite,))
    total_non_paye = c.fetchone()[0] or 0

    # Total des commandes payées
    c.execute('''
        SELECT SUM(s.prix)
        FROM commandes c
        JOIN sandwichs s ON c.sandwich_id = s.id
        WHERE c.paye = 1 AND c.date >= ?
    ''', (date_limite,))
    total_paye = c.fetchone()[0] or 0

    conn.close()

    return jsonify({
        'total_non_paye': round(total_non_paye, 2),
        'total_paye': round(total_paye, 2),
        'total_general': round(total_non_paye + total_paye, 2)
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=8080)
