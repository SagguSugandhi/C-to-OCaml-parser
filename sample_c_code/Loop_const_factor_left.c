int f(int x, int n)
{
    int i, k = 0;
    for (i = 0; i != n; ++i)
    {
        x += k * 5;
        k += 1;
        if (i >= 5)
            k += 3;
    }
    return x;
}
