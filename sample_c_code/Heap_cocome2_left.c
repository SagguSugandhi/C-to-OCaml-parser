int sumItems(int *items, int itemCount, int *onlineItems, int onlineItemCount, int paidOnline)
{

    int sum = 0;
    int i = 0;
    int j = 0;

    while ((i < itemCount || j < onlineItemCount))
    {
        if (i < itemCount)
            sum = sum + items[i];
        if (j < onlineItemCount)
            sum = sum + onlineItems[j];
        i++;
        j++;
    }

    sum = sum - paidOnline;

    return sum;
}
