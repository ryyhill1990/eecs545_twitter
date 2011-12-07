#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <string>
#include <sstream>
#include "tokenize.h"

using namespace std;

map<string, vector<vector<int> > > read_uses(const string &filename, int &num_dimensions) {
    map<string, vector<vector<int> > > uses;
    ifstream in;
    in.open(filename.c_str());
    char buff[100000];
    int i = 0;
    while(in.good()) {
        in.getline(buff, 100000);
        if (in.fail() && !in.eof()) {
            cout << "error in readline, i = " << i << endl;
            return uses;
        }
        ++i;
        if (i % 10000 == 0) cout << i << endl;
        string line(buff);
        if (line.size() == 0) continue;
        vector<string> tokens = tokenize(line, "\t");
        string name = tokens[0];
        for (vector<string>::const_iterator it = tokens.begin() + 1; it != tokens.end(); ++it) {
            vector<string> numbers = tokenize(*it, ",");
            vector<int> values;
            for (vector<string>::const_iterator number = numbers.begin(); number != numbers.end(); ++number) {
                int value = atoi(number->c_str());
                values.push_back(value);
                if (value > num_dimensions + 1) {
                    num_dimensions = value - 1;
                    cout << "found new highest dimension " << value << endl;
                }
            }
            uses[name].push_back(values);
        }
    }
    return uses;
}

void write_uses(const string &filename, const map<string, vector<vector<int> > > &uses) {
    ofstream out;
    out.open(filename.c_str());
    int n = 0;
    for (map<string, vector< vector<int> > >::const_iterator it = uses.begin();
            it != uses.end(); ++it) {
        ++n;
        if (n % 10000 == 0) cout << n << endl;
        out << it->first;
        for (vector<vector<int> >::const_iterator it2 = it->second.begin();
                it2 != it->second.end(); ++ it2) {
            out << '\t';
            for (int i = 0; i < it2->size(); ++i) {
                if (i != 0) out << ',';
                out << (*it2)[i];
            }
        }
        out << endl;
    }
    out.close();
}

// First item in returned pair is count of occurences of each hash tag;
// its length is the number of dimensions (plus one for -1 / not found).
// Second item in pair is a list of the hashtag-ids found in the next tweet.
// Down the line someone will have to figure out how to turn that into
// training data for a classifier.
vector<pair<vector<int>, vector<int> > > get_training_data(const map<string, vector<vector<int> > > &uses, const int num_dimensions, const int history_length) {

    // Return value, vector of (x,y) datapoints.
    vector<pair<vector<int>, vector<int> > > datapoints;

    // Iterate over each user.
    for (map<string, vector<vector<int> > >::const_iterator use = uses.begin(); use != uses.end(); ++use) {

        // Number of datapoints to get from this user.
        int num_datapoints = use->second.size() - history_length;

        // Iterate over each datapoint to get from this user.
        for (int datapoint_index = 0; datapoint_index < num_datapoints; ++datapoint_index) {

            // The index of the first tweet in this datapoint.
            int tweet_begin_index = datapoint_index;

            // The index of the y-value tweet in this datapoint.
            int y_index = tweet_begin_index + history_length;

            // Vector of occurances of each hasgtag cateogry for this datapoint.
            vector<int> x(num_dimensions + 1);

            // Vector with a list of hashtag category-ids for this datapoint's y-value.
            vector<int> y = use->second[y_index];

            // Iterate over each tweet for this datapoint's x-value.
            for (vector<vector<int> >::const_iterator tweet = use->second.begin() + tweet_begin_index; tweet != use->second.begin() + y_index; ++tweet) {

                // Iterate over each tag in this tweet.
                for (vector<int>::const_iterator tag = tweet->begin(); tag != tweet->end(); ++tag) {

                    // Increment the tag category count.
                    int category = *tag;
                    if (category == -1) {
                        category = num_dimensions - 1;
                    }
                    ++x[category];
               }
            }

            // Add this datapoint to the list.
            datapoints.push_back(make_pair(x, y));
        }
    }

    return datapoints;
}

void write_training_data(const string &filename, const vector<pair<vector<int>, vector<int> > > &training_data, const int num_dimensions) {
    ofstream out;
    out.open(filename.c_str());
    for (vector<pair<vector<int>, vector<int> > >::const_iterator datapoint = training_data.begin();
            datapoint != training_data.end(); ++datapoint) {
        bool wrote = false;
        for (int i = 0; i < datapoint->first.size(); ++i) {
            int value = datapoint->first[i];
            if (value == 0) continue;
            if (wrote) {
                out << ',';
            } else {
                wrote = true;
            }
//            out << (i == num_dimensions - 1 ? -1 : i) << '=' << value;
            out << i << '=' << value;
        }
        out << '\t';
        for (vector<int>::const_iterator tag = datapoint->second.begin();
                tag != datapoint->second.end(); ++tag) {
            if (tag != datapoint->second.begin()) {
                out << ",";
            }
            int value = *tag;
            if (value == -1) value = num_dimensions - 1;
            out << value;
        }
        out << '\n';
    }
    out.close();
}

int main() {
    int num_dimensions = 0;
    int history_length = 10;
    map<string, vector<vector<int> > > uses = read_uses("write_aug_cluster_uses.txt", num_dimensions);
    cout << "Read uses, num dimensions " << num_dimensions << endl;
    // write_uses("test_write_cluster_uses.txt", uses);
    vector<pair<vector<int>, vector<int> > > training_data = get_training_data(uses, num_dimensions, history_length);
    cout << "Make training data" << endl;
    write_training_data("write_training_data.txt", training_data, num_dimensions);
    cout << "Wrote training data" << endl;
    return 0;
}
