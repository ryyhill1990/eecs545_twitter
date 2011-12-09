#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <map>
#include <algorithm>
#include <sstream>
#include "three_gram.h"

using namespace std;

class Cluster {
    public:
        // Primary values of the cluster
        vector<string> values;

        // Parallel vector of ThreeGrams
        vector<ThreeGram> three_grams;

        // Maps: value, member-index, pair of member name and member count
        map<string, vector<pair<string, int> > > members;

        // Maps member onto total member count.
        map<string, int> member_counts;

        void add_value(const string &value) {
            values.push_back(value);
            three_grams.push_back(ThreeGram(value));
        }

        void add_member(const string &value, const string &member, int count) {
            pair<string, int> pair(member, count);
            members[value].push_back(pair);
            member_counts[member] += count;
        }

        string values_str() const {
            stringstream ss;
            for(vector<string>::const_iterator it = values.begin(); it != values.end(); ++it) {
                ss << " " << *it;
            }
            return ss.str();
        }

        string str() const {
            stringstream ss;
            for(vector<string>::const_iterator it = values.begin(); it != values.end(); ++it) {
                ss << " " << *it;
            }
            ss << endl;
            for (map<string, vector<pair<string, int> > >::const_iterator it = members.begin();
                    it != members.end(); ++it) {
                for (vector<pair<string, int> >::const_iterator it2 = it->second.begin();
                        it2 != it->second.end(); ++it2) {
                    ss << '#' << it->first << "\t#" << it2->first << '\t' << it2->second << endl;
                }
            }
            return ss.str();
        }
};

vector<Cluster> read_clusters(const string &filename) {
    Cluster current_cluster;
    vector<Cluster> clusters;
    ifstream in;
    in.open(filename.c_str());
    int i = 0;
    while(in.good()) {
        if (++i % 10000 == 0) cout << i << endl;
        string token;
        in >> token;
        if (token.size() == 0) continue;
        if (token[0] == '#') {
            // This is a member
            string member;
            int count;
            in >> member;
            in >> count;
            token = token.substr(1);
            member = member.substr(1);
            current_cluster.add_member(token, member, count);
        } else {
            // This is a new cluster
            // or a new value of the current cluster
            if (current_cluster.members.size() > 0) {
                clusters.push_back(current_cluster);
                current_cluster = Cluster();
            }
            current_cluster.add_value(token);
        }
    }
    in.close();
    clusters.push_back(current_cluster);
    return clusters;
}

map<string, int> read_use_counts(const string &filename) {
    map<string, int> uses;
    ifstream in;
    in.open(filename.c_str());
    int i = 0;
    while(in.good()) {
        if (++i % 1000000 == 0) cout << i << endl;
        string name;
        int count;
        in >> name;
        in >> count;
        uses[name] = count;
    }
    in.close();
    return uses;
}

int find_dot_cluster(const ThreeGram &tag,
        const vector<Cluster> &clusters,
        const map<string, vector<int> > &cluster_map,
        int &num_dot_clusters_found) {
    int best_index = -1;
    double best_cos = 0.0;
    double threshold = 0.5;
    bool to_value = false;
    for (int i = 0; i < clusters.size(); ++i) {
        for (vector<ThreeGram>::const_iterator value = clusters[i].three_grams.begin();
                value != clusters[i].three_grams.end(); ++ value) {
            double cos = dot_cosine(tag, *value);
            if (cos >= threshold && cos > best_cos) {
                best_cos = cos;
                best_index = i;
                to_value = true;
            }
        }
    }
    /* Don't even deal with members -- too much work
    double best_member_cos = 0.0;
    string best_member;
    for (map<string, vector<int> >::const_iterator it = cluster_map.begin();
            it != cluster_map.end(); ++it) {
        double cos = dot_cosine(tag, it->first);
        if (cos >= threshold && cos > best_member_cos) {
            best_member_cos = cos;
            best_member = it->first;
            to_value = false;
        }
    }
    */
    if ( /* best_cos >= best_member_cos && */ best_index >= 0) {
        cout << "Attached tag to cluster value: " << tag.name << " (" << best_cos << ")";
        for (vector<string>::const_iterator value = clusters[best_index].values.begin();
                value != clusters[best_index].values.end(); ++ value) {
            cout << ", " << *value;
        }
        cout << endl;
        ++num_dot_clusters_found;
        return best_index;
    }
    return -1;
    /*
    if (best_member.size() == 0) {
        return -1;
    }
    int best_cluster = -1;
    double best_count = 0.0;
    for (vector<int>::const_iterator cluster_index = cluster_map.find(best_member)->second.begin();
            cluster_index != cluster_map.find(best_member)->second.end();
            ++cluster_index) {
        int count = clusters[*cluster_index].member_counts.find(best_member)->second;
        double count_value = count / clusters[*cluster_index].member_counts.size();
        if (count_value > best_count) {
            best_count = count_value;
            best_cluster = *cluster_index;
        }
    }
    if (best_cluster == -1) {
        return -1;
    }
    cout << "Attached tag to cluster member: " << tag << " (" << best_member_cos << "),";
    for (vector<string>::const_iterator value = clusters[best_cluster].values.begin();
            value != clusters[best_cluster].values.end(); ++ value) {
        cout << ", " << *value;
    }
    cout << endl;
    return best_cluster;
    */
}

