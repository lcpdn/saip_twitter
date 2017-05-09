# Le SAIP sur Twitter officieusement
Un bot qui tweete dès qu'une alerte est émise sur l'appli SAIP.
Ce bot envoie également un message Syslog à chaque nouvelle alerte. Le traitement dans un Splunk/ELK pourrait être sympa à terme.

Parce que le SAIP, c'est bien, mais c'est pas sur Twitter nativement. Le compte Twitter [@Saip_Officieux](https://twitter.com/saip_officieux) tweete dès qu'une nouvelle alerte est émise.

On pourra lire ce petit article que j'avais écrit: https://cloud.lcpdn.net/public/blog/cell-broadcast-quel-brodcast/ 

** Ce bot n'est évidemment pas à favoriser aux comptes officiels du Gouvernement, il n'y a aucune garantie de fonctionnement **

Evidemment, il n'y a pas de documentation officielle, on pourra lire ma prose rageuse à ce sujet ici: https://cloud.lcpdn.net/public/blog/application-pour-saip-ou-apis-pour-applications/ 

Pour le mettre sur son propre serveur ajouter un cron chaque minute lançant le script puis récupérer le fichier à T0:
wget https://3718fa66e6.optimicdn.com/alert_list.txt -O new.json --no-check-certificate

Le serveur retenu pour l'hosting du fichier d'alerte étant plus ou moins fiable, il est parfois nécessaire de recréer un fichier new.json. Le script test_fail.sh est une rustine (sale, je le reconnais) à ce problème.

La crontab suivante permet de lancer les scripts qui vont bien.
```bash
* * * * * python ~/saip.py
* * * * * . ~/test_fail.sh
```
