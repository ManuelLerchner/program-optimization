int a, b;
int result;
int exit;

void main() {
  exit = 0;
  if (a < 0) a = -a;
  if (b < 0) b = -b;

  if (a == 0 || b == 0) {
    if (a == 0 && b == 0) {
      result = 0;
      exit = 1;
    } else if (a == 0) {
      result = b;
      exit = 1;

    } else {
      result = a;
      exit = 1;
    }
  }

  while (exit == 0) {
    if (a == b) {
      result = a;
      exit = 1;
    }

    if (a > b) {
      if (b == 0) {
        exit = 1;
      } else {
        a = a % b;
      }

    } else {
      if (a == 0) {
        exit = 1;
      } else {
        b = b % a;
      }
    }

    if (exit == 0) {
      if (a == b) {
        int temp = a;
        a = b;
        b = temp;
      }
    }
  }

  if (a == 0) {
    result = b;
  } else {
    result = a;
  }
}