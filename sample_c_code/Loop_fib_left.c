int fib(int n)
{
    int f = 0;
    int g = 1;
    int h = 0;

    while ((n > 0))
    {
        h = f + g;
        f = g;
        g = h;
        n--;
    }

    return g;
}
