import matplotlib.pyplot as plt
import numpy
import os 
import sys

script_dir = os.path.dirname(__file__)
modulesPath = os.path.join(script_dir,"..","Test","Modules")
sys.path.append(modulesPath)

import cipherTools
def gen_ioc_graph(text : str, min_period = 1, max_period = 30):
    IoC = cipherTools.IoC()
    IoCData = {
        "min_period" : min_period,
        "max_period" : max_period,
        
        "text" : text.replace("\n","").replace(" ","")
    }

    periods = []
    iocs = []
    best_period, best_ioc = None,100
    threshold_ioc, first_pass = 1.4, None

    for period in range(IoCData["min_period"],IoCData["max_period"]+1):

        partitions = cipherTools.seperators(IoCData["text"],period)
        #rint(partitions)
        total_IoC = sum([IoC.ic(partition) for partition in partitions])/len(partitions) * 26

        iocs.append(total_IoC)
        periods.append(period)

        if abs(1.75-total_IoC)<abs(1.75-best_ioc):
            best_ioc, best_period = total_IoC, period

        if total_IoC>= threshold_ioc and first_pass == None:
            first_pass = [period,total_IoC]

    x = numpy.array(periods)
    y = numpy.array(iocs)


    plt.bar(x,y, color="steelblue")
    plt.bar(best_period,best_ioc,color="orange")

    plt.bar(first_pass[0],first_pass[1],color="#24FFAB")

    plt.axhline(1.75, label = "English IoC (1.75)", linestyle = "dashed", color = "red")
    plt.axhline(1,label = "Random text IoC (1)", linestyle = "dashed", color= "green",linewidth = 3)

    plt.legend() #adds key i think??

    plt.grid(axis="y", alpha = 0.4)

    plt.xlabel("Period")
    plt.ylabel("Index of Coincidence")
    plt.ylim(bottom = 0.6)
    plt.xticks(x)
    plt.title("IoC Comparisons", loc="left")

    plt.show()
if __name__ == "__main__":
    text = """XSIDIJAICIFLRVIWIEXVTPQMDIVLEWPOPRTVLRPWUBRTRSEFTPLQBAUHWPJ
XEZXWSSGPQUIPRAYEBWSIPAVMLHEFIEHJWMRIZBRRPQHJBXSEOIEMETRQGB
FTZWUXVHRZJOEZILTVQWNERTXDINGHZXTIEBRQPMQNMMGIYEGMICW"""
    gen_ioc_graph(text)