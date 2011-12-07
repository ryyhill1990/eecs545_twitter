#include <iostream>
#include <map>
#include <string>
#include <fstream>

using namespace std;

int main() {
    map<string, int> names_counts;
    int i = 0;
    string last_name;
    string last_date;
    string last_time;
    string last_tag;
    map<string, int> current_tags;
    while (cin.good()) {
        if (++i % 100000 == 0) cout << i << endl;
        string name;
        cin >> name;
        if (name.size() == 0) continue;
        string date;
        string time;
        string tag;
        cin >> date;
        cin >> time;
        cin >> tag;
        if (last_name.size() > 0 &&
                (last_name.compare(name) == 0
                 && last_date.compare(date) == 0
                 && last_time.compare(time) == 0
                 && last_tag.compare(tag) == 0)) {
            continue;
        }
        else if (last_name.compare(name) != 0
                || last_date.compare(date) != 0
                || last_time.compare(time) != 0) {
            current_tags.clear();
        }
        if (current_tags.find(tag) != current_tags.end()) {
            continue;
        }
        ++names_counts[name];
        current_tags[name];
        last_name = name;
        last_date = date;
        last_time = time;
        last_tag = tag;
    }
    ofstream out;
    out.open("aug_user_list.txt");
    for (map<string, int>::const_iterator it = names_counts.begin();
            it != names_counts.end(); ++it) {
        // if (it->second < 50) continue;
        out << it->first << '\t' << it->second << endl;
    }
    out.close();
    return 0;
}
