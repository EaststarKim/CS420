int sum(int num)
{
	if(num > 1)
	{
		return num + sum(num-1);
	}
	
	return num;
}


int main(void)
{
	int result;
	result = sum(8);
	printf("\nTotal : %d\n", result);
}