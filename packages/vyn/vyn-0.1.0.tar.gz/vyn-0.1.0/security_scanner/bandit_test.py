from bandit.core import manager, config



def run_bandit_on_path(path_to_code):
    conf = config.BanditConfig()
    mgr = manager.BanditManager(conf, "file", False)
    
    mgr.discover_files([path_to_code])
    mgr.run_tests()

    return mgr.results



if __name__ == "__main__":
    print("testing")
    run_bandit_on_path("setup.py")
