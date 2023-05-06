int f(int t, int c)
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
    else
    {
        while ((0 < c))
        {
            x--;
            c--;
        }
    }

    return x;
}
