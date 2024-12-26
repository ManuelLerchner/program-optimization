int A;
int M[];

void main() {
  int A1 = A + 7;
  int B1 = M[A1];
  int B2 = B1 - 1;
  int A2 = A + 7;
  M[A2] = B2;
}