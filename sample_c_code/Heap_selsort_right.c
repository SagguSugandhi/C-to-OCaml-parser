void selsort(int *a, int n)
{

    int i;
    int j;
    int t;

    i = 0;
    while ((i < n))
    {
        j = i;
        while ((j < n))
        {
            if (a[j] < a[i])
            {
                t = a[i];
                a[i] = a[j];
                a[j] = t;
            }
            j++;
        }
        i++;
    }
}
