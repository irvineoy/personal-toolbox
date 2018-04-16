// 4.4.1 problem: 一定重量かつ一定容積
// txt file name: kpDoubleConstraint20.txt
#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<stdlib.h>
#include<limits.h>
#include<algorithm>
#define N 20   // 遺伝子長
#define M 32   // 個体数
#define T 1000  // 世代数
#define Pc 0.95  // 交叉確率
#define Pm 0.01   // 突然変異確率
#define alpha 10    // The penalty coefficient


void printStruct(struct goods *knapsack);    // show the information of goods which was inputed from file
void fileInput(struct goods *good);    // input the goods information from file
float evaluation(struct genotype ind);    // return the fitness of one individual gene
void one_point_crossover(struct genotype *ind);    // one point crossover operation of two genes
void mutation(struct genotype *ind);    // mutation operation of one gene
void roulette_selection(struct genotype *ind);    // roulette selection operation from the whole population
int flip(float prob);    // Return true with a prob probability
void print_process(struct genotype *ind, int generation);    // print the each gene in the population
void select_best(struct genotype *ind);    // select the gene with best fitness for saving the elite
double max(double a, double b);    // return the bigger one of a and b




struct goods{
		int id;
		int weight;
		int value;
		int bulk;
		// double ratio;
};
struct genotype {
	int gene[N];   // 遺伝子
	float fitness;   // 適応度
};
struct genotype tempGlobal;
int weightCapacity;
int bulkCapacity;
struct goods knapsack[N];




int main(int argc, char *argv[]) {
	fileInput(knapsack);
	printStruct(knapsack);
	struct genotype individual[M];      // 個体
	if(argc < 2) {   // プログラムの引数が足りない場合
		printf("Usage: %s [SEED_NUMBER]\n", argv[0]);
		exit(1);
	}
	else {
		srandom(atoi(argv[1]));
	}
	for(int i=0; i<M; i++) {
		for(int j=0; j<N; j++) {
			individual[i].gene[j] = flip(0.5);
		}
		individual[i].fitness = evaluation(individual[i]); // 個体の適応度計算
	}
	print_process(individual, 0); // 初期世代の個体群を表示
	select_best(individual);
	tempGlobal = individual[0];
	for(int t=1; t<=T; t++) {
		roulette_selection(individual);
		print_process(individual, t);
		one_point_crossover(individual);
		mutation(individual);
	}
	return(0);
}





void select_best(struct genotype *ind){
  struct genotype temp;
  float max_fitness = 0;
  int max_point = 0;
  for(int i = 0; i < M; i++){
	if (max_fitness < ind[i].fitness){
	  max_fitness = ind[i].fitness;
	  max_point = i;
	}
  }
  temp = ind[0];
  ind[0] = ind[max_point];
  ind[max_point] = temp;
}

float evaluation(struct genotype ind) {
	int fitnessTemp=0, allWeight=0, allBulk=0;
	for(int j=0; j<N; j++){
		fitnessTemp += knapsack[j].value * ind.gene[j];
		allBulk += knapsack[j].bulk * ind.gene[j];
		allWeight += knapsack[j].weight * ind.gene[j];
	}
	fitnessTemp = fitnessTemp - 
		alpha * max(0, allWeight - weightCapacity) - 
		alpha * max(0, allBulk - bulkCapacity);
	return fitnessTemp;
}   // End of evaluation()

void one_point_crossover(struct genotype *ind) {
	int i, ia, ib;   // 個体インデックス
	int j;   // 遺伝子座インデックス
	int c;   // 交叉点
	int test[M];   // 個体の利用フラグ
	int temp[N];   // 遺伝子を入れ替えるための仮変数
	int r;   // 乱数値
	struct genotype genoTemp;
	genoTemp = ind[0];
	for(i=0; i<M; i++) test[i] = 0;
	ia = ib = 0;
	for(i=0; i<M/2; i++) {
		// 個体をランダムにペアリング (親個体ia,ibを選ぶ)　// 親iaを決定
		for(; test[ia]==1; ia=(ia+1)%M);
		test[ia] = 1;
		r = random() % (M-2*i) + 1;
		// (iaとは異なる)親ibを決定
		while(r>0) {
			ib=(ib+1)%M;
			for(; test[ib]==1; ib=(ib+1)%M);
			r--;
		}
		test[ib] = 1;
		// 個体iaとibの遺伝子を入れ替える
		if(flip(Pc)) {
			c = random() % N;
			for(j=0; j<c; j++) {
				temp[j] = ind[ia].gene[j];
				ind[ia].gene[j] = ind[ib].gene[j];
				ind[ib].gene[j] = temp[j];
			}
		}
	}
	for(i=0; i<M; i++) {
		ind[i].fitness = evaluation(ind[i]);
	}
}   // End of one_point_crossover()

