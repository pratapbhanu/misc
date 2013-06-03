'''
Created on May 30, 2013

@author: bhanu
'''
import data_io
import author_features as af

author_dup = dict()

def build_author_dup_dict():
    print "Building name dictonary for authors..."
    #add authors with same id to duplicates
    author_id_query = "select id from author order by id"
    authorid = data_io.run_query_db(author_id_query)
    for (aid,) in authorid:
        i = int(aid)
        author_dup[i] = []
        author_dup.get(i).append(i)

    #add authors with same name to duplicates
    #dup_same_name_query = "select a1.id, a2.id from author a1, author a2 where a1.name=a2.name and a1.id!=a2.id and a1.name!='' order by a1.id"
    dup_same_name_query = "select a1.id, a2.id from author a1, author a2 where same_words(a1.name, a2.name) and a1.id!=a2.id"
    dupids = data_io.run_query_db(dup_same_name_query)
    for id1, id2 in dupids:
        i1 = int(id1); i2 = int(id2)
        author_dup.get(i1).append(i2)
        
    #add authors with same name match in any order to duplicates
    author_names = af.build_author_name_dict()
    #for id in author_dup.iterkeys():
               
    print "finished building author-dup dictionary."
    
    
def create_submission_file():
    with open("submission_new.txt", 'w') as subfile:
        subfile.write("AuthorId, DuplicateAuthorIds \n")
        for key, values in author_dup.iteritems():
            line = str(key)+","
            for v in values:
                line += str(v)+" "
            line+="\n"
            subfile.write(line)
            

if __name__ == '__main__':
    build_author_dup_dict()
    create_submission_file()