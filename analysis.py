from main import * 

quote_dir = "/home/kuculo/quotekg/completeQuotes2/"
subdirs = [x[0] for x in os.walk(quote_dir)][1:]  
entity_quotes = dict()
entity_quotes["Q937"] = []
entity_quotes["Q15869"] = []
entity_quotes["Q11571"] = []                                                            
for i, subdir in enumerate(subdirs):  
    for root,dirs,files in os.walk(subdir):
        for filename in files:
            if  "Q937_" not in filename and "Q15869_" not in filename and "Q11571_" not in filename:
                continue
            else:
                with open(subdir+"/"+filename,"rb") as f:
                    entity_quotes[filename.split("_")[0]].append(pickle.load(f))

                
                