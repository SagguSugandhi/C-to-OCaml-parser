int clearstr(int *a)
{
    int *a0 = a;
    while ((*a != 0))
    {
        *a = 0;
        a++;
    }
    return a - a0;
}
