import csv
import matplotlib.pyplot as plt

#we open the txt file by specifying its path
file = open('C:/Users/33763/Desktop/Fichier_a_traiter.txt', "r")
#we will initialize our lists by putting them empty to add what informations we want to them later

ipsource = []
ipdesti = []
length = []
flag=[]
numack=[]
numwin=[]
numseq=[]
request=[]
sourcerequest=[]
destireply=[]
#we will initialize our counters to have statistics
compteurp = 0
compteurpoint = 0
compteurs = 0
compteurrequest = 0
compteurreply = 0
compteurtrame = 0
#we will remove the hexadecimal parts of the frames for more simplicity
#for that we will search line by line where IP is contained in the line
#we will add to each counter (of frames, of flag etc...) +1 when we detect one
#we will also add in our lists the source-destination IPs
#we will also remove the "," or ";" which could be at the end of our infos so as to facilitate the counter
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
                split=line.split(" ")
                compteurrequest += 1
                request.append("Echo request")
                sourcerequest.append(split[2])
                a=split[4]
                split2=a.split(":")
                destireply.append(split2[0])
            if "reply" in line:
                split=line.split(" ")
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

#we will create empty arrays to do a 2nd sort and remove the ports at the end

ipsource2 = []
ipdesti2 = []
ipdestifinale=[]
machine=str(sourcerequest[0])
machine2=str(destireply[0])

#we move on to the deletion of ports or unnecessary elements at the end of the IP address (source and destination)

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


#function to count the number of times an element appears and display the element in question
#everything is contained in a dictionary
def compteurip(liste):
    return {k: liste.count(k) for k in liste}

#we put these counters for the source IP addresses in the sum variable
#same thing in the somme2 variable
somme = compteurip(ipsource2)
somme2 = compteurip(ipdestifinale)

#creation of percentage values ​​for use them in graphs, for flags as well as request/reply

sommedescompteurs=compteurp+compteurs+compteurpoint
compt1=compteurp/sommedescompteurs
compt2=compteurs/sommedescompteurs
compt3=compteurpoint/sommedescompteurs

sommereplyrequest=compteurreply+compteurrequest
compt4=compteurrequest/sommereplyrequest
compt5=compteurreply/sommereplyrequest

#creating the first graphic and saving it in png format
name = ['Flag [P.]', 'Flag [S]', 'Flag[.]']
data = [compt1, compt2, compt3]
colors = ['#00FF00','#FF2400','#0000FF']

plt.pie(data, labels=name, autopct='%1.1f%%', startangle=90, shadow=True, colors=colors)
plt.savefig("C:/Users/33763/Desktop/graphique.png")
plt.show()

#creation of the second graph and saving it in png format

name2 = ['ICMP echo Request', 'ICMP echo Reply']
data2 = [compt4, compt5]
colors = ['#FF2400','#0000FF']

plt.pie(data2, labels=name2, autopct='%1.1f%%', startangle=90, shadow=True, colors=colors)
plt.savefig("C:/Users/33763/Desktop/graphique2.png")
plt.show()


