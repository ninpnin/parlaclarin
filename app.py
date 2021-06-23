from pyparlaclarin.builder import parlaclarin_header, parlaclarin_preface, parlaclarin_body
from pyparlaclarin.builder import create_tei, create_parlaclarin
from pyparlaclarin.builder import create_u, create_note


global_header = parlaclarin_header(title="Parla Clarin Example file",
                                   authority="WESTAC",
                                   source_title="Kungliga Biblioteket",
                                   )
corpus_header = parlaclarin_header(title="Parla Clarin Example corpus",
                                   authority="WESTAC")
text_preface = parlaclarin_preface(date=["1999-01-01", "1999-01-02"])
body = parlaclarin_body()

intro = create_note(text="Herr Talmannen:", attrib=dict(type="speaker"))
body.append(intro)

u = create_u(text="Öääää.")
body.append(u)

note = create_u(text="This is a note.")
body.append(note)

corpus = create_tei(corpus_header, text_preface, body)
pc = create_parlaclarin(global_header, corpus)

print(pc)

f = open("pc.xml", "w")
f.write(pc)
f.close()