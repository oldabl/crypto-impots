# Crypto Impots
Calculer vos plus-values imposables* sur vos cryptomonnaies depuis vos documents Coinbase.

Les plateformes d'échange de cryptomonnaies ne fournissent pas d'imprimé fiscal unique pour déclarer ses plus-values aux impôts.

Ce programme va estimer votre portefeuille au moment des ventes de cryptos, pour en calculer la plus-value imposable par opération de vente, et synthétiser par année fiscale.

![image](https://github.com/oldabl/crypto-impots/assets/18029566/e4e68b8b-0908-41ef-a65a-87c0ffc3046f)

### 1. Téléchargez le code de ce repository

Clonez ce repository sur votre machine.

### 2. Ajouter vos relevés au format _.csv_ aux dossier _statements_

Tous les relevés doivent être présent, depuis l'ouverture de vos comptes jusqu'à la fin de l'année pour laquelle vous souhaitez évaluer vos plus-values, ou même jusqu'à aujourd'hui.

Compatible avec : **Coinbase seulement**

### 3. Téléchargez et installez le logiciel Docker Desktop

A télécharger ici : https://docs.docker.com/desktop/install/windows-install/

Laissez tous les réglages par défaut. Une fois installé, ouvrez Docker en mode Administrateur.

### 4. Lancez l'examen de vos relevés

Ouvrez un terminal Powershell en tant qu'Administrateur et placez vous dans le dossier du repository.

`docker image build -t crypto-impots:0.0.1 ./`

`docker run crypto-impots:0.0.1`

 Le programme vous donnera les plus-values à déclarer par année.
\
\
\
\
\
\* fournit une plus-value à titre indicatif. En aucun cas cet outil ou son concepteur n'est accrédité à faire ces calculs complexes de manière professionnelle. En aucun cas le développeur ayant écrit ce programme ne pourrait être tenu responsable d'une fausse déclaration.