void mutation(struct genotype *ind) {
	int i;   // 個体インデックス
	int j;   // 遺伝子座インデックス
	struct genotype temp;
	temp = ind[0];
	for(i=0; i<M; i++)
		for(j=0; j<N; j++)
			if(flip(Pm)) {
				ind[i].gene[j] = (ind[i].gene[j] + 1) % 2;
			}
	for(i=0; i<M; i++) {
		ind[i].fitness = evaluation(ind[i]);
	}
}   // End of mutation()

void roulette_selection(struct genotype *ind) {
	int h, i;   // 個体インデックス
	float total_fitness;   // 適応度の合計値
	float dart;   // 矢
	float wheel;  // ルーレット・ホイール
	struct genotype ind_new[M];   // 選択操作後の個体集合
	total_fitness = 0;
	for(i=0; i<M; i++) total_fitness += ind[i].fitness;
	for(i=0; i<M; i++) {
		dart = (float)random() / RAND_MAX;
		h = 0;
		wheel = ind[h].fitness / total_fitness;
		while(dart > wheel && h < M-1) {
			h++;
			wheel += ind[h].fitness / total_fitness;
		}
		ind_new[i] = ind[h];
	}
	for(i=0; i<M; i++) {
		ind[i] = ind_new[i];
	}
	select_best(ind);
	ind[1] = tempGlobal;
	select_best(ind);
	tempGlobal = ind[0];
}   // End of roulette_selection()

int flip(float prob) {
	float x = (float)random() / RAND_MAX;
	if(x<prob) return(1);
	else return(0);
}   // End of flip()

void print_process(struct genotype *ind, int generation) {
	float max_fit, min_fit, avg_fit;   // 最大，最小，平均適応度
	int maxPoint, weightSum, bulkSum;
	printf("\nGeneration: %d\n", generation);
	for(int i=0; i<M; i++) {
		printf("%d: ", i);
		weightSum = 0;
		bulkSum = 0;
		for(int j=0; j<N; j++) {
			if(ind[i].gene[j] == 0) ;//printf("%c", ' ');
			else {
				// printf("%c", '*');
				weightSum += knapsack[j].weight;
				bulkSum += knapsack[j].bulk;
			}
		}
		printf(" fitness: %.0f  weightSum:%d  bulkSum:%d\n", ind[i].fitness, weightSum, bulkSum);
	}
	max_fit = min_fit = ind[0].fitness;
	avg_fit = ind[0].fitness / M;
	for(int i=1; i<M; i++) {
		if(max_fit < ind[i].fitness){
			max_fit = ind[i].fitness;
			maxPoint = i;
		}
		if(min_fit > ind[i].fitness) min_fit = ind[i].fitness;
		avg_fit += ind[i].fitness / M;
	}
	printf("max: %.2f  min: %.2f  avg: %.2f\n", max_fit, min_fit, avg_fit);
}   // End of print_process()

void fileInput(struct goods *good){
	FILE *fp;
	int i;
	fp = fopen("kpDoubleConstraint20.txt","r");
	int count = 0;
	if(fp == NULL)
		exit(0);
	while( fscanf(fp, "%d", &i) != EOF ){
		printf("%d\n", i);
		if(count == 0){
		// N = i;
		}
		else if(count == 1){
			weightCapacity = i;
		}
		else if(count == 2){
			bulkCapacity = i;
		}
		else if(count > 2 && count <= 2+N){
			good[count-2-1].value=i;
		}
		else if(count > 2+N && count <= 2+N+N){
			good[count-2-N-1].weight=i;
		}
		else{
			// printf("%d  ", i);
			good[count-(2+N+N)-1].bulk=i;
		}
		count++;
	}
	for(i = 0; i<N; i++){
	knapsack[i].id = i+1;
	// knapsack[i].ratio = knapsack[i].value / (double)knapsack[i].weight;
	}
}

void printStruct(struct goods *knapsack){
  for(int i=0; i<20; i++){
	printf("id:%d  ",knapsack[i].id);
	printf("value:%d  ",knapsack[i].value);
	printf("weight:%d  ",knapsack[i].weight);
	printf("bulk:%d  ",knapsack[i].bulk);
	printf("\n");
  }
  printf("\n");
}

double max(double a, double b){
  if(a>b) return a;
  else return b;
}
