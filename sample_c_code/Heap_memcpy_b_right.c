void memcpy(int *dest, int *src, int size)
{
    src--;
    dest--;

    while (size > 0)
    {
        dest++;
        src++;
        *dest = *src;
        size--;
    }
}
