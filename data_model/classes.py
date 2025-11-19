from __future__ import annotations
from data_model.custom_types import *

class Nazione:
    _index_nome: dict[str, Nazione] = {} # attributo di classe (statico)

    @classmethod
    def all(cls) -> dict[str, Nazione]:
        return dict(cls._index_nome)


    _nome: str  # {id} mutabile, noto alla nascita
    _citta: set[Citta] # da assoc. 'citta_naz' [0..*], possibilmente non noti alla nascita

    def __init__(self, nome: str, citta: set[Citta]|None = None) -> None:
        self.set_nome(nome)
        self._citta = set()
        if citta:
            for c in citta:
                c.set_nazione(self)

    def set_nome(self, nome: str) -> None:
        if nome in self._index_nome:
            raise KeyError(f"Esiste già una nazione con nome='{nome}'!")

        try:
            # sto modificando self
            self._index_nome.pop(self.nome()) # rimuove il vecchio nome dall'indice
        except AttributeError:
            # questo è il caso in cui self non aveva 'nome'
            pass
        self._nome = nome
        self._index_nome[nome] = self


    def nome(self) -> str:
        return self._nome

    def citta(self) -> frozenset[Citta]:
        return frozenset(self._citta)

    def _add_citta(self, c: Citta) -> None:
        self._citta.add(c)

    def _remove_citta(self, citta: Citta) -> None:
        try:
            self._citta.remove(citta)
        except KeyError as e:
            # e.add_note(f"La città {citta} non era nella nazione {self}!")
            raise ValueError(f"La città {citta} non era nella nazione {self}!")

    def __str__(self) -> str:
        return f"Nazione '{self.nome()}'"

    def __repr__(self) -> str:
        return f"Nazione(nome='{self.nome()}')"

    def info(self) -> dict[str, Any]:
        return {
            "nome": self._nome,
        }


class Citta:
    _nome: str  # mutabile, noto alla nascita
    _abitanti: IntGEZ # noto alla nascita
    _nazione: Nazione # da assoc. 'citta_naz' [1..1], nota alla nascita
    _aeroporti: set[Aeroporto] #certamente non noto alla nascita

    def __init__(self, nome: str, abitanti: IntGEZ, nazione: Nazione) -> None:
        self.set_nome(nome)
        self.set_abitanti(abitanti)
        self.set_nazione(nazione)
        self._aeroporti = set()

    def nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome

    def abitanti(self) -> IntGEZ:
        return self._abitanti

    def set_abitanti(self, abitanti: IntGEZ) -> None:
        self._abitanti = abitanti

    def nazione(self) -> Nazione:
        return self._nazione

    def set_nazione(self, nazione: Nazione) -> None:
        try:
            self._nazione._remove_citta(self)
        except AttributeError:
            pass
        self._nazione = nazione
        nazione._add_citta(self)

    def _add_aeroporto(self, aeroporto: Aeroporto) -> None:
        self._aeroporti.add(aeroporto)

    def aeroporti(self) -> frozenset[Aeroporto]:
        return frozenset(self._aeroporti)

    def __str__(self) -> str:
        return f"Citta '{self.nome()}' con {self.abitanti()} abitanti"

    def __repr__(self) -> str:
        return f"Citta(nome='{self.nome()}', abitanti='{self.abitanti()}', nazione='{self.nazione()}')"


    def info(self) -> dict[str, Any]:
        return dict(
            nome = self.nome(),
            abitanti = self.abitanti(),
            nazione = self.nazione(),
            aeroporti = self.aeroporti()
        )

class Compagnia:
    _nome: str # noto alla nascita
    _fondazione: IntGE1900 # immutabile, noto alla nascita
    _citta_direzione: Citta # da aggregazione 'citta_direzione', noto alla nascita
    _voli: set[Volo] # da assoc. 'volo_comp' [0..*], certamente non noti alla nascita

    def __init__(self, nome: str, fondazione: IntGE1900, citta: Citta) -> None:
        self.set_nome(nome)
        self._fondazione = fondazione
        self.set_citta_direzione(citta)
        self._voli = set()

    def nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome

    def fondazione(self) -> IntGE1900:
        return self._fondazione

    def set_citta_direzione(self, citta: Citta) -> None:
        self._citta_direzione = citta

    def citta_direzione(self) -> Citta:
        return self._citta_direzione

    def voli(self) -> frozenset[Volo]:
        return frozenset(self._voli)

    def _add_volo(self, volo: Volo) -> None:
        '''if volo.compagnia() != self:
            raise ValueError(f"Il volo è già della compagnia {volo.compagnia().nome()}!")'''
        self._voli.add(volo)

    def remove_volo(self, volo: Volo) -> None:
        self._voli.remove(volo)

    def __str__(self) -> str:
        return f"Compagnia '{self.nome()}' fondata nel {self.fondazione()}, con sede a {self.citta_direzione().nome()}"

    def info(self) -> dict[str, Any]:
        return dict(
            nome = self.nome(),
            fondazione = self.fondazione(),
            citta_direzione = self.citta_direzione(),
            voli = self.voli()
        )
