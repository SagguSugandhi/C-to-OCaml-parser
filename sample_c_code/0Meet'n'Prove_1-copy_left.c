void copy(const char *from, char *to)
{
    int i = 0;
    while (from[i] != 0)
    {
        to[i] = from[i];
        i++;
    }
}
