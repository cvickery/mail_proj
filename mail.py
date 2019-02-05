#! /usr/local/bin/python3
""" Use pretty much the same commandline args as /usr/bin/mail, but add -t and -h options
    for getting the message body from a text file and/or html file respectively.
    Used only for sending message, not for reading/parsing mail

    This may or may not be a good idea.
      But /usr/bin/mail is broken, and this is my workaround.
"""
import sys
import os
import re
from datetime import datetime
import argparse

from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, formatdate
import smtplib

parser = argparse.ArgumentParser(description='Simplified replacement for /usr/bin/mail',
                                 add_help=False)
parser.add_argument('-?', '--help', action='help')
parser.add_argument('-s', '--subject', default='Test Message')
parser.add_argument('-cc', '--cc_addr', nargs='+')
parser.add_argument('-bcc', '--bcc_addr', nargs='+')
parser.add_argument('-r', '--reply_addr')
parser.add_argument('-h', '--html_file', type=argparse.FileType('r'))
parser.add_argument('-p', '--plaintext_file', type=argparse.FileType('r'))
parser.add_argument('-d', '--debuglevel', default=0)

smtp_server = os.getenv('SMTP_SERVER')
if smtp_server is None:
  smtp_server = 'localhost'

from_addr = os.getenv('EMAIL_SENDER')
if from_addr is None:
  parser.add_argument('from_addr')
parser.add_argument('to_addr', nargs='+')
args = parser.parse_args()

if from_addr is None:
  from_addr = args.from_addr

# Be sure the from_addr contains something that looks like it might be an email address.
#   argparse lets empty strings get through, and then mailer doesn't complain.
if re.search(r'\S+@\S+', from_addr) is None:
  print(f'{sys.argv[0].strip("./")}: error: invalid from_addr', file=sys.stderr)
  exit(1)

try:
  debuglevel = int(args.debuglevel)
except ValueError:
  print(f'{sys.argv[0].strip("./")}: error: debuglevel must be an int', file=sys.stderr)
  exit(1)

# Set up the message parts.
msg = MIMEMultipart('alternative')
msg['Message-ID'] = make_msgid()
msg['Date'] = formatdate(datetime.now().timestamp())
msg['From'] = f'{from_addr}'
msg['Subject'] = args.subject
msg['To'] = ', '.join(args.to_addr)
if args.cc_addr is not None:
  msg['Cc'] = ', '.join(args.cc_addr)
if args.bcc_addr is not None:
  msg['Bcc'] = ', '.join(args.bcc_addr)
if args.reply_addr is not None:
  msg['Reply-To'] = args.reply_addr

# Plain text body if no files specified
if args.html_file is None and args.plaintext_file is None:
  plain_body = ''
  while True:
      try:
          line = input()
      except EOFError:
          break
      if not line:
          break
      plain_body += line + '\n'
  msg.attach(MIMEText(plain_body, 'plain'))

# Plain text part
if args.plaintext_file is not None:
  # f = open(args.plaintext_file, 'r')
  plain_body = args.plaintext_file.read()
  msg.attach(MIMEText(plain_body, 'plain'))

# HTML part
if args.html_file is not None:
  # f = open(args.html_file, 'r')
  html_body = args.html_file.read()
  msg.attach(MIMEText(html_body, 'html'))

# Send the message
server = smtplib.SMTP('smtp_server')
server.set_debuglevel(debuglevel)
server.sendmail(from_addr, args.to_addr, msg.as_string())
server.quit()
