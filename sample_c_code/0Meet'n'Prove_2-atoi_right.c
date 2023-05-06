int my_atoi(const char *s)
{
    int result = 0;
    while ('0' <= *s && *s < '9')
    {
        result += (*s++ - '0') * 10;
    }
    return result;
}
