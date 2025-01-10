int n;
int i;
int fact;
int result;

void main() {
  int n = 5;
  fact = 1;
  i = 1;
  while (i <= n) {
    fact = fact * i;
    i = i + 1;
  }

  result = fact;
}