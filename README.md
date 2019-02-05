# mail_proj
Utility to replace /usr/bin/mail on macos

__mail.py__ is a Python 3 script for sending email messages from the command line. Unlike /usr/bin/mail, it can be used only to send messages,
not to process incoming messages. It supports the -s (subject) option of /usr/bin/mail, plus additional command line options for setting
up plain text (-p) and html (-h) message parts, but will accept a plain text message body from stdin if neither the -p nor -h option is 
specified.

## Why?

Bash scripts that sent email using `/usr/bin/mail` on MacOS failed after an Apple security update in January 2019. I was unable to get any
useful information about the issue from Apple support or on https://developer.apple.com (hundreds of views; zero replies), so I wrote this as a
workaround.

## Requirements and Environment

  * This is a Python 3 application. The command assumes the interpreter is _/usr/local/bin/python3_. Edit the first line if this path needs
to be changed.
  * The environment variable `SMTP_SERVER` specifies the hostname of the server that will send the message. If not set, _localhost_ will be
used instead.
  * The environment variable `EMAIL_SENDER` specifies the sender’s email address. The `from_addr` command line argument may be used instead.
    * `User Name <user@example.com>`
    * `user@example.com`
  * If neither a plain text file (`-p`) nor a HTML file (`-h`) is specified, a plain text message body is read from stdin.
  * The default `Subject:` is _Test Message_
  * Use `-?` or `--help` for command line options and arguments.
  
