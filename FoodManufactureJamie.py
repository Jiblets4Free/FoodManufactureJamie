Hardness = {"V1":8.8,"V2":6.1,"O1":2.0,"O2":4.2,"O3":5.0}
JANCOSTS = {"V1": 110, "V2": 120, "O1": 130, "O2": 110, "O3": 115}
FEBCOSTS = {"V1": 130, "V2": 130, "O1": 110, "O2": 90, "O3": 115}
MARCOSTS = {"V1": 110, "V2": 140, "O1": 130, "O2": 100, "O3": 95}
APRCOSTS = {"V1": 120, "V2": 110, "O1": 120, "O2": 120, "O3": 125}
MAYCOSTS = {"V1": 100, "V2": 120, "O1": 150, "O2": 110, "O3": 105}
JUNCOSTS = {"V1": 90, "V2": 100, "O1": 140, "O2": 80, "O3": 135}
MonthlyCostsDict = {"JANCOSTS":JANCOSTS,"FEBCOSTS":FEBCOSTS,"MARCOSTS":MARCOSTS,"APRCOSTS":APRCOSTS,"MAYCOSTS":MAYCOSTS,"JUNCOSTS":JUNCOSTS}

FinalProductPricePerTon = 150
VegetableOilMonthlyRefineMaxTonnes = 200
OilMontlyRefineMaxTonnes = 250

EachRawOilMaxStorageTonnes = 1000
EachRawOilStorageCostTonnesPerMonth = 5

HardnessMax = 6
HardnessMin = 3

def CalculateCheapestOilCombinationsForOneMonth(AllMonthlyCostsDict,ThisMonthCostDict,HardnessDict):

    #Goes through each oil and calculates the cheapest that it could be when combined with each other oil
    # [Oil1,Oil2,ratio,CostPerTonne,NumberOfTonnesProducable]
    CheapestCostAsMainIngredient = []
    for i in ThisMonthCostDict:
        ListOfCosts = []
        for j in ThisMonthCostDict:
            #Calculates the ratio needed for oil "i" to be the maximum.
            if Hardness[i] == Hardness[j]:
                ratio = 1
                if Hardness[i] > 6 or Hardness[i] < 3:
                    ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],0])
                else:
                    if i[0] == "V" and j[0] == "V":
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],VegetableOilMonthlyRefineMaxTonnes])
                    elif i[0] == "O" and j[0] == "O":
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],OilMontlyRefineMaxTonnes])
                    else:
                        if OilMontlyRefineMaxTonnes > VegetableOilMonthlyRefineMaxTonnes:
                            ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],VegetableOilMonthlyRefineMaxTonnes*2])
                        else:
                            ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],OilMontlyRefineMaxTonnes*2])
            else:
                if Hardness[i] <= 6 and Hardness[i] >= 3:
                    ratio = 1
                    if i[0] == "V":
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],VegetableOilMonthlyRefineMaxTonnes])
                    else:
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i],OilMontlyRefineMaxTonnes])
                else:
                    if Hardness[i] > 6:
                        ratio = (6 - Hardness[j])/(Hardness[i] - Hardness[j])
                    elif Hardness[i] < 3:
                        ratio = (3 - Hardness[j])/(Hardness[i] - Hardness[j])
                    else:
                        print("error")

                    if i[0] == "V":
                        imax = VegetableOilMonthlyRefineMaxTonnes
                    else:
                        imax = OilMontlyRefineMaxTonnes
                    
                    if j[0] == "V":
                        jmax = VegetableOilMonthlyRefineMaxTonnes
                    else:
                        jmax = OilMontlyRefineMaxTonnes
                    
                    if imax * ratio < jmax * (1-ratio):
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i] * ratio + ThisMonthCostDict[j] * (1-ratio),jmax + jmax*(ratio/(1-ratio))])
                    else:
                        ListOfCosts.append([i,j,ratio,ThisMonthCostDict[i] * ratio + ThisMonthCostDict[j] * (1-ratio),imax + imax*((1-ratio)/ratio)])

        CheapestCostAsMainIngredient.append(ListOfCosts)

    #Nice Printing procedure
    """
    for row in CheapestCostAsMainIngredient:
        for collumn in row:
            print(collumn)
        print("\n")
    """

    #print(CheapestCostAsMainIngredient)

    #Finds the best profits.     ArrayFormat: [Oil1,Oil2,ratio,CostPerTon,NumberOfTonnesProducable,Profit]
    OverAllMostProfitCombination = [CheapestCostAsMainIngredient[0][0][0],CheapestCostAsMainIngredient[0][0][1],CheapestCostAsMainIngredient[0][0][2],CheapestCostAsMainIngredient[0][0][3],CheapestCostAsMainIngredient[0][0][4],CheapestCostAsMainIngredient[0][0][4] *(150 - CheapestCostAsMainIngredient[0][0][3])]
    for i in range(0,len(CheapestCostAsMainIngredient)):
        for j in range(0,len(CheapestCostAsMainIngredient[i])):
            #print(CheapestCostAsMainIngredient[i][j][4] * (150 - CheapestCostAsMainIngredient[i][j][3]))
            if CheapestCostAsMainIngredient[i][j][4] * (150 - CheapestCostAsMainIngredient[i][j][3]) > OverAllMostProfitCombination[5]:
                OverAllMostProfitCombination = [CheapestCostAsMainIngredient[i][j][0],CheapestCostAsMainIngredient[i][j][1],CheapestCostAsMainIngredient[i][j][2],CheapestCostAsMainIngredient[i][j][3],CheapestCostAsMainIngredient[i][j][4],CheapestCostAsMainIngredient[i][j][4] * (150 - CheapestCostAsMainIngredient[i][j][3])]
    
    print("\nCombine " + OverAllMostProfitCombination[0] + " with " + OverAllMostProfitCombination[1] + " with a ratio of " + str(round(OverAllMostProfitCombination[2],3)) + ":" + str(round(1-OverAllMostProfitCombination[2],3)) + "\nThis should give a profit of " + str('£{:,.2f}'.format(OverAllMostProfitCombination[5])) + "\n")
    return OverAllMostProfitCombination

TotalProfit = 0
for Month in MonthlyCostsDict:
    TotalProfit += CalculateCheapestOilCombinationsForOneMonth(MonthlyCostsDict,MonthlyCostsDict[Month],Hardness)[5]

print("Total Profit: " + str('£{:,.2f}'.format(TotalProfit)))

"""
First JAN Estimate: Combine V1 with O2 with a ratio of 0.391:0.609
                    This should give a profit of £16,428.57

First Total Estimate: Total profit: £116,785.71
"""

"""
TODO
 - Need to add cross month compatability in order to increase profits.
 - I think there is an issue with oils of the same type being combined in too great amounts inflating profits, see solution for FEB.
"""
