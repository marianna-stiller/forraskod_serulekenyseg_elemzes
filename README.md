# SQL Injection detektálás természetes nyelvi feldolgozó rendszerek és gépi tanulás által
Gépi tanuló algoritmusok és természetes nyelvi feldolgozó rendszerek alkalmazásával tanított program képes detektálni SQL injection típusú sérülékenységet.

Kulcsszavak: `felügyelt tanulás`, `train/test készlet`, `K-Fold`, `confusion matrix`, `recall`.

Előfeltételek:
* JDK 11 (https://www.oracle.com/java/technologies/javase-jdk11-downloads.html)
* Node.js (https://nodejs.dev/download)
* Python3 (https://www.python.org/downloads/)
* apache maven (https://maven.apache.org/download.cgi)
* php-parser 
```sh
npm install php-parser --save
```
* prettytable (https://pypi.org/project/prettytable/)
* numpy (https://numpy.org/install/)
* sklearn (https://scikit-learn.org/stable/install.html)
* pandas (https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
* matplotlib (https://matplotlib.org/stable/users/installing.html)

Lépések:
* cd machine_learning_app
* mvn compile test package
* mvn exec:java
