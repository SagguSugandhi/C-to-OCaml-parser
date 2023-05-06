int f(int t, int c, int r)
{
    int x = 0;

    if (0 < t)
    {
        while ((0 < c))
        {
            x++;
            c--;
        }
    }
    while ((r > 0))
    {
        x += 2;
        r--;
    }

    return x;
}
