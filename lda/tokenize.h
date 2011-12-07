#include <string>
#include <vector>
using namespace std;
vector<string> tokenize(const string &str, const string &delim) {
    int begin = 0;
    vector<string> tokens;
    while (begin != string::npos && begin < str.size()) {
        int end = str.find(delim, begin);
        if (end == string::npos) {
            tokens.push_back(str.substr(begin));
            begin = end;
        } else {
            tokens.push_back(str.substr(begin, end - begin));
            begin = end + 1;
        }
    }
    return tokens;
}
