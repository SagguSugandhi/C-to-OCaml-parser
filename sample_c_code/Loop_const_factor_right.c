int f(int x, int n)
{
    int i, k = 0;
    for (i = 0; i != n; ++i)
    {
        x += k;
        k += 5;
        if (i >= 5)
            k += 15;
    }
    return x;
}