// Determine which cluster is most relevent to the tag.
// Return the index of that cluster.
int find_cluster(string tag,
        const vector<Cluster> &clusters,
        const map<string, vector<int> > &cluster_map,
        int &num_dot_clusters_found) {
    int best_index = -1;
    int best_count = 0;
    if (tag.size() == 0) return -1;
    if (tag.at(0) == '#') tag = tag.substr(1);
    map<string, vector<int> >::const_iterator map_tag = cluster_map.find(tag);
    if (map_tag == cluster_map.end()) {
        //        cerr << "ERROR: no cluster found for tag: " << tag << endl;
        // return -1;
        ThreeGram three_gram(tag);
        int ret = find_dot_cluster(three_gram, clusters, cluster_map, num_dot_clusters_found);
        return ret;
    }
    for (vector<int>::const_iterator map_it = map_tag->second.begin();
            map_it != map_tag->second.end(); ++map_it) {
        const Cluster &cluster = clusters[*map_it];
        vector<string>::const_iterator found = find(cluster.values.begin(), cluster.values.end(), tag);
        if (found != cluster.values.end()) {
            return *map_it;
        }
        map<string, int>::const_iterator counts_found = cluster.member_counts.find(tag);
        if (counts_found == cluster.member_counts.end()) continue;
        int count = counts_found->second;
        if (count > best_count) {
            best_count = count;
            best_index = *map_it;
        }
    }
    return best_index;
}

vector<string> read_tags(const string &filename) {
    ifstream in;
    in.open(filename.c_str());
    vector<string> tags;
    while(in.good()) {
        string tag;
        in >> tag;
        tags.push_back(tag);
    }
    in.close();
    return tags;
}

// Reduces the muti-way cluster map to a one-to-one mapping
map<string, int> make_final_cluster_map(vector<string> tags,
        const vector<Cluster> &clusters,
        const map<string, vector<int> > &cluster_map,
        int &num_dot_clusters_found) {
    map<string, int> final_map;
    int i = 0;
    for (vector<string>::iterator tag = tags.begin(); tag != tags.end(); ++tag) {
        final_map[*tag] = find_cluster(*tag, clusters, cluster_map, num_dot_clusters_found);
        ++i;
        if (i % 1000 == 0) {
            cout << i << " / " << tags.size() << endl;
        }
    }
    return final_map;
}

void write_final_tag_map(const string &filename, const map<string, int> &tag_map) {
    ofstream out;
    out.open(filename.c_str());
    for (map<string, int>::const_iterator it = tag_map.begin(); it != tag_map.end(); ++it) {
        out << it->first << '\t' << it->second << endl;
    }
    out.close();
}

// Maps username onto a list of tweets,
// each tweet in terms of the uses of its use of tags.
map<string, vector<vector<int> > > read_uses(const string &filename,
        const vector<Cluster> &clusters,
        const map<string, int> &cluster_map /* ,
        const map<string, int> &use_counts */) {
    map<string, vector<vector<int> > > uses;
    ifstream in;
    in.open(filename.c_str());
    int i = 0;
    string last_name;
    string last_date;
    string last_time;
    string last_tag;
    vector<int> current_tweet;
    map<string, int> current_tags;
    while (in.good()) {
        if (++i % 10000 == 0) cout << i << endl;
        string name;
        string date;
        string time;
        string tag;
        in >> name;
        if (name.size() == 0) continue;
        in >> date;
        in >> time;
        in >> tag;
        /*
        if (use_counts.find(name) == use_counts.end()) {
            cout << "User not found: " << name << endl;
            continue;
        }
        */
        int cluster_index = cluster_map.find(tag)->second;
        if (last_name.size() > 0
                && (name.compare(last_name) != 0
                    || date.compare(last_date) != 0
                    || time.compare(last_time) != 0)) {
            uses[last_name].push_back(current_tweet);
            current_tweet.clear();
            current_tags.clear();
        } else if (name.compare(last_name) == 0
                && date.compare(last_date) == 0
                && time.compare(last_time) == 0
                && tag.compare(last_tag) == 0) {
            continue;
        }
        if (current_tags.find(tag) == current_tags.end()) {
            current_tweet.push_back(cluster_index);
            current_tags[tag];
        }
        last_name = name;
        last_date = date;
        last_time = time;
        last_tag = tag;
    }
    if (current_tweet.size() > 0) {
        uses[last_name].push_back(current_tweet);
    }
    in.close();
    return uses;
}

