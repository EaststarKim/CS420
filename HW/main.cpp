#include <stdio.h>
#include <string.h>
#include <string>
using namespace std;
#define SZ 60
char a[SZ];
int f[SZ],it,len,chk,tn,fn,on;
string o[SZ],token;
struct Tree{
	string f;
	int l,r;
}t[SZ];
string next_token(){
	string t;
	for(;it<len;){
		char c=a[it++];
		if(47<c&&c<58)t+=c,chk=1;
		else{
			if(chk){
				chk=0,--it;
				return t;
			}
			chk=0;
			if(c!=32)return t=c;
		}
	}
	return t;
}
void make_tree(int op){
	for(;on;){
		if(op&&o[on]!="*")return;
		t[++tn]={o[on--],f[fn-1],f[fn]};
		f[--fn]=tn;
	}
}
int factor(){
	if(token=="")return -1;
	char c=token.at(0);
	if(!isalnum(c))return -1;
	t[++tn]={token,0,0};
	f[++fn]=tn;
	token=next_token();
	return 0;
}
int term();
int expr();
int term_prime(){
	if(token=="*"){
		make_tree(1);
		o[++on]=token;
		token=next_token();
		return term();
	}
	return 0;
}
int term(){
	if(factor()<0)return -1;
	return term_prime();
}
int expr_prime(){
	if(token=="+"||token=="-"){
		make_tree(0);
		o[++on]=token;
		token=next_token();
		return expr();
	}
	return 0;
}
int expr(){
	if(term()<0)return -1;
	return expr_prime();
}
int goal(){
	it=chk=tn=fn=on=0;
	len=strlen(a)-1;
	token=next_token();
	return expr();
}
void preorder(int n){
	if(!n)return;
	printf("%s",t[n].f.c_str());
	preorder(t[n].l);
	preorder(t[n].r);
}
int main(){
	freopen("input.txt","r",stdin);
	freopen("output.txt","w",stdout);
    for(;;){
		if(fgets(a,sizeof a,stdin)==NULL)return 0;
		int r=goal();
		if(r<0||token!=""){
			puts("incorrect syntax");
			continue;
		}
		make_tree(0);
		preorder(tn);
		puts("");
    }
}
