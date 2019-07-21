from tkinter import *
from PIL import ImageTk,Image
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from pandas_datareader import data as dt
import datetime
from tkinter import messagebox
import matplotlib.pyplot as plt
scr=Tk()
scr.title("Welcome to Stock Market")
# global stq=StringVar(scr)

#BACKGROUND IMAGE
i=ImageTk.PhotoImage(Image.open("backimg1.jpg"))
l=Label(scr,image=i)
l.pack()

#STACK LABEL AND OPTION MENU
stack_label=Label(scr,text="SELECT COMPANY NAME :",bg="red",fg="black",font=("times",20,"bold"))
stack_label.place(x=150,y=100)
v=StringVar()
l=["google","microsoft","apple","oracle","msft"]
stack_menu=OptionMenu(scr,v,*l)
stack_menu.place(x=530,y=100)
v.set(l[0])








#FUNCTIONS








def fetch_data():
    start = datetime.datetime(2010, 1, 1)
    end = datetime.datetime.now()
    f = dt.DataReader("msft", 'tiingo', start, end,access_key='911ee28d70118f9cea5a84d2b8f1436fa32d3116')
    return f
f=fetch_data()


def lin(x,y,x1,x_pr):
    x_tr,x_ts,y_tr,y_ts=train_test_split(x1,y,test_size=0.2)
    alg=LinearRegression()
    alg.fit(x_tr,y_tr)
    score=alg.score(x_ts,y_ts)
    #print(score)
    messagebox.showinfo("accuracy","YOR ACCURACY IS = "+str(score))
    return alg.predict(x_pr)

def lin12(x,y,x1,x_pr):
    x_tr,x_ts,y_tr,y_ts=train_test_split(x1,y,test_size=0.2)
    alg=LinearRegression()
    alg.fit(x_tr,y_tr)
    score=alg.score(x_ts,y_ts)
    #print(score)
    #messagebox.showinfo("accuracy","YOR ACCURACY IS = "+str(score))
    return alg.predict(x_pr),alg




def prepare_data(f,days):
    f.reset_index(inplace=True)
    f.set_index('date',inplace=True)
    f=f[['adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',]]
    no_days=days
    pd.set_option('mode.chained_assignment', None)
    f.loc[:,'newclose']=f.loc[:,'adjClose'].shift(-no_days)
    x=f.drop(['adjClose','newclose'],axis=1)
    y=f['newclose'].dropna()
    x1=x[:-no_days]
    x_pr=x[-no_days:]
    return x,y,x1,x_pr

#def fun1(sco):
 #   sc=sco
  #  messagebox.showinfo("accuracy","YOR ACCURACY IS = "+str(sc))

def predict1(pr):
    new=Toplevel(scr)
    new.title("Prediction")
    new.config(bg="yellow")
    new.geometry("1200x700")
    #msg = Message(new, text='PREDICTED DATA :',font=('times',20,'bold'))
    #msg.pack()
    l=Label(new,text=str(pr),font=('times',25,'italic'),bg="yellow")
    l.place(x=100,y=200)
#vt=(vt.get())/100


#PREDICT DAYS LABEL AND ENTRY
sp=IntVar()
predict_label=Label(scr,text="ENTER NUMBER OF DAYS :",bg="red",fg="black",font=("times",20,"bold"))
predict_label.place(x=150,y=200)
predict_entry=Entry(scr,textvariable=sp,bd=10,bg='red',font=('times',20,'bold'))
predict_entry.place(x=550,y=200)
sp.set(20)
days=sp.get()





x,y,x1,x_pr=prepare_data(f,days)
pr,alg=lin12(x,y,x1,x_pr)
   


          
def graph(f,alg):
    f.reset_index(inplace=True)
    f.set_index('date',inplace=True)
    f=f[['adjClose', 'adjHigh', 'adjLow', 'adjOpen', 'adjVolume',]]
    no_days=20
    pd.set_option('mode.chained_assignment', None)
    f.loc[:,'newclose']=f.loc[:,'adjClose'].shift(-no_days)
    f['forecast']=np.nan
    prd=alg.predict(x_pr)
    lastday=(f.iloc[-1].name)
    for i in prd:
        lastday+=datetime.timedelta(1)
        f.loc[lastday]=[np.nan for _ in range(6)]+[i]
    f['adjClose'].plot()
    f['forecast'].plot()
    plt.show()



#TEST SIZE LABEL AND MENU
test_label=Label(scr,text="SELECT TEST SIZE :",bg="red",fg="black",font=("times",20,"bold"))
test_label.place(x=680,y=100)
vt=StringVar()
lt=[10,20,30,40]
test_menu=OptionMenu(scr,vt,*lt)
test_menu.place(x=960,y=100)
l=Label(scr,text="%",bg="red",fg="black",font=("times",20,"bold"))
l.place(x=1030,y=100)
vt.set(lt[0])





#EVALUATE BUTTON
eval_label=Label(scr,text="CLICK TO EVALUATE :",bg="red",fg="black",font=("times",20,"bold"))
eval_label.place(x=100,y=300)
q2 = lambda: predict1(pr)
eval_button=b=Button(scr,bd=15,bg='black',fg='RED',relief='sunken',state='normal',text='EVALUATE',command=q2)
#eval_button.bind("<Button-1>",predict1)
eval_button.place(x=440,y=300)

#ACCURACY LABEL AND BUTTON
acc_label=Label(scr,text="PREDICTION ACCURACY :",bg="red",fg="black",font=("times",20,"bold"))
acc_label.place(x=600,y=300)
q1 = lambda: lin(x,y,x1,x_pr)
acc_button=b=Button(scr,bd=15,bg='black',fg='RED',relief='sunken',state='normal',text='ACCURACY :',command=q1)

acc_button.place(x=980,y=300)


#VISUALISE LABEL AND BUTTON
vis_label=Label(scr,text="DATA CHART :",bg="red",fg="black",font=("times",20,"bold"))
vis_label.place(x=450,y=400)
q3 = lambda:  graph(f,alg)
vis_button=b=Button(scr,bd=15,bg='black',fg='RED',relief='sunken',state='normal',text='VISUALIZE',command=q3)
vis_button.place(x=700,y=400)
























