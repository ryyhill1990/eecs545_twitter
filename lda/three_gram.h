#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <iostream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <map>

using namespace std;

int num_dimensions = 'z' - 'a' + '9' - '0' + 2 + 1; // 2 for '^' and '$', + 1 for '@'

int num_for_char(char c) {
    if (c >= 'a' && c <= 'z') return c - 'a';
    if (c >= 'A' && c <= 'Z') return c - 'A';
    if (c >= '0' && c <= '9') return c - '0' + 'z' - 'a' + 1;
    if (c == '@') return num_dimensions - 3;
    cout << "Error, no int found for char: " << c << endl;
    return -1;
}

char char_for_num(int num) {
    if (num >= 0 && num < 'z' - 'a') return 'a' + num;
    if (num >= 'z' - 'a' && num < 'z' - 'a' + '9' - '0') return '0' + num - ('z' - 'a');
    if (num >= num_dimensions - 2 && num < num_dimensions)
    {
        if (num == num_dimensions - 2) return '^';
        return '$';
    }
    if (num == num_dimensions - 3) return '@';
    return '?';
}

double manhattan_dist(const vector<vector<vector<double> > > &x1, const vector<vector<vector<double> > > &x2) {
    double dist = 0.0;
    for (int i = 0; i < num_dimensions; ++i) {
        for (int j = 0; j < num_dimensions; ++j) {
            for (int k = 0; k < num_dimensions; ++k) {
                double d1 = x1[i][j][k];
                double d2 = x2[i][j][k];
                double diff = abs(d1 - d2);
                dist += diff;
            }
        }
    }
    return dist;
}

vector<vector<vector<double> > > build_chain(const string &word) {
    vector<int> word_ints(word.size() + 2, 0);
    for (int i = 0; i < word.size(); ++i) {
        word_ints[i + 1] = num_for_char(word[i]);
    }
    word_ints[0] = num_dimensions - 2; //- 4; // '^'
    // word_ints[1] = num_dimensions - 3; // '^^'
    // word_ints[word_ints.size() - 2] = num_dimensions - 2; // '$'
    word_ints[word_ints.size() - 1] = num_dimensions - 1; // '$$'
    vector<vector<vector<double> > >chain(num_dimensions, vector<vector<double> >(num_dimensions, vector<double>(num_dimensions, 0.0)));
    double increment = 1.0; // / word.size();
    for (int i = 0; i < word.size(); ++i)
    {
        int first = word_ints[i];
        int second = word_ints[i + 1];
        int third = word_ints[i + 2];
        chain[first][second][third] += increment;
    }
    // Still need to normalize against each row [i][k].
    // Let's not do this, it will speed up calculations later
    // to assume all non-zero entries are equal to zero.
    /*
    for (int i = 0; i < num_dimensions; ++i) {
        for (int j = 0; j < num_dimensions; ++j) {
            double total = 0.0;
            for (int k = 0; k < num_dimensions; ++k) {
                total += chain[i][j][k];
            }
            if (total > 0.0) {
                for (int k = 0; k < num_dimensions; ++k) {
                    chain[i][j][k] /= total;
                }
            }
        }
    }
    */
    return chain;
}

/**
  * Represents a word.
  * Has corresponding data about occurances of
  * three-character sets in the word.
  * Includes dummy token for the head and tail of the word.
  */
class ThreeGram {
    public:
        string name;
        vector<vector<vector<double> > > value;
        vector<vector<int> > values_map;
        double magnitude;
        ThreeGram(string name)
            : name(name), 
            value(build_chain(name)),
            magnitude(0.0) {
                // Find magnitude.
                // Also keep track of whick [i][j][k] cells have non-0 values.
                for (int i = 0; i < num_dimensions; ++i) {
                    for (int j = 0; j < num_dimensions; ++j) {
                        for (int k = 0; k < num_dimensions; ++k) {
                            double v = value[i][j][k];
                            magnitude += v * v;
                            if (v > 0.0) {
                                vector<int> temp;
                                temp.push_back(i);
                                temp.push_back(j);
                                temp.push_back(k);
                                values_map.push_back(temp);
                            }
                        }
                    }
                }
                magnitude = sqrt(magnitude);
        }
        string str() const {
            stringstream ss;
            ss << name << '\n';
            for (int i = 0; i < name.size(); ++i) {
                ss << num_for_char(name[i]) << " ";
            }
            ss << "\n    ";
            for (int i = 0; i < num_dimensions; ++i) {
                ss << char_for_num(i) << " ";
            }
            ss << '\n';
            for (int i = 0; i < num_dimensions; ++i) {
                for (int j = 0; j < num_dimensions; ++j) {
                    stringstream ss2;
                    bool use = false;
                    for (int k = 0; k < num_dimensions; ++k) {
                        ss2 << value[i][j][k] << " ";
                        if (value[i][j][k] > 0.0) use = true;
                    }
                    if (use) {
                        ss << char_for_num(i) << char_for_num(j) << ": " << ss2.str() << '\n';
                    }
                }
            }
            ss << "Values: " << values_map.size() << "\n";
            for (vector<vector<int> >::const_iterator it = values_map.begin(); it != values_map.end(); ++it) {
                ss << (*it)[0] << ", " << (*it)[1] << ", " << (*it)[2] << "\n";
            }
            return ss.str();
        }
        bool operator<(const ThreeGram &other) const {
            return name < other.name;
        };
};

double dot_cosine(const ThreeGram &tag1, const ThreeGram &tag2) {

    static map<pair<string, string>, double> cosine_values;
    pair<string, string> p = make_pair(tag1.name, tag2.name);
    if (cosine_values.find(p) != cosine_values.end()) {
        return cosine_values[p];
    }

    int dot = 0;

    // Take advantage of the fact that these lists are sorted by i, k, j.
    vector<vector<int> >::const_iterator it1 = tag1.values_map.begin();
    vector<vector<int> >::const_iterator it2 = tag2.values_map.begin();
    while (it1 != tag1.values_map.end() && it2 != tag2.values_map.end()) {
        int i1 = (*it1)[0];
        int i2 = (*it2)[0];
        if (i1 < i2) {
            ++it1;
            continue;
        }
        if (i2 < i1) {
            ++it2;
            continue;
        }
        int j1 = (*it1)[1];
        int j2 = (*it2)[1];
        if (j1 < j2) {
            ++it1;
            continue;
        }
        if (j2 < j1) {
            ++it2;
            continue;
        }
        int k1 = (*it1)[2];
        int k2 = (*it2)[2];
        if (k1 < k2) {
            ++it1;
            continue;
        }
        if (k2 < k1) {
            ++it2;
            continue;
        }
        // Assume d1 == 1 for speed
        /*
        double d1 = tag1.value[i1][j1][k2];
        double d2 = tag2.value[i1][j1][k2];
        dot += d1 * d2;
        */
        ++dot;
        ++it1;
        ++it2;
    }

    double ret = dot / (tag1.magnitude * tag2.magnitude);
    cosine_values[p] = ret;
    return ret;
}
