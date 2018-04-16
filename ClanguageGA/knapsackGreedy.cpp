#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#define size 20

struct goods{
        int id;
        int weight;
        int value;
        double ratio;
};

int number = 0;
int capacity;
void fileInput(struct goods *good);
void printStruct(struct goods *knapsack);
void sort(struct goods *knapsack);
void select(struct goods *knapsack);



void fileInput(struct goods *good){
  FILE *fp;
  int i;
  fp = fopen("kp20.txt","r");
  int count = 0;
	if(fp == NULL)
		exit(0);
	while( fscanf(fp, "%d", &i) != EOF ){
		if(count == 0){
      number = i;
    }
		else if(count == 1){
			capacity = i;
		}
		else if(count > 1&& count<2+size){
			good[count-2].value=i;
		}
		else{
      // printf("%d  ", i);
			good[count-(2+size)].weight=i;
		}
		count++;
	}
}


void printStruct(struct goods *knapsack){
  for(int i=0; i<20; i++){
    printf("id:%d  ",knapsack[i].id);
    printf("value:%d  ",knapsack[i].value);
    printf("weight:%d  ",knapsack[i].weight);
    printf("\n");
  }
  printf("\n");
}


void sort(struct goods *knapsack){
  int i,j;
  struct goods temp;
  for(j=0;j<size-1;j++){
    for(i=0;i<size-1-j;i++){
      if (knapsack[i].ratio>knapsack[i+1].ratio){
        temp=knapsack[i];
        knapsack[i]=knapsack[i+1];
        knapsack[i+1]=temp;
      }
    }
  }
}


void select(struct goods *knapsack){
  int j;
  int echoCounter=1;
  int valueSum=0;
  int weightSum=0;
  for(j=19;j>=0;j--){
		valueSum=valueSum+knapsack[j].value;
		weightSum=weightSum+knapsack[j].weight;
		if(weightSum>capacity){  //重量が超えた場合
			valueSum=valueSum-knapsack[j].value;
			weightSum=weightSum-knapsack[j].weight;
      continue;
		}
    printf("echo:%d   ",echoCounter);
    printf("id:%d   ",knapsack[j].id);
    printf("value:%d   ",knapsack[j].value);
    printf("weightSum:%d   ",weightSum);
    printf("\n");
    echoCounter++;
	}
  printf("The sum of value is %d\n", valueSum);
}


int main(){
  struct goods knapsack[size];
  fileInput(knapsack);
  for(int i = 0; i<20; i++){
    knapsack[i].id = i+1;
    knapsack[i].ratio = knapsack[i].value / (double)knapsack[i].weight;
  }
  printf("Original:\n");
  printStruct(knapsack);
  sort(knapsack);
  printf("Sorted:\n");
  printStruct(knapsack);
  select(knapsack);
}
