#!/bin/bash

#------colors----------
red="\033[1;31m"
green="\033[1;32m"
yellow="\033[1;33m"
blue='\033[0;34m'  
purple='\033[1;35m'
cyan='\033[1;36m'  
off="\033[0m"
user=$( echo $USER )
#----------------------



function getdata() {

#--checking --
if ! which mpstat > /dev/null; then
   echo -e "Command not found! Install? (y/n) \c "
   read REPLY
   if "$REPLY" = "y"; then
        sudo apt-get install sysstat
   fi
fi

if ! which free > /dev/null; then
   echo -e "
   Command not found! Install? (y/n) \c"
   read REPLY
   if "$REPLY" = "y"; then
        sudo apt-get install free
   fi
fi

#------------------
echo " "> status.txt

echo -e "\n{ HOST details } \n" >> status.txt
cat /etc/hostname >> status.txt
cat /etc/lsb-release | tail -n 1 | cut -d"=" -f2 | sed 's/\"//g' >> status.txt
echo -e "\n" >> status.txt

echo -e "{ Bloc DISK }\n" >> status.txt 
echo "Sys. de fichiers blocs de 1M Utilisé Disponible Uti% Monté sur" >> status.txt

df -BM | grep -i "/$" >> status.txt
echo -e "\n" >> status.txt 


echo -e "{ Bloc RAM }\n" >> status.txt 
free -tm >> status.txt
echo -e "\n" >> status.txt 

echo -e "{ Bloc CPU } \n" >> status.txt 
mpstat -P ALL | head -4 | awk '{print $14}' | tail -1 >> status.txt
echo -e "\n" >> status.txt 


echo -e "{ Bloc Interfaces } \n" >> status.txt 
ip a | grep -e "UP" | grep BROADCAST,MULTICAST,UP | awk '{print $2}' | cut -d":" -f1 >> status.txt

echo -e "\n{ adresse ip } \n" >> status.txt
ip a | grep brd | grep inet | awk {'print $2'} | cut -d'/' -f1 >> status.txt

echo -e "\n{ Graphic Card } \n" >> status.txt
sudo lshw -C video | grep produit >> status.txt



}

function compilation() {
#-----------------------Compilation --------------------------------------------
   k=$(ls -l | grep server | wc -l )
   if [[ $k -ne 2  ]]; then
   echo -e "${red}[-]You Missed to Compile the Server file ! ${off}"
   sleep 1
   gcc server.c -o server 
   fi

   k=$(ls -l | grep client | wc -l )
   if [[ $k -ne 3  ]]; then
      echo -e "${red}[-]You Missed to Compile the Client file ! ${off}"
      sleep 1
      gcc client.c -o client 

   fi
#-------------------------------------------------------------------
user=$( echo $USER )

  if [[  -n $(find . -type f -name "*.c") ]]; then 
      echo -e "${yellow}[+]binary files exist .. ${off}"
   else
      echo -e "${red}[-]binary files does not exist${off}"
   fi  
   sleep 1

   if [[  -n $(find . -type f -name "status.txt") ]]; then 
      echo -e "${yellow}[+]Generating The Supervisor File ! ${off}"
   else
      echo -e "${red}[-]file does not exist${off}"
   fi  

      echo -e "${blue}[+]Sending The file to the server ${off}"
      echo -e "${purple}[!]Give us your name to save the file with it ${off} :"
      read name
      echo -e "${purple}[!]Give us the Server IP : ${off} :"
      read adr

      ./client $adr $(pwd)/status.txt $name
      sleep 1
      
sleep 1
}

function syncro() {

echo -e "${yellow}[!]Do you want automate it every 30 min with crontab : ${off}[y/n]"
read  reply 
if [ $reply = "y" ]; then

sudo  echo " */30 * * * * sudo ./$(pwd)/status.sh" > /etc/crontab 

fi

}

function logevents() {
sudo cat /var/log/boot.log.1 > /tmp/$name.log
./client $adr  /tmp/$name.log $name


}

#---------------------------------------------------------

function banner() {
echo -e "${yellow}"
cat banner.txt
echo -e "${off}"

}

#-------------------------main----------------------------
if [[ $EUID -ne 0 ]]; then
   echo -e "${red}[!]This script must be run as root${off}" 
   exit 1
else


while [ "$1" != "" ]; do
    PARAM=`echo $1 | awk -F= '{print $1}'`

    case $PARAM in
     -h | --help)
        banner
     echo -e "${blue}+------------------------------------------------------------------------------------+${off}
-h  | --help :${blue} Help menu.${off}
-l  | --loop :${blue} Keep the client sending data each 5 min.${off}
-s  | --simple_send:${blue} send client data and close the connection .${off}
${blue}+------------------------------------------------------------------------------------+${off}
"   exit
    ;;

    -l  | --loop)
   
while true;do
      banner
      getdata
      compilation
      syncro
      #logevents
      sleep 5m
done
     ;;

     -s  | --simple_send)
      banner
      getdata
      compilation
      syncro
      #logevents
     
     ;;
        *)
            echo -e "${red}[-]- ERROR: unknown parameter \"$PARAM\" ${off}"
         
            exit 1
            ;;
    esac
    shift
done


fi