#creation of a web page in a variable, we will then call it to write the content of this variable
#in our webpage
#we will also use variables that we already have such as flag counters etc...
texte = """<html
<head>

<center> <h1>Informations sur le fichier</h1> </center>
<center> <h2>Nombre de trames au total</h2> </center>
<br>
<center><table>
   <tr>
       <td>Trames dans ce fichier : </td>
       <td bgcolor="F9D995"> %s </td>
   </tr>
</table>
</center>
<br>
<center> <h2>Fréquences des flags</h2> </center>
<center><img src="C:/Users/33763/Desktop/graphique.png"></center>
<center> <h4> Signification des différents Flags </h4> </center>
<center><B><p> "S"  ->  SYN&nbsp&nbsp
            "F"  ->  FIN&nbsp&nbsp
            "."  ->  ACK&nbsp&nbsp
            "P"  ->  PUSH&nbsp&nbsp
            "R"  ->  STOP&nbsp&nbsp
</p></B></center>
<center><table>
   <tr>
       <td>Flag [P.]: </td>
       <td bgcolor="F9D995"> %s fois </td>
   </tr>
   <tr>
       <td>Flag [.]: </td> 
       <td bgcolor="F9D995"> %s fois </td>
   </tr>
   <tr>
       <td>Flag [S]: </td>
       <td bgcolor="F9D995"> %s fois </td>
   </tr>
</table>
</center>
<br>
<center> <h3> Nombre de request et de reply </h3> </center>
<center><img src="C:/Users/33763/Desktop/graphique2.png"></center>
<center><table>
   <tr>
       <td>Request : </td>
       <td bgcolor="F9D995"> %s fois </td>
   </tr>
   <br>
   <tr>
       <td>Adresse source : </td>
       <td bgcolor="FD7F65"> %s </td>
   </tr>
</table></center>
<br>
<center>
<table>
   <tr>
       <td>Reply : </td> 
       <td bgcolor="F9D995"> %s fois </td>
   </tr>
   <tr>
       <td>Adresse destination : </td>
       <td bgcolor="FD7F65"> %s </td>
   </tr>
</table>
</center>
<br>
<center> <h3> Légende des fréquences des IP sources et destination </h3> </center>
<br>
<center>
<table border="0">
<tr><td>
<table border="1" width="20" height="5" style="background-color:blue; border-collapse:collapse"><tr><td>&nbsp;</td></tr></table>
<td><span>Fréquence > ou égal à 200 &nbsp</span></td>
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
<center> <h3> Fréquences des IP sources les plus élevées </h3> </center>
<br>
<center>
</head>
</body>
</html>""" % (compteurtrame, compteurp, compteurpoint, compteurs, compteurrequest,machine, compteurreply, machine2)


#we will create the web page if it does not exist
#we will take values ​​from our dictionary (the IPs and their number)
c = open('C:/Users/33763/Desktop/page.html', 'w')
c.write(texte)
a = somme.keys()
b = somme.values()
aa = somme2.keys()
bb = somme2.values()
vide = []

#creation of an empty column in order to facilitate the visual aspect of our excel

for nombre in a:
    vide.append("              |")
compteurdip = 0

#writing of our source addresses as well as their frequency in the web page
#we're going to put some color to highlight their frequency and space them out to make it clearer
#the color will be according to the color code defined just above in our HTML text variable

for y, z in zip(a, b):
    if compteurdip < 4:
        if 200 <= z < 500:
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
c.write("<center> <h3> Fréquences des IP destination les plus élévées </h3> </center> <br>")
compteurdip=0

#writing in our HTML file of destination ip addresses and their frequency
#we're going to put some color to highlight their frequency and space them out to make it clearer
#the color will be according to the color code defined just above in our HTML text variable

for yy, zz in zip(aa, bb):
    if compteurdip < 4:
        if 200 <= zz < 500:
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
c.write("<br><br>")
c.close()


#we transform our counters into a list so that they can be used in the excel file
compteurp = [compteurp]
compteurpoint = [compteurpoint]
compteurs = [compteurs]
compteurrequest = [compteurrequest]
compteurreply = [compteurreply]
compteurtrame=[compteurtrame]

#write data from txt file to a first csv file (excel)
with open('C:/Users/33763/Desktop/donnees.csv', 'w', newline='') as fichiercsv:
    writer = csv.writer(fichiercsv)
    writer.writerow(['IP source', 'IP destination', 'Length', 'Flag', 'Numéro ACK', 'Numéro WIN', 'Numéro seq', 'ICMP Request/Reply'])
    writer.writerows(zip(ipsource2, ipdestifinale, length, flag, numack, numwin, numseq, request))
    fichiercsv.close()

#write statistics to a second csv file (excel)
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






