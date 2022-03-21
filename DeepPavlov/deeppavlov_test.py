from deeppavlov import build_model, configs
model = build_model(configs.syntax.syntax_ru_syntagrus_bert, download=True)
sentences = ["Я шёл домой по незнакомой улице.", "Девушка пела в церковном хоре."]
for parse in model(sentences):
    print(parse, end="\n\n")