class Aeroporto:
    _nome: str # noto alla nascita
    _codice: CodiceIATA # immutabile, noto alla nascita
    _citta: Citta # immutabile

    _voli_in_partenza: set[Volo] # certamente non noto alla nascita
    _voli_in_arrivo: set[Volo] # certamente non noto alla nascita

    def __init__(self, nome: str, codice: CodiceIATA | str, citta: Citta) -> None:
        self.set_nome(nome)
        if isinstance(codice, str):
            self._codice = CodiceIATA(codice)
        else:
            self._codice = codice
        self._codice = codice
        self._citta = citta
        citta._add_aeroporto(self)
        self._voli_in_partenza = set()
        self._voli_in_arrivo = set()

    def nome(self) -> str:
        return self._nome

    def set_nome(self, nome: str) -> None:
        self._nome = nome

    def codice(self) -> CodiceIATA:
        return self._codice

    def citta(self) -> Citta:
        return self._citta

    def voli_in_partenza(self) -> frozenset[Volo]:
        return frozenset(self._voli_in_partenza)

    def voli_in_arrivo(self) -> frozenset[Volo]:
        return frozenset(self._voli_in_arrivo)

    def _add_volo_in_partenza(self, volo: Volo) -> None:
        self._voli_in_partenza.add(volo)

    def _add_volo_in_arrivo(self, volo: Volo) -> None:
        self._voli_in_arrivo.add(volo)

    def __str__(self) -> str:
        return f"Aeroporto '{self.nome()}' ({self.codice()})"

    def info(self) -> dict[str, Any]:
        return dict(
            nome = self.nome(),
            codice = self.codice(),
            citta = self.citta(),
            voli_in_partenza = self.voli_in_partenza(),
            voli_in_arrivo = self.voli_in_arrivo()
        )

class Volo:
    _codice: CodiceVolo # immutabile, noto alla nascita
    _durata_minuti: IntGZ # noto alla nascita
    _compagnia: Compagnia # da assoc. volo_comp [1..1], immutabile, noto alla nascita
    _partenza: Aeroporto # immutabile
    _arrivo: Aeroporto # immutabile

    def __init__(self, codice: CodiceVolo, durata: IntGZ, compagnia: Compagnia,
                 partenza: Aeroporto, arrivo: Aeroporto) -> None:
        self._codice = codice
        self.set_durata_minuti(durata)
        self._compagnia = compagnia
        compagnia._add_volo(self)

        self._partenza = partenza
        self._arrivo = arrivo

        self._partenza._add_volo_in_partenza(self)
        self._arrivo._add_volo_in_arrivo(self)

    def codice(self) -> CodiceVolo:
        return self._codice

    def durata_minuti(self) -> IntGZ:
        return self._durata_minuti

    def set_durata_minuti(self, durata_minuti: IntGZ) -> None:
        self._durata_minuti = durata_minuti

    def compagnia(self) -> Compagnia:
        return self._compagnia

    def partenza(self) -> Aeroporto:
        return self._partenza

    def arrivo(self) -> Aeroporto:
        return self._arrivo


    def __str__(self) -> str:
        return f"Volo '{self.codice()}' di '{self.compagnia().nome()} con durata {self.durata_minuti()} minuti"

    def info(self) -> dict[str, Any]:
        return dict(
            codice = self.codice(),
            durata_minuti = self.durata_minuti(),
            compagnia = self.compagnia(),
            partenza = self.partenza(),
            arrivo = self.arrivo()
        )

if __name__ == "__main__":
    italia: Nazione = Nazione("Italia")
    print(italia)

    roma: Citta = Citta(nome="Roma", abitanti=IntGEZ(2.5*1e6), nazione=italia)
    milano: Citta = Citta(nome="Milano", abitanti=IntGEZ(2.5*1e6), nazione=italia)
    print(roma)
    francia: Nazione = Nazione("Francia")
    parigi: Citta = Citta(nome="Parigi", abitanti=IntGEZ(3.5*1e6), nazione=francia)


    padania: Nazione = Nazione("Padania", citta={milano})

    print(padania)
    print(padania.citta())

    print("città in italia:")
    print(italia.citta())

    magicfly: Compagnia = Compagnia(nome="Magicfly", fondazione=IntGE1900(1990), citta=milano)

    fco: Aeroporto = Aeroporto(nome="Aeroporto Internazionale Leonardo da Vinci",
                               codice=CodiceIATA("FCO"),
                               citta=roma)

    cdg: Aeroporto = Aeroporto(nome="Aéroport Charles de Gaulle", codice="CDG", citta=parigi)

    volo1: Volo = Volo(codice=CodiceVolo("MF0101"),
                       durata=IntGZ(120),
                       compagnia=magicfly,
                       partenza=fco,
                       arrivo=cdg)

    print(volo1)

