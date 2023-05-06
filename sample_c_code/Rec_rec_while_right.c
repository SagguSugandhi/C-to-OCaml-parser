int f(int n, int z)
{
    int r;
    int i;
    if (n <= 0)
    {
        r = n;
    }
    else
    {
        i = 0;
        while ((i < n - 1))
        {
            i = i + 1;
        }
        r = f(i, 0);
    }
    return r;
}