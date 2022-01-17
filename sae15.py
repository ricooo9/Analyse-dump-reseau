import csv
import matplotlib.pyplot as plt

#on ouvre le fichier txt en spécifiant le chemin de celui-ci
file = open('C:/Users/33763/Desktop/Fichier_a_traiter.txt', "r")
#on va initialiser nos listes en les mettant vide pour y ajouter par la suite
#les infos que l'on souhaite classer
ipsource = []
ipdesti = []
length = []
flag=[]
numack=[]
numwin=[]
numseq=[]
request=[]
#on va initialiser des compteurs pour avoir des statistiques
compteurp = 0
compteurpoint = 0
compteurs = 0
compteurrequest = 0
compteurreply = 0
compteurtrame = 0
#on va supprimer les parties hexadécimales des trames pour plus de simplicité
#pour ça on va chercher ligne par ligne où IP est contenu dans la ligne
#on ajoutera à chaque compteur (de trames, de flag etc...) +1 lorsqu'on en détectera un
#on va également ajouter dans nos tableaux les IP sources-destinations
#on va aussi enlever les "," ou ";" qui pourrait être à la fin de nos infos de sorte à faciliter le compteur
for line in file:
    if "IP" in line:
        compteurtrame += 1
        if "[P.]" in line:
            compteurp += 1
            flag.append("[P.]")
        if "[.]" in line:
            compteurpoint += 1
            flag.append("[.]")
        if "[S]" in line:
            compteurs += 1
            flag.append("[S]")
        if "ack" in line:
            split=line.split(" ")
            if "seq" in line:
                a=split[10]
                split2=a.split(",")
                numack.append(split2[0])
            else:
                a=split[8]
                split2=a.split(",")
                numack.append(split2[0])
        if "win" in line:
            split=line.split(" ")
            if "seq" in line:
                if "ack" in line:
                    a=split[12]
                    split2=a.split(",")
                    numwin.append(split2[0])
                if "HTTP" in line:
                    a=split[-4]
                    split2=a.split(",")
                    numwin.append(split2[0])
            else:
                a=split[10]
                split2=a.split(",")
                numwin.append(split2[0])
        if "seq" in line :
            if "ICMP" in line:
                numseq.append(" ")
            else:
                split=line.split(" ")
                a=split[8]
                split2=a.split(",")
                numseq.append(split2[0])
        else:
            numseq.append(" ")
        if "ICMP" in line:
            if "request" in line:
                compteurrequest += 1
                request.append("Echo request")
            if "reply" in line:
                compteurreply += 1
                request.append("Echo reply")
        else:
            request.append(" ")
    if "length" in line:
        split = line.split(" ")
        if "HTTP" in line:
            a=split[-2]
            split2=a.split(":")
            length.append(split2[0])
        else:
            length.append(split[-1])
    if "IP" in line:
        split = line.split(" ")
        ipsource.append(split[2])
        ipdesti.append(split[4])

#on va créer des tableaux vides pour faire un 2ème tri et enlever les ports à la fin
ipsource2 = []
ipdesti2 = []
ipdestifinale=[]
#on passe à la suppresion des ports ou des éléments inutiles en fin d'adresse IP
for i in ipsource:
    if not "." in i:
        ipsource2.append(i)
    elif "ssh" in i or len(i) > 15 or "B" in i:
        ports = i.split(".")
        del ports[-1]
        delim = "."
        delim = delim.join(ports)
        ipsource2.append(delim)
    else:
        ipsource2.append(i)
for j in ipdesti:
    if not "." in j:
        ipdesti2.append(j)
    elif "ssh" in j or len(j) > 15 or "B" in j:
        ports = j.split(".")
        del ports[-1]
        delim = "."
        delim = delim.join(ports)
        ipdesti2.append(delim)
    else:
        ipdesti2.append(j)

for l in ipdesti2:
    if not ":" in l:
        ipdestifinale.append(l)
    else:
        deuxp = l.split(":")
        ipdestifinale.append(deuxp[0])

#fonction permettant de compter le nombre de fois qu'un élément apparaît et afficher l'élément en question
#le tout est contenu dans un dictionnaire
def compteurip(liste):
    return {k: liste.count(k) for k in liste}

#on met ces compteurs pour les adresse IP source dans la variable somme
#même chose dans la variable somme2
somme = compteurip(ipsource2)
somme2 = compteurip(ipdestifinale)

sommedescompteurs=compteurp+compteurs+compteurpoint
compt1=compteurp/sommedescompteurs
compt2=compteurs/sommedescompteurs
compt3=compteurpoint/sommedescompteurs

sommereplyrequest=compteurreply+compteurrequest
compt4=compteurrequest/sommereplyrequest
compt5=compteurreply/sommereplyrequest


name = ['Flag [P.]', 'Flag [S]', 'Flag[.]']
data = [compt1, compt2, compt3]


plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.savefig("C:/Users/33763/Desktop/graphique.png")
plt.show()

name2 = ['ICMP echo Request', 'ICMP echo Reply']
data2 = [compt4, compt5]

plt.pie(data2, labels=name2, autopct='%1.1f%%', startangle=90, shadow=True)
plt.savefig("C:/Users/33763/Desktop/graphique2.png")
plt.show()

