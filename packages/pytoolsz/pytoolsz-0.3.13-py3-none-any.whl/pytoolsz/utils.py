#  ____       _____           _
# |  _ \ _   |_   _|__   ___ | |___ ____
# | |_) | | | || |/ _ \ / _ \| / __|_  /
# |  __/| |_| || | (_) | (_) | \__ \/ /
# |_|    \__, ||_|\___/ \___/|_|___/___|
#        |___/

# Copyright (c) 2024 Sidney Zhang <zly@lyzhang.me>
# PyToolsz is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#          http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import re
import string
import pendulum as plm

import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.utils import formataddr
from email.header import Header
from pathlib import Path
from typing import List, Dict, Union, Optional, Tuple

import imaplib 
import email
import os
from email.header import decode_header 
from datetime import datetime, timedelta 
from imapclient import imap_utf7 

from collections.abc import Iterable
from random import randint
from rich.console import Console
from rich.highlighter import Highlighter
from rich.markdown import Markdown

__all__ = [
    "println", "print_special", "szformat", 
    "now", "isSubset", "quicksendmail", "load_email_by_subject"
]

class RainbowHighlighter(Highlighter):
    def highlight(self, text):
        for index in range(len(text)):
            text.stylize(f"color({randint(16, 255)})", index, index + 1)

def println(text:str, color:str = "auto", 
            style:str|None = None, end:str = "\n",
            width:int|None = None) -> None:
    """带颜色的文本输出"""
    cons = Console(width=width)
    if color == "auto" :
        txt = text
    elif color == "rainbow" :
        txt = RainbowHighlighter()(text)
    else :
        txt = f"[{color}]{text}[/{color}]"
    cons.print(txt, style=style, end=end)

def print_special(data:any, mode:str = "auto", 
                  width:int|None = None) -> None :
    """特殊输出，可指定输出markdown格式。"""
    cons = Console(width=width)
    if mode == "auto" :
        cons.print(data)
    elif mode == "markdown" :
        cons.print(Markdown(data))
    elif mode == "rainbow":
        println(data, color="rainbow", width=width)
    elif re.match(r"^color-\(?[\d|a-z]+\)?$", mode):
        color = re.search("[0-9|a-z]+", mode.split("-")[1]).group()
        if re.match(r"^\d+$", color) :
            color = "color({})".format(color)
        println(data, color=color, width=width)
    else:
        raise ValueError("mode must be 'auto','markdown', 'rainbow' or 'color-(color)'")

def szformat(value:any, fmt:str) -> str :
    """格式化输出转换"""
    tft = string.Formatter()
    return tft.format_field(value, fmt)

def now(sformat:str|bool|None = None) -> plm.DateTime|str:
    """
    获取时间函数。
    1. 如果 sformat 为 False，则返回 pendulum.DateTime 类型
    2. 如果 sformat 为 True，则返回“日期时间”字符串
    3. 如果 sformat 为字符串，则返回字符串，且格式为 sformat
    4. 如果 sformat 为 None，则返回“无标识日期时间”字符串
    """
    dtx = plm.now()
    if isinstance(sformat, bool) :
        return dtx.format("YYYY-MM-DD HH:mm:ss") if sformat else dtx
    else :
        fmt = sformat if sformat else "YYYYMMDD_HHmmss"
        return dtx.format(fmt)

def isSubset(superset:Iterable, subset:Iterable) -> bool :
    """判断一个集合是否是另一个集合的子集。"""
    return all(item in superset for item in subset)

