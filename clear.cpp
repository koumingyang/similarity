#include <iostream>
#include <fstream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include <map>

using namespace std;

const int L = 35000000;
/*
const int M = 22334411;
const int K = 89;

struct node
{
    int key, next, index;
}a[L];
int h[M];

*/

int st[L], fi[L];
string s[L];
map<string, int> a;
int n, m;

void init(void)
{
    freopen("all_texts_151617.txt", "r", stdin);
    string str = "";
    char c;

    map<string, int>::iterator it;

    m = 1, n = 0;
    st[1] = 1;

    while (1)
    {
        c = getchar();
        if (c == ' ')
        {
            s[++n] = str;
            it = a.find(str);
            if(it == a.end())
                a[str] = 1;
            else
                a[str] = a[str] + 1;
            str = "";
        }
        else if (c == '\n')
        {
            fi[m] = n;
            st[++m] = n+1;
            if (m > 240000 || m % 1000 == 0)
                printf("line %d\n", m);
            if (m == 290580)
                break;
        }
        else if (c != EOF)
        {
            str += c;
        }
    }
    cout << "all lines " << m << endl;
    str = "method";
    cout << a[str] << endl;
}

void work(void)
{
    freopen("clear_texts_151617.txt", "w", stdout);
    ofstream fout("log.txt");
    int i, j, cnt = 0;
    string str;
    fout << m << endl;
    for (i = 1; i <= m; i++)
        fout << st[i] << ' ' << fi[i] << ' ' << fi[i] - st[i] << ' ' << i << endl;
    fout << endl;
    for (i = 1; i <= m; i++)
    {
        for (j = st[i]; j <= fi[i]; j++)
        {
            str = s[j];
            if (a[str] > 1)
                printf("%s ", str.c_str()), cnt++;
        }
        printf("\n");
        if (i % 10000 == 0)
            fout << "dealed " << i << " string " << cnt << endl;
    }
    fout << "string " << cnt << endl;
}
int main(void)
{
    init();
    work();
    return 0;
}
