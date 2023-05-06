int clearstr(int *a)
{
    int i = 0;
    while ((a[i] != 0))
    {
        a[i] = 0;
        i++;
    }
    return i;
}
