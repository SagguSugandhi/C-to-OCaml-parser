int findmax(int *a, int n)
{

    int i = 1;
    int max = 0;
    int result;

    while ((i < n))
    {
        if (a[i] >= a[max])
        {
            max = i;
        }
        i++;
    }

    result = a[max];
    return result;
}
