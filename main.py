import random


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
    reine_list = []

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
        ret_occupation = self.echiquier[x][y].setTypeOccupationReine()
        if ret_occupation == Cellule.REINE or ret_occupation == Cellule.MENACEE:
            # print("[placerReine] Cellule indisponible [{}][{}]: {}".format(x, y, ret))
            ret = False
        else:
            # print("[placerReine] Reine placée en [{}][{}]".format(x, y))
            ret = True
            self.reine_list.append((x, y))

            # Calcul menacée horizontale & verticale
            for i in range(self.taille):
                self.modifierCellule(x, i, Cellule.MENACEE)
                self.modifierCellule(i, y, Cellule.MENACEE)

            # Calcul des diagonales menacées
            for i in range(self.taille):
                self.modifierCellule(x - i, y - i, Cellule.MENACEE)
                self.modifierCellule(x - i, y + i, Cellule.MENACEE)
                self.modifierCellule(x + i, y - i, Cellule.MENACEE)
                self.modifierCellule(x + i, y + i, Cellule.MENACEE)
        return ret

    def reset_echiquier(self):
        for x in range(self.taille):
            for y in range(self.taille):
                self.modifierCellule(x, y, Cellule.LIBRE)

    def bestCombination(self, epoch_limit=1000, iterations_in_epoch=100):
        print("[bestCombination] bestCombination launched.")
        combinations_list = []
        for epoch in range(0, epoch_limit):
            print("[bestCombination] epoch: {} on {}".format(epoch + 1, epoch_limit))
            for i in range(0, iterations_in_epoch):
                random.seed(6)
                random.seed(a=None, version=2)
                x_reine = random.randint(0, self.taille - 1)
                y_reine = random.randint(0, self.taille - 1)
                self.placerReine(x_reine, y_reine)

            self.reset_echiquier()
            combinations_list.append(self.reine_list)

        # Debug combination
        # for combinaison in combinations_list:
        #     print("----")
        #     print(combination)
        #     print(len(combination))

        index_of_best_combination = 0
        for i, combination in enumerate(combinations_list):
            if len(combination) > index_of_best_combination:
                index_of_best_combination = i

        # Debug best combinaisons
        print("[bestCombination] Best combination is number: {}".format(i))
        print("[bestCombination] Best combination len: {}".format(len(combinations_list[i])))

        return combinations_list[i]


if __name__ == '__main__':
    echiquier = Echiquier()
    echiquier.echiquier(8)  # 8x8
    # echiquier.placerReine(1, 1)
    # print(echiquier)

    best_combination = echiquier.bestCombination(epoch_limit=500000, iterations_in_epoch=50)
    print("main: best_combination: {}".format(best_combination))
