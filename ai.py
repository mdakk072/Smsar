from llama_cpp import Llama

# Initialisez l'objet Llama avec le chemin vers votre modèle
llm = Llama(model_path=r"D:\alpacaWind.cpp\ggml-alpaca-13b-q4.bin")

# Utilisez l'objet pour générer du texte
output = llm("Q: Name the planets in the solar system? A: ", max_tokens=32, stop=["Q:", "\n"], echo=True)

# Affichez le résultat
print(output)
