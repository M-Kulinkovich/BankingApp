# MXA Banking app

## Application Features
* Registration and Login users
* View the profile 
* Send money from one user to another
* Incoming and Outgoing users transactions
* Download transactions in CSV files
* API with exchanges rates
* The ability for a bank employee to add money to other users
* The employee sees the transactions of all users
* Different interface for users and workers

## Installation

### 1. Сlone Repository & Install Packages
```
git clone https://github.com/M-Kulinkovich/BankingApp.git
pip install -r requirements.txt
```
### 2. Migrate & Start Server on localhost
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
##### 2. Start Server with Docker
```
docker-compose up --build
```
### 3. Run tests
```
python manage.py test
```
##### 3. Run tests with Docker
```
docker-compose run --rm django python manage.py test
```
### Displaying the exchange rate
To display the exchange rate, you need to get your personal API_KEY on the site
``
https://apilayer.com/marketplace/currency_data-api
``