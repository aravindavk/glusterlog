#include <iostream>
#include <string>
#include <regex>
#include <iomanip>

using std::getline;
using std::cin;
using std::cout;
using std::string;
using std::endl;
using std::regex;
using std::regex_match;
using std::smatch;
using std::vector;
using std::setw;
using std::right;
using std::ostringstream;
using std::boolalpha;

/*
Help for Terminal colors

To print Text in Color in bash terminal

    ESC[ATTR;FG_COLOR;BG_COLORm<TEXT>ESC[RESET

    ESC = "\033"
    RESET = "\033[0m"
    
    // Bash Attributes
    ATTR_NORMAL = "[0;"
    ATTR_BOLD = "[1;"
    
    // Bash Foreground colors
    FG_BLACK = "30"
    FG_RED = "31"
    FG_GREEN = "32"
    FG_YELLOW = "33"
    FG_BLUE = "34"
    FG_PURPLE = "35"
    FG_CYAN = "36"
    FG_WHITE = "37"
    
    // Bash Background Colors
    BG_BLACK = "40"
    BG_RED = "41"
    BG_GREEN = "42"
    BG_YELLOW = "43"
    BG_BLUE = "44"
    BG_PURPLE = "45"
    BG_CYAN = "46"
    BG_WHITE = "47"
*/

#define RESET_COLOR "\033[0m"

// Theme, this only looks good in dark terminals
#define TIMESTAMP_COLOR "\033[0;33m"
#define LOG_LEVEL_INFO_COLOR "\033[1;30;42m"
#define LOG_LEVEL_ERROR_COLOR "\033[1;37;41m"
#define LOG_LEVEL_WARN_COLOR "\033[1;30;43m"
#define LOG_LEVEL_DEFAULT_COLOR "\033[1;30;47m"
#define MSG_ID_COLOR "\033[0;30;43m"
#define FILEINFO_COLOR "\033[0;36m"
#define DOMAIN_COLOR "\033[0;34m"
#define MSG_COLOR "\033[0;37m"
#define KEY_COLOR "\033[0;30;47m"
#define VALUE_COLOR "\033[0;33m"

string log_level_color(string log_level)
{
    if (log_level == "I") {
        return LOG_LEVEL_INFO_COLOR;
    } else if (log_level == "E") {
        return LOG_LEVEL_ERROR_COLOR;
    } else if (log_level == "W") {
        return LOG_LEVEL_WARN_COLOR;
    }

    return LOG_LEVEL_ERROR_COLOR;
}

void json_kv(string k, string v, string indent="    ", bool last=false, bool quote_val=true) {
    cout << indent << "\"" << k << "\": ";
    if (quote_val) cout << "\"";
    
    cout << v;
    
    if (quote_val) cout << "\"";

    if (last) {
        cout << endl;
    } else {
        cout << "," << endl;
    }
}

class ParsedData
{
    public:
        bool known_format;
        string ts;
        string log_level;
        string msg_id;
        string file_info;
        string domain;
        string message;
        vector<vector<string>> fields;

        void colorize()
        {
            if (!this->known_format) {
                cout << this->message << endl;
                return;
            }
            cout << TIMESTAMP_COLOR << setw(26) << this->ts << RESET_COLOR
                 << log_level_color(this->log_level) << " " << this->log_level << " " << RESET_COLOR
                 << MSG_ID_COLOR << "MSGID: " << right << setw(5) << this->msg_id << RESET_COLOR
                 << FILEINFO_COLOR << " " << this->file_info << " " << RESET_COLOR
                 << DOMAIN_COLOR << " " << this->domain << " " << RESET_COLOR
                 << MSG_COLOR << this->message << RESET_COLOR;
            for (auto kv : this->fields) {
                cout << " " << KEY_COLOR << kv[0] << RESET_COLOR << "="
                     << VALUE_COLOR << kv[1] << RESET_COLOR;
            }
            cout << endl;
        }

        void json()
        {
            cout << "{" << endl;
            ostringstream known_fmt;
            known_fmt << boolalpha << this->known_format;
            json_kv("known_format", known_fmt.str(), "    ", false, false);
            json_kv("ts", this->ts);
            json_kv("log_level", this->log_level);
            json_kv("msg_id", this->msg_id);
            json_kv("file_info", this->file_info);
            json_kv("domain", this->domain);
            json_kv("message", this->message);
            cout << "    \"fields\": {" << endl;
            auto l = this->fields.size();
            bool last = false;
            for (int i=0; i < l; i++) { 
                last = i == (l - 1);
                json_kv (this->fields[i][0], this->fields[i][1], "        ", last);
            }
            cout << "    }" << endl << "}";
        }
};

void split(const string& s, char delim, vector<string>& v) {
    auto i = 0;
    auto pos = s.find(delim);
    // If No match
    if (pos == string::npos){
        v.push_back(s);
        return;
    }

    while (pos != string::npos) {
        v.push_back(s.substr(i, pos-i));
        i = ++pos;
        pos = s.find(delim, pos);

        if (pos == string::npos)
            v.push_back(s.substr(i, s.length()));
    }
}

void trim(string& s)
{
    s.erase(0, s.find_first_not_of(" \n\r\t"));
    s.erase(s.find_last_not_of(" \n\r\t")+1);
}

static regex pattern("\\[([^\\]]+)\\]\\s"
        "([IEWTD])\\s"
        "(\\[MSGID:\\s([^\\]]+)\\]\\s)?"
        "\\[([^\\]]+)\\]\\s"
        "([^:]+):\\s"
        "(.+)");


void process_line(string line, bool colorize=false, bool json=false, bool add_delim=true)
{
    if (line == "") return;

    ParsedData pd;
    smatch m;
    if (regex_search (line, m, pattern)) {
        pd.known_format = true;
        pd.ts = m[1];
        pd.log_level = m[2];
        pd.msg_id = m[4];
        pd.file_info = m[5];
        pd.domain = m[6];

        string rawmsg = m[7];
        vector<string> msgs;
        split(m[7], '\t', msgs);
        if (msgs.size() > 0) {
            pd.message = msgs[0];
        }
        int i=0;
        for (i=1; i<msgs.size(); i++) {
            vector<string> kv;

            split(msgs[i], '=', kv);
            trim(kv[0]);
            trim(kv[1]);
            pd.fields.push_back(kv);
        }
    } else {
        pd.known_format = false;
        pd.message = line;
    }
    if (json) {
        pd.json();
        if (add_delim){
            cout << ",";
        }
        cout << endl;
    }
    else if (colorize) {
        pd.colorize();
    }
}

int main(int argc, char **argv)
{
    if (argc < 2) {
        cout << "Usage: cat <LOGFILE> | gluster-log <colorize|json>" << endl;
        return 1;
    }
    bool colorize = false;
    bool json = false;
   
    if (string(argv[1]) == "colorize") colorize = true;
    else if (string(argv[1]) == "json") json = true;
    else {
        cout << "Invalid option" << endl;
        cout << "Usage: cat <LOGFILE> | gluster-log <colorize|json>" << endl;
        return 1;
    }

    if (json) cout << "[" << endl;

    string prev_line;
    
    for (string line; getline (cin, line);) {
        process_line(prev_line, colorize, json, true);
        prev_line = line;
    }

    process_line(prev_line, colorize, json, false);

    if (json) cout << "]" << endl;

    return 0;
}
