#include <stdio.h>    // Used for printf() statements
#include <wiringPi.h> // Include WiringPi library!
#include <softPwm.h>  // Software PWM 
#include<string.h> //memset
#include<stdlib.h> //exit(0);
#include<arpa/inet.h>
#include<sys/socket.h>
#include <signal.h>
#include <unistd.h>

void INThandler(int);

#define BUFLEN 512  //Max length of buffer
#define PORT 14000   //The port on which to listen for incoming data

// Pin number declarations. 
const int ENA = 0; 
const int IN1 = 1; 
const int IN2 = 2; 
const int ENB = 3; 
const int IN3 = 4; 
const int IN4 = 5; 

void die(char *s)
{
    perror(s);
    exit(1);
}

//int main(void)

int main(int argc, char **argv)
{
	// Register signals 
	signal(SIGINT, INThandler);

    // Setup stuff:
    wiringPiSetup(); // Initialize wiringPi
	softPwmCreate(ENA,0,100);
	softPwmCreate(ENB,0,100);
	pinMode(IN1,1);
	pinMode(IN2,1);
	pinMode(IN3,1);
	pinMode(IN4,1);

	struct sockaddr_in si_me, si_other;
     
    int s, i, slen = sizeof(si_other) , recv_len;
    char buf[BUFLEN];
     
    //create a UDP socket
    if ((s=socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) == -1)
    {
        die("socket");
    }
     
    // zero out the structure
    memset((char *) &si_me, 0, sizeof(si_me));
     
    si_me.sin_family = AF_INET;
    si_me.sin_port = htons(PORT);
    si_me.sin_addr.s_addr = htonl(INADDR_ANY);
     
    //bind socket to port
    if( bind(s , (struct sockaddr*)&si_me, sizeof(si_me) ) == -1)
    {
        die("bind");
    }     	

	printf("CBiS Education - 4WD Remote Control Car Server\nReady to receive commands...\n");
	
    //keep listening for data
    while(1)
    {
		fflush(stdout);

        //try to receive some data, this is a blocking call
        if ((recv_len = recvfrom(s, buf, BUFLEN, 0, (struct sockaddr *) &si_other, &slen)) == -1)
        {
            die("recvfrom()");
        }
		buf[recv_len] = '\0';// <<-- Really important bit!
		//printf("Data: %s\n" , buf);

		if (strcmp(buf,"RELEASE") == 0)
		{
			printf("RELEASE string received\n");
            softPwmWrite(ENA,0);
            softPwmWrite(ENB,0);
		}
		else
		{				
			if (strstr(buf, "C:") != NULL) {				
				char *ret;
				ret = strchr(buf, ':');				
				char commandstr1[10];
				strcpy(commandstr1, ret);
				
				char *token1;
				char commandstr2[10];
				token1 = strtok(commandstr1, ":");
				strcpy(commandstr2, token1);

				//printf("Car Command Received %s\n", commandstr2);
				//fflush(stdout);

				char lcmd[32], rcmd[32];

				char *token;
				token = strtok(commandstr2, "|");
				strcpy(lcmd, token);
				token = strtok(NULL, "|");
				strcpy(rcmd, token);

				//printf("left breakdown: %s\n", lcmd);
				//printf("right breakdown: %s\n", rcmd);

				int leftcommand;
				int rightcommand;

				leftcommand = atoi(lcmd);				
				rightcommand = atoi(rcmd);

				// Define the direction of the motors
				if(leftcommand < 0)
				{					
					// Left motors backwards
					leftcommand = leftcommand * -1;
					digitalWrite(IN1,1);
					digitalWrite(IN2,0);                       
				}else{
					//Left motors forwards
					digitalWrite(IN1,0);
					digitalWrite(IN2,1);
				}

				if(rightcommand < 0)
				{
					// Right motors backwards					
					rightcommand = rightcommand * -1;
					digitalWrite(IN3,0);
					digitalWrite(IN4,1);
				}else{
					// Right motors forwards
					digitalWrite(IN3,1);
					digitalWrite(IN4,0);
				}

				// Velocity demand - how fast
				softPwmWrite(0,leftcommand);
				softPwmWrite(3,rightcommand); 
			}else{
				//printf("This is not a command string\n");
				//Nothing of use - so just ignore it.
			}
		}
	}
	//Clean up on exit	
    close(s);
    return 0;
}

void  INThandler(int sig)
{
	softPwmWrite(0,0);
	softPwmWrite(3,0);
	exit(0);
}