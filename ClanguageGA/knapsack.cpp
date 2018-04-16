#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#define size 20


void selectionsort(double num[],int num2[],int id[],int len){
	int i,min_pos,n,min_pos2,min_id,id_pos,tmp3;
	double tmp;
	int tmp2;
	double min;
	int min2;
	for(i=0;i<len;i++){
		min=num[i];   /*仮の最小値を最初の数*/
		min_pos=i;    /*仮の最小値の場所*/
		min2=num2[i];
		min_pos2=i;
		for(n=i+1;n<len;n++){
			if(num[n]>min){   /*比較対象の数字が仮の最小値より大きければ、仮の最小値をそれにする*/
				min=num[n];
				min_pos=n;
				min2=num2[n];
				min_pos2=n;
        min_id=id[n];
        id_pos=n;
        // printf("%d  ",n);
			}
		}
		for(int counter=0; counter<20; counter++){
			printf("%d  ",id[counter]);
		}
		printf("\n");
		tmp=num[i];     /*最小値と最初の数を交換*/
		num[i]=min;
		num[min_pos]=tmp;
		tmp2=num2[i];
		num2[i]=min2;
		num2[min_pos2]=tmp2;
    tmp3=id[i];
    id[i]=min_id;
    id[id_pos]=tmp3;
	}

  for(int counter=0; counter<20; counter++){
    printf("%d  ",id[counter]);
  }
  printf("\n");
}

void print_array(double num[],int len){
	int i;
	for(i=0;i<len;i++){
		printf("%f ",num[i]);
	}
}

int main(){
	FILE *fp;
	int N;        //荷物の数
	int b;        //袋の容量
	int c[size];  //荷物の価値
	int a[size];  //荷物の重量
  int id[size] = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20};
	int i,j;
	int count = 0;
	double d[size]; //重量あたりの価値
	int g[size];
	int sum=0,sum2=0;
	fp = fopen("kp20.txt","r");
	if(fp == NULL)
		exit(0);
	while( fscanf(fp, "%d", &i) != EOF ){

		if(count == 0){
			N=i;
		}
		else if(count == 1){
			b=i;
		}
		else if(count > 1&& count<2+size){
			c[count-2]=i;
		}
		else{
      // printf("%d  ", i);
			a[count-(2+size)]=i;
		}
		count++;
	}

	printf("N=%d, b=%d\n",N,b);
	for(j=0; j<size; j++){
		d[j]=(double)c[j]/a[j];   //重量あたりの価値を求める

	}

	selectionsort(d,a,id,size);
  int echoCounter=1;
	for(j=0; j<size; j++){
		g[j]=round(d[j]*a[j]);
	}
	for(j=0;j<size;j++){
		sum=sum+g[j];
		sum2=sum2+a[j];
		if(sum2>b){  //重量が超えた場合
			sum=sum-g[j];
			sum2=sum2-a[j];
      continue;
		}
    printf("echo:%d   ",echoCounter);
    printf("id:%d   ",id[i]);
    printf("value:%d   ",g[j]);
    printf("weight:%d   ",sum2);
    printf("\n");
    echoCounter++;
	}

	printf("価値の総和%d\n",sum);

	fclose(fp);
	return 0;
}
