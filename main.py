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
    reines_placee = []

    def echiquier(self, taille):
        self.taille = taille
        self.echiquier = [[Cellule() for j in range(self.taille)] for i in range(self.taille)]
        self.initialiserEchiquier()


    def initialiserEchiquier(self):
        for x in range(self.taille):
            for y in range(self.taille):
                self.echiquier[x][y].cellule(x, y)


    def __repr__(self):
        ret_display = ""
        for x in range(self.taille):
            ret_display += "\n"
            for line in range(self.taille):
                ret_display += "----"
            ret_display += "\n"
            for y in range(self.taille):
                if y == 0:
                    ret_display += "| "
                ret_display += str(self.echiquier[x][y].type_occupation) + " | "
        return ret_display

    def modifierCellule(self, x, y, valeur):
        if x >= 0 and y >= 0 and x < 8 and y < 8:
            self.echiquier[x][y].setTypeOccupation(valeur)

    def placerReine(self, x, y):
        ret = self.echiquier[x][y].setTypeOccupationReine()
        if ret == Cellule.REINE:
            print("[placerReine] Cellule indisponible [{}][{}]: {}".format(x, y, ret))
        else:
            print("[placerReine] Reine placée en [{}][{}]".format(x, y))
            self.reines_placee.append((x, y))

            # Calcul menacée horizontale & verticale
            for i in range(self.taille):
               self.modifierCellule(x, i, Cellule.MENACEE)
               self.modifierCellule(i, y, Cellule.MENACEE)

            # Calcul des diagonales menacées
            for i in range(self.taille):
                self.modifierCellule(x-i, y-i, Cellule.MENACEE)
                self.modifierCellule(x-i, y+i, Cellule.MENACEE)
                self.modifierCellule(x+i, y-i, Cellule.MENACEE)
                self.modifierCellule(x+i, y+i, Cellule.MENACEE)

    def refreshEchiquier(self):
        # Set echiquier MENACEE to LIBRE
        for x in range(self.taille):
            for y in range(self.taille):
                self.echiquier[x][y].type_occupation = Cellule.LIBRE

        # Define Reine
        self.reines_placee.pop()
        for reine in self.reines_placee:
            self.placerReine(reine[0], reine[1])


    def recuperer_nbr_cellules_menacees(self):
        nbr_cases_menacees = 0
        for i in range(self.taille):
            for j in range(self.taille):
                if self.echiquier[i][j].type_occupation == 2:
                    nbr_cases_menacees += 1
        return nbr_cases_menacees

    def choixPlacementReine(self):

        nbr_cellules_menacees_pre = self.recuperer_nbr_cellules_menacees()
        nbr_cellules_menacees_min = nbr_cellules_menacees_pre
        x_reine, y_reine = (0, 0)
        for i in range(self.taille):
            for j in range(self.taille):
                if self.echiquier[i][j].type_occupation != Cellule.REINE:
                    self.placerReine(i, j)
                    if self.recuperer_nbr_cellules_menacees() < nbr_cellules_menacees_min:
                        nbr_cellules_menacees_min = self.recuperer_nbr_cellules_menacees()
                        x_reine = i
                        y_reine = j
                    self.refreshEchiquier()
        print(x_reine, y_reine)
        self.placerReine(x_reine, y_reine)
        return x_reine, y_reine

if __name__ == '__main__':
    echiquier = Echiquier()
    echiquier.echiquier(8)
    echiquier.placerReine(1, 1)
    print(echiquier)
    print(echiquier.reines_placee)
    echiquier.choixPlacementReine()
    print(echiquier)
