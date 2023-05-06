int my_atoi(const char *s)
{
    int result = 0;
    int i = 0;
    while (1)
    {
        result *= 10;
        switch (s[i])
        {
        case '9':
            result++;
        case '8':
            result++;
        case '7':
            result++;
        case '6':
            result++;
        case '5':
            result++;
        case '4':
            result++;
        case '3':
            result++;
        case '2':
            result++;
        case '1':
            result++;
        case '0':
            break;
        default:
            return result / 10;
        }
        i++;
    }
}
