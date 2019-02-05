# mail_proj
Utility to replace `/usr/bin/mail` on MacOS.

__mail.py__ is a Python 3 script for sending email messages from the command line. Unlike
/usr/bin/mail, it can be used only to send messages, not to process incoming messages. It can be
used to send multipart messages with plain text and/or HTML message parts.

## Why?

Bash scripts that sent email using `/usr/bin/mail` on MacOS failed after an Apple security update in
January 2019. I was unable to get any useful information about the issue from Apple support and on
https://developer.apple.com (hundreds of views; zero replies), so I wrote this as a workaround.

## Requirements and Environment

  * This is a Python 3 application. The command assumes the interpreter is `/usr/local/bin/python3`.
  Edit the first line of the code if this path needs to be changed.
  * The environment variable `SMTP_SERVER` specifies the hostname of the server that will relay the
  message. If not set, the environment variable `HOSTNAME` will be used instead.
  * The `-f` or `--from_addr` command line option may be used to specify the sender’s email address.
  The default value is `$USER@$HOSTNAME`. Valid formats are:
    * `User Name <user@example.com>`
    * `user@example.com`
  * If neither a plain text file (`-p`) nor a HTML file (`-h`) is specified, a plain text message
  body is read from stdin.
  * The default `Subject:` is “Test Message”
  * Use `-?` or `--help` for all command line options and arguments.

