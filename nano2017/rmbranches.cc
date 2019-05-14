void exe(string filename);
void rmbranches() {
    ifstream in("xs_list_2016.txt");
    string   line;
    string   filename;
    if (in) {
        while (getline(in, line)) {
            stringstream sline(line);
            sline >> filename;
            exe(filename);
        }
    }
}
void exe(string filename) {
    TFile    f(("../" + filename).c_str(), "update");
    TTree*   t                = (TTree*)f.Get("Events");
    TBranch* id_sf_branch     = t->GetBranch("id_sf");
    TBranch* pu_weight_branch = t->GetBranch("pu_weight");
    TBranch* xs_sf_branch     = t->GetBranch("xs_sf");
    t->GetListOfBranches()->Remove(id_sf_branch);
    t->GetListOfBranches()->Remove(pu_weight_branch);
    t->GetListOfBranches()->Remove(xs_sf_branch);
    t->Write();
    std::cout << "doudou:    " << filename << std::endl;
    delete id_sf_branch;
    delete pu_weight_branch;
    delete xs_sf_branch;
    delete t;
}
