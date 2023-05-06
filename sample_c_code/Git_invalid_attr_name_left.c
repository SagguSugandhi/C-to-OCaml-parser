int invalid_attr_name(const char *name, int namelen)
{

    if (namelen <= 0 || *name == '-')
        return -1;
    while ((namelen--))
    {
        char ch = *name++;
        if (!(ch == '-' || ch == '.' || ch == '_' ||
              ('0' <= ch && ch <= '9') ||
              ('a' <= ch && ch <= 'z') ||
              ('A' <= ch && ch <= 'Z')))
            return -1;
    }
    return 0;
}
