
int M[];

int ret;
int v1;
int v2;

int max() {
  if (v1 > v2) {
    ret = v1;
  } else {
    ret = v2;
  }
}

void main() {
  int v1 = 3;
  int v2 = 5;

  max();

  M[17] = ret;
  ret = 0;
}