def quicksendmail(
    myMail: str,
    password: str,
    mailText: str,
    attachments: List[Union[Path, str]],
    subject: str,
    recipients: Union[List[str], List[Tuple[str, str]]],
    cc_recipients: Optional[Union[List[str], List[Tuple[str, str]]]] = None,
    html_mode: bool = False,
    other_smtp_config: Optional[Dict[str, tuple]] = None,
    signature: Optional[str] = None,
    inline_images: Optional[Dict[str, Union[Path, str]]] = None,
    sender_name: Optional[str] = None
) -> None:
    """
    发送带附件的邮件（支持UTF-8编码、显示名称、内嵌图片和邮件签名）

    Args:
        myMail: 发件人邮箱地址
        password: 邮箱密码/授权码
        mailText: 邮件正文内容
        attachments: 附件路径列表（Path对象或字符串）
        subject: 邮件标题
        recipients: 收件人列表，可以是邮箱字符串或(名称, 邮箱)元组
        cc_recipients: 抄送人列表，格式同recipients（可选）
        html_mode: 是否使用HTML格式
        other_smtp_config: 自定义SMTP配置字典，格式为{"域名": (服务器, 端口)}
        signature: 邮件签名内容（支持HTML/纯文本）
        inline_images: 内嵌图片字典（格式: {"cid": 图片路径}）
        sender_name: 发件人显示名称（可选）

    Raises:
        ValueError: 参数验证失败时抛出
        RuntimeError: 邮件发送失败时抛出
    """
    # 参数验证
    if not recipients:
        raise ValueError("必须指定至少一个收件人")
    if cc_recipients is None:
        cc_recipients = []

    # 创建邮件对象
    msg = MIMEMultipart()
    
    # 设置邮件编码为UTF-8
    msg.set_charset("utf-8")
    
    # 设置发件人（带可选名称）
    if sender_name:
        # 对名称部分进行UTF-8编码
        sender_name = Header(sender_name, "utf-8").encode()
    msg["From"] = formataddr((sender_name, myMail)) if sender_name else myMail
    
    # 格式化收件人和抄送人地址
    def format_recipients(recipient_list):
        """将收件人列表格式化为标准email格式"""
        formatted = []
        for r in recipient_list:
            if isinstance(r, tuple) and len(r) == 2:
                name, addr = r
                # 对名称部分进行UTF-8编码
                name = Header(name, "utf-8").encode()
                formatted.append(formataddr((name, addr)))
            else:
                formatted.append(str(r))
        return ", ".join(formatted)
    
    # 对邮件主题进行UTF-8编码
    msg["Subject"] = Header(subject, "utf-8")
    msg["To"] = format_recipients(recipients)
    if cc_recipients:
        msg["Cc"] = format_recipients(cc_recipients)

    # 处理邮件正文和签名
    full_text = mailText
    if signature is not None:
        if html_mode:
            full_text += "<br/><br/>" + signature
        else:
            full_text += "\n\n" + signature

    # 添加邮件正文（明确指定UTF-8编码）
    if html_mode:
        msg.attach(MIMEText(full_text, "html", "utf-8"))
    else:
        msg.attach(MIMEText(full_text, "plain", "utf-8"))

    # 添加内嵌图片
    if inline_images:
        mimetypes.init()
        for cid, img_path in inline_images.items():
            img_path = Path(img_path)
            if not img_path.exists():
                raise FileNotFoundError(f"内嵌图片文件不存在: {img_path}")
            
            # 猜测MIME类型
            mime_type, _ = mimetypes.guess_type(img_path.name)
            if mime_type is None or not mime_type.startswith("image/"):
                raise ValueError(f"文件类型不支持或不是图片: {img_path}")
            
            with open(img_path, "rb") as img_file:
                img_data = img_file.read()
            
            _, subtype = mime_type.split("/", 1)
            img_part = MIMEImage(img_data, _subtype=subtype)
            img_part.add_header("Content-ID", f"<{cid}>")
            img_part.add_header("Content-Disposition", "inline", filename=Header(img_path.name, "utf-8").encode())
            msg.attach(img_part)

    # 添加附件（处理附件文件名编码）
    for attachment in attachments:
        file_path = Path(attachment)
        if not file_path.exists():
            raise FileNotFoundError(f"附件文件不存在: {file_path}")
        
        with open(file_path, "rb") as f:
            part = MIMEApplication(f.read(), Name=file_path.name)
        
        # 对附件文件名进行UTF-8编码
        filename = Header(file_path.name, "utf-8").encode()
        part.add_header("Content-Disposition", "attachment", filename=filename)
        msg.attach(part)

    # 自动配置SMTP服务器
    domain = myMail.split("@")[-1].lower()
    smtp_config = {
        "gmail.com": ("smtp.gmail.com", 587),
        "qq.com": ("smtp.qq.com", 465),
        "163.com": ("smtp.163.com", 465),
        "chinaott.net": ("smtp.exmail.qq.com", 465),
    }
    if other_smtp_config:
        smtp_config.update(other_smtp_config)

    try:
        smtp_server, port = smtp_config[domain]
    except KeyError:
        raise ValueError(f"不支持的邮箱服务商: {domain}，请通过other_smtp_config参数手动配置") from None

    try:
        # 建立SMTP连接
        if port == 465:
            server = smtplib.SMTP_SSL(smtp_server, port)
        else:
            server = smtplib.SMTP(smtp_server, port)
            server.starttls()

        # 登录并发送邮件
        server.local_hostname = 'Localhost'
        server.login(myMail, password)
        
        # 获取所有收件人邮箱地址（去除名称部分）
        def extract_emails(recipient_list):
            emails = []
            for r in recipient_list:
                if isinstance(r, tuple) and len(r) == 2:
                    emails.append(r[1])
                else:
                    emails.append(str(r))
            return emails
        
        all_recipients = extract_emails(recipients) + extract_emails(cc_recipients)
        server.sendmail(myMail, all_recipients, msg.as_string())
        server.quit()

    except Exception as e:
        raise RuntimeError(f"邮件发送失败: {str(e)}") from e

