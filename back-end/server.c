#include <stdio.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <string.h>
#include<pthread.h> //for threading , link with lpthread


//the thread function
void *connection_handler(void *);
 

int main(int argc, char *argv[]){

    int fd =0, confd = 0,b,tot;
    struct sockaddr_in serv_addr;

    char buff[1025];
    int num;

    char nom[1024];

 /*char nom[200];
        printf("donner un nom pour ce client :");
        scanf("%s",nom);
        char lien[100] = "/var/www/html/";
        strcat(lien,nom );
        strcat(lien,".html" );
        printf("le chemin de la client %s est %s\n",nom ,lien);    
*/

    fd = socket(AF_INET, SOCK_STREAM, 0);
    printf("Socket created\n");

    memset(&serv_addr, '0', sizeof(serv_addr));
    memset(buff, '0', sizeof(buff));
    
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(5000);

    bind(fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr));
    listen(fd, 10);
    printf("----------------------------------------------------------------\n");
   
    while(1){
        confd = accept(fd, (struct sockaddr*)NULL, NULL);
        if (confd==-1) {
            perror("Accept");
            continue;


        }
    
pid_t pid = fork();
        
        if (pid == -1) {
		// Il y a une erreur
		perror("fork");
		return EXIT_FAILURE;
        
        } 
        else if (pid == 0) {
            recv(confd, nom, sizeof(nom), 0);
            printf("Thread Created for client : %s \n",nom);

		//change the value of this directory if you don't work with a oba user ! 
            char lien[300] = "/home/oba/Documents/oba/App/clients/";
            strcat(lien,nom );
            strcat(lien,".txt" );
            printf("le fichier est enregistrer sous : %s\n",lien); 

            FILE* fp = fopen( lien, "wb");
            tot=0;
            if(fp != NULL){
                while( (b = recv(confd, buff, 1024,0))> 0 ) {
                    tot+=b;
                    fwrite(buff, 1, b, fp);
                }

                printf("Received byte: %d\n",tot);
                if (b<0)
                perror("Receiving");
                printf("----------------------------------------------------------------\n");
                fclose(fp);
            } else {
                perror("File");
            }
            close(confd);
            }
    }

    return 0;
}
