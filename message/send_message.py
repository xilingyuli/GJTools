from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP_SSL
from email.mime.text import MIMEText

import cfg
from message import log_message


def send_message(message, images=None):
    try:
        # 填写真实的发邮件服务器用户名、密码
        user = 'xilingyuli_test@163.com'
        password = 'PECWVHHACWBVLSBA'
        # 邮件内容
        msg = MIMEMultipart()
        msg["Subject"] = Header('GJTool', 'utf-8')
        msg["from"] = user
        msg["to"] = cfg.receive_addr
        msg.attach(MIMEText(message, 'html', 'utf-8'))
        try:
            image_path = 'gold_report/gold_img.png'
            for index in range(0, len(images)):
                images[index].save(image_path)
                with open(image_path, 'rb') as image_file:
                    image_tag = 'image' + str(index + 1)
                    msg.attach(MIMEText('<br><img src="cid:' + image_tag + '">', 'html', 'utf-8'))
                    mail_image = MIMEImage(image_file.read())
                    mail_image.add_header('Content-ID', '<' + image_tag + '>')
                    # 通过多组件类型将图片附件打包进来
                    msg.attach(mail_image)
        except:
            log_message.log_error('add image failed')
        with SMTP_SSL(host="smtp.163.com", port=465) as smtp:
            # 登录发邮件服务器
            smtp.login(user=user, password=password)
            # 实际发送、接收邮件配置
            smtp.sendmail(from_addr=user, to_addrs=cfg.receive_addr, msg=msg.as_string())
    except:
        log_message.log_error(message)
