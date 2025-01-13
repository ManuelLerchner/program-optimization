
int M[];
int curr;
int i;
int ret;

int fact() {
  if (i == 0) {
    ret = curr;
  } else {
    curr = curr * i;
    i = i - 1;
    fact();
  }
}

void main() {
  curr = 1;
  i = 5;
  fact();

  M[17] = ret;
  ret = 0;
}