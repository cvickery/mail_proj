#! /usr/local/bin/python3
""" Use pretty much the same commandline args as /usr/bin/mail, but add -t and -h options
    for getting the message body from a text file and/or html file respectively.
    Used only for sending message, not for reading/parsing mail

    This may or may not be a good idea.
      But /usr/bin/mail is broken, and this is my workaround.
"""
import sys
import os
import socket
import re
from datetime import datetime
import argparse

from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid, localtime, format_datetime
from email.headerregistry import Address
import smtplib

# Prefix for error reporting
whoami = f'{sys.argv[0].strip("./")}: error:'


def parse_addr_str(str):
  """ Extract display_name, username and domain from a string.
      Return an Address object
  """
  m = re.search(r'([^\<\s\@]+)@([^\s\>\@]+)', str)
  if m is None:
    return m
  username = m[1]
  domain = m[2]
  display_name = str.replace(m[0], '').strip('> <')
  return Address(display_name, username, domain)


parser = argparse.ArgumentParser(description='Simplified replacement for /usr/bin/mail',
                                 add_help=False)
parser.add_argument('-?', '--help', action='help')
parser.add_argument('-s', '--subject', default='Test Message')
parser.add_argument('-c', '--cc_addr', nargs='+')
parser.add_argument('-b', '--bcc_addr', nargs='+')
parser.add_argument('-r', '--reply_addr')
parser.add_argument('-h', '--html_file', type=argparse.FileType('r'))
parser.add_argument('-t', '--text_file', type=argparse.FileType('r'))
parser.add_argument('-d', '--debug_level', type=int, default=0)
parser.add_argument('-f', '--from_addr',
                    default=f"{os.getenv('USER')} <{os.getenv('USER')}@{os.getenv('HOSTNAME')}>")
parser.add_argument('to_addr', nargs='+')
args = parser.parse_args()

# Be sure all recipients have valid email addresses; build list of all recipents
if parse_addr_str(args.from_addr) is None:
  exit(f'{whoami} “{args.from_addr}” is not a valid return address')

all_recipients = []
for recipient in args.cc_addr, args.bcc_addr, args.reply_addr, args.to_addr:
  if type(recipient) == list:
    for r in recipient:
      if parse_addr_str(r) is None:
        exit(f'{whoami} “{r}” is not a valid email address')
      else:
        all_recipients += [r]
  if type(recipient) == str:
    if parse_addr_str(recipient) is None:
      exit(f'{whoami} “{r}” is not a valid email address')
    else:
      all_recipients += [recipient]
all_recipents = ', '.join(all_recipients)

# There has to be an SMTP server
fallback_servers = ['149.4.100.41', '149.4.100.42']   # Only valid at QC
servers = [os.getenv('SMTP_SERVER')] + fallback_servers
smtp_server = None
for server in servers:
  try:
    if args.debug_level > 0:
      print('try', server, file=sys.stderr)
    smtp_server = smtplib.SMTP(server)
    if smtp_server is None:
      continue
    break
  except (socket.gaierror, TimeoutError, ConnectionRefusedError) as err:
    print(f'{whoami} unable to connect to smtp server “{server}”: {err}', file=sys.stderr)

if smtp_server is None:
  sys.exit('No viable SMTP server')

smtp_server.set_debuglevel(args.debug_level)

# Set up the message parts.
msg = MIMEMultipart('alternative')
msg['Message-ID'] = make_msgid()
msg['Date'] = format_datetime(localtime())
msg['From'] = args.from_addr
msg['Subject'] = args.subject
msg['To'] = ', '.join(args.to_addr)
if args.cc_addr is not None:
  msg['Cc'] = ', '.join(args.cc_addr)
if args.bcc_addr is not None:
  msg['Bcc'] = ', '.join(args.bcc_addr)
if args.reply_addr is not None:
  msg['Reply-To'] = args.reply_addr

# Plain text body if no files specified
if args.html_file is None and args.text_file is None:
  text_body = ''
  while True:
      try:
          line = input()
      except EOFError:
          break
      if not line:
          break
      text_body += line + '\n'
  msg.attach(MIMEText(text_body, 'plain'))

# Plain text part
if args.text_file is not None:
  text_body = args.text_file.read()
  msg.attach(MIMEText(text_body, 'plain'))

# HTML part
if args.html_file is not None:
  html_body = args.html_file.read()
  msg.attach(MIMEText(html_body, 'html'))

# Send the message
try:
  smtp_server.sendmail(args.from_addr, all_recipients, msg.as_string())
except Exception as e:
  exit(f'{whoami} sending failed: {e}')

smtp_server.quit()
exit(0)
