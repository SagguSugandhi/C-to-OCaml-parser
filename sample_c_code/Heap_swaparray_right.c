void swap(int *a, int *b, int n)
{
    int *start = a;
    while ((a - start < n))
    {
        *a = *a + *b;
        *b = *a - *b;
        *a = *a - *b;
        a++;
        b++;
    }
}
