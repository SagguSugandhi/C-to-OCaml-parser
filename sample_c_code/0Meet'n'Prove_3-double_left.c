int f(int n, int doubl)
{
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        sum += i;
        if (doubl)
            sum += i;
    }
    return sum;
}