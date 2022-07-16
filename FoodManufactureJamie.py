from cmath import inf


Hardness = {"V1":8.8,"V2":6.1,"O1":2.0,"O2":4.2,"O3":5.0}
JANCOSTS = {"V1": 110, "V2": 120, "O1": 130, "O2": 110, "O3": 115}
FEBCOSTS = {"V1": 130, "V2": 130, "O1": 110, "O2": 90, "O3": 115}
MARCOSTS = {"V1": 110, "V2": 140, "O1": 130, "O2": 100, "O3": 95}
APRCOSTS = {"V1": 120, "V2": 110, "O1": 120, "O2": 120, "O3": 125}
MAYCOSTS = {"V1": 100, "V2": 120, "O1": 150, "O2": 110, "O3": 105}
JUNCOSTS = {"V1": 90, "V2": 100, "O1": 140, "O2": 80, "O3": 135}

FinalProductPricePerTon = 150
VegetableOilMonthlyRefineMaxTonnes = 200
OilMontlyRefineMaxTonnes = 250

EachRawOilMaxStorageTonnes = 1000
EachRawOilStorageCostTonnesPerMonth = 5

HardnessMax = 6
HardnessMin = 3

def CalculateCheapestOilCombinationsForOneMonth(MonthCostDict,HardnessDict):

    #Goes through each oil and calculates the cheapest that it could be when combined with each other oil
    BigArray = []
    CheapestCostAsMainIngredient = []
    for i in MonthCostDict:
        for j in MonthCostDict:
            #Calculates the ratio needed for oil "i" to be the maximum.
            ListOfCosts = []
            if Hardness[i] == Hardness[j]:
                ratio = 1
                if Hardness[i] > 6 or Hardness[i] < 3:
                    ListOfCosts.append([i,j,ratio,float("inf")])
                else:
                    ListOfCosts.append([i,j,ratio,MonthCostDict[i]])
            else:
                if Hardness[i] <= 6 and Hardness[i] >= 3:
                    ratio = 1
                    ListOfCosts.append([i,j,ratio,MonthCostDict[i]])
                else:
                    if Hardness[i] > 6:
                        ratio = (6 - Hardness[j])/(Hardness[i] - Hardness[j])
                    elif Hardness[i] < 3:
                        ratio = (3 - Hardness[j])/(Hardness[i] - Hardness[j])
                    else:
                        print("error")

                    ListOfCosts.append([i,j,ratio,MonthCostDict[i] * ratio + MonthCostDict[j] * (1-ratio)])            
            
            CheapestCostAsMainIngredient.append(ListOfCosts)
        BigArray.append(CheapestCostAsMainIngredient)

    #Nice Printing procedure
    for row in BigArray:
        for collumn in row:
            print(collumn)
        print("\n")

    #Finds the best profits, NEED TO CONSIDR THE MAXIMUM REFINEMENT REQUIREMENTS
    OverAllCheapestCombination = [CheapestCostAsMainIngredient[0][0][0],CheapestCostAsMainIngredient[0][0][1],CheapestCostAsMainIngredient[0][0][2],CheapestCostAsMainIngredient[0][0][3]]
    for i in range(0,len(CheapestCostAsMainIngredient)):
        for j in range(0,len(CheapestCostAsMainIngredient[i])):
            if CheapestCostAsMainIngredient[i][j][3] < OverAllCheapestCombination[3]:
                OverAllCheapestCombination = [CheapestCostAsMainIngredient[i][j][0],CheapestCostAsMainIngredient[i][j][1],CheapestCostAsMainIngredient[i][j][2],CheapestCostAsMainIngredient[i][j][3]]
    
    print(OverAllCheapestCombination)

CalculateCheapestOilCombinationsForOneMonth(JANCOSTS,Hardness)