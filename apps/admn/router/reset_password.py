from fastapi import Depends, HTTPException, APIRouter, Path
import re
from email.mime.text import MIMEText
from smtplib import SMTP
# from config import HOST, USERNAME, PASSWORD, PORT, MailBody
from ssl import create_default_context
from fastapi import Depends, HTTPException, APIRouter, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from config.database import get_db

# Lib
from lib import auth_service3, auth_service2
# Model
from model.modules.auth.user_models import NewPasswordEmailModel
from model.modules.auth.models import ResetPasswordEmailModel
# Repo
from repository.user.user_repository import UserRepository, AuthUserPasswordResetRepository


router = APIRouter(
    prefix="/password",
    tags=["PasswordReset"],
    # dependencies=[Depends(get_token_header)],
)


class MailBody:
    def __init__(self, body: str, to: list, subject: str):
        self.body = body
        self.to = to
        self.subject = subject

HOST = "smtp.gmail.com"
PORT = 587
USERNAME = "hazardsober540@gmail.com"
PASSWORD = "eoqkirhvsnjlywxm"


def send_mail(data: dict | None = None):
    msg = MailBody(**data)
    message = MIMEText(msg.body, "html")
    message["From"] = USERNAME
    message["To"] = ", ".join(msg.to)
    message["Subject"] = msg.subject

    ctx = create_default_context()

    try:
        with SMTP(HOST, PORT) as server:
            server.ehlo()
            server.starttls(context=ctx)
            server.ehlo()
            server.login(USERNAME, PASSWORD)
            server.send_message(message)
            server.quit()
        return {"status": 200, "errors": None}
    except Exception as e:
        return {"status": 500, "errors": str(e)}


@router.post('/reset')
def reset_password(
   model: ResetPasswordEmailModel, 
   db: Session = Depends(get_db)
):
    emailData = UserRepository(db).findOneByEmail(model.email)
    reset_repo = AuthUserPasswordResetRepository(db)

    if not emailData:
        raise HTTPException(status_code=404, detail="email not found")
    
    reset_token = auth_service3.generate_reset_token()
    
    reset_data = {
        "authUserId": emailData.id,
        "token": reset_token,
        "state": "o"
    }
    
    reset_repo.create(reset_data)
    
    data1 = reset_repo.findOneId(emailData.id)
    
    model1 = jsonable_encoder(data1)

    if not model1:
        raise HTTPException(status_code=404, detail="id not found")
    
    data2 = reset_repo.findOneByEmail(model1['authUserId'])
    model2 = jsonable_encoder(data2)
    email1 = model2['email']

    if not email1:
        raise HTTPException(status_code=404, detail="email not found")

    reset_url = f"http://localhost:3000/new/password/{reset_token}"
    link_name = "changepassword"
    
    email_body = f"Дараах холбоос дээр дарж нууц үгээ шинэчилнэ үү. <a href='{reset_url}' style='color: blue; text-decoration: underline;'>{link_name}</a>"

    email_subject = "Password Reset"
    email_data = {
        "body": email_body,
        "to": [email1],
        "subject": email_subject
    }
    
    send_mail(email_data)


@router.put('/reset/{reset_token}')
def new_password_page(
    model: NewPasswordEmailModel,
    reset_token: str = Path(),
    db: Session = Depends(get_db)
):
    
    reset_repo = AuthUserPasswordResetRepository(db)
    reset_data = reset_repo.find_one_by_active_token(reset_token)

    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$', model.password):
        raise HTTPException(status_code=400, detail="Password must be Upper and lower case letters, numbers and special characters and  must be 8 characters")

    if not reset_data:
        raise HTTPException(status_code=404, detail="Reset token not found")
    
    data1 = UserRepository(db).findOne(reset_data.userId)
    if not data1:
        raise HTTPException(status_code=404, detail="User not found")

    passwordPlain = data1.password
    passwordHash = auth_service2.passwordHash(passwordPlain)
    data1.password = passwordHash

    db.commit()
    db.refresh(data1)

    return jsonable_encoder(data1)