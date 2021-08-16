int sumAll(int num)
{
	if(num > 1)
	{
		return num + sumAll(num-1);
	}
	
	return num;
}
int sum(int a, int b)
{
	return a + b;
}
int sub(int a, int b)
{
	return a - b;
}
int mult(int a, int b)
{
	return a * b;
}

int main(void)
{
	int a, b, c, d;
	a = 3;
	b = 7;
	for(c = 0; c < 5; c++)
	{
		d = a + 1;
	}
	c = sum(a, b);
	d = sumAll(b);

	printf("c = %d, d = %d\n", c, d);

	return 0;
}