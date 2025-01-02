int M[];
int x;
int y;
int A;

void main(int A0) {
  int x = 23;
  int y = 42;
  int u = 42;

  M[u] = x * y;

  int z = M[u] + 1;

  M[u] = z;
}