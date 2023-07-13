import requests

# Définir les informations de l'API Flask
api_host = 'localhost'  # Remplacez par l'adresse de votre API
api_port = 5000  # Remplacez par le port de votre API

# Endpoint pour obtenir les propriétés
proprietes_endpoint = f'http://{api_host}:{api_port}/get_record/Proprietes'
params = {'Etat': 'New'}
response = requests.get(proprietes_endpoint, params=params)

# Vérifier la réponse de la requête
if response.status_code == 200:
    # Succès - obtenir les propriétés avec l'état "NEW"
    data = response.json()
    proprietes_records = data
    print("Propriétés avec l'état 'NEW':")
    for propriete in proprietes_records:
        print(propriete)
else:
    # Échec - afficher le message d'erreur
    data = response.json()
    message = data['message']
    print("Échec de l'obtention des propriétés. Message d'erreur:", message)
