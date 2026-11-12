from database.distributore_DAO import DistributoreDAO
#importo anche il prezzo_DAO
from database.prezzo_DAO import PrezzoDAO
'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._distributori = None
        self.load_distributori()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

        #Li inserisco nell'init perchè vengono utilizzati per entrambe le funzioni da implementare
        #così queste operazioni vengono eseguite una volta sola
        self.prezziA = PrezzoDAO.get_prezzi(self._distributori[0].id)
        self.prezziB = PrezzoDAO.get_prezzi(self._distributori[1].id)

    def load_distributori(self):
        """ Carica tutti i distributori e li setta nella variabile self._distributori """
        self._distributori = DistributoreDAO.get_distributori()

    def get_prezzo_medio(self, mese:int):
        """
        Calcola, per ogni distributore, il prezzo medio al litro per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome del distributore, media), es. (Distributore A, 1.789)
        """
        n = 0
        somma = float(0)
        for i in self.prezziA:
            if i.data.month == int(mese):
                somma = somma + float(i.prezzo_litro)
                n = n + 1
        mediaA = somma / n


        n = 0
        somma = float(0)
        for i in self.prezziB:
            if i.data.month == int(mese):
                somma = somma + float(i.prezzo_litro)
                n = n + 1
        mediaB = somma / n

        return [mediaA,mediaB]



    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di rifornimenti nei primi 7 giorni
        :return: sequenza di nomi distributore ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        prezzi_settimana = self.__get_prezzi_prima_settimana_mese(mese)
        id = list(prezzi_settimana.keys())
        self.__ricorsione([], 1, None, 0, prezzi_settimana, id)

        # Traduci gli ID in nomi
        id_to_nome = {distributore.id: distributore.nome for distributore in self._distributori}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, round(self.__costo_ottimo, 2)

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_distributore, costo_corrente, prezzi_settimana, id):
        """ Implementa la ricorsione usando il pattern di Backtracking """

        # 1.
        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__costo_ottimo = costo_corrente
                self.__sequenza_ottima = sequenza_parziale.copy()
            return

        # 2.
        for ID in id:
            # Prendo il prezzo in questo modo perchè precedentemente sono stati ordinati per data
            prezzo_giorno = prezzi_settimana[ID][giorno - 1] * 100

            costo_oggi = prezzo_giorno

            if ultimo_distributore is not None and ultimo_distributore != ID:
                costo_oggi += 5

            nuovo_costo = costo_corrente + costo_oggi


            # 3.
            sequenza_parziale.append(ID)

            self.__ricorsione(sequenza_parziale, giorno + 1, ID, nuovo_costo, prezzi_settimana, id)

            sequenza_parziale.pop()




    def __get_prezzi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i prezzi dei primi 7 giorni del mese selezionato per ciascun distributore.
        :return: un dizionario: {id_distributore: [prezzo_giorno1, ..., prezzo_giorno7]}
        """
        id_A = self.prezziA[0].id_distributore
        id_B = self.prezziB[0].id_distributore

        dizionario = {id_A : [], id_B : []}

        self.prezziA = sorted(self.prezziA, key=lambda x: x.data)
        self.prezziB = sorted(self.prezziB, key=lambda x: x.data)

        for p in self.prezziA:
            if p.data.month == mese and p.data.day <= 7:
                dizionario[id_A].append(p.prezzo_litro)


        for p in self.prezziB:
            if p.data.month == mese and p.data.day <= 7:
                dizionario[id_B].append(p.prezzo_litro)


        return dizionario




