void memcpy(int *dest, int *src, int size)
{
    int i = 0;
    while (i < size)
    {
        dest[i] = src[i];
        i++;
    }
}
