from ipymarkup import show_dep_ascii_markup as show_markup
from razdel import sentenize, tokenize
from navec import Navec
from slovnet import Syntax
import re

# text = "Двойные латексные смотровые нестерильные неопудренные перчатки с индикацией прокола, размер S"
# text = "(Латексные) Смотровые нестерильные повышенной прочности перчатки HIGH RISK  (без пудры) Размер L"
# text = "Отвод стальной П 90˚ 1-60,3х4,0 Ст20 ГОСТ 17375-01"
# chunk = []
# for sent in sentenize(text):
#     tokens = [_.text for _ in tokenize(sent.text)]
#     chunk.append(tokens)
# chunk[:1]
# # [['Европейский', 'союз', 'добавил', 'в', 'санкционный', 'список', 'девять', 'политических', 'деятелей', 'из', 'самопровозглашенных', 'республик', 'Донбасса', '—', 'Донецкой', 'народной', 'республики', '(', 'ДНР', ')', 'и', 'Луганской', 'народной', 'республики', '(', 'ЛНР', ')', '—', 'в', 'связи', 'с', 'прошедшими', 'там', 'выборами', '.']]
#
# navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
# syntax = Syntax.load('slovnet_syntax_news_v1.tar')
# syntax.navec(navec)
#
# markup = next(syntax.map(chunk))
#
# # Convert CoNLL-style format to source, target indices
# words, deps = [], []
# for token in markup.tokens:
#     words.append(token.text)
#     source = int(token.head_id) - 1
#     target = int(token.id) - 1
#     if source > 0 and source != target:  # skip root, loops
#         deps.append([source, target, token.rel])
# show_markup(words, deps)


if __name__ == '__main__':
    navec = Navec.load('navec_news_v1_1B_250K_300d_100q.tar')
    syntax = Syntax.load('slovnet_syntax_news_v1.tar')
    syntax.navec(navec)
    stat = dict()
    with open(r'../results/razdel/syntax_stat_2.txt','w+') as out:
        with open("../resources/fullrequests.txt", 'r') as inp:
            for i, line in enumerate(inp.readlines()):
                if i %500 == 1:
                    print(i)
                chunk = []
                # for sent in sentenize(line):
                #     tokens = [_.text for _ in tokenize(sent.text)]
                #     chunk.append(tokens)
                splitted_words = [word for word in re.split('[,.\+](?!\d)|[^\w.,\\\/]+', line.lower()) if word != '']
                tokens = [_.text for _ in tokenize(line)]
                chunk.append(splitted_words)

                markup = next(syntax.map(chunk))

                for token in markup.tokens:
                    # out.write(token.text +" - "+ token.rel+'\n')
                    if token.rel not in stat.keys():
                        stat[token.rel] = dict()
                    if token.text not in stat[token.rel].keys():
                        stat[token.rel][token.text] = 0
                    stat[token.rel][token.text] += 1
                # words, deps = [], []
                # for token in markup.tokens:
                #     words.append(token.text)
                #     source = int(token.head_id) - 1
                #     target = int(token.id) - 1
                #     if source > 0 and source != target:  # skip root, loops
                #         deps.append([source, target, token.rel])
                # show_markup(words, deps)
                # out.write('------------------------\n')
                # print(markup.tokens)
            out.write(str(len(stat.keys()))+"\n")
            print(str(len(stat.keys())) + "\n")
            marklist = sorted(stat.items(), key=lambda x: -len(x[1].keys()))
            stat = dict(marklist)
            for key1,val1 in stat.items():
                marklist = sorted(val1.items(), key=lambda x: -x[1])
                val1 = dict(marklist)
                out.write(key1 + " --- ")
                print(key1 + " --- ")
                for key2,val2 in val1.items():
                    out.write("         ( "+ key2 + " , " + str(val2)+"),\n")
                    print("             ( "+ key2 + " , " + str(val2)+"), ")
                out.write("\n")


