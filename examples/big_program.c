int a, b;
int result;

void main() {
  if (a < 0) a = -a;
  if (b < 0) b = -b;

  if (a == 0 || b == 0) {
    if (a == 0 && b == 0) {
      result = 0;
    } else if (a == 0) {
      result = b;
    } else {
      result = a;
    }
  }

  while (a != 0 && b != 0) {
    if (a == b) {
      result = a;
    }

    if (a > b) {
      if (b != 0)
        a = a % b;
    } else {
      if (a != 0)
        b = b % a;
    }

    if (a == b) {
      int temp = a;
      a = b;
      b = temp;
    }
  }

  if (a == 0) {
    result = b;
  } else {
    result = a;
  }
}