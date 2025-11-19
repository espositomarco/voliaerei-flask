import sys

from data_model.citta import Citta
from data_model.nazione import Nazione
from db.utils import load_nazioni, load_citta, store_nazione

if __name__ == "__main__":

    nazioni: dict[str, Nazione] = load_nazioni()
    print(nazioni)
    all_citta: dict[str, Citta] = load_citta(nazioni)
    print(all_citta)

    for nazione in nazioni.values():
        print(nazione.citta())


    italia: Nazione = nazioni.get('Italia')
    italia.set_fondazione(1947)

    francia: Nazione = nazioni.get('Francia')
    francia.set_fondazione(1900)


    sys.exit(0)
    italia: Nazione = Nazione(nome="Italia")
    jugo: Nazione = Nazione(nome="Jugo")

    roma: Citta = Citta(nome="Roma", abitanti=2_500_000, nazione=italia)
    fiume: Citta = Citta(nome="Fiume", abitanti=40_000, nazione=italia)

    fiume.set_nazione(jugo)
    fiume.set_nome("Rijeka")
    croazia: Nazione = Nazione(nome="Croazia")
    fiume.set_nazione(croazia)


    print(f"Città in italia: {italia.citta()}")
    print(f"Città in Jugoslavia: {jugo.citta()}")
    print(f"Città in Croazia: {croazia.citta()}")
