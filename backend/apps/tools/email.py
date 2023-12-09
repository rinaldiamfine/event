from cmath import e
from email.message import EmailMessage
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from datetime import date
import os
from dotenv import load_dotenv
load_dotenv()

class EmailManager:
    '''Mail Schedule Manager'''
    def __init__(self):
        self.server = smtplib.SMTP_SSL(os.getenv('MAIL_SMTP_SERVER'), os.getenv('MAIL_SMTP_PORT'))
        self.user = os.getenv('MAIL_USER')
        self.password = os.getenv('MAIL_PASSWORD')
        self.context = ssl.create_default_context()
        self.user_receive = []
        self.msg = EmailMessage()
        self.is_login = False
        if not self.is_login:
            self.authenticate()

    def authenticate(self):
        try:
            self.server.login(self.user, self.password)
            self.is_login = True
        except Exception as e:
            print('Something went wrong...', e)
    
    def send_email(self, msg):
        self.server.send_message(msg)
        # for email in self.user_receive:
        #     try:
        #         message = self.msg
        #         message['To'] = email
        #         self.server.send_message(message)
        #     except Exception as e:
        #         print('Something went wrong...', e)

    def invitation_email(self):
        from jinja2 import Environment, FileSystemLoader
        load_path = os.path.join(os.getenv('BASE_PATH'), "apps", "templates")
        file_load_env = Environment(
            loader=FileSystemLoader(load_path)
        )
        email_template = file_load_env.get_template('email_invitation.html')

        email = vals[0].get('email')
        username = vals[0].get('username').capitalize()
        template_render = email_template.render(
            {
                "username": username,
            } 
        )
        
        message = MIMEMultipart()
        message['To'] = email
        message['Subject'] = "Infineon - Expired Loan Notification"
        message['From'] = formataddr(("Inventory Loan", self.user))
        message.attach(MIMEText(template_render, "html"))
        self.server.send_message(message)
                
    # def order_notification_scheduler(self):
    #     from jinja2 import Environment, FileSystemLoader
    #     import os
    #     from datetime import date, datetime
    #     load_path = os.path.join(os.getenv('BASE_PATH'), "app", "templates")
    #     file_load_env = Environment(
    #         loader=FileSystemLoader(load_path)
    #     )
    #     email_template = file_load_env.get_template('email_invitation.html')
        
        
    #     datas = dict()
    #     for order_id in order_ids:
    #         employee_status, employee_ids = EmployeeModel().get_employee_by_id(
    #             id=order_id.get("employee_id")
    #         )
    #         product_status, product_ids = ProductModel().get_product_by_id(
    #             id=order_id.get("product_id")
    #         )
    #         if employee_status and product_status:
    #             employee_id = employee_ids[0]
    #             product_id = product_ids[0]
    #             emp_id = employee_id.get("id")
    #             order_data = {
    #                 'email': employee_id.get("email"),
    #                 'username': employee_id.get("name"),
    #                 'product_name': product_id.get("name"),
    #                 'qty': order_id.get('qty'),
    #                 'loan_date': order_id.get('start_date').strftime("%d-%m-%Y") if order_id.get('start_date') else "",
    #                 'due_date': order_id.get('end_date').strftime("%d-%m-%Y") if order_id.get('end_date') else ""
    #             }
                
    #             if datas.get(str(emp_id)) is not None:
    #                 datas[str(emp_id)].append(
    #                     order_data
    #                 )
                    
    #             else:
    #                 datas[str(emp_id)] = [order_data]
        
    #     for index, vals in datas.items():
    #         if len(vals) > 0:
    #             email = vals[0].get('email')
    #             username = vals[0].get('username').capitalize()
    #             template_render = email_template.render(
    #                 {
    #                     "username": username,
    #                     "date_returned": str(date.today().strftime("%d-%m-%Y")),
    #                     "current_year": str(datetime.now().year),
    #                     "order_ids": vals
    #                 } 
    #             )
                
    #             message = MIMEMultipart()
    #             message['To'] = email
    #             message['Subject'] = "Infineon - Expired Loan Notification"
    #             message['From'] = formataddr(("Inventory Loan", self.user))
    #             message.attach(MIMEText(template_render, "html"))
    #             self.server.send_message(message)
        
    #     return "Finish the notification scheduler"