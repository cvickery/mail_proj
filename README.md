# mail_proj
Utility to replace `/usr/bin/mail` for sending email on macOS.

__mail.py__ is a Python 3 script for sending email messages from the command line. Unlike
/usr/bin/mail, it can be used only to send mail, not to receive messages. However, it can be
used to send multipart messages with plain text and/or HTML message parts, and the smtp server
to use can be set with an environment variable.

## Why?

Bash scripts that sent email using `/usr/bin/mail` on macOS stopped working after an Apple security update in
January 2019. PHP scripts that used the PHP Mailer package stopped working too. But Python's smtplib continued
to work okay.

I was unable to get any useful information about the issue from Apple support and on
https://developer.apple.com (hundreds of views; zero replies), so I wrote this as a workaround.

## Requirements and Environment

  * This is a Python 3 application. The command assumes the interpreter is `/usr/local/bin/python3`.
  Edit the first line of the code if this path needs to be changed. Alternatively, invoke as
  `python3 /path/to/mail.py options... `.
  * The environment variable `SMTP_SERVER` specifies the hostname of the server that will relay the
  message. If `SMTP_SERVER` is not set, the environment variable `HOSTNAME` will be used instead.
  * The `-f` or `--from_addr` command line option may be used to specify the sender’s email address.
  The default value is `$USER@$HOSTNAME`. Valid formats are:
    * `Real Name <username@domain>`
    * `username@domain`
  * If neither a plain text file (`-p`) nor a HTML file (`-h`) is specified, a plain text message
  body is read from stdin.
  * The default `Subject:` is “Test Message”
~~~
$ mail.py -?
usage: mail.py [-?] [-s SUBJECT] [-c CC_ADDR [CC_ADDR ...]]
               [-b BCC_ADDR [BCC_ADDR ...]] [-r REPLY_ADDR] [-h HTML_FILE]
               [-p PLAINTEXT_FILE] [-d DEBUGLEVEL] [-f FROM_ADDR]
               to_addr [to_addr ...]

Simplified replacement for /usr/bin/mail

positional arguments:
  to_addr

optional arguments:
  -?, --help
  -s SUBJECT, --subject SUBJECT
  -c CC_ADDR [CC_ADDR ...], --cc_addr CC_ADDR [CC_ADDR ...]
  -b BCC_ADDR [BCC_ADDR ...], --bcc_addr BCC_ADDR [BCC_ADDR ...]
  -r REPLY_ADDR, --reply_addr REPLY_ADDR
  -h HTML_FILE, --html_file HTML_FILE
  -p PLAINTEXT_FILE, --plaintext_file PLAINTEXT_FILE
  -d DEBUGLEVEL, --debuglevel DEBUGLEVEL
  -f FROM_ADDR, --from_addr FROM_ADDR
~~~
