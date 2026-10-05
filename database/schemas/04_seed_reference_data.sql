-- ============================================
-- BANKS
-- ============================================

INSERT INTO monetic.dim_bank (bank_code, bank_name)
VALUES
    ('BACI', 'Banque Atlantique Côte d''Ivoire'),
    ('SGCI', 'Société Générale Côte d''Ivoire'),
    ('NSIA', 'NSIA Banque Côte d''Ivoire'),
    ('BDA', 'Banque de Développement de la Côte d''Ivoire'),
    ('SIB', 'Société Ivoirienne de Banque')
ON CONFLICT (bank_code) DO NOTHING;


-- ============================================
-- TRANSACTION TYPES
-- ============================================

INSERT INTO monetic.dim_transaction_type
    (transaction_code, transaction_name, channel, description)
VALUES
    ('ATM_WD', 'Retrait DAB', 'ATM', 'Retrait d''espèces sur DAB'),
    ('POS_PAY', 'Paiement TPE', 'POS', 'Paiement chez un commerçant'),
    ('TRANSFER', 'Virement', 'BANKING', 'Virement bancaire'),
    ('BAL_INQ', 'Consultation solde', 'ATM', 'Consultation du solde'),
    ('CASH_DEP', 'Dépôt espèces', 'ATM', 'Dépôt d''espèces'),
    ('ONLINE_PAY', 'Paiement en ligne', 'E_COMMERCE', 'Paiement sur Internet')
ON CONFLICT (transaction_code) DO NOTHING;


-- ============================================
-- RESPONSE CODES
-- ============================================

INSERT INTO monetic.dim_response_code
    (response_code, response_label, response_category, is_success)
VALUES
    ('00', 'Transaction approuvée', 'SUCCESS', TRUE),
    ('05', 'Transaction refusée', 'DECLINED', FALSE),
    ('14', 'Carte invalide', 'CARD_ERROR', FALSE),
    ('51', 'Fonds insuffisants', 'INSUFFICIENT_FUNDS', FALSE),
    ('54', 'Carte expirée', 'CARD_ERROR', FALSE),
    ('55', 'Code PIN incorrect', 'AUTHENTICATION_ERROR', FALSE),
    ('57', 'Transaction non autorisée', 'AUTHORIZATION_ERROR', FALSE),
    ('91', 'Émetteur indisponible', 'SYSTEM_ERROR', FALSE),
    ('96', 'Erreur système', 'SYSTEM_ERROR', FALSE)
ON CONFLICT (response_code) DO NOTHING;


-- ============================================
-- LOCATIONS
-- ============================================

INSERT INTO monetic.dim_location
    (city, district, region, country)
VALUES
    ('Abidjan', 'Cocody', 'District Autonome d''Abidjan', 'Côte d''Ivoire'),
    ('Abidjan', 'Plateau', 'District Autonome d''Abidjan', 'Côte d''Ivoire'),
    ('Abidjan', 'Marcory', 'District Autonome d''Abidjan', 'Côte d''Ivoire'),
    ('Abidjan', 'Yopougon', 'District Autonome d''Abidjan', 'Côte d''Ivoire'),
    ('Abidjan', 'Adjamé', 'District Autonome d''Abidjan', 'Côte d''Ivoire'),
    ('Bouaké', NULL, 'Gbêkê', 'Côte d''Ivoire'),
    ('Yamoussoukro', NULL, 'Bélier', 'Côte d''Ivoire'),
    ('San-Pédro', NULL, 'San-Pédro', 'Côte d''Ivoire'),
    ('Korhogo', NULL, 'Poro', 'Côte d''Ivoire'),
    ('Daloa', NULL, 'Haut-Sassandra', 'Côte d''Ivoire');


-- ============================================
-- MERCHANTS
-- ============================================

INSERT INTO monetic.dim_merchant
    (merchant_id, merchant_name, merchant_category, city)
VALUES
    ('MERCH0001', 'Supermarché Abidjan Centre', 'SUPERMARKET', 'Abidjan'),
    ('MERCH0002', 'Pharmacie Cocody', 'PHARMACY', 'Abidjan'),
    ('MERCH0003', 'Station Service Plateau', 'FUEL', 'Abidjan'),
    ('MERCH0004', 'Restaurant Marcory', 'RESTAURANT', 'Abidjan'),
    ('MERCH0005', 'Boutique Yopougon', 'RETAIL', 'Abidjan'),
    ('MERCH0006', 'Supermarché Bouaké', 'SUPERMARKET', 'Bouaké'),
    ('MERCH0007', 'Hôtel Yamoussoukro', 'HOTEL', 'Yamoussoukro'),
    ('MERCH0008', 'Commerce San-Pédro', 'RETAIL', 'San-Pédro')
ON CONFLICT (merchant_id) DO NOTHING;


-- ============================================
-- TERMINALS
-- ============================================

INSERT INTO monetic.dim_terminal
    (terminal_id, terminal_type, terminal_status, bank_key, city, location, installation_date)
SELECT
    'ATM0001', 'ATM', 'ONLINE', bank_key, 'Abidjan', 'Cocody', '2024-01-15'
FROM monetic.dim_bank
WHERE bank_code = 'BACI'
ON CONFLICT (terminal_id) DO NOTHING;

INSERT INTO monetic.dim_terminal
    (terminal_id, terminal_type, terminal_status, bank_key, city, location, installation_date)
SELECT
    'ATM0002', 'ATM', 'ONLINE', bank_key, 'Abidjan', 'Plateau', '2024-02-10'
FROM monetic.dim_bank
WHERE bank_code = 'SGCI'
ON CONFLICT (terminal_id) DO NOTHING;

INSERT INTO monetic.dim_terminal
    (terminal_id, terminal_type, terminal_status, bank_key, city, location, installation_date)
SELECT
    'ATM0003', 'ATM', 'ONLINE', bank_key, 'Abidjan', 'Marcory', '2024-03-05'
FROM monetic.dim_bank
WHERE bank_code = 'NSIA'
ON CONFLICT (terminal_id) DO NOTHING;

INSERT INTO monetic.dim_terminal
    (terminal_id, terminal_type, terminal_status, bank_key, city, location, installation_date)
SELECT
    'ATM0004', 'ATM', 'ONLINE', bank_key, 'Bouaké', 'Centre-ville', '2024-04-20'
FROM monetic.dim_bank
WHERE bank_code = 'SIB'
ON CONFLICT (terminal_id) DO NOTHING;

INSERT INTO monetic.dim_terminal
    (terminal_id, terminal_type, terminal_status, bank_key, city, location, installation_date)
SELECT
    'ATM0005', 'ATM', 'MAINTENANCE', bank_key, 'Yamoussoukro', 'Centre-ville', '2024-05-12'
FROM monetic.dim_bank
WHERE bank_code = 'BDA'
ON CONFLICT (terminal_id) DO NOTHING;