def load_email_by_subject(
    email_account: str, 
    password: str, 
    target_subject: str,
    imap_server: Optional[str] = None,
    port: int = 993,
    use_ssl: bool = True,
    fuzzy_match: bool = False,
    date_range: Optional[Tuple[datetime, datetime]] = None,
    mailbox: str = 'INBOX',
    download_attachments: bool = False,
    attachment_dir: str = 'attachments'
) -> List[Dict[str, Union[str, List[Dict[str, str]]]]]:
    """ 
    登录邮箱并加载匹配条件的邮件(支持附件下载) 
    
    参数: 
        email_account: 邮箱账号 
        password: 邮箱密码/授权码 
        imap_server: IMAP服务器地址
        port: IMAP端口(默认993) 
        use_ssl: 是否使用SSL连接(默认True) 
        target_subject: 要查找的邮件主题 
        fuzzy_match: 是否启用模糊匹配(默认False) 
        date_range: 日期范围元组(start_date, end_date)，如未指定则搜索最近7天 
        mailbox: 要搜索的邮箱文件夹(默认'INBOX') 
        download_attachments: 是否下载附件(默认False) 
        attachment_dir: 附件保存目录(默认'attachments') 
        
    返回: 
        匹配的邮件内容列表(包含附件信息) 
    """
    try:
        # 设置默认日期范围(最近7天)
        if date_range is None:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            date_range = (start_date, end_date)
            
        # 创建附件目录 
        if download_attachments and not os.path.exists(attachment_dir): 
            os.makedirs(attachment_dir)
        
        # 确认服务器
        if imap_server is None :
            serv = email_account.split("@")[-1].lower()
            IMSERVE = {
                "qq.com": ("imap.qq.com",993),
                "gmail.com": ("imap.gmail.com",993),
                "163.com": ("imap.163.com",993),
                "aliyun.com":("imap.aliyun.com",993),
                "chinaott.net":("imap.exmail.qq.com",993),
            }
            imap_server, port = IMSERVE[serv]
        
        # 连接IMAP服务器 
        if use_ssl:
            mail = imaplib.IMAP4_SSL(imap_server, port)
        else:
            mail = imaplib.IMAP4(imap_server, port)
        mail.login(email_account, password)
        status, mailboxes = mail.list()
        for mb in mailboxes:
                tmpmailbox = imap_utf7.decode(mb).split('"')[-2]
                if mailbox in tmpmailbox:
                    selmailbox = imap_utf7.encode(tmpmailbox)
        mail.select(selmailbox)  # 选择指定邮箱文件夹
        
        # 构建日期搜索条件
        start_str = date_range[0].strftime("%d-%b-%Y")
        end_str = date_range[1].strftime("%d-%b-%Y")
        date_criteria = f'(SINCE "{start_str}" BEFORE "{end_str}")'
        
        # 搜索邮件
        status, messages = mail.search(None, date_criteria)
        if status != 'OK':
            return []
            
        email_contents = []
        for mail_id in messages[0].split():
            # 获取邮件内容
            status, data = mail.fetch(mail_id, '(RFC822)')
            if status != 'OK':
                continue
                
            # 解析邮件
            msg = email.message_from_bytes(data[0][1])
            subject_header = decode_header(msg['Subject'])
            subject = ""
            for part, encoding in subject_header:
                if isinstance(part, bytes):
                    try:
                        subject += part.decode(encoding if encoding else 'utf-8', errors='replace')
                    except:
                        subject += part.decode('gbk', errors='replace')
                else:
                    subject += str(part)
            
            # 检查主题匹配
            if fuzzy_match:
                pattern = re.compile(re.escape(target_subject), re.IGNORECASE)
                if not pattern.search(subject):
                    continue
            else:
                if target_subject.lower() != subject.lower():
                    continue
            
            # 提取邮件正文
            body = ""
            html_body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    
                    if "attachment" not in content_disposition:
                        if content_type == "text/plain":
                            body += part.get_payload(decode=True).decode(
                                part.get_content_charset() or 'utf-8', 
                                errors='replace'
                            )
                        elif content_type == "text/html":
                            html_body += part.get_payload(decode=True).decode(
                                part.get_content_charset() or 'utf-8',
                                errors='replace'
                            )
            else:
                body = msg.get_payload(decode=True).decode(
                    msg.get_content_charset() or 'utf-8',
                    errors='replace'
                )
            
            # 处理附件
            attachments = []
            if download_attachments:
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    
                    filename = part.get_filename()
                    if filename:
                        filename = decode_header(filename)[0][0]
                        if isinstance(filename, bytes):
                            filename = filename.decode('utf-8', errors='replace')
                        
                        filepath = os.path.join(attachment_dir, filename)
                        with open(filepath, 'wb') as f:
                            f.write(part.get_payload(decode=True))
                        attachments.append({
                            'filename': filename,
                            'filepath': os.path.abspath(filepath)
                        })
            
            email_contents.append({
                'subject': subject,
                'from': msg.get('From'),
                'date': msg.get('Date'),
                'text_body': body.strip(),
                'html_body': html_body.strip(),
                'attachments': attachments
            })
            
        mail.close()
        mail.logout()
        return email_contents
        
    except Exception as e:
        print(f"发生错误: {e}")
        return []