#création d'une page web dans une variable, on l'appellera ensuite pour écrire le contenu de cette variable
#dans notre page web
texte = """<html

<head>

<center> <h1>Informations sur le fichier</h1> </center>
<center> <h2>Nombre de trames au total</h2> </center>
<br>
<center><table>
   <tr>
       <td>Trames dans ce fichier : </td>
       <td bgcolor="E8DADA"> %s </td>
   </tr>
</table>
</center>
<br>
<center> <h2>Fréquences des flags</h2> </center>
<center><img src="C:/Users/33763/Desktop/graphique.png"></center>
<center><table>
   <tr>
       <td>Flag [P.]: </td>
       <td bgcolor="E8DADA"> %s fois </td>
   </tr>
   <tr>
       <td>Flag [.]: </td> 
       <td bgcolor="E8DADA"> %s fois </td>
   </tr>
   <tr>
       <td>Flag [S]: </td>
       <td bgcolor="E8DADA"> %s fois </td>
   </tr>
</table>
</center>
<br>
<center> <h3> Nombre de request et de reply </h3> </center>
<center><img src="C:/Users/33763/Desktop/graphique2.png"></center>
<center><table>
   <tr>
       <td>Request : </td>
       <td bgcolor="E8DADA"> %s fois </td>
   </tr>
   <tr>
       <td>Reply : </td> 
       <td bgcolor="E8DADA"> %s fois </td>
   </tr>
   <tr>
</table>
</center>
<br>
<center> <h3> Légende des fréquences des IP sources et destination </h3> </center>
<br>
<center>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:#BBB23B; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span> Fréquence inférieur à 100 &nbsp&nbsp&nbsp</span></td>
</tr>
</table>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:blue; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>Fréquence > ou égal à 100 &nbsp</span></td>
</tr>
</table>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:#419C09; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>  Fréquence supérieur à 500 &nbsp</span></td>
</tr>
</table>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:#CB2C10; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>Fréquence supérieur à 1000</span></td>
</tr>
</table>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:#7F07AD; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>Fréquence supérieur à 2000</span></td>
</tr>
</table>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:#F769F1; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>Fréquence supérieur à 3000</span></td>
</tr>
</table>
</center>
<br><br>
<center> <h3> Fréquences des adresses IP sources </h3> </center>
<br>
<center>
</head>
</html>""" % (compteurtrame, compteurp, compteurpoint, compteurs, compteurrequest, compteurreply)


#on va créer la page web si elle n'existe pas 
#on va récupérer des valeurs de notre dictionnaire (les IP et leur nombre)
c = open('C:/Users/33763/Desktop/page.html', 'w')
c.write(texte)
a = somme.keys()
b = somme.values()
aa = somme2.keys()
bb = somme2.values()
vide = []

#création d'une colonne vide afin de faciliter l'aspect visuel de notre excel

for nombre in a:
    vide.append("              |")
compteurdip = 0

#écriture de nos adresses sources ainsi que leur fréquence dans la page web 

for y, z in zip(a, b):
    if compteurdip < 4:
        if z < 100:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#BBB23B>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 100 <= z < 500:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("blue>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 500 <= z < 1000:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#419C09>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 1000 <= z < 2000:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#CB2C10>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 2000 <= z < 3000:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#7F07AD>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif z > 3000:
            c.write(str(y))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#F769F1>")
            c.write(str(z))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
    if compteurdip == 4:
        c.write("<br><br>")
        compteurdip = 0
c.write("<center> <h3> Fréquences des adresse IP destination </h3> </center> <br>")
compteurdip=0

#écriture dans notre fichier HTML des adresses ip destination et leur fréquence
for yy, zz in zip(aa, bb):
    if compteurdip < 4:
        if zz < 100:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#BBB23B>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 100 <= zz < 500:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("blue>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 500 <= zz < 1000:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#419C09>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 1000 <= zz < 2000:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#CB2C10>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif 2000 <= zz < 3000:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#7F07AD>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
        elif zz > 3000:
            c.write(str(yy))
            c.write(" : ")
            c.write("<b>")
            c.write("<font color=")
            c.write("#F769F1>")
            c.write(str(zz))
            c.write("</font>")
            c.write("</b>")
            c.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp")
            compteurdip += 1
    if compteurdip == 4:
        c.write("<br><br>")
        compteurdip = 0
c.close()


#on transforme nos compteurs en liste de sorte à être utilisées dans le fichier excel
compteurp = [compteurp]
compteurpoint = [compteurpoint]
compteurs = [compteurs]
compteurrequest = [compteurrequest]
compteurreply = [compteurreply]
compteurtrame=[compteurtrame]

#écriture des données du fichier txt dans un premier fichier csv(excel)
with open('C:/Users/33763/Desktop/donnees.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['IP source', 'IP destination', 'Length', 'Flag', 'Numéro ACK', 'Numéro WIN', 'Numéro seq', 'ICMP Request/Reply'])
    writer.writerows(zip(ipsource2, ipdestifinale, length, flag, numack, numwin, numseq, request))
    fichiercsv.close()

#écriture des statistiques dans un second fichier csv (excel)
with open('C:/Users/33763/Desktop/statistiques.csv', 'w', newline='') as stat:
    writer = csv.writer(stat)
    writer.writerow(['Nombre Flag [P.]', 'Nombre Flag [.]', 'Nombre Flag [S]', 'Compteur de request', 'Compteur de reply', 'Nombre de trames'])
    writer.writerows(zip(compteurp, compteurpoint, compteurs, compteurrequest, compteurreply, compteurtrame))
    writer.writerow([' '])
    writer.writerows(zip())
    writer.writerow([' '])
    writer.writerows(zip())
    writer.writerow(['Adresse IP Source ', 'Fréquence', "              |", "Adresse IP Destination", "Fréquence"])
    writer.writerows(zip(a, b, vide, aa, bb))
    stat.close()

file.close()






