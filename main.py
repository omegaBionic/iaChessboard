

class Cellule:
    x = 0
    y = 0

    type_occupation = 0

    LIBRE = 0
    REINE = 1
    MENACEE = 2


    def cellule(self, x, y):
        self.x = x
        self.y = y
        self.type_occupation = self.LIBRE

    def setTypeOccupation(self, type_occupation):
        if self.type_occupation == self.LIBRE:
            self.type_occupation = type_occupation

    def setTypeOccupationReine(self):
        if self.type_occupation == self.LIBRE:
            self.type_occupation = self.REINE
            return self.LIBRE
        elif self.type_occupation == self.MENACEE:
            return self.MENACEE
        else:
            return self.REINE


class Echiquier:
    echiquier = []
    taille = 0

    def echiquier(self, taille):
        self.taille = taille
        self.echiquier = [[Cellule() for j in range(self.taille)] for i in range(self.taille)]
        self.initialiserEchiquier()


    def initialiserEchiquier(self):
        for x in range(self.taille):
            for y in range(self.taille):
                self.echiquier[x][y].cellule(x, y)


    def displayCellules(self):
        for x in range(self.taille):
            print("")
            for line in range(self.taille):
                print("----", end='')
            print("")
            for y in range(self.taille):
                # DEBUG: for display all cellules
                #print("case[{}][{}]: [{}]".format(x, y, self.echiquier[x][y].typeOccupation))

                if y == 0:
                    print("|", end='')
                print(" {} |".format(self.echiquier[x][y].type_occupation), end='')
        print("")

    def modifierCellule(self, x, y, valeur):
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            self.echiquier[x][y].setTypeOccupation(valeur)

    def placerReine(self, x, y):
        ret = self.echiquier[x][y].setTypeOccupationReine()
        if ret == Cellule.REINE or ret == Cellule.MENACEE:
            print("[placerReine] Cellule indisponible [{}][{}]: {}".format(x, y, ret))
        else:
            print("[placerReine] Reine placée en [{}][{}]".format(x, y))

            # Calcul menacée horizontale & verticale
            for i in range(self.taille):
               self.modifierCellule(x, i, Cellule.MENACEE)
               self.modifierCellule(i, y, Cellule.MENACEE)

            # Calcul des diagonales menacées
            for i in range(8):
                self.modifierCellule(x-i, y-i, Cellule.MENACEE)
                self.modifierCellule(x-i, y+i, Cellule.MENACEE)
                self.modifierCellule(x+i, y-i, Cellule.MENACEE)
                self.modifierCellule(x+i, y+i, Cellule.MENACEE)


if __name__ == '__main__':
    echiquier = Echiquier()
    echiquier.echiquier(8)
    echiquier.placerReine(1, 1)
    echiquier.displayCellules()
