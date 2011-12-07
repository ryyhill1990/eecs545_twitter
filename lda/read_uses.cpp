#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <map>
#include <algorithm>
#include <sstream>

using namespace std;

class Cluster {
    public:
        // Primary values of the cluster
        vector<string> values;

        // Maps: value, member-index, pair of member name and member count
        map<string, vector<pair<string, int> > > members;

        // Maps member onto total member count.
        map<string, int> member_counts;

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
        if (++i % 1000 == 0) cout << i << endl;
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
            current_cluster.values.push_back(token);
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
        if (++i % 1000 == 0) cout << i << endl;
        string name;
        int count;
        in >> name;
        in >> count;
        uses[name] = count;
    }
    in.close();
    return uses;
}

// Determine which cluster is most relevent to the tag.
// Return the index of that cluster.
int find_cluster(string tag,
        const vector<Cluster> &clusters,
        const map<string, vector<int> > &cluster_map) {
    int best_index = -1;
    int best_count = 0;
    if (tag.size() == 0) return -1;
    if (tag.at(0) == '#') tag = tag.substr(1);
    map<string, vector<int> >::const_iterator map_tag = cluster_map.find(tag);
    if (map_tag == cluster_map.end()) {
//        cerr << "ERROR: no cluster found for tag: " << tag << endl;
        return -1;
    }
    for (vector<int>::const_iterator map_it = map_tag->second.begin();
            map_it != map_tag->second.end(); ++map_it) {
        const Cluster &cluster = clusters[*map_it];
        vector<string>::const_iterator found = find(cluster.values.begin(), cluster.values.end(), tag);
        if (found != cluster.values.end()) return *map_it;
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

// Maps username onto a list of tweets,
// each tweet in terms of the uses of its use of tags.
map<string, vector<vector<int> > > read_uses(const string &filename,
        const vector<Cluster> &clusters,
        const map<string, vector<int> > &cluster_map,
        const map<string, int> &use_counts) {
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
        if (++i % 100000 == 0) cout << i << endl;
        string name;
        string date;
        string time;
        string tag;
        in >> name;
        if (name.size() == 0) continue;
        in >> date;
        in >> time;
        in >> tag;
        if (use_counts.find(name) == use_counts.end()) {
            continue;
        }
        int cluster_index = find_cluster(tag, clusters, cluster_map);
        /*
        if (cluster_index == -1) {
            // cout << "no cluster found for " << tag << endl;
        }
        */
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

map<string, vector<int> > make_cluster_map(const vector<Cluster> &clusters) {
    map<string, vector<int> > cluster_map;
    int i = 0;
    for (int clusters_index = 0; clusters_index < clusters.size(); ++clusters_index) {
        if (++i % 1000 == 0) cout << i << endl;
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
    for (vector<Cluster>::const_iterator it = clusters.begin();
            it != clusters.end(); ++it) {
        out << it->str();
    }
    out.close();
}

void write_cluster_map(const string &filename, const vector<Cluster> &clusters, const map<string, vector<int> > &cluster_map) {
    ofstream out;
    out.open(filename.c_str());
    for (map<string, vector<int> >::const_iterator it = cluster_map.begin(); it != cluster_map.end(); ++it) {
        out << it->first << endl;
        for (vector<int>::const_iterator it2 = it->second.begin(); it2 != it->second.end(); ++it2) {
            out << "  " << clusters[*it2].values_str() << endl;
        }
    }
    out.close();
}

int main() {
    cout << "Begin" << endl;
    vector<Cluster> clusters = read_clusters("all_clusters.txt");
    cout << "Read clusters" << endl;
    write_clusters("test_clusters_write.txt", clusters);
    cout << "Clusters size" << clusters.size() << endl;
    map<string, vector<int> > cluster_map = make_cluster_map(clusters);
    cout << "Made cluster maps, size " << cluster_map.size() << endl;
    // write_cluster_map("test_cluster_map.txt", clusters, cluster_map);
    map<string, int> use_counts = read_use_counts("aug_user_list.txt");
    cout << "Read use counts, size " << use_counts.size() << endl;
    map<string, vector<vector<int> > > uses = read_uses("aug_uses.txt", clusters, cluster_map, use_counts);
    cout << "Read uses, size " << uses.size() << endl;
    write_uses("write_aug_cluster_uses.txt", uses);
    cout << "Done" << endl;
    return 0;
}
