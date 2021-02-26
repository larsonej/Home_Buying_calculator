#fhb.py
# To determine if buying a house is really a good option, and what we
# should buy.  
#ALL values in thousands of dollars

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


#START user inputs ==================
#Street name of the house, to keep track of different properties
name='YT'
loc='som' # med, som, cam, arl These are different cities near us with different property tax rates
price=530.00  #price in thousands
hoa = 0.00 # monthly HOA fees
dp=.15*price  # down payment

#mortgage specs, numbers are in $1000 ============
apr=0.03 # annual percent rate  
cc = 5. #0.015*price  # closing cost estimate

# monthly house costs ============
mi=.077 #(price-dp)*.0031/12.  #mortgate insurance until 20% equity
maintenance = 0.1             #monthly maintenance
hi = 0.030   # home owners insurance
elec=0.0
internet=0.00
bills=elec+internet

# Calculate local property tax ===================
pt=0.08
if loc == 'cam':
  pt = 0.007/12.*price*.87  # property tax per month
if loc == 'som' or loc == 'arl':
  pt = 0.012/12*price*.87  # property tax per month
if loc == 'med':
  pt = 0.01056/12.*price*.87


# economy assumptions =======================
infl=.025 #inflation of 2.5%
inflate=np.power(1.+infl/12.,np.arange(361))
inv=0.045 # investment return on down payment (in leiu of homebuying) of 6.5%

#rent assumptions
initrent = 2.0 # initial monthly rent cost


#END of user inputs ==========================================


yr=np.arange(361)/12.

#CALCULATING MORTGAGE PAYMENT IN $10 INCREMENTS - needs adjustment for
#                                              different home prices
n=201
payment= ((np.arange(n,dtype=float)/(n-1))-.5)+(price-dp)/220. #Guessing around $100/20k
finaleq=np.arange(n,dtype=float)
for p in np.arange(n):
  loan=price-dp
  equity=dp
  for i in np.arange(361):
    interest = apr/12.*loan
    equity = equity + payment[p] - interest
    loan=price-equity
    #print( i,' loan',loan, '  equity', equity)
  finaleq[p]=equity

#plot, payment, abs(finaleq-price), xtitle='payment', ytitle='difference between price and final equity', charthick=3, thick=3, charsize=1.5

dummy=np.abs(finaleq-price,dtype=float)
ind=np.where(dummy == np.amin(dummy)) #mortgage rate
mr=payment[ind]
#print('ind',ind, 'mr',mr)


#CALCULATING EQUITY IN HOME OVER TIME
loan=price-dp
equ=np.zeros(361)    # equity over time
equ[0]=dp
for i in np.arange(361)[1:361]:
    interest = apr*loan/12.
    equ[i] = equ[i-1] + mr - interest
    loan=price-equ[i]
#    print( i,' loan',loan, '  equity', equ[i])

fig1,ax=plt.subplots()
ax.plot(yr,equ)
ax.set(xlabel='Year',ylabel='Equity, $1000')
fig1.savefig(name+'Equity.png')
plt.show()

# CALCULATE MONTHLY AND TOTAL COSTS
if equ[0] >= 0.2*price:
  monthly=(np.zeros(361)+mr[0])+(hoa+maintenance+pt+hi)*inflate # calculate monthly costs associated with house
else: 
  ind=np.amin(np.where(equ >= 0.2*price)) # when mortgage insurance stops
  mitot=np.zeros(361,dtype=float)
  mitot[0:ind+1]=mi
  monthly=(np.zeros(361,dtype=float)+mr[0])+(np.zeros(361,dtype=float)+hoa+maintenance+pt+hi)*inflate+mitot # calculate monthly costs associated with house

print( 'mortgage', mr, ' monthly cost', monthly[0])
totalbuycost=np.cumsum(monthly)+cc # calcuate cumulative cost associated with house and closing
mc=monthly[0]

#CALCULATE HOW MUCH RENTING WILL COST
# cumulative rent cost
rent = np.cumsum(initrent*inflate)

fig2,ax=plt.subplots()
ax.plot(yr,monthly, label='Buying')
ax.plot(yr,initrent*inflate,label='Renting')
ax.set(xlabel='Year',ylabel='Monthly cost, $1000')
fig2.savefig(name+'Mortgage-vs-rent.png')
ax.legend()
plt.show()

fig3,ax=plt.subplots()
ax.plot(yr,totalbuycost, label='Buy Cost')
ax.plot(yr, rent,label='Rent cost')
ax.set(xlabel='Year',ylabel='Total cost assuming inflation, $1000')
fig3.savefig(name+'Totalcosts.png')
ax.legend()
plt.show()

#cumulative investment increase
investment=dp*np.power(1.+inv/12.,np.arange(361,dtype=float))-dp

#total cost of renting + dp investment
rentcost=rent-investment

#CALCULATE HOW MUCH A HOUSE WILL APPRECIATE
value=price*inflate

# Calculate income from selling (-6% due to realtor/closing costs)
income=value*0.94 - (price-equ)-dp
homecost=totalbuycost-income

fig4,ax=plt.subplots()
ax.plot(yr,income, label='Home appreciation - loan and CC')
ax.plot(yr, investment,label='Downpayment appreciation')
ax.set(xlabel='Year',ylabel='Appreciation, $1000')
fig4.savefig(name+'Appreciation.png')
ax.legend()
plt.show()


#Final plots of costs
fig5,ax=plt.subplots()
ax.plot(yr,homecost, label='Buying')
ax.plot(yr, rentcost,label='Rent')
ax.set(xlabel='Year',ylabel='Total cost - appreciation, $1000')
fig5.savefig(name+'total_costs.png')
ax.legend()
plt.show()


#Cost savings from selling
savings=rentcost-homecost
ind2=np.amin(np.where(savings >= 0.))
print(ind)
fig6,ax=plt.subplots()
ax.plot(yr,savings)
ax.plot(yr, np.zeros(361), color='gray')
ax.set(xlabel='Year',ylabel='Savings compared to renting, $1000')
fig6.savefig(name+'Savings.png')
plt.show()

print(name)
print( 'Savings after 1-7 years ',savings[[12,24,36,48,60,72,84]])
print('Better to buy point', ind2, ' months')
print('Estimated monthly property tax before any exemptions', pt)
print('Mortgage, ',mr)
