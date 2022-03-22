#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>

void sigint_handler(int sig) {
  return;
}

int main(int argc, char *argv[]){
  if(signal(SIGINT, sigint_handler)==SIG_ERR){
      printf("signal error\n");
      exit(0);
  }
  
  int total = atoi(argv[1]);
  unsigned int k = sleep(total);
  printf("Slept for %d of %d secs\n", total-k, total);
  return 0;
}
