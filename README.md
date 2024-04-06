# Crypto Impots
Calculer vos impôts depuis vos documents Coinbase.

Le site Coinbase ne fournit pas de relevé pour déclarer ses plus-value aux impôts. Ce programme va estimer votre portefeuille au moment des ventes de cryptos, pour en calculer la plus-value imposable par opération de vente.

### 1. Téléchargez le code de ce repository

Téléchargez directement le code de ce repo sur votre disque.

### 2. Ajouter vos relevés au format _.csv_ aux dossier _statements_

Tous les relevés doivent être présent, depuis l'ouverture de votre compte Coinbase.

### 3. Téléchargez et installez le logiciel Docker Desktop

A télécharger ici : https://docs.docker.com/desktop/install/windows-install/

Laissez tous les réglages par défaut. Une fois installé, ouvrez Docker en mode Administrateur.

### 4. Lancez l'examen de vos relevés

Ouvrez un terminal Powershell en tant qu'Administrateur et placez vous dans le dossier du code.

`docker image build -t crypto-impots:0.0.1 ./`

`docker run crypto-impots:0.0.1`

 Le programme vous donnera les plus-value à déclarer par année.
