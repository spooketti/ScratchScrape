import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import func 
from init import Session
from model.user import User

session = Session()
rawCountryData = session.query(User.country,func.count(User.country)).group_by(User.country).all()
countries = []
countryCount = []
seperatePie = []

for i in rawCountryData:
    countries.append(i[0])
    countryCount.append(i[1])
    seperatePie.append(0.02)

fig = plt.figure(figsize=(13,10))
plt.pie(countryCount,labels=countries,shadow=True, autopct=lambda p:f'{p:.2f}%, {p*sum(countryCount)/100 :.0f} users',explode=seperatePie)
plt.title("Scratch User Country Origins")
plt.legend(countries,title="Countries",loc="lower right")

# show plot
plt.show()