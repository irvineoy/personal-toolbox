// 1-max-sga.c
// Kazutoshi Sakakibara (June 13, 2010)

#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

#define N 15   // 遺伝子長
#define M 15   // 個体数
#define T 100  // 世代数
#define Pc 0.30  // 交叉確率
#define Pm 0.10   // 突然変異確率

// 遺伝子型の定義
struct genotype {
    int gene[N];   // 遺伝子
    float fitness;   // 適応度
};
int maxArray[100];
int globalPoint = 0;

float evaluation(int *a);
void one_point_crossover(struct genotype *ind);
void mutation(struct genotype *ind);
void roulette_selection(struct genotype *ind);
int flip(float prob);
void print_process(struct genotype *ind, int generation);
void select_best(struct genotype *ind);
void writeFile();

int main(int argc, char *argv[]) {
    int i;   // 個体インデックス
    int j;   // 遺伝子座インデックス
    int t;   // 世代インデックス
    struct genotype individual[M];      // 個体

    // 乱数seedの設定
    if(argc < 2) {   // プログラムの引数が足りない場合
        printf("Usage: %s [SEED_NUMBER]\n", argv[0]);
        exit(1);
    }
    else {
        srandom(atoi(argv[1]));
    }

    // ステップ1 (0世代目)
    for(i=0; i<M; i++) {
        for(j=0; j<N; j++) {
            individual[i].gene[j] = flip(0.5);
        }
        individual[i].fitness = evaluation(individual[i].gene); // 個体の適応度計算
    }
    print_process(individual, 0); // 初期世代の個体群を表示
    select_best(individual);

    // ステップ2 (1～T世代)
    for(t=1; t<=T; t++) {
        roulette_selection(individual);
        print_process(individual, t);
        one_point_crossover(individual);
        mutation(individual);
    }
    writeFile();
    return(0);
}   // End of main()


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


// 個体の適応度計算
float evaluation(int *a) {
    int j;   // 遺伝子座インデックス
    int count = 0;   // 遺伝子中の`1'の数

    for(j=0; j<N; j++) {
        count += a[j];
    }
    return((float)count);
}   // End of evaluation()


// 一点交叉
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
        ind[i].fitness = evaluation(ind[i].gene);
    }
    //select_best(ind);
    //if (ind[0].fitness < genoTemp.fitness)
    ind[0] = genoTemp;
    //else ind[0] = genoTemp;
}   // End of one_point_crossover()


// 突然変異
void mutation(struct genotype *ind) {
    int i;   // 個体インデックス
    int j;   // 遺伝子座インデックス
    struct genotype temp;

    //select_best(ind);
    temp = ind[0];
    for(i=0; i<M; i++)
        for(j=0; j<N; j++)
            if(flip(Pm)) {
                ind[i].gene[j] = (ind[i].gene[j] + 1) % 2;
            }
    for(i=0; i<M; i++) {
        ind[i].fitness = evaluation(ind[i].gene);
    }
    //select_best(ind);
    //if (ind[0].fitness < temp.fitness)
    ind[0] = temp;
    //else ind[0] = temp;
}   // End of mutation()


// ルーレット選択
void roulette_selection(struct genotype *ind) {
    int h, i;   // 個体インデックス
    float total_fitness;   // 適応度の合計値
    float dart;   // 矢
    float wheel;  // ルーレット・ホイール
    struct genotype ind_new[M];   // 選択操作後の個体集合

    // 適応度の合計値を計算
    select_best(ind);
    ind_new[0] = ind[0];

    total_fitness = 0;
    for(i=1; i<M; i++) total_fitness += ind[i].fitness;

    // ルーレット・ホイールに従って次世代(ind_new[])を決定
    for(i=1; i<M; i++) {
        dart = (float)random() / RAND_MAX;
        h = 1;
        wheel = ind[h].fitness / total_fitness;
        while(dart > wheel && h < M-1) {
            h++;
            wheel += ind[h].fitness / total_fitness;
        }
        ind_new[i] = ind[h];
    }

    // 個体集合の更新
    for(i=1; i<M; i++) {
        ind[i] = ind_new[i];
    }

}   // End of roulette_selection()


// 引数`prob'の確率で1を返す
int flip(float prob) {
    float x = (float)random() / RAND_MAX;

    if(x<prob) return(1);
    else return(0);
}   // End of flip()


// 個体の中身や適応度値を画面に出力
void print_process(struct genotype *ind, int generation) {
    int i;   // 個体インデックス
    int j;   // 遺伝子座インデックス
    float max_fit, min_fit, avg_fit;   // 最大，最小，平均適応度

    // 各個体の中身を出力
    printf("\nGeneration: %d\n", generation);
    for(i=0; i<M; i++) {
        printf("%d: ", i);
        for(j=0; j<N; j++) {
            if(ind[i].gene[j] == 0) printf("%c", ' ');
            else printf("%c", '*');
        }
        printf(" : %.0f\n", ind[i].fitness);
    }

    // 個体集団の最大，最小，平均適応度を求める
    max_fit = min_fit = ind[0].fitness;
    avg_fit = ind[0].fitness / M;
    for(i=1; i<M; i++) {
        if(max_fit < ind[i].fitness) max_fit = ind[i].fitness;
        if(min_fit > ind[i].fitness) min_fit = ind[i].fitness;
        avg_fit += ind[i].fitness / M;
    }
    printf("max: %.2f  min: %.2f  avg: %.2f\n", max_fit, min_fit, avg_fit);
    maxArray[globalPoint] = max_fit;
    globalPoint ++;
}   // End of print_process()

void writeFile(){
  FILE *fp;
  if((fp = fopen("outPut.txt", "a+")) == NULL){
    printf("The file can not be opened.¥n");
    exit(1);
  }
  for(int i = 0; i < 100; i++){
    fprintf(fp, "%d,", maxArray[i]);
    printf("%d  ", maxArray[i]);
  }
  fprintf(fp, "\n");
  fclose(fp);
}