/**
 * Maps the string values of each cluster member onto
 * a list of indexes that that string belongs to.
 */
map<string, vector<int> > make_cluster_map(const vector<Cluster> &clusters) {
    map<string, vector<int> > cluster_map;
    int i = 0;
    for (int clusters_index = 0; clusters_index < clusters.size(); ++clusters_index) {
        if (++i % 100000 == 0) cout << i << endl;
        for (vector<string>::const_iterator values_it = clusters[clusters_index].values.begin();
                values_it != clusters[clusters_index].values.end();
                ++values_it) {
            cluster_map[*values_it].push_back(clusters_index);
        }
        for (map<string, int>::const_iterator members_it = clusters[clusters_index].member_counts.begin();
                members_it != clusters[clusters_index].member_counts.end(); ++members_it) {
            cluster_map[members_it->first].push_back(clusters_index);
        }
    }
    return cluster_map;
}

void write_uses(const string &filename, const map<string, vector<vector<int> > > &uses) {
    ofstream out;
    out.open(filename.c_str());
    for (map<string, vector<vector<int> > >::const_iterator it = uses.begin();
            it != uses.end(); ++it) {
        out << it->first;
        for (vector<vector<int> >::const_iterator it2 = it->second.begin();
                it2 != it->second.end(); ++it2) {
            out << '\t';
            for (int i = 0; i < it2->size(); ++i) {
                if (i != 0) out << ",";
                out << (*it2)[i];
            }
        }
        out << endl;
    }
    out.close();
}

void write_clusters(string filename, const vector<Cluster> &clusters) {
    ofstream out;
    out.open(filename.c_str());
    int index = 0;
    for (vector<Cluster>::const_iterator it = clusters.begin();
            it != clusters.end(); ++it) {
        out << index << it->str();
        ++index;
    }
    out.close();
}

void write_cluster_map(const string &filename, const vector<Cluster> &clusters, const map<string, vector<int> > &cluster_map) {
    ofstream out;
    out.open(filename.c_str());
    for (map<string, vector<int> >::const_iterator it = cluster_map.begin(); it != cluster_map.end(); ++it) {
        out << it->first << endl;
        for (vector<int>::const_iterator it2 = it->second.begin(); it2 != it->second.end(); ++it2) {
            out << " " << *it2 << endl;
        }
    }
    out.close();
}

int main() {
    cout << "Begin" << endl;
    vector<string> tags = read_tags("all_tags.txt");
    cout << "Read tags" << endl;
    vector<Cluster> clusters = read_clusters("all_clusters.txt");
    cout << "Read clusters" << endl;
    write_clusters("test_clusters_write.txt", clusters);
    cout << "Clusters size " << clusters.size() << endl;
    map<string, vector<int> > cluster_map = make_cluster_map(clusters);
    cout << "Made cluster maps, size " << cluster_map.size() << endl;
    int num_dot_clusters_found = 0;
    map<string, int> final_cluster_map = make_final_cluster_map(tags, clusters, cluster_map, num_dot_clusters_found);
    cout << "Made final cluster map, size: " << final_cluster_map.size() << ", num dot clusters: " << num_dot_clusters_found << endl;
    write_final_tag_map("cluster_map.txt", final_cluster_map);
    cout << "Wrote final cluster map" << endl;
//    map<string, int> use_counts = read_use_counts("aug_user_list.txt");
//    cout << "Read use counts, size " << use_counts.size() << endl;

    // TODO enable this
    // map<string, vector<vector<int> > > uses = read_uses("filtered_uses.txt", clusters, final_cluster_map /* , use_counts*/ );
    // cout << "Read uses, size " << uses.size() << endl;
    // write_uses("all_cluster_uses.txt", uses);
    // cout << "Wrote uses" << endl;

    // write_cluster_map("test_cluster_map.txt", clusters, cluster_map);
    // cout << "Wrote cluster map" << endl;
    return 0;
}
