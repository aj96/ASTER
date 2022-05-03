# cd ./tools/stanford/stanford-corenlp-full-2016-10-31
cd ./tools/stanford-corenlp-4.4.0
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

