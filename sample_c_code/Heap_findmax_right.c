int findmax(int *a, int n)
{

    int i = 1;
    int maxv = a[0];
    int result;

    while ((i < n))
    {
        if (a[i] >= maxv)
        {
            maxv = a[i];
        }
        i++;
    }

    result = maxv;
    return result;
}
