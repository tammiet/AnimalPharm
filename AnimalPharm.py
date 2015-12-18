import urllib2
import json

''''''''''''''''''''' AnimalPharm '''''''''''''''''''''
''''Tammie Thong (tt24) Bioinformatics Final Project '''


''' Asks users to specify the path to input and output files '''

input_file=raw_input("Please enter the path of the query file, which must be a .txt file: ")
output_file=raw_input("Please enter the path of the results file, which must be a .txt file: ")

''' Opens input and output files and reads in input files as a list and removes empty strings from the list'''


with open(input_file) as f:
    lines = f.read().splitlines()
    lines =filter(None, lines)
f.close()

output_file = open(output_file, "w")

disease=[]
animal = []

#Stores disease and animal terms in separate lists.
for i in range(0,len(lines)):
    if (i%2 == 0):
        disease.append(lines[i])
    else:
        animal.append(lines[i])


''' The function pub_med(term, model) searches the PubMed database and returns abstracts which meet the search query requirments
@parameters: term, model
@return: abstracts'''


def pub_med(term, model):

    new_term  = term.replace(' ', '%20')
    new_model = model.replace(' ', '%20')

    ''' Finds ID numbers of articles that meet the search term requirements'''

    #base address of pubmed search database
    url = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    #concatenate all parts of the search together with the base url, to return json data. It returns a maxiumum of 100 articles.
    final_url = url + 'esearch.fcgi?db=pubmed&term=' +new_term +"+" + new_model +"&retmode=json&retmax=100"
    #opens final_url as a string
    json_obj = urllib2.urlopen(final_url)
    #deserialize fp(a.read()-supporting file-like object containing a JSON document to python object using a conversion table
    data = json.load(json_obj)
    data2 = json.dumps(data)
    #converts data2 from a string to a dictionary
    temp = eval(data2)
    #creates dictionary from id 'esearchresult' to get 'idlist', which contains ids of scientific data
    id=temp['esearchresult']
    idlist=id['idlist']
    count=len(idlist)
    total_results = "Returning " + str(count)+" abstracts" + "\n" + "\n" + "\n"
    output_file.write(total_results)


    ''' Looks through the abstracts of articles from the ID list and writes abstract to output file'''
    for i in idlist:
        #efetch is used to get abstracts of articles, given the article id
        id_url = url + "efetch.fcgi?db=pubmed&retmode=text&rettype=abstract&id=" +i
        abs_json_obj = urllib2.urlopen(id_url)
        # reads the json object
        abstract=abs_json_obj.read()
        output_file.write(abstract)


# parses through the lists of diseases and animal models and calls pubm_med(disease, model)
for i in range(0,len(disease)):
    title_string =disease[i].upper()+" using "+animal[i].upper()+" model" + "\n"+ "\n"
    output_file.write(title_string)
    pub_med(disease[i], animal[i])


# end of search message, allowing user to know when the search is finished.
print "Search is complete! See output file for results."


output_file.close()