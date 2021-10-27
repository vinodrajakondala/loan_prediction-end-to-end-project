from fastapi import FastAPI, Request, Form, requests
import pickle
import numpy as np
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

app =FastAPI()
templates = Jinja2Templates(directory="templates")



with open('models/model_rf.pkl','rb') as f:
    loaded_model_rf = pickle.load(f)

with open('models/model_lf.pkl','rb') as f:
    loaded_model_lg = pickle.load(f)



@app.get("/",response_class=HTMLResponse)
async def start(request: Request,):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/loan_predict")
async def anomaly_predict(request: Request):
    return templates.TemplateResponse("loan_prediction.html", {"request":request})

@app.post("/loan_predict")
async def loan_predict(request: Request, nam :str = Form(...), gender : str = Form(...), married :str = Form(...), dependents : str = Form(...), education : str = Form(...),employee : str = Form(...), credit : str = Form(...), area : str = Form(...), applicantincome : str = Form(...), coapplicantIncome : str = Form(...), loanAmount : str = Form(...)):
    
    NAME = nam.capitalize().title()
    # gender
    male = 1 if gender == "Male" else 0
    
    # married
    m_yes = 1 if married=="Yes" else 0
    
    #credithistory
    credit = float(credit)

    # dependents
    if(dependents=='1'):
        dep_1 = 1
        dep_2 = 0
        dep_3 = 0
    elif(dependents == '2'):
        dep_1 = 0
        dep_2 = 1
        dep_3 = 0
    elif(dependents=="3+"):
        dep_1 = 0
        dep_2 = 0
        dep_3 = 1
    else:
        dep_1 = 0
        dep_2 = 0
        dep_3 = 0  

        # education
    not_graduate = 1 if (education=="Not Graduate") else 0

    # employed
    emp_yes = 1 if (employee == "Yes") else 0

    # property area
    if(area=="Semiurban"):
        semiurban=1
        urban=0
    elif(area=="Urban"):
        semiurban=0
        urban=1
    else:
        semiurban=0
        urban=0

    applicantincome = float(applicantincome)
    coapplicantIncome = float(coapplicantIncome)
    loanAmount = float(loanAmount)

    ApplicantIncomelog = np.log(applicantincome)
    totalincomelog = np.log( applicantincome+ coapplicantIncome)
    LoanAmountlog = np.log(loanAmount)
    
    val = [credit, ApplicantIncomelog, LoanAmountlog, totalincomelog, male, m_yes, dep_1, dep_2, dep_3, not_graduate,emp_yes,semiurban, urban]

    prediction = loaded_model_rf.predict([val])

    if prediction == "N":
        pred = "Sorry " + NAME +", you are not eligible for Loan"
    else:
        pred = "Congratulations " + NAME + ", you are eligible for Loan"

    return templates.TemplateResponse("loan_output.html",  {"request":request, "p_text" : pred })

 

@app.get("/anomaly_detection")
async def anomaly_predict(request: Request):
    return templates.TemplateResponse("anomaly_detection.html", {"request":request})

@app.get("/personality_predict")
async def personality_predict(request: Request):
    return templates.TemplateResponse("personality_prediction.html", {"request":request})

@app.get("/spam_mail_detection")
async def spam_mail_detection(request: Request):
    return templates.TemplateResponse("spam_mail_detection.html", {"request":request})

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0",port=8076,reload=True)

