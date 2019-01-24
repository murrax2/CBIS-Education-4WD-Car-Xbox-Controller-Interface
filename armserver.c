#include <stdio.h>    // Used for printf() statements
#include<string.h> //memset
#include<stdlib.h> //exit(0);
#include<arpa/inet.h>
#include<sys/socket.h>
#include <signal.h>
#include <unistd.h>
#include <sys/types.h> 
#include <stddef.h>
#include <sys/wait.h>

/* Execute the command using this shell program.  */
#define ARMCONTROL "/bin/armcontrol"

int
controlarm (const char *command1, const char *command2, const char *command3)
{
  int status;
  pid_t pid;
  pid = fork ();
  if (pid == 0)
    {
      /* This is the child process.  Execute the shell command. */
      execl (ARMCONTROL, ARMCONTROL, command1, command2, command3, NULL);
      _exit (EXIT_FAILURE);
    }
  else if (pid < 0)
    /* The fork failed.  Report failure.  */
    status = -1;
  else
    /* This is the parent process.  Wait for the child to complete.  */
    if (waitpid (pid, &status, 0) != pid)
      status = -1;
  return status;
}

void INThandler(int);

#define BUFLEN 512  //Max length of buffer
#define PORT 14100   //The port on which to listen for incoming data

void die(char *s)
{
    perror(s);
    exit(1);
}

int main(int argc, char **argv)
{
	// Register signals 
	signal(SIGINT, INThandler);

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

	printf("CBiS Education - Robot Arm Server\nReady to receive commands...\n");
	
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
		
		printf("Command: %s\n", buf);

		if (strcmp(buf,"STOP") == 0)
		{
			controlarm("00","00", "00");
		}
		else if (strcmp(buf,"LIGHTON") == 0)
		{
			controlarm("00","00", "01");
		}
		else if (strcmp(buf,"LIGHTOFF") == 0)
		{
			controlarm("00","00", "00");
		}
		else if (strcmp(buf,"GRIPPEROPEN") == 0)
		{
			controlarm("02","00", "00");
		}
		else if (strcmp(buf,"GRIPPERCLOSE") == 0)
		{
			controlarm("01","00", "00");
		}
		else if (strcmp(buf,"WRISTUP") == 0)
		{
			controlarm("04","00", "00");
		}
		else if (strcmp(buf,"WRISTDOWN") == 0)
		{
			controlarm("08","00", "00");
		}
		else if (strcmp(buf,"ELBOWUP") == 0)
		{
			controlarm("10","00", "00");
		}
		else if (strcmp(buf,"ELBOWDOWN") == 0)
		{
			controlarm("20","00", "00");
		}
		else if (strcmp(buf,"SHOULDERUP") == 0)
		{
			controlarm("40","00", "00");
		}
		else if (strcmp(buf,"SHOULDERDOWN") == 0)
		{
			controlarm("80","00", "00");
		}
		else if (strcmp(buf,"BASELEFT") == 0)
		{
			controlarm("00","02", "00");
		}
		else if (strcmp(buf,"BASERIGHT") == 0)
		{
			controlarm("00","01", "00");
		}
		else
		{
			printf("Unknown Command - Stop All\n" );
			controlarm("00","00", "00");
		}
	}
	//Clean up on exit	
    close(s);
    return 0;
}

void  INThandler(int sig)
{
	controlarm("00","00", "00");
	exit(0);
}