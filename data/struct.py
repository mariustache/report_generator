
from utils import Error


class Iesire:

    def __init__(self, nr_iesire, id_iesire, denumire, data, total, nr_bonuri):
        self.nr_iesire = nr_iesire
        self.id_iesire = id_iesire
        self.denumire = denumire
        self.data = data
        self.total = total
        self.nr_bonuri = nr_bonuri
    
    def pprint(self):
        output = ""
        output += "NUMAR:  {}\n".format(self.nr_iesire)
        output += "ID:     {}\n".format(self.id_iesire)
        output += "NUME:   {}\n".format(self.denumire)
        output += "DATA:   {}\n".format(self.data)
        output += "TOTAL:  {}\n".format(self.total)
        output += "BONURI: {}\n".format(self.nr_bonuri)
        print(output)

        
class Intrare:

    def __init__(self, id_intrare, nr_nir, nr_intrare, denumire, data, total, tip):
        self.id_intrare = id_intrare
        self.nr_nir = nr_nir
        self.nr_intrare = nr_intrare
        self.denumire = denumire
        self.data = data
        self.total = total
        self.tip = tip

        self.produse = list()
        self.total_vanz = 0
    
    def pprint(self):
        output = ""
        output += "ID:         {}\n".format(self.id_intrare)
        output += "NIR:        {}\n".format(self.nr_nir)
        output += "NUMAR:      {}\n".format(self.nr_intrare)
        output += "NUME:       {}\n".format(self.denumire)
        output += "DATA:       {}\n".format(self.data)
        output += "TOTAL:      {}\n".format(self.total)
        output += "TIP:        {}\n".format(self.tip)
        output += "NR PRODUSE: {}\n".format(len(self.produse))
        output += "TOTAL VANZ: {}\n".format(self.total_vanz)
        print(output)
    
    def AddProduct(self, produs):
        self.produse.append(produs)
        self.total_vanz += produs.total_vanz


class Produs:

    def __init__(self, id_u, id_intrare, denumire, den_gest, den_tip, tva_art, cantitate, pret_vanz):
        self.id_u = id_u
        self.id_intrare = id_intrare
        self.denumire = denumire
        self.den_gest = den_gest
        self.den_tip = den_tip
        self.tva_art = tva_art
        self.cantitate = float(cantitate)
        if pret_vanz is None:
            pret_vanz = 0
        self.pret_vanz = float(pret_vanz)
        self.total_vanz = self.cantitate * self.pret_vanz
    
    def pprint(self):
        output = ""
        output += "ID:             {}\n".format(self.id_u)
        output += "ID INTRARE:     {}\n".format(self.id_intrare)
        output += "NUME:           {}\n".format(self.denumire)
        output += "GESTIUNE:       {}\n".format(self.den_gest)
        output += "TIP:            {}\n".format(self.den_tip)
        output += "TVA:            {}%\n".format(self.tva_art)
        output += "CANTITATE:      {}\n".format(self.cantitate)
        output += "PRET VANZARE:   {}\n".format(self.pret_vanz)
        print(output)
    