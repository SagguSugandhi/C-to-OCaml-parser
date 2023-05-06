int fib(int n, int *a)
{
    int i = 2;
    a[0] = 1;
    a[1] = 1;

    while (i < n)
    {
        a[i] = a[i - 1] + a[i - 2];
        i++;
    }

    return a[i - 1];
}
