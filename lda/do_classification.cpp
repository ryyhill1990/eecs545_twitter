#include <iostream>
#include <map>
#include <vector>
#include <fstream>
#include <string>
#include <cstdlib>
#include <utility>
#include "tokenize.h"

using namespace std;

vector<pair<vector<int>, int> > read_datapoints(const string &filename, const int num_dimensions) {
    vector<pair<vector<int>, int> > datapoints;
    char buff[1000];
    ifstream in;
    in.open(filename.c_str());
    int n = 0;
    while (in.good()) {
        ++n;
        if (n % 1000 == 0) cout << n << endl;
        in.getline(buff, 1000);
        if (in.fail() && !in.eof()) {
            cout << "error in getline" << endl;
            return datapoints;
        }
        string line(buff);
        if (line.size() == 0) continue;
        vector<string> sides = tokenize(line, "\t");
        if (sides.size() != 2) {
            cout << "not 2 sides" << endl;
            return datapoints;
        }
        vector<string> x_tokens = tokenize(sides[0], ",");
        vector<int> x(num_dimensions);
        for (vector<string>::const_iterator x_token = x_tokens.begin(); x_token != x_tokens.end(); ++x_token) {
            vector<string> x_token_parts = tokenize(*x_token, "=");
            if (x_token_parts.size() != 2) {
                cout << "not two parts to x token" << endl;
                return datapoints;
            }
            int dimension_index = atoi(x_token_parts[0].c_str());
            int dimension_value = atoi(x_token_parts[1].c_str());
            x[dimension_index] = dimension_value;
        }
        vector<string> y_tokens = tokenize(sides[1], ",");
        for (vector<string>::const_iterator y_token = y_tokens.begin(); y_token != y_tokens.end(); ++y_token) {
            int y_value = atoi(y_token->c_str());
            datapoints.push_back(make_pair(x, y_value));
        }
    }
    in.close();
    return datapoints;
}

double rand_int(int max) {
    return int((rand() / double(RAND_MAX)) * max);
}

vector<int> choose_subset(const int num_datapoints, const int subset_size) {
    vector<int> subset;
    if (subset_size > num_datapoints) {
        cout << "error, too big of subset" << endl;
        return subset;
    }
    map<int, int> used;
    for (int i = 0; i < subset_size; ++i) {
        bool found = false;
        while (!found) {
            int index = rand_int(num_datapoints);
            if (used.find(index) == used.end()) {
                found = true;
                subset.push_back(index);
            }
        }
    }
    return subset;
}

int do_majority_vote(const string &filename, const vector<pair<vector<int>, int> > &datapoints) {
    int correct = 0;
    for (vector<pair<vector<int>, int> >::const_iterator datapoint = datapoints.begin();
            datapoint != datapoints.end(); ++datapoint) {
        // Find majority vote.
        int largest_dimension = -1;
        int largest_size = 0;
        for (int i = 0; i < datapoint->first.size(); ++i) {
            int size = datapoint->first[i];
            if (size > largest_size) {
                largest_size = size;
                largest_dimension = i;
            }
        }
        if (largest_dimension == datapoint->second) {
            ++correct;
        }
    }
    return correct;
}

int main() {
    srand(time(NULL));
    int num_dimensions = 50;
    vector<pair<vector<int>, int> > datapoints = read_datapoints("write_training_data.txt", num_dimensions);
    cout << "Read datapoints" << endl;
    // vector<int> test_indexes = choose_subset(datapoints.size(), datapoints.size() / 10);
    int correct = do_majority_vote("write_majority_vote.txt", datapoints);
    cout << "Majority vote accuracy: " << correct << " / " << datapoints.size() << ", " << (100 * correct / double(datapoints.size())) << "%" << endl;
    return 0;
}
